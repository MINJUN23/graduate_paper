from map_factory.map_factory import get_received_power, get_index
from map_factory.get_map import get_local_dted, get_height
from map_factory.utility.utility import get_observer_predicted_power, get_info_about_observer_predicted_power, convert_to_si
from map_factory.utility.model import scaler, model
from math import log10
import pandas as pd
import numpy as np

r_h = 10


def check_outlier_error(frequency, transmitter):
    name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
    dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)
    t_ix, t_iy = get_index(dted_data, t_lon, t_lat)

    # MATRIX OF (d, (h,d1,d2)) TUPLE. MidHeight would be none if there is no midheight
    INFO_LIST = []
    for y in range(len(dted_data["grid_lat"])):
        for x in range(len(dted_data["grid_lon"])):
            RP = get_received_power(
                dted_data, frequency, t_ix, t_iy, t_h, x, y, r_h)
            if not np.isnan(RP):
                INFO_LIST.append({"RP": RP, "x": x, "y": y})
    
    INFO_LIST.sort(key=lambda INFO: INFO["RP"])

    I3 = int(len(INFO_LIST)/4*3)
    I1 = int(len(INFO_LIST)/4)
    IQR = INFO_LIST[I3]["RP"] - INFO_LIST[I1]["RP"]
    MIN_BOUND = INFO_LIST[int(len(INFO_LIST)/4)]['RP'] - IQR * 1.5
    OUTLIERS = list(filter(lambda INFO: INFO['RP'] < MIN_BOUND, INFO_LIST))
    print(f"{name}_{convert_to_si(frequency)}Hz IQR : {IQR}, MIN_BOUND : {MIN_BOUND}, NUMBER_OF_OUTLIERS : {len(OUTLIERS)}")
    if len(OUTLIERS) != 0 :
        PRED_ERRORS, CALC_ERRORS = [], []
        for OUTLIER in OUTLIERS:
            x, y = OUTLIER["x"], OUTLIER["y"]

            INFO = get_info_about_observer_predicted_power(
                dted_data, t_ix, t_iy, t_h, x, y, r_h)
            # ,R,D,H,F
            INPUT = pd.DataFrame([[INFO["R"], INFO["D"], INFO["H"], log10(frequency)]], columns=[
                "R", 'D', "H", "F"])
            INPUT = scaler.transform(INPUT)
            PRED = model.predict(INPUT)[0][0]
            PRED_ERRORS.append(abs(PRED - OUTLIER["RP"]))
            CALC = get_observer_predicted_power(
                dted_data, frequency, t_ix, t_iy, t_h, x, y, r_h)
            CALC_ERRORS.append(abs(CALC - OUTLIER["RP"]))
        PRED_ERROR = sum(PRED_ERRORS) / len(PRED_ERRORS)
        CALC_ERROR = sum(CALC_ERRORS) / len(CALC_ERRORS)
        print(f"{name}_{convert_to_si(frequency)}Hz OUTLIER_CALC_ERROR: {CALC_ERROR}")
        print(f"{name}_{convert_to_si(frequency)}Hz OUTLIER_PRED_ERROR: {PRED_ERROR}")
    else:
        print(f"{name}_{convert_to_si(frequency)} doesn't have OUTLIER")