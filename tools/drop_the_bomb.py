from common_interface import *
from ai_interface import *

import sys
sys.path.append('app/')
from utils import *

import random


class DropTheBomb:
    def __init__(self):
        self.into_orbit = None
        self.into_orbit_moves = []
        self.into_orbit_moves_idx = 0
        self.ship_zero = None

    def action(self, state):
        res = dict()
        if self.ship_zero is None:
            self.ship_zero = state.my_ships[0].id

        sz = None
        for ship in state.my_ships:
            res[ship.id] = []
            if ship.id == self.ship_zero:
                sz = ship

        if self.into_orbit is None:
            self.into_orbit = False
            self.into_orbit_moves = go_into_orbit(state.planet_radius, state.gravity_radius, sz.x, sz.y, sz.vx, sz.vy)
            self.into_orbit_moves_idx = 0
        
        if not self.into_orbit:
            ms = self.into_orbit_moves[self.into_orbit_moves_idx]
            res[sz.id].append({'command': 'accel', 'x': ms[0], 'y': ms[1]})
            self.into_orbit_moves_idx += 1
            self.into_orbit = self.into_orbit_moves_idx == len(self.into_orbit_moves)
        elif sz.params.soul > 1:
            res[sz.id].append({'command': 'split', 'p1': 1, 'p2': 0, 'p3': 0, 'p4': 1})
        
        (znx, zny, _, _) = next_pos(state.planet_radius, sz.x, sz.y, sz.vx, sz.vy)
        
        for ship in state.my_ships:
            if ship.id == sz.id:
                continue

            mvx, mvy = ship.vx, ship.vy
            if ship.params.energy > 0:
                ds = []
                for d in range(8):
                    if gravity_check(state.planet_radius, state.gravity_radius, ship.x, ship.y, ship.vx, ship.vy, [(DX[d], DY[d])]):
                        ds.append(d)
                if len(ds) > 0:
                    d = random.choice(ds)
                    res[ship.id].append({'command': 'accel', 'x': DX[d], 'y': DY[d]})
                    mvx += DX[d]
                    mvy += DY[d]
            
            (mynx, myny, _, _) = next_pos(state.planet_radius, ship.x, ship.y, mvx, mvy)
            if abs(znx - mynx) <= 3 and abs(zny - myny) <= 3:
                continue

            for eship in state.enemy_ships:
                (nx, ny, _, _) = next_pos(state.planet_radius, eship.x, eship.y, eship.vx, eship.vy)
                if abs(nx - mynx) <= 3 and abs(ny - myny) <= 3:
                    res[ship.id].append({'command': 'suicide'})
                    break
    
        return res


    def set_specs(self, limit, side):
        if side == Side.ATTACK:
            return ShipParameter(152, 0, 10, 120)
        else:
            return ShipParameter(128, 0, 10, 100)
