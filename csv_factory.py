from typing_extensions import assert_type
from pyproj import Proj
from math import log10
import pandas as pd
import numpy as np
from map_factory.get_map import get_local_dted
from map_factory.map_factory import get_csv_map
from map_factory.utility.utility import convert_to_si
from environments.transmitter import transmitters

frequency_list = list(range(80000000,100000001,5000000))
to_utm = Proj(proj='utm', zone=52, ellps='WGS84', preserve_units=False)
r_h = 10


def create_CSV():
    df = pd.DataFrame(
        {"R": [], "D": [], "H": [], "RP": []})
    for transmitter in transmitters:
        name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
        dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)
        # MATRIX OF (r, (h,d1,d2)) TUPLE. MidHeight would be none if there is no midheight
        for f in frequency_list:
            DATA = get_csv_map(
                f, t_h, r_h, t_lon, t_lat, span_lon, span_lat)
            for i in range(len(DATA["RP"])):  # LAT_index
                for j in range(len(DATA["RP"][0])):  # LON_index
                    if not np.isnan(DATA["RP"][i][j]) and not np.isnan(DATA["H"][i][j]):
                        R = DATA["R"][i][j]
                        D = DATA["D"][i][j]
                        H = DATA["H"][i][j]
                        RP = DATA["RP"][i][j]
                        
                        dfNew = pd.DataFrame(
                            {"R": [R], "D": [D],"H": [H], "F":[log10(f)],"RP": [RP]})
                        df = pd.concat([df, dfNew])
            print(
                f"Processing {name} Transmitter For Ray {convert_to_si(f)}Hz Finish")
            # df.to_csv("MLP/DATA/data.csv")
    df_shuffled = df.sample(frac=1).reset_index(drop=True)
    print("CSV DATA IS CREATED")
    df_shuffled.to_csv("MLP/DATA/data.csv")


create_CSV()
