from common_interface import *
from multiship import ShipAIInfo
from ship_ai_example import MainShipAI
import escaper
import sniper

# 君だけの AISelector を作って最高の AI を選択しよう！
class AISelector:
    def select(self, side, limit, enemy_params) -> ShipAIInfo:
        if side == Side.ATTACK:
            # enemy_params is ShipParameter
            return ShipAIInfo(sniper.Sniper(), limit - (96*4 + 12*8 + 1*2), 96, 8, 1)
        else:
            # enemy_params is None
            cool_rate = 16
            return ShipAIInfo(escaper.Escaper(), limit - (12*cool_rate + 2*1), 0, cool_rate, 1)
