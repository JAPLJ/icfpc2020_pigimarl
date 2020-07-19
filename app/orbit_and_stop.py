import sys
import utils

sys.path.append("tools/")

from common_interface import *

class OrbitStop:
    COOL_RATE = 10
    accs = []

    def action(self, state):
        ship = state.my_ships[0]
        if state.current_turn == 0:
            self.accs = utils.go_into_orbit(state.planet_radius, ship.x, ship.y, ship.vx, ship.vy)
        commands = {}
        acc = (0, 0)
        if self.accs:
            acc = self.accs.pop(0)
        elif state.current_turn >= 100:
            acc = utils.stop(ship)
        if acc != (0, 0):
            commands[ship.id] = [{'command': 'accel', 'x': acc[0], 'y': acc[1]}]
        return commands

    def set_specs(self, limit, side):
        return ShipParameter(limit - 12 * self.COOL_RATE - 2 * 1, 0, self.COOL_RATE, 1)
