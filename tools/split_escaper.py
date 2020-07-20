import sys

sys.path.append('app/')

from multiship import *
from utils import *


def go_into_orbit_2(planet_r, gravity_r, x0, y0, vx0, vy0):
    ln = 1
    while True:
        for d in range(8):
            dx, dy = neighbours[d]
            ms = [(dx * 2, dy * 2) for i in range(ln)]
            if gravity_check_g(planet_r, gravity_r, x0, y0, vx0, vy0, ms):
                return ms
        ln += 1


class SplitEscaper:
    def __init__(self):
        self.turn = 0
        self.orbit2 = None
    
    def _go_outer(self, state, ship):
        g = complex(ship.x, ship.y) * complex(1, 1)
        mcos = -1e10
        resd = None
        for d in range(8):
            nd = neighbours[d]
            if gravity_check_g(state.planet_radius, state.gravity_radius, ship.x, ship.y, ship.vx, ship.vy, [nd]):
                nd = complex(nd[0], nd[1])
                cos = (g * nd.conjugate()).real / abs(nd)
                if cos > mcos:
                    mcos = cos
                    resd = neighbours[d]
        return resd

    def action(self, state, ship):
        res = []

        if self.orbit2 is None:
            self.orbit2 = go_into_orbit_2(state.planet_radius, state.gravity_radius, ship.x, ship.y, ship.vx, ship.vy)

        if len(self.orbit2) > 0:
            nd = self.orbit2[0]
            res.append({'command': 'accel', 'x': nd[0], 'y': nd[1]})
            self.orbit2 = self.orbit2[1:]
        
        elif self.turn % 3 == 0 and ship.params.energy >= 10:
            nd = self._go_outer(state, ship)
            if nd is not None:
                res.append({'command': 'accel', 'x': nd[0], 'y': nd[1]})
        
        elif ship.params.soul >= 2:
            res.append({'command': 'split', 'ship_ai_info': ShipAIInfo(DebrisEscaper(), 0, 0, 0, 1)})

        self.turn += 1
        return res


class DebrisEscaper:
    def __init__(self):
        pass

    def action(self, state, ship):
        mother = None
        for s in state.my_ships:
            if s.id == self.mother_id:
                mother = s

        for eship in state.enemy_ships:
            (enx, eny, _, _) = next_pos(eship.x, eship.y, eship.vx, eship.vy)
            if abs(nx - enx) <= 3 and abs(ny - eny) <= 3:
                return [{'command': 'suicide'}]
        
        return []

