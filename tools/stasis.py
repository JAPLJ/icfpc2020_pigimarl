from common_interface import ShipParameter

class SolverStasis:
    COOL_RATE = 10

    def action(self, state):
        commands = {}
        for ship in state.my_ships:
            ax = 0
            ay = 0
            if ship.x >= abs(ship.y):
                ax = 1
            if ship.x <= -abs(ship.y):
                ax = -1
            if ship.y >= abs(ship.x):
                ay = 1
            if ship.y <= -abs(ship.x):
                ay = -1
            commands[ship.id] = [{'command': 'accel', 'x': ax, 'y': ay}]
        return commands

    def set_specs(self, limit, side):
        return ShipParameter(limit - 12 * self.COOL_RATE - 2 * 1, 0, self.COOL_RATE, 1)
