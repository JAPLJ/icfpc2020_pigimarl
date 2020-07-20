import sys

sys.path.append('app/')

from multiship import *
from utils import *

MAX_TURNS = 256


class SplitEscaper2:
    COOL_RATE = 16
    CHECK_TURN = 15 # 今後このターンで墜落・範囲外にならないことを確認
    ESCAPE_DMG = 50 # これ以上のダメージ（温度増加含む）で回避行動を取る
    DUPLICATION_TURN = 10

    def __init__(self):
        self.into_orbit_moves = None
        self.past_acc = (0, 0)
        self.mother_id = None
        self.duplication_cunt = self.DUPLICATION_TURN

    def finc_valid_acc(self, ship, planet_radius, gravity_radius):
        a_range = range(-ship.max_accel, ship.max_accel + 1)
        acc_candidate = []
        current_energy = utils.mechanical_energy(ship.x, ship.y, ship.vx, ship.vy)
        for ax, ay in product(a_range, a_range):
            if (ax, ay) == (0, 0):
                continue
            next_energy = utils.mechanical_energy(
                ship.x,
                ship.y,
                ship.vx + ax,
                ship.vy + ay
            )
            if current_energy > next_energy and current_energy < 100:
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
        return stop(ship.x, ship.y, ship.vx, ship.vy


    def action(self, state, ship):
        commands = []
        self.duplication_cunt -= 1
        acc = (0, 0)
        left_time = MAX_TURNS - state.current_turn

        if self.into_orbit_moves is None:
            self.into_orbit_moves = utils.go_into_orbit(
                state.planet_radius, state.gravity_radius, ship.x, ship.y, ship.vx, ship.vy)
            
        # 動き
        acc_lg = False
        if len(self.into_orbit_moves) > 0:
            acc = self.into_orbit_moves.pop(0)
            acc_flg = True
        elif not utils.gravity_check(state.planet_radius, state.gravity_radius,
                                     ship.x, ship.y, ship.vx, ship.vy, [], left_time):
            acc = self.finc_valid_acc(ship, state.planet_radius, state.gravity_radius)
            acc_flg = True
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
                acc_flg = True

        if ship.params.soul >= 2 and self.duplication_cunt < 0 and acc_flg:
            commands.append({'command': 'split', 'ship_ai_info': ShipAIInfo(SubShipAI(), 0, 0, 0, 1)})

        if acc != (0, 0):
            commands.append({'command': 'accel', 'x': acc[0], 'y': acc[1]})
        self.past_acc = acc

        return commands


class SubShipAI:
    def __init__(self):
        pass

    def action(self, state, ship):
        return []
