import sys

sys.path.append('app/')

from multiship import *
from utils import *


class MainShipAI:
    def __init__(self):
        pass

    def action(self, state, ship):
        # 最も右下の点へ向かって移動
        ax, ay = move_to_target(state.gravity_radius, state.planet_radius, ship.x, ship.y, ship.vx, ship.vy,
                                state.gravity_radius, state.gravity_radius)
        commands = [{'command': 'accel', 'x': ax, 'y': ay}]

        # soul がある間は SubShipAI を産み続ける
        if ship.params.soul > 1:
            commands.append({'command': 'split', 'ship_ai_info': ShipAIInfo(SubShipAI(count=20), 0, 0, 0, 1)})

        return commands


class SubShipAI:
    def __init__(self, count):
        self.count = count

    def action(self, state, ship):
        # カウントが 0 になったら自爆
        if self.count == 0:
            return [{'command': 'suicide'}]

        self.count -= 1
        return []
