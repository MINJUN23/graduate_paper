import matplotlib.pyplot as plt
from get_map import get_local_dted
from utility import to_utm, get_dots_in_line
from transmitter import transmitters
from math import sqrt

DeogyuTransmitter = transmitters[1]
ChiakTransmitter = transmitters[2]


def minus_midheight_case():
    name, t_lon, t_lat, span_lon, span_lat, t_h = DeogyuTransmitter()
    dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)
    t_x, t_y = to_utm(t_lon, t_lat)
    dots = get_dots_in_line(59, 59, 87, 59)
    distance_list = []
    height_list = []
    for dot in dots:
        x, y = to_utm(dted_data["grid_lon"][dot[0]],
                      dted_data["grid_lat"][dot[1]])
        z = dted_data["grid_height"][dot[1]][dot[0]]
        distance = sqrt((t_x-x)*(t_x-x)+(t_y-y)*(t_y-y))
        distance_list.append(distance)
        height_list.append(z)
    plt.plot(distance_list, height_list)
    plt.xlabel("distance, (m)")
    plt.ylabel("height, (m)")
    plt.title(f"DeogYu to another mountain when midheight is under -200m")
    plt.show()


def minus_height_of_max_v_case():
    name, t_lon, t_lat, span_lon, span_lat, t_h = DeogyuTransmitter()
    dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)
    t_x, t_y = to_utm(dted_data["grid_lon"][59],
                      dted_data["grid_lat"][59])
    dots = [(59, 59)]
    dots += get_dots_in_line(59, 59, 115, 12)
    dots.append((115, 12))
    distance_list = []
    height_list = []
    for dot in dots:
        x, y = to_utm(dted_data["grid_lon"][dot[0]],
                      dted_data["grid_lat"][dot[1]])
        z = dted_data["grid_height"][dot[1]][dot[0]]
        distance = sqrt((t_x-x)*(t_x-x)+(t_y-y)*(t_y-y))
        distance_list.append(distance)
        height_list.append(z)
    plt.plot(distance_list, height_list)
    plt.xlabel("distance, (m)")
    plt.ylabel("height, (m)")
    plt.title(f"DeogYu to another mountain when height of max-v is under -200m")
    plt.show()


minus_height_of_max_v_case()
