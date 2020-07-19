import dataclasses
from typing import List


@dataclasses.dataclass
class Ship:
    id: int
    side: int
    x: int
    y: int
    vx: int
    vy: int
    temp: int
    energy: int
    laser_power: int
    cooling_rate: int
    soul: int


@dataclasses.dataclass
class State:
    game_stage: int
    current_turn: int
    my_side: int
    my_ships: List[Ship]
    enemy_ships: List[Ship]


if __name__ == '__main__':
    ship1 = Ship(0, 1, 2, 3, 4, 5, 6)
    ship2 = Ship(0, 1, 2, 3, 4, 5, 6)
    state = State(0, 1, 2, [ship1], [ship2])
