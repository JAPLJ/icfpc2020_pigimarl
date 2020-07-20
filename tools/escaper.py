from common_interface import *
from ai_interface import *
from itertools import product
import sys
sys.path.append('app/')
import utils

MAX_TURNS = 256

class Escaper:
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
        left_time = MAX_TURNS - state.current_turn
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
        return stop(ship.x, ship.y, ship.vx, ship.vy)

    def action(self, state):
        commands = []
        self.duplication_cunt -= 1
        if self.mother_id is None:
            self.mother_id = state.my_ships[0].id
        for s in state.my_ships:
            if s.id == self.mother_id:
        acc = (0, 0)

        if self.into_orbit_moves is None:
            self.into_orbit_moves = utils.go_into_orbit(
                state.planet_radius, state.gravity_radius, ship.x, ship.y, ship.vx, ship.vy)

        if len(self.into_orbit_moves) > 0:
            acc = self.into_orbit_moves.pop(0)

        elif not utils.gravity_check(state.planet_radius, state.gravity_radius,
                                     ship.x, ship.y, ship.vx, ship.vy, [], left_time):
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

        if ship.params.soul >= 2 and self.duplication_cunt < 0:
            commands.append({'command': 'split', 'ship_ai_info': ShipAIInfo(DebrisBomb(ship.id), 0, 0, 0, 1)})

        if acc != (0, 0):
            commands.append({'command': 'accel', 'x': acc[0], 'y': acc[1]})
        self.past_acc = acc
        return {ship.id: commands}


    def set_specs(self, limit, side):
        return ShipParameter(limit - (12*self.COOL_RATE + 2*4), 0, self.COOL_RATE, 4)


class DebrisBomb:
    def __init__(self, mother_id):
        self.mother_id = mother_id

    def action(self, state, ship):
        mother = None
        for s in state.my_ships:
            if s.id == self.mother_id:
                mother = s

        (nx, ny, _, _) = next_pos(ship.x, ship.y, ship.vx, ship.vy)
        (mnx, mny, _, _) = next_pos(mother.x, mother.y, mother.vx, mother.vy)
        if abs(nx -  mnx) <= 3 and abs(ny - mny) <= 3:
            return []

        for eship in state.enemy_ships:
            (enx, eny, _, _) = next_pos(eship.x, eship.y, eship.vx, eship.vy)
            if abs(nx - enx) <= 3 and abs(ny - eny) <= 3:
                return [{'command': 'suicide'}]
        
        return []
