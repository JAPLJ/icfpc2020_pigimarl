import sys
sys.path.append('tools')
from typing import Dict, List
import math
from tournament_client import run
from common_interface import GameStage, ShipParameter, Side
from ai_interface import Ship, State


class NaiveOrbit:
    def __init__(self, cool=8):
        self.cool = cool

    def action(self, state: State) -> Dict[int, List[dict]]:
        all_commands = {}
        for myship in state.my_ships:
            commands = []
            x = myship.x
            y = myship.y
            params = myship.params
            print(myship)
            print(params)
            print(state)
            if params.soul > 1:
                command = {
                    'command': 'split',
                    'p1': params.energy//2,
                    'p2': 0,
                    'p3': params.cooling_rate//2,
                    'p4': params.soul//2,
                }
                commands.append(command)
            elif state.current_turn % 2:
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
                commands.append(command)
            all_commands[myship.id] = commands

        return all_commands

    def set_specs(self, limit: int, side: int) -> ShipParameter:
        energy = limit - 12*self.cool - 2*4
        return ShipParameter(energy, 0, self.cool, 4)

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
