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


class IntelligentMissle:
    def __init__(self, accels):
        self.go_into_orbit_accels = None
        self.accels = accels

    def action(self, state, ship):
        commands = []

        if self.go_into_orbit_accels is None:
            rot_sum = 0
            for s in state.enemy_ships:
                rot_sum += s.x * s.vy - s.y * s.vx
            rot_sign = 1 if rot_sum > 0 else -1
            self.go_into_orbit_accels = go_into_orbit(state.gravity_radius, state.planet_radius, ship.x, ship.y,
                                                        ship.vx, ship.vy,
                                                        -rot_sign)

        if len(self.go_into_orbit_accels) > 0:
                ax, ay = self.go_into_orbit_accels.pop(0)
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
                for s in state.enemy_ships:
                    rot_sum += s.x * s.vy - s.y * s.vx
                rot_sign = 1 if rot_sum > 0 else -1
                self.go_into_orbit_accels = go_into_orbit(state.gravity_radius, state.planet_radius, ship.x, ship.y,
                                                          ship.vx, ship.vy,
                                                          -rot_sign)

            if len(self.go_into_orbit_accels) > 0:
                ax, ay = self.go_into_orbit_accels.pop(0)
                commands.append({'command': 'accel', 'x': ax, 'y': ay})
            elif self.turn % 2 == 0:
                nx, ny, nvx, nvy = next_pos(ship.x, ship.y, ship.vx, ship.vy)
                accels = go_into_orbit(state.gravity_radius, state.planet_radius, nx, ny, nvx, nvy)
                commands.append(
                    {'command': 'split', 'ship_ai_info': ShipAIInfo(Missile(accels), len(accels), 0, 0, 1)})

        self.turn += 1

        return commands
