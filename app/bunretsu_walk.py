import sys
sys.path.append('tools')
from typing import Dict, List
import math
import numpy as np
from tournament_client import run
from common_interface import GameStage, ShipParameter, Side
from ai_interface import Ship, State
from utils import go_into_orbit, get_random_accel
import dataclasses


@dataclasses.dataclass
class ShipState:
    age: int


class BunretsuWalk:
    def __init__(self, cooling_rate=8*4, soul=8):
        self.cooling_rate = cooling_rate
        self.soul = soul
        self.ship_states = {}

    def action(self, state: State) -> Dict[int, List[dict]]:
        all_commands = {}

        print(len(state.my_ships), file=sys.stderr)
        for ship in state.my_ships:
            commands = []
            params = ship.params

            if ship.id not in self.ship_states:
                self.ship_states[ship.id] = ShipState(0)

            ship_state = self.ship_states[ship.id]

            if state.current_turn % 5 == 0 and ship.id < 2 and params.soul > 1:
                command = {
                    'command': 'split',
                    'p1': params.energy // self.soul,
                    'p2': params.laser_power // self.soul,
                    'p3': params.cooling_rate // self.soul,
                    'p4': 1,
                }
                commands.append(command)
            elif 3 <= ship_state.age < 6:
                moves = go_into_orbit(
                    state.planet_radius,
                    ship.x, ship.y, ship.vx, ship.vy
                )
                if len(moves) > 0:
                    command = {
                        'command': 'accel',
                        'x': moves[0][0],
                        'y': moves[0][1],
                    }
                    commands.append(command)
            elif np.random.randint(0, 2):
                axy = get_random_accel(
                    state.planet_radius, state.gravity_radius,
                    ship.x, ship.y, ship.vx, ship.vy
                )
                command = {
                    'command': 'accel',
                    'x': axy[0],
                    'y': axy[1],
                }
                commands.append(command)

            ship_state.age += 1
            all_commands[ship.id] = commands
            print(all_commands, file=sys.stderr)

        return all_commands

    def set_specs(self, limit: int, side: int) -> ShipParameter:
        energy = limit - 12*self.cooling_rate - 2*self.soul
        print(energy, file=sys.stderr)
        return ShipParameter(energy, 0, self.cooling_rate, self.soul)


if __name__ == '__main__':
    solver = BunretsuWalk()
    server_url = sys.argv[1]
    player_key = int(sys.argv[2])
    json_log_path = None if len(sys.argv) < 4 else sys.argv[3]

    run(server_url, player_key, solver, json_log_path=json_log_path)
