from common_interface import *
from multiship import ShipAIInfo
from ship_ai_example import MainShipAI
from sniper import Sniper
from split_escaper import SplitEscaper

# 君だけの AISelector を作って最高の AI を選択しよう！
class AISelector:
    def select(self, side, limit, enemy_params) -> ShipAIInfo:
        if side == Side.ATTACK:
            # enemy_params is ShipParameter
            return ShipAIInfo(Sniper(), 128, 0, 10, 100)
        else:
            # enemy_params is None
            return ShipAIInfo(SplitEscaper(), 128, 0, 10, 100)
