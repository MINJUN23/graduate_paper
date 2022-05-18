import matplotlib.pyplot as plt
import numpy as np
from map_factory import get_max_v_map, get_mid_height_map
from utility import convert_to_si
from transmitter import transmitters


r_h = 10
frequency = 1000000

max_h = 1600
min_h = -1000


def plot_max_v_from_transmitter(transmitter):
    name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
    V = get_max_v_map(
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
    plt.savefig(f"V_IMGS/MAXV_{name}_{convert_to_si(frequency)}Hz.png")
    print(f"MAXV_{name}_{convert_to_si(frequency)}Hz.png CREATED")
    plt.clf()


def plot_height_of_max_v_from_transmitter(transmitter):
    name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
    V = get_max_v_map(
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
        f"V_IMGS/H_OF_MAXV_{name}_{convert_to_si(frequency)}Hz.png")
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
        f"V_IMGS/MAX_MIDHEIGHT_{name}.png")
    print(f"MAX_MIDHEIGHT_{name}.png CREATED")
    plt.clf()


def plot_mvh_and_mh(transmitter):
    name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
    DATA = get_mid_height_map(
        t_h, r_h, t_lon, t_lat, span_lon, span_lat)
    V = get_max_v_map(
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
        f"V_IMGS/MAX_MIDHEIGHT_{name}.png")
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
        f"V_IMGS/H_OF_MAXV_{name}_{convert_to_si(frequency)}Hz.png")
    print(f"H_OF_MAXV_{name}_{convert_to_si(frequency)}Hz.png CREATED")
    plt.clf()


for transmitter in transmitters:
    plot_mvh_and_mh(transmitter)
    plot_max_v_from_transmitter(transmitter)
