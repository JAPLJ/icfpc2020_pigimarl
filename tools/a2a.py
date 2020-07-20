import sys

sys.path.append('app/')

from multiship import *
from utils import *

def is_near(p0, p1):
    (x0, y0) = p0
    (x1, y1) = p1
    d = max(abs(x0 - x1), abs(y0 - y1))
    return d <= 3


class Fortress:
    def __init__(self):
        self.lock_on = set()
        self.orbit_moves = None

    def action(self, state, ship):
        commands = []

        if self.orbit_moves is None:
            self.orbit_moves = go_into_orbit(
                state.planet_radius, state.gravity_radius, ship.x, ship.y, ship.vx, ship.vy)

        if self.orbit_moves:
            acc = self.orbit_moves.pop(0)
            commands.append({'command': 'accel', 'x': acc[0], 'y': acc[1]})

        elif ship.params.soul > 1:
            target_eship = None
            missile_acc = None
            res_turn = 256 - state.current_turn
            for eship in state.enemy_ships:
                if sum(eship.params.list()) == 0:
                    continue
                if eship.params.energy > 0:
                    continue
                if eship.id in self.lock_on:
                    continue
                eship_trajectory = calc_trajectory(eship.x, eship.y, eship.vx, eship.vy, [], res_turn)
                accs = []
                for ax in range(-2, 3):
                    for ay in range(-2, 3):
                        accs.append((ax, ay))
                accs = sorted(accs, key=lambda a: max(abs(a[0]), abs(a[1])))

                for acc in accs:
                    moves = [(0, 0), acc]
                    missile_trajectory = calc_trajectory(ship.x, ship.y, ship.vx, ship.vy, moves, res_turn)
                    ok = False
                    for i in range(res_turn):
                        if is_near(missile_trajectory[i], eship_trajectory[i]):
                            ok = True
                            break
                    if ok:
                        target_eship = eship
                        missile_acc = acc
                        break

                if target_eship is not None:
                    break

            if target_eship is not None:
                self.lock_on.add(target_eship.id)
                missile = Missile(eship.id, missile_acc)
                energy = max(abs(missile_acc[0]), abs(missile_acc[1]))
                commands.append({'command': 'split', 'ship_ai_info': ShipAIInfo(missile, energy, 0, 0, 1)})

        return commands


class Missile:
    def __init__(self, target_id, initial_acc):
        self.target_id = target_id
        self.initial_acc = initial_acc
        self.turn = 0

    def action(self, state, ship):
        commands = []
        if self.turn == 0:
            commands.append({'command': 'accel', 'x': self.initial_acc[0], 'y': self.initial_acc[1]})

        self.turn += 1

        target_eship = None
        for eship in state.enemy_ships:
            if eship.id == self.target_id:
                target_eship = eship
                break

        if target_eship is None:
            # commands.append({'command': 'suicide'})
            pass

        else:
            mx, my, _, _ = next_pos(ship.x, ship.y, ship.vx, ship.vy)
            ex, ey, _, _ = next_pos(target_eship.x, target_eship.y, target_eship.vx, target_eship.vy)
            if is_near(mx, my, ex, ey):
            commands.append({'command': 'suicide'})

        return commands
