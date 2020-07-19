import sys
from math import sqrt
from typing import Dict, Tuple, List

import numpy as np

sys.path.append('tools/')
sys.path.append('app/')
from utils import l_inf_dist, normalize_vector, calc_gravity_acceration, calc_normalized_direction
from tournament_client import run
from common_interface import GameStage, ShipParameter, Side
from ai_interface import Ship, State


def create_accel_command(x: int, y: int) -> Dict:
    return {'command': 'accel', 'x': x, 'y': y}


def create_suiside_command() -> Dict:
    return {'command': 'suiside'}


def calc_next_pos(x, vx, y, vy) -> Tuple[int, int]:
    return x + vx, y + vy


class APPROACH_SUISIDE:
    def __init__(self, cool=16):
        self.suiside_dist_th = 5
        self.cool = cool

    def set_specs(self, limit: int, side: int) -> ShipParameter:
        energy = limit - 12*self.cool - 2
        return ShipParameter(energy, 0, self.cool, 1)

    def action(self, state: State) -> Dict[int, List[Dict]]:

        ret = {s.id: [] for s in state.my_ships}

        # 分離しない場合を考える
        s1 = state.my_ships[0]

        enemy_dist = [l_inf_dist(s1.x, s1.y, s2.x, s2.y) for s2 in state.enemy_ships]
        nearest_enemy_idx = np.argsort(enemy_dist)[0]
        s2 = state.enemy_ships[nearest_enemy_idx]
        p2_next = calc_next_pos(s2.x, s2.vx, s2.y, s2.vy)

        if s1.params.energy > 2:
            grav_acc = calc_gravity_acceration(s1.x, s1.y, state.gravity_radius)
            enemy_dir = calc_normalized_direction(s1.x, s1.y, p2_next[0], p2_next[1])
            a1 = normalize_vector( - grav_acc[0] + enemy_dir[0], - grav_acc[1] + enemy_dir[1])
            p1_next = calc_next_pos(s1.x, a1[0], s1.y, a1[1])
            ret[s1.id].append(create_accel_command(a1[0], a1[1]))
        else:
            p1_next = (s1.x, s1.y)

        dist = l_inf_dist(p1_next[0], p1_next[1], p2_next[0], p2_next[1])

        if dist < self.suiside_dist_th and s1.side == Side.ATTACK:
            ret[s1.id].append(create_suiside_command())

        return ret


if __name__ == '__main__':
    solver = APPROACH_SUISIDE()
    server_url = sys.argv[1]
    player_key = int(sys.argv[2])
    json_log_path = None if len(sys.argv) < 4 else sys.argv[3]

    run(server_url, player_key, solver, json_log_path=json_log_path)
