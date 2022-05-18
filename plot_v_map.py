import matplotlib.pyplot as plt
from map_factory import get_max_v_map
from transmitter import transmitters

r_h = 10


def plot_max_v_from_transmitter(transmitter):
    name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
    V = get_max_v_map(
        t_h, r_h, t_lon, t_lat, span_lon, span_lat)
    fig = plt.pcolormesh(
        V["X"], V["Y"], V["V"], shading="auto")
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(f"Max value of v factor of the ray near {name}")
    cbar = plt.colorbar(fig)
    cbar.set_label('V - factor')

    plt.show()


def plot_height_of_max_v_from_transmitter(transmitter):
    name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
    V = get_max_v_map(
        t_h, r_h, t_lon, t_lat, span_lon, span_lat)
    fig = plt.pcolormesh(
        V["X"], V["Y"], V["H"], shading="auto")
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(f"Height of max v factor of the ray near {name}")
    cbar = plt.colorbar(fig)
    cbar.set_label('Height, m')

    plt.show()


for transmitter in transmitters:
    plot_max_v_from_transmitter(transmitter)
    plot_height_of_max_v_from_transmitter(transmitter)
