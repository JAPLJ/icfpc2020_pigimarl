import sys

sys.path.append('app/')

from multiship import *
from utils import *


class Missile:
    def __init__(self, accels):
        self.accels = accels

    def action(self, state, ship):
        commands = []

        if len(self.accels) > 0:
            ax, ay = self.accels.pop(0)
            commands.append({'command': 'accel', 'x': ax, 'y': ay})
        else:
            nx, ny, _, _ = next_pos(ship.x, ship.y, ship.vx, ship.vy)

            near = False
            for ship in state.enemy_ships:
                enx, eny, _, _ = next_pos(ship.x, ship.y, ship.vx, ship.vy)
                if max(abs(nx - enx), abs(ny - eny)) <= 3:
                    near = True

            if near:
                commands.append({'command': 'suicide'})

        return commands


class MissileMan:
    def __init__(self):
        self.go_into_orbit_accels = None
        self.turn = 0

    def action(self, state, ship):
        commands = []

        # 最初の数ターンは様子見
        if self.turn < 10:
            gx, gy = calc_gravity(ship.x, ship.y)
            commands.append({'command': 'accel', 'x': -gx, 'y': -gy})

        else:
            if self.go_into_orbit_accels is None:
                rot_sum = 0
                for ship in state.enemy_ships:
                    rot_sum += ship.x * ship.vy - ship.y * ship.vx
                rot_sign = 1 if rot_sum > 0 else -1
                self.go_into_orbit_accels = go_into_orbit(state.planet_radius, ship.x, ship.y, ship.vx, ship.vy,
                                                          -rot_sign)
                print('#######################', self.go_into_orbit_accels)
                print(gravity_check(state.planet_radius, ship.x, ship.y, ship.vx, ship.vy, self.go_into_orbit_accels,
                                    -rot_sign, True))

            if len(self.go_into_orbit_accels) > 0:
                ax, ay = self.go_into_orbit_accels.pop(0)
                commands.append({'command': 'accel', 'x': ax, 'y': ay})

            if self.turn % 2 == 0:
                commands.append(
                    {'command': 'split', 'ship_ai_info': ShipAIInfo(Missile([random.choice(neighbours)]), 1, 0, 0, 1)})

        self.turn += 1

        return commands
