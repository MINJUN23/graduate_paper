import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from map_factory.map_factory import get_received_power_map, get_predicted_power_map, get_received_power_by_mid_height_map
from environments.transmitter import transmitters
from map_factory.utility.utility import convert_to_si

frequenct_list = [1000000, 10000000, 100000000, 1000000000]
r_h = 10


def plot_received_power_near_transmitter(frequency, transmitter):
    name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
    DATA = get_received_power_map(
        frequency, t_h, r_h, t_lon, t_lat, span_lon, span_lat)
    fig = plt.pcolormesh(
        DATA["X"], DATA["Y"], DATA["RP"], shading="auto")
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(f"Received Power near {name} ({convert_to_si(frequency)}Hz)")
    cbar = plt.colorbar(fig)
    cbar.set_label('Received Power (dBm)')
    plt.savefig(f"main/IMGS/RP/{name}_{convert_to_si(frequency)}Hz.png")
    print(f"{name}_{convert_to_si(frequency)}Hz.png CREATED")
    plt.clf()


def plot_expected_received_power_near_transmitter(frequency, transmitter):
    name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
    DATA = get_received_power_by_mid_height_map(
        frequency, t_h, r_h, t_lon, t_lat, span_lon, span_lat)
    fig = plt.pcolormesh(
        DATA["X"], DATA["Y"], DATA["RP"], shading="auto")
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(f"Calculated Power near {name} ({convert_to_si(frequency)}Hz)")
    cbar = plt.colorbar(fig)
    cbar.set_label('Received Power (dBm)')
    plt.savefig(f"main/IMGS/RP/CAL_{name}_{convert_to_si(frequency)}Hz.png")
    print(f"CAL_{name}_{convert_to_si(frequency)}Hz.png CREATED")
    plt.clf()


def plot_predicted_power_near_transmitter(frequency, transmitter):
    name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
    DATA = get_predicted_power_map(
        frequency, t_h, r_h, t_lon, t_lat, span_lon, span_lat)
    fig = plt.pcolormesh(
        DATA["X"], DATA["Y"], DATA["RP"], shading="auto")
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(
        f"Predicted Received Power near {name} ({convert_to_si(frequency)}Hz)")
    cbar = plt.colorbar(fig)
    cbar.set_label('Received Power (dBm)')
    plt.savefig(f"main/IMGS/RP/PRED_{name}_{convert_to_si(frequency)}Hz.png")
    print(f"PRED_{name}_{convert_to_si(frequency)}Hz.png CREATED")
    plt.clf()


def plot_differences(frequency, transmitter):
    name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
    REAL = get_received_power_map(
        frequency, t_h, r_h, t_lon, t_lat, span_lon, span_lat)
    CALC = get_received_power_by_mid_height_map(
        frequency, t_h, r_h, t_lon, t_lat, span_lon, span_lat)
    CALC_DIFFERENCE = pd.DataFrame(REAL["RP"]) - pd.DataFrame(CALC["RP"])

    PRED = get_predicted_power_map(
        frequency, t_h, r_h, t_lon, t_lat, span_lon, span_lat)
    PRED_DIFFERENCE = pd.DataFrame(REAL["RP"]) - pd.DataFrame(PRED["RP"])

    v_min = min([np.nanmin(PRED_DIFFERENCE), np.nanmin(CALC_DIFFERENCE)])
    v_max = max([np.nanmax(PRED_DIFFERENCE), np.nanmax(CALC_DIFFERENCE)])

    fig = plt.pcolormesh(
        REAL["X"], REAL["Y"], CALC_DIFFERENCE, shading="auto")
    ERRORS = CALC_DIFFERENCE.abs()
    ERROR = ERRORS.stack().mean()
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(f"CALC Difference")
    cbar = plt.colorbar(fig)
    plt.clim(v_min, v_max)
    cbar.set_label('Received Power (dBm)')
    plt.savefig(
        f"main/IMGS/RP/DIFF/CALC_{name}_{convert_to_si(frequency)}Hz_ERROR:{ERROR:.3f}.png")
    print(f"DIFF_CALC_{name}_{convert_to_si(frequency)}Hz.png CREATED")
    print(f"ERROR: {ERROR:.3f}")
    plt.clf()

    fig = plt.pcolormesh(
        REAL["X"], REAL["Y"], PRED_DIFFERENCE, shading="auto")
    ERRORS = PRED_DIFFERENCE.abs()
    ERROR = ERRORS.stack().mean()
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(
        f"PRED Difference")
    cbar = plt.colorbar(fig)
    plt.clim(v_min, v_max)
    cbar.set_label('Received Power (dBm)')
    plt.savefig(
        f"main/IMGS/RP/DIFF/PRED_{name}_{convert_to_si(frequency)}Hz_ERROR:{ERROR:.3f}.png")
    print(f"DIFF_PRED_{name}_{convert_to_si(frequency)}Hz.png CREATED")
    print(f"ERROR: {ERROR:.3f}")
    plt.clf()


for transmitter in transmitters:
    for frequency in frequenct_list:
        plot_differences(frequency, transmitter)
