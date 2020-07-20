import sys

sys.path.append('app/')

from multiship import *
from utils import *


class SplitEscaper2:
    MAX_TURNS = 256
    CHECK_TURN = 15  # 今後このターンで墜落・範囲外にならないことを確認
    ESCAPE_DMG = 50  # これ以上のダメージ（温度増加含む）で回避行動を取る
    DUPLICATION_TURN = 10

    def __init__(self):
        self.into_orbit_moves = None
        self.past_acc = (0, 0)
        self.mother_id = None
        self.duplication_count = self.DUPLICATION_TURN

    def action(self, state, ship):
        # 最も右下の点へ向かって移動
        ax, ay = move_to_target(state.gravity_radius, state.planet_radius, ship.x, ship.y, ship.vx, ship.vy,
                                state.gravity_radius, state.gravity_radius)
        commands = [{'command': 'accel', 'x': ax, 'y': ay}]

        # soul がある間は SubShipAI を産み続ける
        if ship.params.soul > 1:
            # !!! split コマンドだけ今までと渡すものが違う。ship_ai_info (発射する AI のインスタンスとパラメータ 4 個) を渡す
            commands.append({'command': 'split', 'ship_ai_info': ShipAIInfo(SubShipAI(), 0, 0, 0, 1)})

        return commands


class SubShipAI:
    def __init__(self):
        pass

    def action(self, state, ship):
        return []
