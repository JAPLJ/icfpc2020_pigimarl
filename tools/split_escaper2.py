import sys
from itertools import product

sys.path.append('app/')
from multiship import *
import utils


MAX_TURNS = 256


class SplitEscaper2:
    CHECK_TURN = 15  # 今後このターンで墜落・範囲外にならないことを確認
    ESCAPE_DMG = 50  # これ以上のダメージ（温度増加含む）で回避行動を取る
    DUPLICATION_TURN = 5

    def __init__(self):
        self.into_orbit_moves = None
        self.past_acc = (0, 0)
        self.mother_id = None
        self.duplication_count = self.DUPLICATION_TURN
        self.states = []
        self.target = None

    def finc_valid_acc(self, ship, planet_radius, gravity_radius, left_time):
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
                                   ship.x, ship.y, ship.vx, ship.vy, moves, left_time):
                acc_candidate.append((ax, ay))
        for acc in acc_candidate:
            if acc != self.past_acc:
                return acc
        if acc_candidate:
            return acc_candidate[0]
        return utils.stop(ship.x, ship.y, ship.vx, ship.vy)

    def chase_move(self, state, ship, enemy):
        a_range = range(-ship.max_accel, ship.max_accel + 1)
        x = ship.x
        y = ship.y
        ex = enemy.x
        ey = enemy.y
        evx = enemy.vx
        evy = enemy.vy

        min_length = 10000
        best_ax = 0
        best_ay = 0
        for ax, ay in product(a_range, a_range):
            vx = ship.vx + ax
            vy = ship.vy + ay
            if not utils.gravity_check(state.planet_radius, state.gravity_radius,
                                     ship.x, ship.y, vx, vy, [], 30):
                continue
                                    
            for i in range(20):
                x, y, vx, vy = utils.next_pos(x, y, vx, vy)
                ex, ey, evx, evy = utils.next_pos(ex, ey, evx, evy)
                length = abs(x - ex) + abs(y - ey)
                if length < min_length:
                    min_length = length
                    best_ax = ax
                    best_ay = ay
        return best_ax, best_ay

    def similar_energy_enemies(self, state, ship):
        count = 0
        current_m_energy = utils.mechanical_energy(ship.x, ship.y, ship.vx, ship.vy)
        for enemy in state.enemy_ships:
            if sum(enemy.params.list()) == 0:
                continue
            enemy_m_energy = utils.mechanical_energy(enemy.x, enemy.y, enemy.vx, enemy.vy)
            if current_m_energy - 2 > enemy_m_energy or current_m_energy + 2 > enemy_m_energy:
                count += 1
        return count

    def action(self, state, ship):
        target = state.enemy_ships[0]
        self.states.append(state)
        commands = []
        self.duplication_count -= 1
        acc = (0, 0)
        left_time = MAX_TURNS - state.current_turn

        if self.into_orbit_moves is None:
            self.into_orbit_moves = utils.go_into_orbit(
                state.planet_radius, state.gravity_radius, ship.x, ship.y, ship.vx, ship.vy)

        if len(self.into_orbit_moves) > 0:
            acc = self.into_orbit_moves.pop(0)
        # elif not utils.gravity_check(state.planet_radius, state.gravity_radius,
        #                              ship.x, ship.y, ship.vx, ship.vy, [], left_time):
        #     acc = self.finc_valid_acc(ship, state.planet_radius, state.gravity_radius, left_time)
        acc = self.chase_move(state, ship, target)

        if acc != (0, 0):
            commands.append({'command': 'accel', 'x': acc[0], 'y': acc[1]})

        # if ship.params.soul > 2 or self.duplication_count < 0:
        #     self.duplication_count = self.DUPLICATION_TURN
        #     commands.append({'command': 'split', 'ship_ai_info': ShipAIInfo(SubShipAI(), 0, 0, 0, 1)})

        return commands


class SubShipAI:
    def __init__(self):
        pass

    def action(self, state, ship):
        return []
