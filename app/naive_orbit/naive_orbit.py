import sys
sys.path.append('tools')
from typing import Dict, List
import math
from tournament_client import run
from common_interface import GameStage, ShipParameter, Side
from ai_interface import Ship, State


class NaiveOrbit:
    def __init__(self, cool=16):
        self.cool = cool

    def action(self, state: State) -> Dict[int, List[dict]]:
        # 分裂しないっす
        myship = state.my_ships[0]
        x = myship.x
        y = myship.y
        print(x, y)
        ship_id = myship.id
        energy = myship.params.energy
        if energy < 16:
            return {ship_id: []}

        # (x, y) とは直行する方向に進むし
        to_x = -y
        to_y = +x
        theta = math.degrees(math.atan2(to_y, to_x))
        dx, dy = self._calc_direction(theta)
        command = {
            'command': 'accel',
            'x': dx,
            'y': dy
        }
        return {ship_id: [command]}

    def set_specs(self, limit: int, side: int) -> ShipParameter:
        energy = limit - 12*self.cool - 2
        return ShipParameter(energy, 0, self.cool, 1)

    def _calc_direction(self, theta):
        # theta方向に向いた加速先を得る
        x = 16 * (theta + 180) / 360  # 0~16
        DIRS = [
            (-1, -1),
            (0, -1),
            (1, -1),
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
        ]
        for i in range(7):
            y = 2 * i + 1
            if y <= x < y + 2:
                return DIRS[i]
        return (-1, 0)


if __name__ == '__main__':
    solver = NaiveOrbit(16)
    server_url = sys.argv[1]
    player_key = int(sys.argv[2])
    json_log_path = None if len(sys.argv) < 4 else sys.argv[3]

    run(server_url, player_key, solver, json_log_path=json_log_path)
