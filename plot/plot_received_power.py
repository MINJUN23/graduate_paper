import matplotlib.pyplot as plt
from ..map_factory import get_received_power_map
from ..transmitter import transmitters
from ..utility import convert_to_si

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
    plt.savefig(f"ReceivedPowerImgs/{name}_{convert_to_si(frequency)}Hz.png")
    print(f"{name}_{convert_to_si(frequency)}Hz.png CREATED")
    plt.clf()

def plot_expected_received_power_near_transmitter(frequency, transmitter):
    pass




for transmitter in transmitters:
    for frequency in frequenct_list:
        plot_received_power_near_transmitter(frequency, transmitter)
