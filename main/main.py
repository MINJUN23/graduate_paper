from map_factory.outlier_check import check_outlier_error
from environments.transmitter import transmitters

frequency_list = list(range(80000000, 100000001, 5000000))

for transmitter in transmitters:
    for frequency in frequency_list:
        check_outlier_error(frequency, transmitter)
