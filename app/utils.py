
import random
from collections import deque

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


def gravity_check(gravity_r, planet_r, x0, y0, vx0, vy0, moves, rot_sign=None):
    """
    (x0, y0) から速度 (vx0, vy0) で始めて、かつ最初の len(moves) 回は moves に従って accel するとする
    このとき 256 ターンにわたって墜落しないかつ外に出ないなら True を返す
    """
    x, y = x0, y0
    vx, vy = vx0, vy0
    rot_sum = 0
    for i in range(256):
        if i < len(moves):
            vx, vy = vx + moves[i][0], vy + moves[i][1]
        (x, y, vx, vy) = next_pos(x, y, vx, vy)
        rot_sum += x * vy - y * vx
        if max(abs(x), abs(y)) <= planet_r or max(abs(x), abs(y)) > gravity_r:
            return False
    if rot_sign is None:
        return True
    return sign(rot_sum) == rot_sign


def go_into_orbit(gravity_r, planet_r, x0, y0, vx0, vy0, rot_sign=None):
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
            if gravity_check(gravity_r, planet_r, x0, y0, vx0, vy0, ms, rot_sign):
                return ms
        ln += 1

def gravity_check_g(planet_r, gravity_r, x0, y0, vx0, vy0, moves):
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
        if max(abs(x), abs(y)) <= planet_r or max(abs(x), abs(y)) > gravity_r:
            return False
    return True


def go_into_orbit_g(planet_r, gravity_r, x0, y0, vx0, vy0):
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
            if gravity_check_g(planet_r, gravity_r, x0, y0, vx0, vy0, ms):
                return ms
        ln += 1

def future_orbit(gravity_r, planet_r, x0, y0, vx0, vy0, moves, turns):
    x, y = x0, y0
    vx, vy = vx0, vy0
    orbit = []
    for i in range(turns):
        if i < len(moves):
            vx, vy = vx + moves[i][0], vy + moves[i][1]
        (x, y, vx, vy) = next_pos(x, y, vx, vy)
        if max(abs(x), abs(y)) <= planet_r or max(abs(x), abs(y)) > gravity_r:
            break
        orbit.append((x, y))
    return orbit


def min_turn(gravity_r, planet_r, x0, y0, vx0, vy0, moves, turns, ships):
    orbit0 = future_orbit(gravity_r, planet_r, x0, y0, vx0, vy0, moves, turns)
    min_i = 1000
    for s in ships:
        orbit1 = future_orbit(gravity_r, planet_r, s.x, s.y, s.vx, s.vy, [], turns)
        for i in range(min(len(orbit0), len(orbit1))):
            x0, y0 = orbit0[i]
            x1, y1 = orbit1[i]
            if i >= len(moves) and max(abs(x0 - x1), abs(y0 - y1)) <= 3:
                min_i = min(min_i, i)
    return min_i


def fire_target(gravity_r, planet_r, x0, y0, vx0, vy0, turns, ships, max_ln, ub):
    mt_opt = ub + 1
    accs_opt = None

    for ln in range(1, max_ln + 1):
        p = list(range(8))
        random.shuffle(p)
        for i in range(8):
            d = p[i]
            dx, dy = DX[d], DY[d]
            ms = [(0, 0)] + [(dx, dy) for i in range(ln)]
            mt = min_turn(gravity_r, planet_r, x0, y0, vx0, vy0, ms, turns, ships)
            if mt < mt_opt:
                mt_opt = mt
                accs_opt = ms[1:]

    return accs_opt


def near_score(gravity_r, planet_r, x0, y0, vx0, vy0, moves, turns, ships):
    orbit0 = future_orbit(gravity_r, planet_r, x0, y0, vx0, vy0, moves, turns)
    if len(orbit0) < turns:
        return 0.0

    score = 0.0
    for s in ships:
        orbit1 = future_orbit(gravity_r, planet_r, s.x, s.y, s.vx, s.vy, [], turns)
        for i in range(min(len(orbit0), len(orbit1))):
            x0, y0 = orbit0[i]
            x1, y1 = orbit1[i]
            d = max(abs(x0 - x1), abs(y0 - y1))
            score += 1.0 / (d + 1)
    return score


def stalk(gravity_r, planet_r, x0, y0, vx0, vy0, turns, ships, max_ln):
    score_opt = -1
    accs_opt = None

    for ln in range(0, max_ln + 1):
        p = list(range(8))
        random.shuffle(p)
        for i in range(8):
            d = p[i]
            dx, dy = DX[d], DY[d]
            ms = [(dx, dy) for i in range(ln)]
            score = near_score(gravity_r, planet_r, x0, y0, vx0, vy0, ms, turns, ships)
            if score > score_opt:
                score_opt = score
                accs_opt = ms

    return accs_opt


# 8 近傍
neighbours = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]


def move_to_target(gravity_r, planet_r, sx, sy, vx, vy, tx, ty):
    """
    現在位置が (sx, sy) で現在速度が (vx, vy) のときに (tx, ty) へ移動して静止するための最初の加速度を返す
    注意: abs(vx) <= 1 かつ abs(vy) <= 1 でなければならない
    :param gravity_r:
    :param planet_r:
    :param sx:
    :param sy:
    :param vx:
    :param vy:
    :param tx:
    :param ty:
    :return:
    """
    gr = gravity_r
    gx, gy = calc_gravity(sx, sy)

    if (sx, sy) == (tx, ty):  # 目標の座標に到達したら静止する
        return -(vx + gx), -(vy + gy)

    dist = np.full((gr * 2 + 1, gr * 2 + 1), 10 ** 9)
    dist[tx + gr][ty + gr] = 0
    q = deque()
    q.append((tx, ty))

    while len(q) > 0:
        x, y = q.popleft()
        if (x, y) == (sx, sy):
            break

        for dx, dy in neighbours:
            nx = x + dx
            ny = y + dy
            if abs(nx) <= planet_r and abs(ny) <= planet_r:
                continue
            if abs(nx) <= gravity_r and abs(ny) <= gravity_r and dist[nx + gr][ny + gr] > dist[x + gr][y + gr] + 1:
                dist[nx + gr][ny + gr] = dist[x + gr][y + gr] + 1
                q.append((nx, ny))

    for dx, dy in neighbours:
        nx = sx + dx
        ny = sy + dy
        if abs(nx) <= gravity_r and abs(ny) <= gravity_r and dist[nx + gr][ny + gr] == dist[sx + gr][sy + gr] - 1:
            ax = dx - (vx + gx)
            ay = dy - (vy + gy)
            if abs(ax) <= 2 and abs(ay) <= 2:
                return ax, ay

    return -(vx + gx), -(vy + gy)  # 一旦静止して次のターンに備える


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


def guess_next(v):
    '''
    list vを受け取って周期性があるかを判定し，ある場合は次の要素を推測する
    ない場合はNone
    例: [-1, 0, 1, -1, 0, 1] -> -1
    '''
    for p in range(1, len(v) // 2 + 1):
        ok = True
        for i in range(len(v) - p):
            if v[i] != v[i + p]:
                ok = False
                break
        if ok:
            return v[-p]
    return None
