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


def next_pos(planet_r, gravity_r, x, y, vx, vy):
    if abs(x) <= abs(y):
        if y > 0:
            vy -= 1
        elif y < 0:
            vy += 1
    if abs(y) <= abs(x):
        if x > 0:
            vx -= 1
        elif x < 0:
            vx += 1
    x, y = x + vx, y + vy
    return (x, y, vx, vy)


def sign(val):
    if val > 0:
        return 1
    elif val < 0:
        return -1
    else:
        return 0


def calc_gravity(gravity_r, x, y):
    """
    座標 (x, y) に働く重力のベクトルを返す
    :param gravity_r:
    :param x:
    :param y:
    :return:
    """
    # 重力半径外
    if max(abs(x), abs(y)) > gravity_r:
        return 0, 0

    if abs(x) > abs(y):
        return -sign(x), 0
    elif abs(x) < abs(y):
        return 0, -sign(y)
    else:
        return -sign(x), -sign(y)
