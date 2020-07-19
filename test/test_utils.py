import sys
sys.path.append('app')
from utils import *

# 8方向 => フルダメージ
assert laser_damage(0, 0,  1,  0, 1) == 3
assert laser_damage(0, 0,  1,  0, 1) == 3
assert laser_damage(0, 0,  1,  1, 1) == 3
assert laser_damage(0, 0,  1, -1, 1) == 3
assert laser_damage(0, 0,  0,  1, 1) == 3
assert laser_damage(0, 0,  0, -1, 1) == 3
assert laser_damage(0, 0, -1,  0, 1) == 3
assert laser_damage(0, 0, -1,  1, 1) == 3
assert laser_damage(0, 0, -1, -1, 1) == 3

# 最小ダメージ
assert laser_damage(0, 0,  2,  1, 100) == 0
assert laser_damage(0, 0,  2, -1, 100) == 0
assert laser_damage(0, 0,  1,  2, 100) == 0
assert laser_damage(0, 0,  1, -2, 100) == 0
assert laser_damage(0, 0, -1,  2, 100) == 0
assert laser_damage(0, 0, -1, -2, 100) == 0
assert laser_damage(0, 0, -2,  1, 100) == 0
assert laser_damage(0, 0, -2, -1, 100) == 0

D = [227, 211, 195, 179, 163, 147, 131, 115, 98, 82, 66, 50, 34, 18, 2, 0, 0, 0, 2, 18, 34, 50, 66, 82, 98, 115, 131, 147, 163, 179, 195, 211, 227]
for y in range(0, 33):
    assert laser_damage(0, 0, 32, y, 86) == D[y]