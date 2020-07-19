from common_interface import ShipParameter

class BoundaryStop:
    COOL_RATE = 10

    def rot_cw(self, v):
        return (v[1], -v[0])

    def rot_ccw(self, v):
        return (-v[1], v[0])

    def move(self, ship, planet_radius, dst):
        planet_radius = state.planet_radius
        pos = (ship.x, ship.y)
        vel = (ship.vs, ship.vy)
        rot_cnt = 0
        while pos[1] <= 0 or pos[0] > pos[1] or pos[0] < -pos[1]:
            pos = rot_cw(pos)
            vel = rot_cw(vel)
            dst = rot_cw(dst)
            rot_cnt += 1
        

    def action(self, state):
        commands = {}
        for ship in state.my_ships:
            acc = self.accel(ship)
            if acc != (0, 0):
                commands[ship.id] = [{'command': 'accel', 'x': acc[0], 'y': acc[1]}]
        return commands

    def set_specs(self, limit, side):
        return ShipParameter(limit - 12 * self.COOL_RATE - 2 * 1, 0, self.COOL_RATE, 1)
