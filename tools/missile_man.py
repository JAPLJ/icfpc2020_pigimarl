import sys

sys.path.append('app/')

from multiship import *
from utils import *


class Missile:
    def __init__(self, accels):
        self.accels = accels

    def action(self, state, ship):
        commands = []

        if len(self.accels) > 0:
            ax, ay = self.accels.pop(0)
            commands.append({'command': 'accel', 'x': ax, 'y': ay})
        else:
            nx, ny, _, _ = next_pos(ship.x, ship.y, ship.vx, ship.vy)

            near = False
            for s in state.enemy_ships:
                enx, eny, _, _ = next_pos(s.x, s.y, s.vx, s.vy)
                if max(abs(nx - enx), abs(ny - eny)) <= 3:
                    near = True

            safe = True
            for s in state.my_ships:
                mnx, mny, _, _ = next_pos(s.x, s.y, s.vx, s.vy)
                if max(abs(nx - mnx), abs(ny - mny)) <= 3 and s.params.soul > 1:
                    safe = False

            if near and safe:
                commands.append({'command': 'suicide'})

        return commands


# パラメータはこんな感じで
# attacker = ShipAIInfo(MissileMan(), 512 - (12 * 8 + 2 * 128), 0, 8, 128)
# defender = ShipAIInfo(MissileMan(), 448 - (12 * 8 + 2 * 128), 0, 8, 128)

class MissileMan:
    def __init__(self, yousumi_turns=10, missile_interval=2, missile_max_energy=1, stalk_interval=20,
                 stalk_max_energy=4):
        self.go_into_orbit_accels = None
        self.turn = 0
        self.yousumi_turns = yousumi_turns  # 最初に静止して相手の回転方向を見るターン数
        self.missile_interval = missile_interval  # ミサイルを撃つ間隔 (1 だったら毎ターン)
        self.missile_max_energy = missile_max_energy  # ミサイル一発あたりに持っていかれる燃料の最大値
        self.stalk_interval = stalk_interval  # 方向転換してストーキングする間隔 (1 だったら毎ターン)
        self.stalk_max_energy = stalk_max_energy  # ストーキング一回あたりに使う燃料の最大値

    def action(self, state, ship):
        commands = []

        # 最初の数ターンは様子見
        if self.turn < self.yousumi_turns:
            gx, gy = calc_gravity(ship.x, ship.y)
            commands.append({'command': 'accel', 'x': -gx, 'y': -gy})

        else:
            if self.go_into_orbit_accels is None:
                rot_sum = 0
                for s in state.enemy_ships:
                    rot_sum += s.x * s.vy - s.y * s.vx
                rot_sign = 1 if rot_sum > 0 else -1
                self.go_into_orbit_accels = go_into_orbit(state.gravity_radius, state.planet_radius, ship.x, ship.y,
                                                          ship.vx, ship.vy,
                                                          -rot_sign)

            if len(self.go_into_orbit_accels) == 0 and self.turn % self.stalk_interval == 0:
                self.go_into_orbit_accels = stalk(state.gravity_radius, state.planet_radius, ship.x, ship.y, ship.vx,
                                                  ship.vy, min(100, 384 - self.turn), state.enemy_ships,
                                                  self.stalk_max_energy)

            if len(self.go_into_orbit_accels) > 0:
                ax, ay = self.go_into_orbit_accels.pop(0)
                commands.append({'command': 'accel', 'x': ax, 'y': ay})
            elif self.turn % self.missile_interval == 0:
                accels = fire_target(state.gravity_radius, state.planet_radius, ship.x, ship.y, ship.vx, ship.vy,
                                     min(100, 384 - self.turn), state.enemy_ships, self.missile_max_energy, 1000)
                if accels is not None:
                    commands.append(
                        {'command': 'split', 'ship_ai_info': ShipAIInfo(Missile(accels), len(accels), 0, 0, 1)})

        self.turn += 1

        return commands
