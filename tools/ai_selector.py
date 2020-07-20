from common_interface import *
from multiship import ShipAIInfo
from ship_ai_example import MainShipAI

from carpet_bomb import CarpetBombMother

# 君だけの AISelector を作って最高の AI を選択しよう！
class AISelector:
    def select(self, side, limit, enemy_params) -> ShipAIInfo:
        if side == Side.ATTACK:
            # enemy_params is ShipParameter
            return ShipAIInfo(CarpetBombMother(), 152, 0, 10, 120)
        else:
            # enemy_params is None
            return ShipAIInfo(MainShipAI(), 100, 0, 8, 100)
