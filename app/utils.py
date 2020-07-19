from typing import Tuple


def l_inf_dist(x1, y1, x2, y2) -> int:
    """
    位置p1とp2のl_infty距離を計算する
    """
    return max(abs(x1 - x2), abs(y1 - y2))


def normalize_vector(x, y) -> Tuple[int, int]:
    if abs(x) > 0:
        x //= abs(x)
    if abs(y) > 0:
        y //= abs(y)
    return x, y


def calc_normalized_direction(x1, y1, x2, y2) -> Tuple[int, int]:
    """
    (x1, y1) から (x2, y2) への向きを返す
    ただし、各成分は -1, 0, 1のいずれかの値
    """
    dx = x2 - x1
    dy = y2 - y1
    return normalize_vector(dx, dy)


def calc_gravity_acceration(x, y, gravity_radius) -> Tuple[int, int]:
    d = l_inf_dist(x, y, 0, 0)
    if d > gravity_radius:
        return 0, 0

    dir = calc_normalized_direction(x, y, 0, 0)
    if abs(x) == abs(y) == d:
        return dir
    elif abs(x) == d:
        return dir[0], 0
    else:
        return 0, dir[1]


def laser_damage(atk_ship_x, atk_ship_y, target_x, target_y, laser_power):
    """
    (atk_ship_x, atk_ship_y) から(target_x, target_y)に対してレーザーを射出して、その地点へ与えるダメージ。
    距離減衰は別に考える必要がある。
    """
    vmax = laser_power * 3
    x_dist = abs(atk_ship_x - target_x)
    y_dist = abs(atk_ship_y - target_y)
    d = max([x_dist, y_dist])
    if d == 0:
        return vmax
    v0 = max(0, vmax - (d - 1))
    y = y_dist if x_dist > y_dist else x_dist
    if y > d // 2:
        y = d - y
    v = max(0, v0 - (vmax * 2 * y // d))
    return abs(v)

