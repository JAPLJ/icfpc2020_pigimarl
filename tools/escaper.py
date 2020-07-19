from common_interface import *
from ai_interface import *
from itertools import product
import sys
sys.path.append('app/')
import utils

# Laserが痛そうなら回避行動

class Escaper:
    COOL_RATE = 16
    CHECK_TURN = 20 # 今後このターンで墜落・範囲外にならないことを確認
    ESCAPE_DMG = 50 # これ以上のダメージ（温度増加含む）で回避行動を取る

    def __init__(self):
        self.into_orbit_moves = None
        self.past_acc = (0, 0)

    def finc_valid_acc(self, ship, planet_radius, gravity_radius):
        a_range = range(-ship.max_accel, ship.max_accel + 1)
        acc_candidate = []
        for ax, ay in product(a_range, a_range):
            if (ax, ay) == (0, 0):
                continue
            moves = [(ax, ay)]
            if utils.gravity_check(planet_radius, gravity_radius,
                                   ship.x, ship.y, ship.vx, ship.vy, moves, self.CHECK_TURN):
                acc_candidate.append((ax, ay))
        for acc in acc_candidate:
            if acc != self.past_acc:
                return acc
        if acc_candidate:
            return acc_candidate[0]
        return stop(ship.x, ship.y, ship.vx, ship.vy)

    def action(self, state):
        commands = []
        ship = state.my_ships[0]
        acc = (0, 0)

        if self.into_orbit_moves is None:
            self.into_orbit_moves = utils.go_into_orbit(
                state.planet_radius, state.gravity_radius, ship.x, ship.y, ship.vx, ship.vy)

        if len(self.into_orbit_moves) > 0:
            acc = self.into_orbit_moves.pop(0)

        elif not utils.gravity_check(state.planet_radius, state.gravity_radius,
                                     ship.x, ship.y, ship.vx, ship.vy, [], self.CHECK_TURN):
            acc = self.finc_valid_acc(ship, state.planet_radius, state.gravity_radius)

        else:
            max_dmg = 0
            for eship in state.enemy_ships:
                if sum(eship.params.list()) == 0:
                    continue
                mx, my, _, _ = utils.next_pos(ship.x, ship.y, ship.vx, ship.vy)
                ex, ey, _, _ = utils.next_pos(eship.x, eship.y, eship.vx, eship.vy)
                max_lp = min(eship.params.laser_power, eship.max_temp - eship.temp)
                dmg = utils.laser_damage(ex, ey, mx, my, max_lp)
                max_dmg = max(max_dmg, dmg)

            if max_dmg > self.ESCAPE_DMG:
                a_range = range(-ship.max_accel, ship.max_accel + 1)
                acc = self.finc_valid_acc(ship, state.planet_radius, state.gravity_radius)

        if acc != (0, 0):
            commands.append({'command': 'accel', 'x': acc[0], 'y': acc[1]})
        self.past_acc = acc
        return {ship.id: commands}


    def set_specs(self, limit, side):
        return ShipParameter(limit - (12*self.COOL_RATE + 2*1), 0, self.COOL_RATE, 1)
