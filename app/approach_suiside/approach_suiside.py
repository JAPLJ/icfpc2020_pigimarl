import sys
from math import sqrt
from typing import Dict, Tuple, List

import numpy as np

sys.path.append('tools/')
sys.path.append('app/')
from utils import next_pos, go_into_orbit
from tournament_client import run
from common_interface import GameStage, ShipParameter, Side
from ai_interface import Ship, State


def dist(x1, y1, x2, y2):
    return max(abs(x1 - x2), abs(y1 - y2))


def within_explosion(x1, y1, vx1, vy1, x2, y2, vx2, vy2, explotion_radius):
    nx1, ny1, _, _ = next_pos(x1, y1, vx1, vy1)
    nx2, ny2, _, _ = next_pos(x2, y2, vx2, vy2)

    return dist(nx1, ny1, nx2, ny2) <= explotion_radius
    

class APPROACH_SUISIDE:
    def __init__(self, cool=16):
        self.explosion_radius = 5
        self.cool = cool
        self.stage = 1
        self.into_orbit_moves = {}
        self.into_orbit_idx = 0
        self.into_orbit = False

    def set_specs(self, limit: int, side: int) -> ShipParameter:
        energy = limit - 12*self.cool - 2
        return ShipParameter(energy, 0, self.cool, 1)

    def action(self, state: State) -> Dict[int, List[Dict]]:

        ret = {s.id: [] for s in state.my_ships}

        # 分離しない場合を考える
        s1 = state.my_ships[0]

        enemy_dist = [max( abs(s1.x - s2.x), abs(s1.y - s2.y)) for s2 in state.enemy_ships]
        nearest_enemy_idx = np.argsort(enemy_dist)[0]
        s2 = state.enemy_ships[nearest_enemy_idx]

        if self.stage == 1:
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
            suiside = within_explosion(s1.x, s1.y, s1.vx1, s1.vx2, s2.x, s2.y, s2.vx, s2.vy, self.explosion_radius)
            if suiside:
                ret[s1.id].append({'command': 'suiside'})

        return ret


if __name__ == '__main__':
    solver = APPROACH_SUISIDE()
    server_url = sys.argv[1]
    player_key = int(sys.argv[2])
    json_log_path = None if len(sys.argv) < 4 else sys.argv[3]

    run(server_url, player_key, solver, json_log_path=json_log_path)
