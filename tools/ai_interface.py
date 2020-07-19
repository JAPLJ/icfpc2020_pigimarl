# AI 側が受け取るステートや、返すコマンド達のデータ型の定義

import dataclasses
from typing import List

from common_interface import *

@dataclasses.dataclass
class ResponseCommand:
    kind: int = -1
    x: int = 0
    y: int = 0
    v: int = 0
    p1: int = 0
    p2: int = 0
    p3: int = 0
    p4: int = 0

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
    commands: List[ResponseCommand]

@dataclasses.dataclass
class State:
    game_stage: GameStage
    planet_radius: int
    gravity_radius: int
    current_turn: int
    my_side: Side
    my_ships: List[Ship]
    enemy_ships: List[Ship]
