import sys

from ai_interface import *

sys.path.append('app/')

from utils import *


class TestAI:
    def __init__(self):
        pass

    def action(self, state):
        res = {}

        for ship in state.my_ships:
            if state.my_side == Side.ATTACK:
                tx = state.gravity_radius
                ty = state.gravity_radius
            else:
                tx = state.planet_radius + 1
                ty = state.planet_radius + 1
            ax, ay = move_to_target(state.gravity_radius, state.planet_radius, ship.x, ship.y, ship.vx, ship.vy, tx, ty)
            res[ship.id] = [{'command': 'accel', 'x': ax, 'y': ay}]

        return res

    def set_specs(self, limit, side):
        return ShipParameter(limit - (4 * 0 + 12 * 8 + 1 * 2), 0, 8, 1)
