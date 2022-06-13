from plot.plot_v_map import plot_differnce_of_max_v_and_v_by_observer
from environments.transmitter import transmitters

frequency_list = list(range(80000000, 100000001, 5000000))


for transmitter in transmitters:
    plot_differnce_of_max_v_and_v_by_observer(transmitter)
