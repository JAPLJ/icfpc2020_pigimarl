from common_interface import *
from missile_man import MissileMan
from multiship import ShipAIInfo


# 君だけの AISelector を作って最高の AI を選択しよう！
class AISelector:
    def select(self, side, limit, enemy_params) -> ShipAIInfo:
        if side == Side.ATTACK:
            # enemy_params is ShipParameter
            return ShipAIInfo(MissileMan(), 512 - (12 * 8 + 2 * 128), 0, 8, 128)
        else:
            # enemy_params is None
            return ShipAIInfo(MissileMan(), 448 - (12 * 8 + 2 * 128), 0, 8, 128)
