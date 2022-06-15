from plot.plot_map import plot_surround_of_transmitter
from plot.plot_v_map import plot_differnce_of_max_v_and_v_by_observer
from plot.plot_received_power import plot_abs_differences, plot_received_and_observer_predicted, plot_diffence_of_error
from environments.transmitter import all_transmitters, test_transmitters

frequency_list = list(range(80000000, 100000001, 5000000))

for transmitter in all_transmitters:
    plot_diffence_of_error(90000000, transmitter)


