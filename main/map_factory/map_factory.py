import numpy as np
import pandas as pd
from math import sqrt, atan, log10
from map_factory.utility.utility import get_v_factor, to_utm, get_index, get_mid_height, get_received_power, get_max_v
from map_factory.utility.model import model, scaler
from map_factory.get_map import get_korea_dted, get_local_dted, get_height


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
            z = dted_data["grid_height"][i][j]
            r = sqrt((t_x - x)*(t_x - x) + (t_y - y)
                     * (t_y - y) + (t_z - z)*(t_z - z))

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
        utm_x_all.append(utm_x_row)
        utm_y_all.append(utm_y_row)
        utm_slope_all.append(utm_slope_row)

    return {"X": utm_x_all, "Y": utm_y_all, "S": utm_slope_all}


def get_mid_height_map(t_h=10, r_h=10, t_lon=127.3845, t_lat=36.3504, span_lon=1.0, span_lat=1.0):
    dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)
    t_ix, t_iy = get_index(dted_data, t_lon, t_lat)

    # MATRIX OF (d, (h,d1,d2)) TUPLE.
    # (h,d1,d2) would be nan in case of LOS
    MH_all = []
    for i in range(len(dted_data["grid_lat"])):
        MH_row = []
        for j in range(len(dted_data["grid_lon"])):
            MH = get_mid_height(dted_data, t_ix, t_iy, t_h, j, i, r_h)
            try:
                MH_row.append(MH[1][0])
            except TypeError:
                MH_row.append(np.nan)
        MH_all.append(MH_row)
    LON, LAT = np.meshgrid(
        dted_data["grid_lon"], dted_data["grid_lat"])   # lon & lat tiles
    return {"X": LON, "Y": LAT, "H": MH_all}

def get_v_by_mid_height_map(f, t_h=10, r_h=10, t_lon=127.3845, t_lat=36.3504, span_lon=1.0, span_lat=1.0):
    dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)
    t_ix, t_iy = get_index(dted_data, t_lon, t_lat)

    # MATRIX OF (d, (h,d1,d2)) TUPLE.
    # (h,d1,d2) would be nan in case of LOS
    V_all = []
    for i in range(len(dted_data["grid_lat"])):
        V_row = []
        for j in range(len(dted_data["grid_lon"])):
            MH = get_mid_height(dted_data, t_ix, t_iy, t_h, j, i, r_h)
            try:
                V = get_v_factor(MH[1][0], f, MH[1][1], MH[1][2])
                V_row.append(V)
            except TypeError:
                V_row.append(np.nan)
        V_all.append(V_row)
    LON, LAT = np.meshgrid(
        dted_data["grid_lon"], dted_data["grid_lat"])   # lon & lat tiles
    return {"X": LON, "Y": LAT, "V": V_all}

def get_max_v_map(f, t_h=10, r_h=10, t_lon=127.3845, t_lat=36.3504, span_lon=1.0, span_lat=1.0):
    dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)
    t_ix, t_iy = get_index(dted_data, t_lon, t_lat)

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


def get_received_power_map(f, t_h=10, r_h=10, t_lon=127.3845, t_lat=36.3504, span_lon=1.0, span_lat=1.0):
    dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)
    t_ix, t_iy = get_index(dted_data, t_lon, t_lat)

    # MATRIX OF (d, (h,d1,d2)) TUPLE. MidHeight would be none if there is no midheight
    RP_all = []
    for i in range(len(dted_data["grid_lat"])):
        RP_row = []
        for j in range(len(dted_data["grid_lon"])):
            V = get_max_v(dted_data, f, t_ix, t_iy, t_h, j, i, r_h)
            RP = get_received_power(
                f, V["d1"]+V["d2"], V["h"], V["d1"], V["d2"])
            RP_row.append(RP)
        RP_all.append(RP_row)
    LON, LAT = np.meshgrid(
        dted_data["grid_lon"], dted_data["grid_lat"])   # lon & lat tiles
    return {"X": LON, "Y": LAT, "RP": RP_all}


def get_received_power_by_mid_height_map(f, t_h=10, r_h=10, t_lon=127.3845, t_lat=36.3504, span_lon=1.0, span_lat=1.0):
    dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)
    t_ix, t_iy = get_index(dted_data, t_lon, t_lat)

    # MATRIX OF (d, (h,d1,d2)) TUPLE. MidHeight would be none if there is no midheight
    RP_all = []
    for i in range(len(dted_data["grid_lat"])):
        RP_row = []
        for j in range(len(dted_data["grid_lon"])):
            MH = get_mid_height(dted_data, t_ix, t_iy, t_h, j, i, r_h)
            try:
                RP = get_received_power(f, MH[1][1] + MH[1][2], MH[1][0], MH[1][1], MH[1][2])
                RP_row.append(RP)
            except TypeError:
                RP_row.append(np.nan)
        RP_all.append(RP_row)
    LON, LAT = np.meshgrid(
        dted_data["grid_lon"], dted_data["grid_lat"])   # lon & lat tiles
    return {"X": LON, "Y": LAT, "RP": RP_all}

def get_csv_map(f, t_h=10, r_h=10, t_lon=127.3845, t_lat=36.3504, span_lon=1.0, span_lat=1.0):
    dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)
    t_ix, t_iy = get_index(dted_data, t_lon, t_lat)

    RP_all = []
    H_all = []
    for i in range(len(dted_data["grid_lat"])):
        RP_row = []
        H_row = []
        for j in range(len(dted_data["grid_lon"])):
            V = get_max_v(dted_data, f, t_ix, t_iy, t_h, j, i, r_h)
            H = get_mid_height(dted_data, t_ix, t_iy, t_h, j, i, r_h)
            try:
                H_row.append(H[1][0])
            except TypeError:
                H_row.append(np.nan)
            RP = get_received_power(
                f, V["d1"]+V["d2"], V["h"], V["d1"], V["d2"])
            RP_row.append(RP)

        RP_all.append(RP_row)
        H_all.append(H_row)
    LON, LAT = np.meshgrid(
        dted_data["grid_lon"], dted_data["grid_lat"])   # lon & lat tiles
    return {"X": LON, "Y": LAT, "RP": RP_all, "H": H_all}


def get_predicted_power_map(f, t_h=10, r_h=10, t_lon=127.3845, t_lat=36.3504, span_lon=1.0, span_lat=1.0):
    dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)
    t_ix, t_iy = get_index(dted_data, t_lon, t_lat)
    t_x, t_y = to_utm(t_lon, t_lat)
    t_z = get_height(t_lon, t_lat)
    RP_all = []
    for i in range(len(dted_data["grid_lat"])):
        RP_row = []
        for j in range(len(dted_data["grid_lon"])):
            try:
                x, y = to_utm(dted_data["grid_lon"][j],
                              dted_data["grid_lat"][i])
                z = dted_data["grid_height"][i][j]
                DX = x - t_x
                DY = y - t_y
                DZ = z - t_z
                H = get_mid_height(dted_data, t_ix, t_iy, t_h, j, i, r_h)[1][0]
                # {"DX": [], "DY": [], "DZ": [], "H": [], "log_f": []
                INPUT = pd.DataFrame([[DX[0], DY[0], DZ, H, log10(f)]], columns=["DX",'DY',"DZ","H","log_f"])
                INPUT = scaler.transform(INPUT)
                RP = model.predict(INPUT)[0][0]
                RP_row.append(RP)
            except Exception:
                RP_row.append(np.nan)
        RP_all.append(RP_row)
    LON, LAT = np.meshgrid(
        dted_data["grid_lon"], dted_data["grid_lat"])   # lon & lat tiles
    return {"X": LON, "Y": LAT, "RP": RP_all}
