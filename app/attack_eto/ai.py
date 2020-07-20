from typing import *
import sys
sys.path.append('tools')
from common_interface import *
from ai_interface import *
sys.path.append('app')
from utils import *
from collections import defaultdict
import random

TEMP_LIMIT = 64

class AI:
    def __init__(self):
        self.into_orbit = dict()
        self.into_orbit_moves = dict()
        self.into_orbit_moves_idx = dict()

    def action(self, state):
        commands = defaultdict(list)
        enemy_ships = list(filter(lambda eship: eship.params.soul != 0, state.enemy_ships))
        if len(enemy_ships) == 0:
            return {}
        enemy_ship = state.enemy_ships[0]
        target_x, target_y, _, _ = next_pos(enemy_ship.x, enemy_ship.y, enemy_ship.vx, enemy_ship.vy)
        # もし相手が残り1体で体力も少なかったらこのターンで決着をつける
        if len(enemy_ships) == 1 and self.__can_kill_in_this_turn(state.my_ships, enemy_ships[0]):
            for ship in state.my_ships:
                laser_power = ship.params.laser_power  # フルバースト
                commands[ship.id] = [{"command": "laser", "power": laser_power, "x": target_x, "y":target_y}]

        for ship in state.my_ships:
            # 一番IDが小さい敵を撃つ。有効なダメージじゃなかったらやめる
            laser_power = min(ship.params.laser_power, TEMP_LIMIT - ship.temp)
            expected_damage = laser_damage(ship.x, ship.y, target_x, target_y, laser_power)
            if expected_damage <= enemy_ship.params.cooling_rate:
                commands[ship.id] = [{"command": "laser", "power": laser_power, "x": target_x, "y":target_y}]


            if ship.id not in self.into_orbit:
                self.into_orbit[ship.id] = False
                self.into_orbit_moves[ship.id] = go_into_orbit(state.planet_radius, ship.x, ship.y, ship.vx, ship.vy)
                self.into_orbit_moves_idx[ship.id] = 0

            if not self.into_orbit[ship.id]:
                ms = self.into_orbit_moves[ship.id][self.into_orbit_moves_idx[ship.id]]
                commands[ship.id].append({'command': 'accel', 'x': ms[0], 'y': ms[1]})
                self.into_orbit_moves_idx[ship.id] += 1
                self.into_orbit[ship.id] = self.into_orbit_moves_idx[ship.id] == len(self.into_orbit_moves[ship.id])
            # # random walk
            # gravity_x, gravity_y = calc_gravity(ship.x, ship.y)
            # dx = -gravity_x
            # dy = -gravity_y
            # # dx = min(max(random.randint(-1, 1) - gravity_x, -1), 1)
            # # dy = min(max(random.randint(-1, 1) - gravity_y, -1), 1)
            # commands[ship.id] = [{"command": "accel", "x": dx, "y": dy}]

        return commands

    def set_specs(self, limit: int, side: int) -> ShipParameter:
        energy = 60
        laser_power = 64
        cooling_rate = 0
        soul = 1
        extra = limit - energy - laser_power*4 - cooling_rate*12 - soul*2
        if extra < 0:
            return ShipParameter(limit - 4 - 12 - 2, 1, 1, 1)
        cooling_rate += extra // 12
        return ShipParameter(energy, laser_power, cooling_rate, soul)

    @staticmethod
    def __can_kill_in_this_turn(my_ships: List[Ship], enemy_ship : Ship) -> bool:
        """
        全艦(my_ships)一斉放射してenemy_shipをこのターン中に殺せるかどうか。
        """
        # 動かないと仮定して直撃を狙う場合
        enemy_life = (TEMP_LIMIT - enemy_ship.temp) + enemy_ship.params.energy
        damage = 0
        for ship in my_ships:
            # energyが少なくて温度が高い状態で撃つと、撃った直後に死ぬかもしれないけどそういう事は考えなくてフルバースト
            laser_power = ship.params.laser_power
            laser_damage(ship.x, ship.y, enemy_ship.x, enemy_ship.y, laser_power)
        damage //= 4  # 正確に狙っても最大1ずれるのでその分のダメージ減衰を考える
        return enemy_life <= damage

        # TODO 動くかもしれないと仮定し、周囲8マスにもできるだけ均等にダメージを与える場合

if __name__ == '__main__':
    ship1 = Ship(0, 1, 2, 3, 4, 5, ShipParameter(6, 7, 8, 9), 10, [])
    ship2 = Ship(0, 1, 2, 3, 4, 5, ShipParameter(6, 7, 8, 9), 10, [])
    state = State(GameStage.NOT_STARTED, 1, 2, 3, Side.ATTACK, [ship1], [ship2])
    ai = AI()
    ai.action(state)
    ai.set_specs(1, 1)

