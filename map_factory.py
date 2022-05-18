import numpy as np
from math import sqrt, atan
from utility import to_utm, get_index, get_mid_height, get_gain, get_max_v
from get_map import get_korea_dted, get_local_dted, get_height


def get_height_map(t_lon, t_lat):
    dted_data = get_korea_dted()
    index_lon = np.absolute(
        dted_data["grid_lon"] - t_lon).argmin()  # nearest lon index
    index_lat = np.absolute(
        dted_data["grid_lat"] - t_lat).argmin()  # nearest lat index
    return dted_data["grid_height"][index_lat][index_lon]


def get_distance_map(t_lon=127.3845, t_lat=36.3504, span_lon=1.0, span_lat=1.0):
    t_x, t_y = to_utm(t_lon, t_lat)
    t_z = get_height(t_lon, t_lat)
    dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)
    utm_x_all = []
    utm_y_all = []
    utm_r_all = []
    for i in range(len(dted_data["grid_lat"])):
        utm_x_row = []
        utm_y_row = []
        utm_r_row = []
        for j in range(len(dted_data["grid_lon"])):
            x, y = to_utm(dted_data["grid_lon"][j],
                          dted_data["grid_lat"][i])
            r = sqrt((t_x - x)*(t_x - x) + (t_y - y)
                     * (t_y - y) + (t_z - dted_data["grid_height"][i][j])*(t_z - dted_data["grid_height"][i][j]))

            x = int(x)
            y = int(y)
            r = int(r)
            utm_x_row.append(x)
            utm_y_row.append(y)
            utm_r_row.append(r)
        utm_x_all.append(utm_x_row)
        utm_y_all.append(utm_y_row)
        utm_r_all.append(utm_r_row)

    return {"X": utm_x_all, "Y": utm_y_all, "R": utm_r_all}


def get_difference_map(t_lon=127.3845, t_lat=36.3504, span_lon=1.0, span_lat=1.0):
    dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)
    t_x, t_y = to_utm(t_lon, t_lat)
    t_z = get_height(t_lon, t_lat)
    utm_x_all = []
    utm_y_all = []
    utm_d_all = []
    for i in range(len(dted_data["grid_lat"])):
        utm_x_row = []
        utm_y_row = []
        utm_d_row = []
        for j in range(len(dted_data["grid_lon"])):
            x, y = to_utm(dted_data["grid_lon"][j],
                          dted_data["grid_lat"][i])
            z = dted_data["grid_height"][i][j]
            d = sqrt((t_x - x)*(t_x - x) + (t_y - y) * (t_y - y) + (t_z - z)
                     * (t_z - z)) - sqrt((t_x - x)*(t_x - x) + (t_y - y) * (t_y - y))
            x = int(x)
            y = int(y)
            d = int(d)
            utm_x_row.append(x)
            utm_y_row.append(y)
            utm_d_row.append(d)
        utm_x_all.append(utm_x_row)
        utm_y_all.append(utm_y_row)
        utm_d_all.append(utm_d_row)

    return {"X": utm_x_all, "Y": utm_y_all, "D": utm_d_all}


def get_slope_map(t_lon=127.3845, t_lat=36.3504, span_lon=1.0, span_lat=1.0):
    dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)
    t_x, t_y = to_utm(t_lon, t_lat)
    t_z = get_height(t_lon, t_lat)
    utm_x_all = []
    utm_y_all = []
    utm_slope_all = []
    for i in range(len(dted_data["grid_lat"])):
        utm_x_row = []
        utm_y_row = []
        utm_slope_row = []
        for j in range(len(dted_data["grid_lon"])):
            x, y = to_utm(dted_data["grid_lon"][j],
                          dted_data["grid_lat"][i])
            z = dted_data["grid_height"][i][j]
            tan = (t_z-z)/sqrt((t_x - x)*(t_x - x) + (t_y - y) * (t_y - y))
            slope = atan(tan)
            x = int(x)
            y = int(y)
            utm_x_row.append(x)
            utm_y_row.append(y)
            utm_slope_row.append(slope)
        print(max(utm_slope_row))
        utm_x_all.append(utm_x_row)
        utm_y_all.append(utm_y_row)
        utm_slope_all.append(utm_slope_row)

    return {"X": utm_x_all, "Y": utm_y_all, "S": utm_slope_all}


def get_midheight_map(t_h=10, r_h=10, t_lon=127.3845, t_lat=36.3504, span_lon=1.0, span_lat=1.0):
    dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)
    t_ix, t_iy = get_index(dted_data, t_lon, t_lat)

    # MATRIX OF (d, (h,d1,d2)) TUPLE.
    # (h,d1,d2) would be nan in case of LOS
    MH_all = []
    for i in range(len(dted_data["grid_lat"])):
        MH_row = []
        for j in range(len(dted_data["grid_lon"])):
            MH = get_mid_height(dted_data, t_ix, t_iy, t_h, i, j, r_h)
            try:
                MH_row.append(MH[1][0])
            except TypeError:
                MH_row.append(0)
        MH_all.append(MH_row)
    LON, LAT = np.meshgrid(
        dted_data["grid_lon"], dted_data["grid_lat"])   # lon & lat tiles
    return {"X": LON, "Y": LAT, "D": MH_all}


def get_LOS_map(f, t_h=10, r_h=10, t_lat=36.3504, t_lon=127.3845, span_lat=1.0, span_lon=1.0):
    dted_data = get_local_dted(t_lat, t_lon, span_lat, span_lon)
    t_ix, t_iy = get_index(dted_data, t_lat, t_lon)

    # MATRIX OF (r, (h,d1,d2)) TUPLE. MidHeight would be none if there is no midheight
    LOS_all = []
    for i in range(len(dted_data["grid_lat"])):
        LOS_row = []
        for j in range(len(dted_data["grid_lon"])):
            dm = get_mid_height(dted_data, t_ix, t_iy, t_h, i, j, r_h)
            if isinstance(dm[1], tuple) and dm[1][0] != 0 and dm[1][1] != 0 and dm[1][2] != 0:
                LOS = np.NaN
            else:
                LOS = (f, dm[0])
            LOS_row.append(LOS)
        LOS_all.append(LOS_row)
    LON, LAT = np.meshgrid(
        dted_data["grid_lon"], dted_data["grid_lat"])   # lon & lat tiles
    return {"X": LON, "Y": LAT, "LOS": LOS_all}


def get_NLOS_map(f, t_h=10, r_h=10, t_lat=36.3504, t_lon=127.3845, span_lat=1.0, span_lon=1.0):
    dted_data = get_local_dted(t_lat, t_lon, span_lat, span_lon)
    t_ix, t_iy = get_index(dted_data, t_lat, t_lon)

    # MATRIX OF (d, (h,d1,d2)) TUPLE. MidHeight would be none if there is no midheight
    NLOS_all = []
    H_all = []
    D1_all = []
    D2_all = []
    for i in range(len(dted_data["grid_lat"])):
        NLOS_row = []
        H_row = []
        D1_row = []
        D2_row = []
        for j in range(len(dted_data["grid_lon"])):
            dm = get_mid_height(dted_data, t_ix, t_iy, t_h, i, j, r_h)
            if isinstance(dm[1], tuple) and dm[1][0] != 0 and dm[1][1] != 0 and dm[1][2] != 0:
                NLOS = calc_NLOS(f, dm[0], dm[1][0], dm[1][1], dm[1][2])
                H = dm[1][0]
                D1 = dm[1][1]
                D2 = dm[1][2]
            else:
                NLOS = np.NaN
                H = np.NaN
                D1 = np.NaN
                D2 = np.NaN
            NLOS_row.append(NLOS)
            H_row.append(H)
            D1_row.append(D1)
            D2_row.append(D2)
        NLOS_all.append(NLOS_row)
        H_all.append(H_row)
        D1_all.append(D1_row)
        D2_all.append(D2_row)
    LON, LAT = np.meshgrid(
        dted_data["grid_lon"], dted_data["grid_lat"])   # lon & lat tiles
    return {"X": LON, "Y": LAT, "NLOS": NLOS_all,
            "H": H_all, "D1": D1_all, "D2": D2_all}


def get_G(f, t_h=10, r_h=10, t_lat=36.3504, t_lon=127.3845, span_lat=1.0, span_lon=1.0):
    dted_data = get_local_dted(t_lat, t_lon, span_lat, span_lon)
    t_ix, t_iy = get_index(dted_data, t_lat, t_lon)

    # MATRIX OF (d, (h,d1,d2)) TUPLE. MidHeight would be none if there is no midheight
    G_ALL = []
    for i in range(len(dted_data["grid_lat"])):
        G_ROW = []
        for j in range(len(dted_data["grid_lon"])):
            dm = get_mid_height(dted_data, t_ix, t_iy, t_h, i, j, r_h)
            if isinstance(dm[1], tuple) and dm[1][0] != 0 and dm[1][1] != 0 and dm[1][2] != 0:
                G = calc_NLOS(f, dm[0], dm[1][0], dm[1][1], dm[1][2])
            else:
                G = calc_LOS(f, dm[0])
            G_ROW.append(G)
        G_ALL.append(G_ROW)
    LON, LAT = np.meshgrid(
        dted_data["grid_lon"], dted_data["grid_lat"])   # lon & lat tiles
    return {"X": LON, "Y": LAT, "G": G_ALL}


def get_received_power_map(f, t_h=10, r_h=10, t_lon=127.3845, t_lat=36.3504, span_lon=1.0, span_lat=1.0):
    dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)
    t_ix, t_iy = get_index(dted_data, t_lon, t_lat)

    # MATRIX OF (d, (h,d1,d2)) TUPLE. MidHeight would be none if there is no midheight
    RP_all = []
    H_all = []
    D1_all = []
    D2_all = []
    for i in range(len(dted_data["grid_lat"])):
        RP_row = []
        H_row = []
        D1_row = []
        D2_row = []
        for j in range(len(dted_data["grid_lon"])):
            dm = get_mid_height(dted_data, t_ix, t_iy, t_h, i, j, r_h)
            if isinstance(dm[1], tuple) and dm[1][0] != 0 and dm[1][1] != 0 and dm[1][2] != 0:
                RP = get_gain(f, dm[0], dm[1][0], dm[1][1], dm[1][2])
                H = dm[1][0]
                D1 = dm[1][1]
                D2 = dm[1][2]
            else:
                # print(dm[1])
                RP = np.NaN
                H = np.NaN
                D1 = np.NaN
                D2 = np.NaN
            RP_row.append(RP)
            H_row.append(H)
            D1_row.append(D1)
            D2_row.append(D2)
        RP_all.append(RP_row)
        H_all.append(H_row)
        D1_all.append(D1_row)
        D2_all.append(D2_row)
    LON, LAT = np.meshgrid(
        dted_data["grid_lon"], dted_data["grid_lat"])   # lon & lat tiles
    return {"X": LON, "Y": LAT, "RP":
            RP_all,
            "H": H_all, "D1": D1_all, "D2": D2_all}


def get_max_v_map(f, t_h=10, r_h=10, t_lon=127.3845, t_lat=36.3504, span_lon=1.0, span_lat=1.0):
    dted_data = get_local_dted(t_lat, t_lon, span_lat, span_lon)
    t_ix, t_iy = get_index(dted_data, t_lat, t_lon)

    # MATRIX OF (d, (h,d1,d2)) TUPLE. MidHeight would be none if there is no midheight
    V_ALL = []
    H_ALL = []
    for i in range(len(dted_data["grid_lat"])):
        V_ROW = []
        H_ROW = []
        for j in range(len(dted_data["grid_lon"])):
            V = get_max_v(dted_data, f, t_ix, t_iy, t_h, j, i, r_h)
            V_ROW.append(V["v"])
            H_ROW.append(V["h"])
        V_ALL.append(V_ROW)
        H_ALL.append(H_ROW)
    LON, LAT = np.meshgrid(
        dted_data["grid_lon"], dted_data["grid_lat"])   # lon & lat tiles
    return {"X": LON, "Y": LAT, "V": V_ALL, "H": H_ALL}
