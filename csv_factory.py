import pandas as pd
import numpy as np
from get_map import get_local_dted
from map_factory import get_csv_map
from utility import get_index, convert_to_si
from pyproj import Proj
from math import log10
from transmitter import transmitters

frequency_list = [1000000, 10000000, 100000000, 1000000000]
to_utm = Proj(proj='utm', zone=52, ellps='WGS84', preserve_units=False)
r_h = 10


def create_CSV():
    df = pd.DataFrame(
        {"DX": [], "DY": [], "DZ": [],
         "H": [], "log_f": [], "RP": []})
    for transmitter in transmitters:
        name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
        dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)
        t_ix, t_iy = get_index(dted_data, t_lon, t_lat)

        TX, TY = to_utm(t_lon, t_lat)
        TZ = dted_data["grid_height"][t_iy][t_ix] + t_h
        # MATRIX OF (r, (h,d1,d2)) TUPLE. MidHeight would be none if there is no midheight
        for f in frequency_list:
            DATA = get_csv_map(
                f, t_h, r_h, t_lon, t_lat, span_lon, span_lat)
            for i in range(len(DATA["RP"])):  # LAT_index
                for j in range(len(DATA["RP"][0])):  # LON_index
                    if not np.isnan(DATA["RP"][i][j]):
                        RX, RY = to_utm(
                            DATA["X"][i][j], DATA["Y"][i][j])
                        RZ = dted_data["grid_height"][i][j] + r_h
                        DX = RX-TX
                        DY = RY-TY
                        DZ = RZ-TZ
                        H = DATA["H"][i][j]
                        RP = DATA["RP"][i][j]
                        dfNew = pd.DataFrame(
                            {"DX": [DX], "DY": [DY], "DZ": [DZ],
                             "H": [H], "log_f": [log10(f)], "RP": [RP]})
                        df = pd.concat([df, dfNew])
            print(
                f"Processing {name} Transmitter For Ray {convert_to_si(f)}Hz Finish")
    df_shuffled = df.sample(frac=1).reset_index(drop=True)
    df_shuffled.to_csv("csv/data.csv")


create_CSV()
