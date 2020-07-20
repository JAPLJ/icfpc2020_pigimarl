import sys

from ai_interface import *

from utils import *


class TestAI:
    def __init__(self):
        pass

    def action(self, state):
        res = {}

        for ship in state.my_ships:
            if state.my_side == Side.DEFENSE:
                if ship.params.soul > 1 and ship.temp > 0:
                    res[ship.id] = [{'command': 'split', 'p1': 1, 'p2': 0, 'p3': 0, 'p4': 1}]
                else:
                    gx, gy = calc_gravity(ship.x, ship.y)
                    res[ship.id] = [{'command': 'accel', 'x': gx, 'y': gy}]
            else:
                res[ship.id] = [
                    {'command': 'lazer', 'x': state.enemy_ships[0].x, 'y': state.enemy_ships[0].y,
                     'power': ship.params.p2}]

            print(f'id={ship.id}, x={ship.x}, y={ship.y}, vx={ship.vx}, vy={ship.vy}, ')

        return res

    def set_specs(self, limit, side):
        if side == Side.ATTACK:
            return ShipParameter(0, (limit - 2) // 12, 0, 1)
        else:
            return ShipParameter(limit - (4 * 0 + 12 * 0 + 2 * 2), 0, 0, 2)
