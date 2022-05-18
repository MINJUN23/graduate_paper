from cmath import isnan
import numpy as np
from math import floor, ceil, sqrt, pi, log10
from pyproj import Proj
# Utm zone of Daejeon is 52

to_utm = Proj(proj='utm', zone=52, ellps='WGS84', preserve_units=False)
c = 299792458


def convert_to_si(num):
    K = 1000
    M = 1000000
    G = 1000000000
    T = 1000000000000
    if num < K:
        return f"{num}"
    elif num >= K and num < M:
        return f"{num/K}K"
    elif num >= M and num < G:
        return f"{num/M}M"
    elif num >= G and num < T:
        return f"{num/G}G"
    elif num >= T:
        return f"{num/T}T"


def get_index(dted_data, t_lon, t_lat):
    t_ix = np.absolute(
        dted_data["grid_lon"] - t_lon).argmin()  # nearest lon index
    t_iy = np.absolute(
        dted_data["grid_lat"] - t_lat).argmin()  # nearest lat index
    return (t_ix, t_iy)


def close_bound(bounding_num, center_num):
    bounding_num = float(bounding_num)
    if bounding_num - floor(bounding_num) == 0.5:
        if bounding_num > center_num:
            return floor(bounding_num)
        else:
            return ceil(bounding_num)
    else:
        return round(bounding_num)


def get_range(start, end):
    if start <= end:
        return range(start, end+1)
    else:
        return range(start, end-1, -1)


def get_dots_in_line(t_ix, t_iy, r_ix, r_iy):
    dots_in_line = []

    if t_ix == r_ix:
        dots_in_line += [(t_ix, iy) for iy in get_range(t_iy, r_iy)]
    else:
        a = float(t_iy - r_iy)/float(t_ix-r_ix)
        if r_ix > t_ix:
            dots_in_line += [(t_ix, t_iy+iy)
                             for iy in list(get_range(0, close_bound(0.5*a, 0)))]
            if r_ix-t_ix != 1:
                for ix in get_range(1, r_ix-t_ix-1):
                    by = t_iy + a*ix
                    min_bound = close_bound(by-0.5*a, by)
                    max_bound = close_bound(by+0.5*a, by)
                    dots_in_line += [(t_ix+ix, iy)
                                     for iy in list(get_range(min_bound, max_bound))]
            dots_in_line += [(r_ix, r_iy+iy)
                             for iy in list(get_range(0, close_bound(-0.5*a, 0)))]
        elif r_ix < t_ix:
            dots_in_line += [(t_ix, t_iy+iy)
                             for iy in list(get_range(0, close_bound(-0.5*a, 0)))]
            if t_ix-r_ix != 1:
                for ix in get_range(-1, r_ix-t_ix+1):
                    by = t_iy + a*ix
                    min_bound = close_bound(by-0.5*a, by)
                    max_bound = close_bound(by+0.5*a, by)
                    dots_in_line += [(t_ix+ix, iy)
                                     for iy in list(get_range(min_bound, max_bound))]
            dots_in_line += [(r_ix, r_iy+iy)
                             for iy in list(get_range(0, close_bound(0.5*a, 0)))]
    return dots_in_line


def get_friis_gain(f, r):
    try:
        return 10 * log10(c*c/((4*pi*r*f) * (4*pi*r*f)))
    except Exception:
        return np.NaN


def get_v_factor(h, f, d1, d2):
    if h == 0:
        return -1
    try:
        return h * sqrt(2*f*(d1+d2)/(c*d1*d2))
    except Exception:
        return np.NaN


def get_loss_by_knife_edge(v):
    try:
        if v > -0.78:
            loss = 6.9 + 20 * log10(sqrt((v-0.1)*(v-0.1)+1) + v - 0.1)
            return loss
        else:
            return 0

    except Exception:
        return np.NaN


def get_gain(f, r, h, d1, d2):
    try:
        v = get_v_factor(h, f, d1, d2)
        loss = get_loss_by_knife_edge(v)
        return get_friis_gain(f, r) - loss
    except Exception:
        return np.NaN


def get_mid_height(dted_data, t_ix, t_iy, t_h, r_ix, r_iy, r_h):
    if t_ix == r_ix and t_iy == r_iy:
        return (0, np.NaN)

    dots_in_line = get_dots_in_line(t_ix, t_iy, r_ix, r_iy)
    t_x, t_y = to_utm(dted_data["grid_lon"][t_ix], dted_data["grid_lat"][t_iy])
    t_z = dted_data["grid_height"][t_iy][t_ix]
    r_x, r_y = to_utm(dted_data["grid_lon"][r_ix], dted_data["grid_lat"][r_iy])
    r_z = dted_data["grid_height"][r_iy][r_ix]
    distance = sqrt((t_x-r_x)*(t_x-r_x) + (t_y-r_y)
                    * (t_y-r_y) + (t_z + t_h - r_z - r_h) * (t_z + t_h - r_z - r_h))
    D = sqrt((t_x-r_x)*(t_x-r_x) + (t_y-r_y)*(t_y-r_y))
    DZ = r_z + r_h - t_z - t_h
    blocked_dots = []
    for dot in dots_in_line:
        try:
            x, y = to_utm(dted_data["grid_lon"][dot[0]],
                          dted_data["grid_lat"][dot[1]])
            z = dted_data["grid_height"][dot[1]][dot[0]] + r_h
            d = sqrt((x-t_x) * (x-t_x) + (y-t_y)*(y-t_y))
            lz = t_z + t_h + DZ / D * d
            if z > lz:
                blocked_dots.append((distance, (z - lz, d, D - d), dot))
        except IndexError:
            print(f"get_mid_height indexError : {dot}")
        except Exception as e:
            print(e, "Exception in get_mid_height")
    if len(blocked_dots) == 0:
        return (distance, np.NaN)
    else:
        return max(blocked_dots, key=lambda x: x[1][0])


def max_key(x):
    if np.isnan(x):
        return -1


def get_max_v(dted_data, f, t_ix, t_iy, t_h, r_ix, r_iy, r_h):
    if t_ix == r_ix and t_iy == r_iy:
        return {"v": np.nan, "h": np.nan, "d1": np.nan, "d2": np.nan}

    dots_in_line = get_dots_in_line(t_ix, t_iy, r_ix, r_iy)
    t_x, t_y = to_utm(dted_data["grid_lon"][t_ix], dted_data["grid_lat"][t_iy])
    t_z = dted_data["grid_height"][t_iy][t_ix]
    r_x, r_y = to_utm(dted_data["grid_lon"][r_ix], dted_data["grid_lat"][r_iy])
    r_z = dted_data["grid_height"][r_iy][r_ix]
    distance = sqrt((t_x-r_x)*(t_x-r_x) + (t_y-r_y)
                    * (t_y-r_y) + (t_z + t_h - r_z - r_h) * (t_z + t_h - r_z - r_h))
    D = sqrt((t_x-r_x)*(t_x-r_x) + (t_y-r_y)*(t_y-r_y))
    DZ = r_z + r_h - t_z - t_h

    # v_info : {"v": float, "h': float, "d1": float, "d2": float}
    v_info_list = []
    for dot in dots_in_line:
        x, y = to_utm(dted_data["grid_lon"][dot[0]],
                      dted_data["grid_lat"][dot[1]])
        z = dted_data["grid_height"][dot[1]][dot[0]]
        d = sqrt((x-t_x) * (x-t_x) + (y-t_y)*(y-t_y))
        lz = t_z + t_h + DZ / D * d
        v = get_v_factor(z-lz, f, d, D-d)
        if np.isnan(v):
            v_info = {"v": np.nan, "h": np.nan, "d1": np.nan, "d2": np.nan}
        else:
            v_info = {"v": v, "h": z-lz, "d1": d, "d2": D-d}
        v_info_list.append(v_info)
    if len(v_info_list) == 0:
        return {"v": np.nan, "h": np.nan, "d1": np.nan, "d2": np.nan}
    else:
        print(max(v_info_list, key=lambda x: x["v"]))
        return max(v_info_list, key=lambda x: x["v"])
