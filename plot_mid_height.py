import matplotlib.pyplot as plt
from map_factory import get_midheight_map
from transmitter import transmitters

r_h = 10


def plot_midheight_from_transmitter(transmitter):
    name, t_lon, t_lat, span_lon, span_lat, t_h = transmitter()
    MD = get_midheight_map(
        t_h, r_h, t_lon, t_lat, span_lon, span_lat)
    fig = plt.pcolormesh(
        MD["X"], MD["Y"], MD["D"], shading="auto")
    fig.axes.set_aspect("equal")
    plt.plot(t_lon, t_lat, "ro", markersize=2)
    plt.xlabel("LAT, (degree)")
    plt.ylabel("LON, (degree)")
    plt.title(f"Max mid-height of the ray near {name}")
    cbar = plt.colorbar(fig)
    cbar.set_label('MIDHEIGHT, m')

    plt.show()


for transmitter in transmitters:
    plot_midheight_from_transmitter(transmitter)
