import sys
from math import sqrt
from typing import Dict, Tuple, List
import random

import numpy as np

sys.path.append('tools/')
sys.path.append('app/')
from utils import next_pos, go_into_orbit, DX, DY
from tournament_client import run
from common_interface import GameStage, ShipParameter, Side
from ai_interface import Ship, State


def dist(x1, y1, x2, y2):
    return max(abs(x1 - x2), abs(y1 - y2))


def within_explosion(x1, y1, vx1, vy1, x2, y2, vx2, vy2, explotion_radius):
    nx1, ny1, _, _ = next_pos(x1, y1, vx1, vy1)
    nx2, ny2, _, _ = next_pos(x2, y2, vx2, vy2)

    return dist(nx1, ny1, nx2, ny2) <= explotion_radius


def random_direction():
    idx = random.randint(0, 7)
    return DX[idx], DY[idx]
    

class APPROACH_SUISIDE:
    def __init__(self, cool=16):
        self.explosion_radius = 5
        self.cool = cool
        self.stage = 1
        self.into_orbit_moves = {}
        self.into_orbit_idx = 0
        self.into_orbit = False
        self.num_split = 64

    def set_specs(self, limit, side):
        p2 = 32
        p3 = 1
        p4 =self.num_split
        return ShipParameter(limit - (p2*4 + p3*12 + p4*2), p2, p3, p4)

    def action(self, state: State) -> Dict[int, List[Dict]]:

        ret = {s.id: [] for s in state.my_ships}

        # 分離しない場合を考える
        if self.stage == 1:
            s1 = state.my_ships[0]

            enemy_dist = [max( abs(s1.x - s2.x), abs(s1.y - s2.y)) for s2 in state.enemy_ships]
            nearest_enemy_idx = np.argsort(enemy_dist)[0]
            s2 = state.enemy_ships[nearest_enemy_idx]


            if not self.into_orbit and len(self.into_orbit_moves) == 0:
                self.into_orbit_moves = go_into_orbit(state.planet_radius, s1.x, s1.y, s1.vx, s1.vy)
            elif not self.into_orbit:
                ms = self.into_orbit_moves[self.into_orbit_idx]
                ret[s1.id].append({'command': 'accel', 'x': ms[0], 'y': ms[1]})
                self.into_orbit_idx += 1
                self.into_orbit = self.into_orbit_idx == len(self.into_orbit_moves)
                if self.into_orbit:
                    self.stage += 1
        elif self.stage == 2:
            # print(f'[DEBUG] stage2 num my_ships = {len(state.my_ships)}')
            if len(state.my_ships) < self.num_split:
                for s1 in state.my_ships:
                    if s1.params.soul >= 2:
                        ret[s1.id].append({
                            'command': 'split',
                            'p1': s1.params.energy//2,
                            'p2': s1.params.laser_power//2,
                            'p3': s1.params.cooling_rate//2,
                            'p4': s1.params.soul//2
                        })
                    # print(f'[DEBUG] len(ret[s1.id]) = {len(ret[s1.id])}')
                if len(ret) >= self.num_split//2:
                    self.stage += 1
        elif self.stage == 3:
            for s1 in state.my_ships:
                dx, dy = random_direction()
                ret[s1.id].append({'command': 'accel', 'x': dx, 'y': dy})
            self.stage += 1
        else:
            for s1 in state.my_ships:
                for s2 in state.enemy_ships:
                    suiside = within_explosion(s1.x, s1.y, s1.vx, s1.vy, s2.x, s2.y, s2.vx, s2.vy, self.explosion_radius)
                    if suiside:
                        ret[s1.id].append({'command': 'suiside'})
                    break

        return ret


if __name__ == '__main__':
    solver = APPROACH_SUISIDE()
    server_url = sys.argv[1]
    player_key = int(sys.argv[2])
    json_log_path = None if len(sys.argv) < 4 else sys.argv[3]

    run(server_url, player_key, solver, json_log_path=json_log_path)
