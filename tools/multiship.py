import sys

from conversion import *


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
        self.par_ship_id_to_ship_ai = {}

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
        ship_id_to_ship = {}
        for ship in state.my_ships:
            ship_id_to_ship[ship.id] = ship

        for ship in state.my_ships:
            if ship.id not in self.ship_id_to_ship_ai:
                par_ship_id_opt = None
                for par_ship_id in self.par_ship_id_to_ship_ai.keys():
                    par_ship = ship_id_to_ship[ship.id]
                    if (ship.x, ship.y, ship.vx, ship.vy) == (par_ship.x, par_ship.y, par_ship.vx, par_ship.vy):
                        par_ship_id_opt = par_ship_id
                self.ship_id_to_ship_ai[ship.id] = self.par_ship_id_to_ship_ai[par_ship_id_opt]
                del self.par_ship_id_to_ship_ai[par_ship_id_opt]

        res = {}

        for ship in state.my_ships:
            ship_ai = self.ship_id_to_ship_ai[ship.id]
            commands = ship_ai.action(state, ship)

            for command in commands:
                if command['command'] == 'split':
                    ship_ai_info = command['ship_ai_info']

                    command['p1'] = ship_ai_info.p1
                    command['p2'] = ship_ai_info.p2
                    command['p3'] = ship_ai_info.p3
                    command['p4'] = ship_ai_info.p4

                    self.par_ship_id_to_ship_ai[ship.id] = ship_ai_info.ship_ai

            res[ship.id] = commands

        return res
