import sys

from ai_interface import *

sys.path.append('app/')
from utils import *
from collections import defaultdict


class Sniper:
    def __init__(self, stalk_interval=20, stalk_max_energy=4):
        self.turn = 0
        self.orbit = None
        self.eship_accel_history = defaultdict(list)
        self.stalk_interval = stalk_interval  # 方向転換してストーキングする間隔 (1 だったら毎ターン)
        self.stalk_max_energy = stalk_max_energy  # ストーキング一回あたりに使う燃料の最大値

    def action(self, state, ship):
        res = []

        # 敵の accel ヒストリーを更新
        for eship in state.enemy_ships:
            if sum(eship.params.list()) == 0:
                # 死んでるし
                continue
            rc_accel = [rc for rc in eship.commands if rc.kind == 0]
            if len(rc_accel) == 0:
                self.eship_accel_history[eship.id].append((0, 0))
            else:
                self.eship_accel_history[eship.id].append((rc_accel[0].x, rc_accel[0].y))

        # 最初の軌道入りへのルート計算がまだなら、計算する
        if self.orbit is None:
            self.orbit = go_into_orbit(state.gravity_radius, state.planet_radius, ship.x, ship.y, ship.vx, ship.vy)

        # 最初の軌道入りはもう終わっている and 燃料が残っている and ストーキングのタイミングが来た場合
        if len(self.orbit) == 0 and ship.parameters.enemy > 0 and self.turn % self.stalk_interval == 0:
            self.orbit = stalk(state.gravity_radius, state.planet_radius, ship.x, ship.y, ship.vx, ship.vy,
                               min(100, 384 - self.turn), state.enemy_ships, self.stalk_max_energy)

        # 軌道入りがまだなら入る or ストーキング開始
        if len(self.orbit) > 0:
            ms = self.orbit[0]
            res.append({'command': 'accel', 'x': ms[0], 'y': ms[1]})
            self.orbit = self.orbit[1:]

        # 撃つぜレーザー
        to_attack = None
        max_dmg = 0
        for eship in state.enemy_ships:
            if sum(eship.params.list()) == 0:
                # 死んでるし
                continue

            pvx, pvy = 0, 0
            # 次の一手が直近N手の周期性から予測できる場合はそれを使い、そうでないなら最新のaccelのものを使う
            next_command = guess_next(self.eship_accel_history[eship.id][-10:])
            if next_command is not None:
                pvx, pvy = -next_command[0], -next_command[1]
            else:
                for rc in eship.commands:
                    if rc.kind == 0:
                        pvx, pvy = -rc.x, -rc.y

            (nx, ny, _, _) = next_pos(eship.x, eship.y, eship.vx + pvx, eship.vy + pvy)
            max_lp = min(ship.params.laser_power, ship.max_temp - ship.temp)
            ldmg = laser_damage(ship.x, ship.y, nx, ny, max_lp)
            edmg = ldmg - (eship.max_temp - eship.temp)
            if edmg > max_dmg:
                to_attack = {'command': 'laser', 'x': nx, 'y': ny, 'power': max_lp}
                max_dmg = edmg
        if max_dmg > 0 and to_attack is not None:
            res.append(to_attack)

        self.turn += 1

        return res

    def set_specs(self, limit, side):
        souls = 100
        if side == Side.ATTACK:
            return ShipParameter(limit - (96 * 4 + 12 * 8 + 1 * 2), 96, 8, 1)
        else:
            return ShipParameter(limit - (32 * 4 + 12 * 16 + 1 * 2), 32, 16, 1)
