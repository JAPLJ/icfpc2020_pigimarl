from common_interface import *
from ai_interface import *
from itertools import product
import sys
sys.path.append('app/')
import utils

# Laserが痛そうなら回避行動

class Escaper:
    COOL_RATE = 16
    ESCAPE_DMG = 50 # これ以上のダメージ（温度増加含む）で回避行動を取る

    def __init__(self):
        self.into_orbit_moves = None

    def action(self, state):
        commands = []
        ship = state.my_ships[0]

        if self.into_orbit_moves is None:
            self.into_orbit_moves = utils.go_into_orbit(state.planet_radius, ship.x, ship.y, ship.vx, ship.vy)

        if len(self.into_orbit_moves) > 0:
            acc = self.into_orbit_moves.pop(0)
            commands.append({'command': 'accel', 'x': acc[0], 'y': acc[1]})

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
                acc = None
                a_range = range(-ship.max_accel, ship.max_accel + 1)
                for ax, ay in product(a_range, a_range):
                    moves = [(ax, ay)]
                    if utils.gravity_check(state.planet_radius, ship.x, ship.y, ship.vx, ship.vy, moves):
                        acc = (ax, ay)
                if acc:
                    commands.append({'command': 'accel', 'x': acc[0], 'y': acc[1]})

        return {ship.id: commands}


    def set_specs(self, limit, side):
        return ShipParameter(limit - (12*self.COOL_RATE + 2*1), 0, self.COOL_RATE, 1)