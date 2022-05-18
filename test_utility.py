from re import L
import unittest
from utility import *
from get_map import get_korea_dted, get_local_dted

dted_data = get_korea_dted()
t_lon, t_lat = 127.3845, 36.3504
span_lon, span_lat = 2.0, 2.0
local_dted_data = get_local_dted(t_lon, t_lat, span_lon, span_lat)


class TestUtility(unittest.TestCase):
    def test_get_index(self):
        ix, iy = get_index(dted_data, t_lon, t_lat)
        min_lon = dted_data["grid_lon"][ix]
        max_lon = dted_data["grid_lon"][ix+1]
        min_lat = dted_data["grid_lat"][iy]
        max_lat = dted_data["grid_lat"][iy+1]

        self.assertTrue(min_lon < t_lon and max_lon > t_lon)
        self.assertTrue(min_lat < t_lat and max_lat > t_lat)

    def test_close_bound(self):
        bounding_num, center_num = 0.5, 2
        self.assertTrue(close_bound(bounding_num, center_num), 1)
        bounding_num, center_num = 3.5, 2
        self.assertTrue(close_bound(bounding_num, center_num), 3)

    def test_get_range(self):
        start, end = -2, 0
        self.assertTrue(list(get_range(start, end)) == [-2, -1, 0])
        start, end = 0, -2
        self.assertTrue(list(get_range(start, end)) == [0, -1, -2])
        start, end = 0, 0
        self.assertTrue(list(get_range(start, end)) == [0])

    def test_get_dots_in_line(self):
        t_ix, t_iy, r_ix, r_iy = 0, 0, 3, 4
        dots = get_dots_in_line(t_ix, t_iy, r_ix, r_iy)
        self.assertTrue(set(dots) == set(
            [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 3), (3, 3), (3, 4)]))
        t_ix, t_iy, r_ix, r_iy = 0, 0, -3, -4
        dots = get_dots_in_line(t_ix, t_iy, r_ix, r_iy)
        self.assertTrue(set(dots) == set(
            [(0, 0), (0, -1), (-1, -1), (-1, -2), (-2, -2), (-2, -3), (-3, -3), (-3, -4)]))
        t_ix, t_iy, r_ix, r_iy = 0, 0, -3, 4
        dots = get_dots_in_line(t_ix, t_iy, r_ix, r_iy)
        self.assertTrue(set(dots) == set(
            [(0, 0), (0, 1), (-1, 1), (-1, 2), (-2, 2), (-2, 3), (-3, 3), (-3, 4)]))
        t_ix, t_iy, r_ix, r_iy = 0, 0, 3, -4
        dots = get_dots_in_line(t_ix, t_iy, r_ix, r_iy)
        self.assertTrue(set(dots) == set(
            [(0, 0), (0, -1), (1, -1), (1, -2), (2, -2), (2, -3), (3, -3), (3, -4)]))

    def test_get_mid_height(self):
        r_lon, r_lat = 127.825, 35.63
        t_ix, t_iy = get_index(local_dted_data, t_lon, t_lat)
        r_ix, r_iy = get_index(local_dted_data, r_lon, r_lat)
        # 해발고도 200m지점의 recevier에서 중간에 최대높이 약 1300m의 산맥을 만난다. 그래서 약 1100m정도의 최대 height가 나와야 한다.
        mid_height = get_mid_height(local_dted_data, t_ix,
                                    t_iy, 10, r_ix, r_iy, 10)
        self.assertTrue(mid_height[1][0] > 1100)

    def test_get_loss_by_knife_edge(self):
        # v=-0.78이면 loss는 0에 가까워야 함. Propagation of radiowaves 140p, 단 식을 v > -0.78일때만 사용하므로 v=-0.77로 적용함.
        v = -0.77
        loss = get_loss_by_knife_edge(v)
        self.assertTrue(loss < 0.1 and loss > -0.1)
        # Propagation of radiowaves 140p Firgure 9.7 에 따르면 v=0일때 loss = -6에 가까움.
        v = 0
        loss = get_loss_by_knife_edge(v)
        self.assertTrue(loss < 6.1 and loss > 5.9)

    def test_get_frris_gain(self):
        f = 1000000
        r = 1000
        # 역제곱에 반비례하는지 확인
        gain_diffrence = get_friis_gain(f, r)-get_friis_gain(f*10, r)
        self.assertTrue(gain_diffrence < 20.01 and gain_diffrence > 19.99)
        gain_diffrence = get_friis_gain(f, r)-get_friis_gain(f, r*10)
        self.assertTrue(gain_diffrence < 20.01 and gain_diffrence > 19.99)

    def test_get_gain(self):
        gain = get_gain(1000000, 1000, 100, 500, 500)
        self.assertTrue(gain > -42.87 and gain < -42.86)


if __name__ == '__main__':
    unittest.main()
