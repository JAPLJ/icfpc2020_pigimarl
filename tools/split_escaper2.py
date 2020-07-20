import sys
from itertools import product

sys.path.append('app/')
from multiship import *
import utils


MAX_TURNS = 256


class SplitEscaper2:
    CHECK_TURN = 15  # 今後このターンで墜落・範囲外にならないことを確認
    ESCAPE_DMG = 50  # これ以上のダメージ（温度増加含む）で回避行動を取る
    DUPLICATION_TURN = 8

    def __init__(self):
        self.into_orbit_moves = None
        self.past_acc = (0, 0)
        self.mother_id = None
        self.duplication_count = self.DUPLICATION_TURN

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
        return utils.stop(ship.x, ship.y, ship.vx, ship.vy)

    def action(self, state, ship):
        commands = []
        self.duplication_count -= 1
        acc = (0, 0)
        left_time = MAX_TURNS - state.current_turn

        if self.into_orbit_moves is None:
            self.into_orbit_moves = utils.go_into_orbit(
                state.planet_radius, state.gravity_radius, ship.x, ship.y, ship.vx, ship.vy)

        if len(self.into_orbit_moves) > 0:
            acc = self.into_orbit_moves.pop(0)
        elif not utils.gravity_check(state.planet_radius, state.gravity_radius,
                                     ship.x, ship.y, ship.vx, ship.vy, [], left_time):
            acc = self.finc_valid_acc(ship, state.planet_radius, state.gravity_radius)

        if acc != (0, 0):
            commands.append({'command': 'accel', 'x': acc[0], 'y': acc[1]})

        if ship.params.soul > 2 and self.duplication_count < 0:
            self.duplication_count = self.DUPLICATION_TURN
            commands.append({'command': 'split', 'ship_ai_info': ShipAIInfo(SubShipAI(), 0, 0, 0, 1)})

        return commands


class SubShipAI:
    def __init__(self):
        pass

    def action(self, state, ship):
        return []
