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
            for s in state.enemy_ships:
                enx, eny, _, _ = next_pos(s.x, s.y, s.vx, s.vy)
                if max(abs(nx - enx), abs(ny - eny)) <= 3:
                    near = True

            safe = True
            for s in state.my_ships:
                mnx, mny, _, _ = next_pos(s.x, s.y, s.vx, s.vy)
                if max(abs(nx - mnx), abs(ny - mny)) <= 3 and s.params.soul > 1:
                    safe = False

            if near and safe:
                commands.append({'command': 'suicide'})

        return commands


class Mine:
    def __init__(self):
        pass
    
    def action(self, state, ship):
        commands = []

        nx, ny, _, _ = next_pos(ship.x, ship.y, ship.vx, ship.vy)

        near = False
        for s in state.enemy_ships:
            enx, eny, _, _ = next_pos(s.x, s.y, s.vx, s.vy)
            if max(abs(nx - enx), abs(ny - eny)) <= 3:
                near = True

        safe = True
        for s in state.my_ships:
            mnx, mny, _, _ = next_pos(s.x, s.y, s.vx, s.vy)
            if max(abs(nx - mnx), abs(ny - mny)) <= 3 and s.params.soul > 1:
                safe = False

        if near and safe:
            commands.append({'command': 'suicide'})
        else:
            dv, dy = stop(ship,x, ship.y, ship.vx, ship.vy)
            commands.append({'command': 'accel', 'x': dv, 'y': dy})

        return commands


# パラメータはこんな感じで
# attacker = ShipAIInfo(MissileMan(), 512 - (12 * 8 + 2 * 128), 0, 8, 128)
# defender = ShipAIInfo(MissileMan(), 448 - (12 * 8 + 2 * 128), 0, 8, 128)

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
            elif self.turn % 4 == 0:
                accels = fire_target(state.gravity_radius, state.planet_radius, ship.x, ship.y, ship.vx, ship.vy,
                                     256 - self.turn, state.enemy_ships, 1, 1000)
                if accels is not None:
                    commands.append(
                        {'command': 'split', 'ship_ai_info': ShipAIInfo(Missile(accels), len(accels), 0, 0, 1)})
            elif self.turn % 2 == 0:

                if accels is not None:
                    commands.append(
                        {'command': 'split', 'ship_ai_info': ShipAIInfo(Mine, 5, 0, 0, 1)})

        self.turn += 1

        return commands
