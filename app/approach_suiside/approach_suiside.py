import sys
from math import sqrt
from typing import Dict, Tuple, List
import random

import numpy as np

sys.path.append('tools/')
sys.path.append('app/')
from utils import next_pos, go_into_orbit, DX, DY, move_to_target
from tournament_client import run
from common_interface import GameStage, ShipParameter, Side
from ai_interface import Ship, State
from multiship import ShipAI, ShipAIInfo, Multiship
from ship_ai_example import MainShipAI


def dist(x1, y1, x2, y2):
    return max(abs(x1 - x2), abs(y1 - y2))


def within_explosion(x1, y1, vx1, vy1, x2, y2, vx2, vy2, explotion_radius):
    nx1, ny1, _, _ = next_pos(x1, y1, vx1, vy1)
    nx2, ny2, _, _ = next_pos(x2, y2, vx2, vy2)

    return dist(nx1, ny1, nx2, ny2) <= explotion_radius


def random_direction():
    idx = random.randint(0, 7)
    return DX[idx], DY[idx]
    

class Suicider:
    def __init__(self, count):
        self.count = count  

    def action(self, state, ship):
        # カウントが 0 になったら自爆
        if self.count == 0:
            return [{'command': 'suicide'}]

        self.count -= 1
        return []


class MainAI:
    def __init__(self, cool=16):
        self.explosion_radius = 5
        self.cool = cool
        self.stage = 1
        self.into_orbit_moves = {}
        self.into_orbit_idx = 0
        self.into_orbit = False
        self.num_split = 128

    def set_specs(self, limit, side):
        p2 = 32
        p3 = 1
        p4 =self.num_split
        return ShipParameter(limit - (p2*4 + p3*12 + p4*2), p2, p3, p4)

    def action(self, state: State, ship: Ship) -> Dict[int, List[Dict]]:

        ret = []
        # 分離しない場合を考える
        if self.stage == 1:
            # enemy_dist = [max( abs(s1.x - s2.x), abs(s1.y - s2.y)) for s2 in state.enemy_ships]
            # nearest_enemy_idx = np.argsort(enemy_dist)[0]
            # s2 = state.enemy_ships[nearest_enemy_idx]

            if not self.into_orbit and len(self.into_orbit_moves) == 0:
                self.into_orbit_moves = go_into_orbit(state.planet_radius, ship.x, ship.y, ship.vx, ship.vy)
            elif not self.into_orbit:
                ms = self.into_orbit_moves[self.into_orbit_idx]
                ret.append({'command': 'accel', 'x': ms[0], 'y': ms[1]})
                self.into_orbit_idx += 1
                self.into_orbit = self.into_orbit_idx == len(self.into_orbit_moves)
                if self.into_orbit:
                    self.stage += 1
        elif self.stage == 2:
            if ship.params.soul > 1:
                ret.append({
                    'command': 'split',
                    'ship_ai_info': ShipAIInfo(Suicider(count=20), 0, 0, 0, 1)
                })
            else:
                self.stage += 1
        # elif self.stage == 3:
        #     for s1 in state.my_ships:
        #         dx, dy = random_direction()
        #         ret.append({'command': 'accel', 'x': dx, 'y': dy})
        #     self.stage += 1
        
        return ret


if __name__ == '__main__':
    attacker = ShipAIInfo(MainAI(), 152, 0, 10, 120)
    defender = ShipAIInfo(MainShipAI(), 100, 0, 8, 100)

    server_url = sys.argv[1]
    player_key = int(sys.argv[2])
    json_log_path = None if len(sys.argv) < 4 else sys.argv[3]

    run(server_url, player_key, Multiship(attacker, defender), json_log_path=json_log_path)
