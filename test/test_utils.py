import sys
sys.path.append('app')
from utils import *

# 8方向 => フルダメージ
assert laser_damage(0, 0,  1,  0, 1), 3
assert laser_damage(0, 0,  1,  0, 1), 3
assert laser_damage(0, 0,  1,  1, 1), 3
assert laser_damage(0, 0,  1, -1, 1), 3
assert laser_damage(0, 0,  0,  1, 1), 3
assert laser_damage(0, 0,  0, -1, 1), 3
assert laser_damage(0, 0, -1,  0, 1), 3
assert laser_damage(0, 0, -1,  1, 1), 3
assert laser_damage(0, 0, -1, -1, 1), 3

# 最小ダメージ
assert laser_damage(0, 0,  2,  1, 100), 1
assert laser_damage(0, 0,  2, -1, 100), 1
assert laser_damage(0, 0,  1,  2, 100), 1
assert laser_damage(0, 0,  1, -2, 100), 1
assert laser_damage(0, 0, -1,  2, 100), 1
assert laser_damage(0, 0, -1, -2, 100), 1
assert laser_damage(0, 0, -2,  1, 100), 1
assert laser_damage(0, 0, -2, -1, 100), 1
