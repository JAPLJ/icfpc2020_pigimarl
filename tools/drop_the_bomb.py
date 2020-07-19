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

def go_into_orbit2(planet_r, gravity_r, x0, y0, vx0, vy0):
    """
    (x0, y0) から速度 (vx0, vy0) で始めたとき、256 ターンにわたって墜落しないかつ外に出ないような
    最初に行うべき accel の列を返す
    """
    ln = 1
    while True:
        isok = [False] * 8
        for d in range(8):
            dx, dy = DX[d], DY[d]
            ms = [(dx, dy) for i in range(ln)]
            if gravity_check(planet_r, gravity_r, x0, y0, vx0, vy0, ms):
                isok[d] = True
        for d in range(8):
            for am in range(5):
                dd = (d + 2 + am) % 8
                if isok[d] and isok[dd]:
                    md = [(DX[d], DY[d]) for i in range(ln)]
                    mdd = [(DX[dd], DY[dd]) for i in range(ln)]
                    return (md, mdd)
        ln += 1

class DropThe2Bombs:
    def __init__(self):
        self.turn = 0
        self.into_orbit_moves = dict()
        self.into_orbit_moves_idx = dict()
        self.mother = None

    def action(self, state):
        res = dict()
        for ship in state.my_ships:
            res[ship.id] = []

        if self.turn == 0:
            self.turn += 1
            s = state.my_ships[0]
            res[s.id].append({'command': 'split', 'p1': s.params.energy // 2, 'p2': 0, 'p3': s.params.cooling_rate // 2, 'p4': s.params.soul // 2})
            (_, _, vx, vy) = next_pos(state.planet_radius, s.x, s.y, s.vx, s.vy)
            res[s.id].append({'command': 'accel', 'x': -vx, 'y': -vy})
            return res
        elif self.turn == 1:
            self.mother = [state.my_ships[0].id, state.my_ships[1].id]
            m = state.my_ships[0]
            zz = go_into_orbit2(state.planet_radius, state.gravity_radius, m.x, m.y, m.vx, m.vy)
            print(zz)
            self.into_orbit_moves = {self.mother[0]: zz[0], self.mother[1]: zz[1]}
            self.into_orbit_moves_idx = {self.mother[0]: 0, self.mother[1]: 0}

        self.turn += 1
        sz, so = None, None
        for ship in state.my_ships:
            if ship.id not in self.mother:
                continue
            if ship.id == self.mother[0]:
                sz = ship
            elif ship.id == self.mother[1]:
                so = ship
            
            if self.into_orbit_moves_idx[ship.id] < len(self.into_orbit_moves[ship.id]):
                ms = self.into_orbit_moves[ship.id][self.into_orbit_moves_idx[ship.id]]
                res[ship.id].append({'command': 'accel', 'x': ms[0], 'y': ms[1]})
                self.into_orbit_moves_idx[ship.id] += 1
            elif ship.params.soul > 1:
                res[ship.id].append({'command': 'split', 'p1': 1, 'p2': 0, 'p3': 0, 'p4': 1})

        if sz is not None:
            (znx, zny, _, _) = next_pos(state.planet_radius, sz.x, sz.y, sz.vx, sz.vy)
        if so is not None:
            (onx, ony, _, _) = next_pos(state.planet_radius, so.x, so.y, so.vx, so.vy)
        
        for ship in state.my_ships:
            if ship.id in self.mother:
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
            if sz is not None and abs(znx - mynx) <= 3 and abs(zny - myny) <= 3:
                continue
            if so is not None and abs(onx - mynx) <= 3 and abs(ony - myny) <= 3:
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
