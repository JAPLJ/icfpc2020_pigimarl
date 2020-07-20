from common_interface import *
from multiship import ShipAIInfo
from ship_ai_example import MainShipAI
from missile_man import MissileMan

# 君だけの AISelector を作って最高の AI を選択しよう！
class AISelector:
    def select(self, side, limit, enemy_params) -> ShipAIInfo:
        if side == Side.ATTACK:
            # enemy_params is ShipParameter
            # return ShipAIInfo(MainShipAI(), 152, 0, 10, 120)
            return ShipAIInfo(MissileMan(), 512 - (12 * 8 + 2 * 128), 0, 8, 128)
        else:
            # enemy_params is None
            return ShipAIInfo(MainShipAI(), 100, 0, 8, 100)
            # return ShipAIInfo(MissileMan(), 512 - (12 * 8 + 2 * 128), 0, 8, 128)
