import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from map_factory import get_distance_map, get_difference_map, get_slope_map
from transmitter import transmitters
from utility import to_utm
# 대전의 위도 : 36.3504° N
# 대전의 경도 : 127.3845° E


def plot_distance_from_transmitter(transmitter):
    name, t_lon, t_lat, span_lon, span_lat, _ = transmitter()
    utm_data = get_distance_map(t_lon, t_lat, span_lon, span_lat)
    fig = plt.pcolormesh(
        utm_data["X"], utm_data["Y"], utm_data["R"], shading="auto")
    fig.axes.set_aspect("equal")
    x, y = to_utm(t_lon, t_lat)
    plt.plot(x, y, 'ro', markersize=2)
    plt.xlabel("UTM-X, (m)")
    plt.ylabel("UTM-N, (m)")
    plt.title(f"Distance From {name}")
    cbar = plt.colorbar(fig)
    cbar.set_label('Distance, m')

    plt.show()


def plot_difference_from_transmitter(transmitter):
    name, t_lon, t_lat, span_lon, span_lat, _ = transmitter()
    utm_data = get_difference_map(t_lon, t_lat, span_lon, span_lat)
    fig = plt.pcolormesh(
        utm_data["X"], utm_data["Y"], utm_data["D"], shading="auto")
    fig.axes.set_aspect("equal")
    x, y = to_utm(t_lon, t_lat)
    plt.plot(x, y, 'ro', markersize=2)
    plt.xlabel("UTM-X, (m)")
    plt.ylabel("UTM-N, (m)")
    plt.title(f"Distance Difference From {name}")
    cbar = plt.colorbar(fig)
    cbar.set_label('Diffrence, m')

    plt.show()


def plot_slope_from_transmitter(transmitter):
    name, t_lon, t_lat, span_lon, span_lat, _ = transmitter()
    utm_data = get_slope_map(t_lon, t_lat, span_lon, span_lat)
    fig = plt.pcolormesh(
        utm_data["X"], utm_data["Y"], utm_data["S"], shading="auto")
    fig.axes.set_aspect("equal")
    x, y = to_utm(t_lon, t_lat)
    plt.plot(x, y, 'ro', markersize=2)
    plt.xlabel("UTM-X, (m)")
    plt.ylabel("UTM-N, (m)")
    plt.title(f"Slope Of Ray From {name}")
    cbar = plt.colorbar(fig)
    cbar.set_label('Slope, degree')

    plt.show()


for transmitter in transmitters:
    plot_slope_from_transmitter(transmitter)
