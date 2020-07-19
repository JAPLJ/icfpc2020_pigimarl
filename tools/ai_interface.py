# AI 側が受け取るステートや、返すコマンド達のデータ型の定義

import dataclasses
from typing import List

from common_interface import *

@dataclasses.dataclass
class Ship:
    id: int
    side: Side
    x: int
    y: int
    vx: int
    vy: int
    params: ShipParameter
    temp: int
    # commands: unsupported

@dataclasses.dataclass
class State:
    game_stage: GameStage
    planet_radius: int
    gravity_radius: int
    current_turn: int
    my_side: Side
    my_ships: List[Ship]
    enemy_shps: List[Ship]
