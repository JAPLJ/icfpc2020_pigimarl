import random


def sign(val):
    if val > 0:
        return 1
    elif val < 0:
        return -1
    else:
        return 0


def calc_gravity(x, y):
    """
    座標 (x, y) に働く重力のベクトルを返す
    :param x:
    :param y:
    :return:
    """
    if abs(x) > abs(y):
        return -sign(x), 0
    elif abs(x) < abs(y):
        return 0, -sign(y)
    else:
        return -sign(x), -sign(y)


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


def next_pos(x, y, vx, vy):
    gx, gy = calc_gravity(x, y)
    vx += gx
    vy += gy
    x += vx
    y += vy
    return x, y, vx, vy


DX = [-1, -1, -1, 0, 1, 1, 1, 0]
DY = [-1, 0, 1, 1, 1, 0, -1, -1]


def gravity_check(planet_r, x0, y0, vx0, vy0, moves):
    """
    (x0, y0) から速度 (vx0, vy0) で始めて、かつ最初の len(moves) 回は moves に従って accel するとする
    このとき 256 ターンにわたって墜落しないかつ外に出ないなら True を返す
    """
    x, y = x0, y0
    vx, vy = vx0, vy0
    for i in range(256):
        if i < len(moves):
            vx, vy = vx + moves[i][0], vy + moves[i][1]
        (x, y, vx, vy) = next_pos(x, y, vx, vy)
        if max(abs(x), abs(y)) <= planet_r:
            return False
    return True


def go_into_orbit(planet_r, x0, y0, vx0, vy0):
    """
    (x0, y0) から速度 (vx0, vy0) で始めたとき、256 ターンにわたって墜落しないかつ外に出ないような
    最初に行うべき accel の列を返す
    """
    ln = 1
    while True:
        p = list(range(8))
        random.shuffle(p)
        for i in range(8):
            d = p[i]
            dx, dy = DX[d], DY[d]
            ms = [(dx, dy) for i in range(ln)]
            if gravity_check(planet_r, x0, y0, vx0, vy0, ms):
                return ms
        ln += 1


def walk_on_square_orbit(planet_r, x, y, vx, vy, d):
    if (vx, vy) == (0, 0):  # 静止状態ならまず時計回りに動き出す
        if x <= planet_r and y < -planet_r:  # 左上
            wx, wy = 1, 0
        elif x > planet_r and y <= planet_r:  # 右上
            wx, wy = 0, 1
        elif x >= -planet_r and y > planet_r:  # 右下
            wx, wy = -1, 0
        elif x < -planet_r and y >= -planet_r:  # 左下
            wx, wy = 0, -1
        else:
            print('(x, y) が planet 内だし')
            exit(2)

    else:
        ma = max(x, y)
        next_ma = max(x + vx, y + vy)
        mi = min(x, y)
        next_mi = min(x + vx, y + vy)

        if ma == d and next_ma == d + 1:  # 半径 d の軌道から外れそうだから右折する
            wx, vy = -vy, vx
        elif mi == d and next_mi == d + 1:  # 半径 d の軌道に入れそうだから右折する
            wx, vy = -vy, vx
        else:  # 現状維持
            wx, wy = vx, vy

    gx, gy = calc_gravity(x, y)
    return wx - vx - gx, wy - vy - gy


def move_to_target(planet_r, x, y, vx, vy, tx, ty):
    if (x, y) == (tx, ty):
        gx, gy = calc_gravity(x, y)
        return -vx - gx, -vy - gy
    else:
        return walk_on_square_orbit(planet_r, x, y, vx, vy, max(tx, ty))
