import sys

sys.path.append('app/')

from multiship import *
from utils import *

def calc_gravity1(x, y):
    """
    座標 (x, y) に働く重力のベクトルを返す
    :param x:
    :param y:
    :return:
    """
    if abs(x) > abs(y):
        return -sign(x), 0
    elif abs(x) < abs(y):
        return 0, -sign(y)
    else:
        return -sign(x), -sign(y)


def go_into_orbit_2(planet_r, gravity_r, x0, y0, vx0, vy0):
    ln = 1
    while True:
        for d in range(8):
            dx, dy = neighbours[d]
            ms = [(dx * 2, dy * 2) for i in range(ln)]
            if gravity_check(planet_r, gravity_r, x0, y0, vx0, vy0, ms):
                return ms
        ln += 1

class CarpetBombMother:
    def __init__(self):
        self.turn = 0
        self.orbit2 = None
    
    def _go_to(self, state, ship, to):
        g = to
        mcos = -1e10
        resd = None
        for d in range(8):
            nd = neighbours[d]
            if gravity_check(state.planet_radius, state.gravity_radius, ship.x, ship.y, ship.vx, ship.vy, [nd]):
                nd = complex(nd[0], nd[1])
                cos = (g * nd.conjugate()).real / abs(nd)
                if cos > mcos:
                    mcos = cos
                    resd = neighbours[d]
        return resd        

    def _go_outer(self, state, ship):
        return self._go_to(state, ship, ship.vx, ship.vy)
    
    def _go_inner(self, state, ship):
        return self._go_to(state, ship, -ship.vx, -ship.vy)

    def action(self, state, ship):
        res = []

        if self.turn == 0:
            gx, gy = calc_gravity1(ship.x, ship.y)
            res.append({'command': 'accel', 'x': -gx, 'y': -gy})
            self.turn += 1
            return res
        
        if self.turn == 1:
            e_move = None
            for eship in state.enemy_ships:
                for rc in eship.commands:
                    if rc.kind == 0:
                        e_move = (-rc.x, -rc.y)
            if e_move is not None:
                res.append({'command': 'accel', 'x': e_move[0], 'y': e_move[1]})
                self.turn += 1
                return res

        if self.orbit2 is None:
            self.orbit2 = go_into_orbit_2(state.planet_radius, state.gravity_radius, ship.x, ship.y, ship.vx, ship.vy)

        if len(self.orbit2) > 0:
            nd = self.orbit2[0]
            res.append({'command': 'accel', 'x': nd[0], 'y': nd[1]})
            self.orbit2 = self.orbit2[1:]
        
        elif self.turn % 5 == 0 and ship.params.energy >= 1:
            if ship.params.soul >= 2:
                nd = self._go_outer(state, ship)
            else:
                nd = self._go_inner(state, ship)
            if nd is not None:
                res.append({'command': 'accel', 'x': nd[0], 'y': nd[1]})
        
        elif ship.params.soul >= 2:
            res.append({'command': 'split', 'ship_ai_info': ShipAIInfo(DebrisBomb(ship.id), 0, 0, 0, 1)})
        
        if ship.params.laser_power > 0:
            max_dmg = 0
            to_attack = None
            target = None
            for eship in state.enemy_ships:
                if sum(eship.params.list()) == 0:
                    continue
            
                pvx, pvy = 0, 0
                for rc in eship.commands:
                    if rc.kind == 0:
                        pvx, pvy = -rc.x, -rc.y
                
                (nx, ny, _, _) = next_pos(eship.x, eship.y, eship.vx + pvx, eship.vy + pvy)
                max_lp = min(ship.params.laser_power, ship.max_temp - ship.temp)
                ldmg = laser_damage(ship.x, ship.y, nx, ny, max_lp)
                edmg = ldmg - (eship.max_temp - eship.temp)
                if edmg > 0:
                    edmg += eship.params.soul * 100
                
                if edmg > max_dmg:
                    target = eship
                    to_attack = {'command': 'laser', 'x': nx, 'y': ny, 'power': max_lp}
                    max_dmg = edmg

            if max_dmg > 0:
                lo, hi = 0, to_attack['power']
                while hi - lo > 1:
                    mid = (hi + lo) // 2
                    ldmg = laser_damage(ship.x, ship.y, to_attack['x'], to_attack['y'], mid)
                    edmg = ldmg - (eship.max_temp - eship.temp)
                    if edmg >= sum(eship.params.list) == 0:
                        hi = mid
                    else:
                        lo = mid
                to_attack['power'] = min(to_attack['power'], hi + 5)
                res.append(to_attack)

        self.turn += 1
        return res


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

