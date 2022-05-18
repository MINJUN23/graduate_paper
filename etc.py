import matplotlib.pyplot as plt
from get_map import get_local_dted
from utility import to_utm, get_dots_in_line
from transmitter import transmitters
from math import sqrt


DeogyuTransmitter = transmitters[1]
ChiakTransmitter = transmitters[2]

name, t_lon, t_lat, span_lon, span_lat, t_h = DeogyuTransmitter()
dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)

x, y = to_utm(dted_data["grid_lon"][0], dted_data["grid_lat"][0])

for i in range(1, 10):
    nx, ny = to_utm(dted_data["grid_lon"][i], dted_data["grid_lat"][0])
    print(nx, ny)
    print(f"Distance : {sqrt((nx-x)*(nx-x)+(ny-y)*(ny-y))}")
    x, y = nx, ny
