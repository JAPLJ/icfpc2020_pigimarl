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

def next_pos(planet_r, x, y, vx, vy):
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


DX = [-1, -1, -1, 0, 1, 1, 1, 0]
DY = [-1, 0, 1, 1, 1, 0, -1, -1]


def gravity_check(planet_r, gravity_r, x0, y0, vx0, vy0, moves):
    """
    (x0, y0) から速度 (vx0, vy0) で始めて、かつ最初の len(moves) 回は moves に従って accel するとする
    このとき 256 ターンにわたって墜落しないかつ外に出ないなら True を返す
    """
    x, y = x0, y0
    vx, vy = vx0, vy0
    for i in range(256):
        if i < len(moves):
            vx, vy = vx + moves[i][0], vy + moves[i][1]
        (x, y, vx, vy) = next_pos(planet_r, gravity_r, x, y, vx, vy)
        if max(abs(x), abs(y)) <= planet_r or max(abs(x), abs(y)) > gravity_r:
            return False
    return True


def go_into_orbit(planet_r, gravity_r, x0, y0, vx0, vy0):
    """
    (x0, y0) から速度 (vx0, vy0) で始めたとき、256 ターンにわたって墜落しないかつ外に出ないような
    最初に行うべき accel の列を返す
    """
    ln = 1
    while True:
        for d in range(8):
            dx, dy = DX[d], DY[d]
            ms = [(dx, dy) for i in range(ln)]
            if gravity_check(planet_r, gravity_r, x0, y0, vx0, vy0, ms):
                return ms
        ln += 1