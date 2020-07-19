from common_interface import *
from ai_interface import *

import sys
sys.path.append('../app/')
from utils import *


DX = [-1, -1, -1, 0, 1, 1, 1, 0]
DY = [-1, 0, 1, 1, 1, 0, -1, -1]


def gravity_check(planet_r, gravity_r, x0, y0, vx0, vy0, moves):
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
    ln = 1
    while True:
        for d in range(8):
            dx, dy = DX[d], DY[d]
            ms = [(dx, dy) for i in range(ln)]
            if gravity_check(planet_r, gravity_r, x0, y0, vx0, vy0, ms):
                print(ms)
                return ms
        ln += 1


class RotatingAI:
    def __init__(self):
        self.into_orbit = dict()
        self.into_orbit_moves = dict()
        self.into_orbit_moves_idx = dict()

    def action(self, state):
        res = dict()
        for ship in state.my_ships:
            res[ship.id] = []

        for ship in state.my_ships:
            if ship.id not in self.into_orbit:
                self.into_orbit[ship.id] = False
                self.into_orbit_moves[ship.id] = go_into_orbit(state.planet_radius, state.gravity_radius, ship.x, ship.y, ship.vx, ship.vy)
                self.into_orbit_moves_idx[ship.id] = 0

            if not self.into_orbit[ship.id]:
                ms = self.into_orbit_moves[ship.id][self.into_orbit_moves_idx[ship.id]]
                res[ship.id].append({'command': 'accel', 'x': ms[0], 'y': ms[1]})
                self.into_orbit_moves_idx[ship.id] += 1
                self.into_orbit[ship.id] = self.into_orbit_moves_idx[ship.id] == len(self.into_orbit_moves[ship.id])
            
            to_attack = None
            max_dmg = -1
            for eship in state.enemy_ships:
                if sum(eship.params.list()) == 0:
                    # 死んでるし
                    continue
                
                (nx, ny, _, _) = next_pos(state.planet_radius, state.gravity_radius, eship.x, eship.y, eship.vx, eship.vy)
                max_lp = min(ship.params.laser_power, 64 - ship.temp)
                ldmg = laser_damage(ship.x, ship.y, nx, ny, max_lp)
                if ldmg > max_dmg:
                    to_attack = {'command': 'laser', 'x': nx, 'y': ny, 'power': max_lp}
                    max_dmg = ldmg
            if ldmg > 10 and ldmg >= max_lp * 3 / 10 and to_attack is not None:
                res[ship.id].append(to_attack)

        return res


    def set_specs(self, limit, side):
        return ShipParameter(limit - (64*4 + 12*10 + 1*2), 64, 10, 1)
