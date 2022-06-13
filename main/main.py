from plot.plot_v_map import plot_differnce_of_max_v_and_v_by_observer
from plot.plot_received_power import plot_abs_differences, plot_received_and_observer_predicted
from environments.transmitter import all_transmitters, test_transmitters

frequency_list = list(range(80000000, 100000001, 5000000))

for frequency in frequency_list:
    for transmitter in test_transmitters:
        plot_abs_differences(frequency, transmitter)
        plot_received_and_observer_predicted(frequency, transmitter)

for transmitter in all_transmitters:
    plot_differnce_of_max_v_and_v_by_observer(transmitter)


