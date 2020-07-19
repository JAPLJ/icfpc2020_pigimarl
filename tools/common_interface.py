# AI, client で共通のデータ型

from enum import IntEnum
import dataclasses

class Pt:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class GameStage(IntEnum):
    NOT_STARTED = 0
    STARTED = 1
    FINISHED = 2


class Side(IntEnum):
    ATTACK = 0
    DEFENSE = 1


@dataclasses.dataclass
class ShipParameter:
    energy: int
    laser_power: int
    cooling_rate: int
    soul: int

    def list(self):
        return [self.energy, self.laser_power, self.cooling_rate, self.soul]
