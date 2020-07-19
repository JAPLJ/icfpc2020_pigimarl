from common_interface import *
from ai_interface import *

import sys
sys.path.append('app/')
from utils import *


class Sniper:
    def __init__(self):
        self.into_orbit = dict()
        self.into_orbit_moves = dict()
        self.into_orbit_moves_idx = dict()
        self.states = list()

    def action(self, state):
        self.states.append(state)

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
            max_dmg = 0
            for eship in state.enemy_ships:
                if sum(eship.params.list()) == 0:
                    # 死んでるし
                    continue

                pvx, pvy = 0, 0
                for rc in eship.commands:
                    if rc.kind == 0:
                        pvx, pvy = -rc.x, -rc.y
                
                (nx, ny, _, _) = next_pos(state.planet_radius, eship.x, eship.y, eship.vx + pvx, eship.vy + pvy)
                max_lp = min(ship.params.laser_power, ship.max_temp - ship.temp)
                ldmg = laser_damage(ship.x, ship.y, nx, ny, max_lp)
                edmg = ldmg - (eship.max_temp - eship.temp)
                if edmg > max_dmg:
                    to_attack = {'command': 'laser', 'x': nx, 'y': ny, 'power': max_lp}
                    max_dmg = edmg
            if edmg > 0 and to_attack is not None:
                res[ship.id].append(to_attack)

        return res


    def set_specs(self, limit, side):
        if side == Side.ATTACK:
            return ShipParameter(limit - (96*4 + 12*8 + 1*2), 96, 8, 1)
        else:
            return ShipParameter(limit - (32*4 + 12*16 + 1*2), 32, 16, 1)
