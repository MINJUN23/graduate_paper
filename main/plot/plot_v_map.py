import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from map_factory.map_factory import get_v_map, get_mid_height_map, get_v_by_mid_height_map, get_observer_predicted_v_map
from map_factory.utility.utility import convert_to_si


r_h = 10
frequency = 90000000

max_h = 1600
min_h = -1000


def plot_max_v_from_transmitter(transmitter):
    name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
    V = get_v_map(
        frequency, t_h, r_h, t_lon, t_lat, span_lon, span_lat)
    fig = plt.pcolormesh(
        V["X"], V["Y"], V["V"], shading="auto")
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(f"Max value of v factor of the ray near {name}")
    cbar = plt.colorbar(fig)
    cbar.set_label('V - factor')
    plt.savefig(f"main/IMGS/V_MAP/MAXV_{name}_{convert_to_si(frequency)}Hz.png")
    print(f"MAXV_{name}_{convert_to_si(frequency)}Hz.png CREATED")
    plt.clf()


def plot_height_of_max_v_from_transmitter(transmitter):
    name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
    V = get_v_map(
        frequency, t_h, r_h, t_lon, t_lat, span_lon, span_lat)
    fig = plt.pcolormesh(
        V["X"], V["Y"], V["H"], shading="auto")
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(
        f"Height of the dot that makes max value of v factor near {name}")
    cbar = plt.colorbar(fig)
    plt.clim(min_h, max_h)
    cbar.set_label('Height, m')
    plt.savefig(
        f"main/IMGS/V_MAP/H_OF_MAXV_{name}_{convert_to_si(frequency)}Hz.png")
    print(f"H_OF_MAXV_{name}_{convert_to_si(frequency)}Hz.png CREATED")
    plt.clf()


def plot_midheight_from_transmitter(transmitter):
    name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
    DATA = get_mid_height_map(
        t_h, r_h, t_lon, t_lat, span_lon, span_lat)
    fig = plt.pcolormesh(
        DATA["X"], DATA["Y"], DATA["H"], shading="auto")
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(f"Max mid-height of the ray near {name}")
    cbar = plt.colorbar(fig)
    plt.clim(min_h, max_h)
    cbar.set_label('Height, m')
    plt.savefig(
        f"main/IMGS/V_MAP/MAX_MIDHEIGHT_{name}.png")
    print(f"MAX_MIDHEIGHT_{name}.png CREATED")
    plt.clf()

def plot_obserber_predicted_v_from_transmitter(transmitter):
    name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
    DATA = get_mid_height_map(
        t_h, r_h, t_lon, t_lat, span_lon, span_lat)
    fig = plt.pcolormesh(
        DATA["X"], DATA["Y"], DATA["H"], shading="auto")
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(f"Max mid-height of the ray near {name}")
    cbar = plt.colorbar(fig)
    plt.clim(min_h, max_h)
    cbar.set_label('Height, m')
    plt.savefig(
        f"main/IMGS/V_MAP/MAX_MIDHEIGHT_{name}.png")
    print(f"MAX_MIDHEIGHT_{name}.png CREATED")
    plt.clf()





def plot_mvh_and_mh(transmitter):
    name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
    DATA = get_mid_height_map(
        t_h, r_h, t_lon, t_lat, span_lon, span_lat)
    V = get_v_map(
        frequency, t_h, r_h, t_lon, t_lat, span_lon, span_lat)
    v_min = min([np.nanmin(V["H"]), np.nanmin(DATA["H"])])
    v_max = max([np.nanmax(V["H"]), np.nanmax(DATA["H"])])
    print(v_min, v_max)

    fig = plt.pcolormesh(
        DATA["X"], DATA["Y"], DATA["H"], shading="auto")
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(f"Max mid-height of the ray near {name}")
    cbar = plt.colorbar(fig)
    plt.clim(v_min, v_max)
    cbar.set_label('Height, m')
    plt.savefig(
        f"main/IMGS/V_MAP/MAX_MIDHEIGHT_{name}.png")
    print(f"MAX_MIDHEIGHT_{name}.png CREATED")
    plt.clf()

    fig = plt.pcolormesh(
        V["X"], V["Y"], V["H"], shading="auto")
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(
        f"Height of the dot that makes max value of v factor near {name}")
    cbar = plt.colorbar(fig)
    plt.clim(v_min, v_max)
    cbar.set_label('Height, m')
    plt.savefig(
        f"main/IMGS/V_MAP/H_OF_MAXV_{name}_{convert_to_si(frequency)}Hz.png")
    print(f"H_OF_MAXV_{name}_{convert_to_si(frequency)}Hz.png CREATED")
    plt.clf()

def plot_max_v_and_v_by_max_midheight(transmitter):
    name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
    V_BY_MID_HEIGHT = get_v_by_mid_height_map(
        frequency, t_h, r_h, t_lon, t_lat, span_lon, span_lat)
    V = get_v_map(
        frequency, t_h, r_h, t_lon, t_lat, span_lon, span_lat)
    v_min = min([np.nanmin(V["V"]), np.nanmin(V_BY_MID_HEIGHT["V"])])
    v_max = max([np.nanmax(V["V"]), np.nanmax(V_BY_MID_HEIGHT["V"])])

    fig = plt.pcolormesh(
        V_BY_MID_HEIGHT["X"], V_BY_MID_HEIGHT["Y"], V_BY_MID_HEIGHT["V"], shading="auto")
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(f"V by mid-height of the ray near {name}")
    cbar = plt.colorbar(fig)
    plt.clim(v_min, v_max)
    cbar.set_label('V-factor')
    plt.savefig(
        f"main/IMGS/V_MAP/V_by_midheight_{name}_{convert_to_si(frequency)}Hz.png")
    print(f"V_by_midheight_{name}_{convert_to_si(frequency)}Hz.png CREATED")
    plt.clf()

    fig = plt.pcolormesh(
        V["X"], V["Y"], V["V"], shading="auto")
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(
        f"Max V of the ray near {name}")
    cbar = plt.colorbar(fig)
    plt.clim(v_min, v_max)
    cbar.set_label('V-factor')
    plt.savefig(
        f"main/IMGS/V_MAP/MAXV_{name}_{convert_to_si(frequency)}Hz.png")
    print(f"MAXV_{name}_{convert_to_si(frequency)}Hz.png CREATED")
    plt.clf()

    V_DIFFERENCE = pd.DataFrame(V["V"]) - pd.DataFrame(V_BY_MID_HEIGHT["V"])
    V_DIFFERENCE = V_DIFFERENCE.abs()
    fig = plt.pcolormesh(
        V["X"], V["Y"], V_DIFFERENCE, shading="auto")
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(
        f"Max V of the ray near {name}")
    cbar = plt.colorbar(fig)
    cbar.set_label('V-factor')
    plt.savefig(
        f"main/IMGS/V_MAP/V_DIFFERENCE_{name}_{convert_to_si(frequency)}Hz.png")
    print(f"V_DIFFERENCE_{name}_{convert_to_si(frequency)}Hz.png CREATED")
    plt.clf()


def plot_differnce_of_max_v_and_v_by_observer(transmitter):
    name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
    V_BY_OBSERVER = get_observer_predicted_v_map(
        frequency, t_h, r_h, t_lon, t_lat, span_lon, span_lat)
    V = get_v_map(
        frequency, t_h, r_h, t_lon, t_lat, span_lon, span_lat)
        
    v_min = min([np.nanmin(V["V"]), np.nanmin(V_BY_OBSERVER["V"])])
    v_max = max([np.nanmax(V["V"]), np.nanmax(V_BY_OBSERVER["V"])])

    fig = plt.pcolormesh(
        V_BY_OBSERVER["X"], V_BY_OBSERVER["Y"], V_BY_OBSERVER["V"], shading="auto")
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(f"V by observer of the ray near {name}")
    cbar = plt.colorbar(fig)
    plt.clim(v_min, v_max)
    cbar.set_label('V-factor')
    plt.savefig(
        f"main/IMGS/V_MAP/V_by_observer_{name}_{convert_to_si(frequency)}Hz.png")
    print(f"V_by_observer_{name}_{convert_to_si(frequency)}Hz.png CREATED")
    plt.clf()

    fig = plt.pcolormesh(
        V["X"], V["Y"], V["V"], shading="auto")
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(
        f"Max V of the ray near {name}")
    cbar = plt.colorbar(fig)
    plt.clim(v_min, v_max)
    cbar.set_label('V-factor')
    plt.savefig(
        f"main/IMGS/V_MAP/MAXV_{name}_{convert_to_si(frequency)}Hz.png")
    print(f"MAXV_{name}_{convert_to_si(frequency)}Hz.png CREATED")
    plt.clf()

    V_DIFFERENCE = pd.DataFrame(V["V"]) - pd.DataFrame(V_BY_OBSERVER["V"])
    V_DIFFERENCE = V_DIFFERENCE.abs()
    fig = plt.pcolormesh(
        V["X"], V["Y"], V_DIFFERENCE, shading="auto")
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(
        f"Max V of the ray near {name}")
    cbar = plt.colorbar(fig)
    cbar.set_label('V-factor')
    plt.savefig(
        f"main/IMGS/V_MAP/V_DIFFERENCE_{name}_{convert_to_si(frequency)}Hz.png")
    print(f"V_DIFFERENCE_{name}_{convert_to_si(frequency)}Hz.png CREATED")
    plt.clf()

