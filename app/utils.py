import numpy as np

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
    ln = 0
    while True:
        for d in range(8):
            dx, dy = DX[d], DY[d]
            ms = [(dx, dy) for i in range(ln)]
            if gravity_check(planet_r, x0, y0, vx0, vy0, ms):
                return ms
        ln += 1


def stop(x, y, vx, vy):
    '''
    return tuple(int, int)
    速度の絶対値が小さくなるような加速方向を返す
    運が悪いとplanetに落ちる
    '''
    def _stop(v, g):
        v_next = v + g
        if v_next > 0:
            return -1
        elif v_next < 0:
            return +1
        else:
            return 0
    gx, gy = calc_gravity(x, y)
    return (_stop(vx, gx), _stop(vy, gy))


def is_safe_zone(planet_r, gravity_r, x, y):
    """
    (x, y)が安全な場所ならTrue
    """
    mx = max(abs(x), abs(y))
    return planet_r < mx < gravity_r


def get_random_accel(planet_r, gravity_r, x0, y0, vx0, vy0):
    """
    (x, y), (vx, vy)時に加速しても安全な方向をランダムに選ぶ
    全部ダメなら適当に返す
    安全かどうかは20回くらい中心と端の近い方から離れる動きをして判断する
    """
    axy = list(zip(DX, DY))
    np.random.shuffle(axy)
    MAX_STEPS = 20

    def _is_safe(planet_r, gravity_r, x, y, vx, vy, max_steps):
        if not is_safe_zone(planet_r, gravity_r, x, y):
            return False

        for i in range(max_steps):
            dx_planet = abs(x)-planet_r
            dx_gravity = gravity_r-abs(x)
            dy_planet = abs(y)-planet_r
            dy_gravity = gravity_r-abs(y)
            vx += 1 if dx_planet < dx_gravity else -1
            vy += 1 if dy_planet < dy_gravity else -1
            next_pos(x, y, vx, vy)
            if not is_safe_zone(planet_r, gravity_r, x, y):
                return False

    for ax, ay in axy:
        x, y, vx, vy = x0, y0, vx0, vy0
        vx += ax
        vx += ax
        next_pos(x, y, vx, vy)
        if _is_safe(planet_r, gravity_r, x, y, vx, vy, MAX_STEPS):
            return ax, ay
    return axy[0]
