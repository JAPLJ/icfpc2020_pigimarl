from collections import defaultdict

import sys

sys.path.append('app/')

from conversion import *
from utils import *


@dataclasses.dataclass
class ShipAI:
    def action(self, state, ship):
        pass


@dataclasses.dataclass
class ShipAIInfo:
    ship_ai: ShipAI
    p1: int
    p2: int
    p3: int
    p4: int

    def __init__(self, ship_ai, p1, p2, p3, p4):
        self.ship_ai = ship_ai
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4


class Multiship:
    def __init__(self, attacker_ship_ai_info: ShipAIInfo, defender_ship_ai_info: ShipAIInfo):
        self.attacker_ship_ai_info = attacker_ship_ai_info
        self.defender_ship_ai_info = defender_ship_ai_info
        self.ship_id_to_ship_ai = {}
        self.x_y_vx_vy_to_ship_ai_list = defaultdict(list)

    def set_specs(self, limit, side):
        if side == Side.ATTACK:
            initial_ship_ai_info = self.attacker_ship_ai_info
            self.ship_id_to_ship_ai[1] = initial_ship_ai_info.ship_ai
        else:
            initial_ship_ai_info = self.defender_ship_ai_info
            self.ship_id_to_ship_ai[0] = initial_ship_ai_info.ship_ai

        return ShipParameter(initial_ship_ai_info.p1, initial_ship_ai_info.p2, initial_ship_ai_info.p3,
                             initial_ship_ai_info.p4)

    def action(self, state):
        res = {}

        for ship in state.my_ships:
            if ship.id not in self.ship_id_to_ship_ai:
                ship_ai = self.x_y_vx_vy_to_ship_ai_list[(ship.x, ship.y, ship.vx, ship.vy)].pop()
                self.ship_id_to_ship_ai[ship.id] = ship_ai

            ship_ai = self.ship_id_to_ship_ai[ship.id]
            print(ship.id, ship_ai)

            commands = ship_ai.action(state, ship)

            vx = ship.vx
            vy = ship.vy
            gx, gy = calc_gravity(ship.x, ship.y)
            vx += gx
            vy += gy

            for command in commands:
                if command['command'] == 'accel':
                    ax = command['x']
                    ay = command['y']
                    vx += ax
                    vy += ay

            for command in commands:
                if command['command'] == 'split':
                    ship_ai_info = command['ship_ai_info']
                    command['p1'] = ship_ai_info.p1
                    command['p2'] = ship_ai_info.p2
                    command['p3'] = ship_ai_info.p3
                    command['p4'] = ship_ai_info.p4
                    self.x_y_vx_vy_to_ship_ai_list[(ship.x + vx, ship.y + vy, vx, vy)].append(ship_ai_info.ship_ai)

            res[ship.id] = commands

        return res


class MainShipAI:
    def __init__(self):
        pass

    def action(self, state, ship):
        print(f'MainShipAI: id={ship.id}, x={ship.x}, y={ship.y}')

        gx, gy = calc_gravity(ship.x, ship.y)
        commands = [{'command': 'accel', 'x': -gx, 'y': -gy}]

        if ship.params.soul > 1:
            commands.append({'command': 'split', 'ship_ai_info': ShipAIInfo(SubShipAI(), 0, 0, 0, 1)})

        return commands


class SubShipAI:
    def __init__(self):
        pass

    def action(self, state, ship):
        print(f'SubShipAI: id={ship.id}, x={ship.x}, y={ship.y}')
        return []
