import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from math import sqrt
from map_factory.get_map import get_local_dted
from map_factory.utility.utility import to_utm, get_dots_in_line, get_v_factor
from environments.transmitter import transmitters

DeogyuTransmitter = transmitters[1]
ChiakTransmitter = transmitters[2]


def minus_midheight_case():
    name, t_lon, t_lat, span_lon, span_lat, t_h = ChiakTransmitter()
    dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)
    t_x, t_y = to_utm(dted_data["grid_lon"][59],
                      dted_data["grid_lat"][59])
    t_z = dted_data["grid_height"][59][59]
    r_x, r_y = to_utm(dted_data["grid_lon"][114], dted_data["grid_lat"][78])
    r_z = dted_data["grid_height"][78][114]
    D = sqrt((t_x-r_x)*(t_x-r_x) + (t_y-r_y)*(t_y-r_y))
    DZ = r_z - t_z 

    dots = [(59, 59)]
    dots += get_dots_in_line(59, 59, 114, 78)
    dots.append((114, 78))
    distance_list = []
    h_list = []
    v_list = []
    for dot in dots:
        x, y = to_utm(dted_data["grid_lon"][dot[0]],
                      dted_data["grid_lat"][dot[1]])
        z = dted_data["grid_height"][dot[1]][dot[0]]
        d = sqrt((t_x-x)*(t_x-x)+(t_y-y)*(t_y-y))
        lz = t_z + t_h + DZ / D * d
        v = get_v_factor(z-lz, 1000000, d, D-d)

        distance_list.append(d)
        h_list.append(z)
        v_list.append(v)
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('distance, m') 
    ax1.set_ylabel('v-factor', color=color)
    ax1.plot(distance_list, v_list, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('height, m', color=color)  # we already handled the x-label with ax1
    ax2.plot(distance_list, h_list, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(18, 9, forward=True)
    plt.title(f"Chiak to another mountain when midheight is under -200m")
    txt=f"Transmitter - lat : [{t_lat}], lon : [{t_lon}]\nReceiver - lat {dted_data['grid_lat'][78]}, lon : {dted_data['grid_lon'][114]}"
    plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
    plt.savefig(f"main/IMGS/COS/under-200_midheight_{name}.png")
    print(f"under-200_midheight_{name}.png CREATED")
    plt.clf()


def minus_height_of_max_v_case():
    name, t_lon, t_lat, span_lon, span_lat, t_h = DeogyuTransmitter()
    dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)
    t_x, t_y = to_utm(dted_data["grid_lon"][59],
                      dted_data["grid_lat"][59])
    t_z = dted_data["grid_height"][59][59]
    r_x, r_y = to_utm(dted_data["grid_lon"][115], dted_data["grid_lat"][12])
    r_z = dted_data["grid_height"][12][115]
    D = sqrt((t_x-r_x)*(t_x-r_x) + (t_y-r_y)*(t_y-r_y))
    DZ = r_z - t_z 

    dots = [(59, 59)]
    dots += get_dots_in_line(59, 59, 115, 12)
    dots.append((115, 12))
    distance_list = []
    h_list = []
    v_list = []
    for dot in dots:
        x, y = to_utm(dted_data["grid_lon"][dot[0]],
                      dted_data["grid_lat"][dot[1]])
        z = dted_data["grid_height"][dot[1]][dot[0]]
        d = sqrt((t_x-x)*(t_x-x)+(t_y-y)*(t_y-y))
        lz = t_z + t_h + DZ / D * d
        v = get_v_factor(z-lz, 1000000, d, D-d)

        distance_list.append(d)
        h_list.append(z)
        v_list.append(v)
    # plt.plot(distance_list, h_list)
    # plt.xlabel("distance, (m)")
    # plt.ylabel("height, (m)")
    # plt.title(f"DeogYu to another mountain when height of max-v is under -200m")
    # plt.show()
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('distance, m')
    ax1.set_ylabel('v-factor', color=color)
    ax1.plot(distance_list, v_list, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('height, m', color=color)  # we already handled the x-label with ax1
    ax2.plot(distance_list, h_list, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.set_size_inches(18, 9, forward=True)
    txt=f"Transmitter - lat : [{t_lat}], lon : [{t_lon}]\nReceiver - lat {dted_data['grid_lat'][12]}, lon : {dted_data['grid_lon'][115]}"
    plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=12)
    plt.title(f"Deogyu to another mountain when height of max_v is under -200m")
    plt.savefig(f"main/IMGS/COS/under-200_height_of_max_v_{name}.png")
    print(f"under-200_height_of_max_v_{name}.png CREATED")
    plt.clf()


def plot_example_of_dots_in_line(t_x,t_y,r_x,r_y):
    dots = [(t_x,t_y)]
    dots += get_dots_in_line(t_x,t_y,r_x,r_y)
    dots += [(r_x,r_y)]
    x_list = [t_x,r_x]
    y_list = [t_y,r_y]

    fig, ax =plt.subplots()
    ax.set_xlim([t_x-2,r_x+2])
    ax.set_ylim([t_y-2,r_y+2])

    x_ticks = np.arange(t_x-1.5, r_x+2.5, 1)
    x_major_ticks = np.arange(t_x-1.5, r_x+2.5, 10)
    y_ticks = np.arange(t_y-1.5, r_y+2.5, 1)
    y_major_ticks =np.arange(t_y-1.5, r_y+2.5, 10)

    ax.set_xticks(x_ticks, minor=True)
    ax.set_xticks(x_major_ticks,)
    ax.set_yticks(y_ticks, minor=True)
    ax.set_yticks(y_major_ticks)
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)

    plt.plot(x_list, y_list)
    for dot in dots:
        ax.add_patch(
        patches.Rectangle(
            (dot[0]-0.5,dot[1]-0.5),
            1,
            1,
            edgecolor = 'blue',
            fill=True, 
            alpha=0.5
        ))


    plt.show()

plot_example_of_dots_in_line(1,2,18,37)
