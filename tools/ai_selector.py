from common_interface import *
from missile_man import MissileMan
from multiship import ShipAIInfo
from sniper import Sniper
from split_escaper import SplitEscaper

# 君だけの AISelector を作って最高の AI を選択しよう！
class AISelector:
    def select(self, side, limit, enemy_params) -> ShipAIInfo:
        if side == Side.ATTACK:
            # enemy_params is ShipParameter
            if enemy_params.soul > 1:
                return ShipAIInfo(MissileMan(), 512 - (12 * 8 + 2 * 128), 0, 8, 128)
            else:
                return ShipAIInfo(Sniper(), limit - (96*4 + 12*8 + 1*2), 96, 8, 1)
        else:
            # enemy_params is None
            return ShipAIInfo(SplitEscaper(), 128, 0, 10, 100)
