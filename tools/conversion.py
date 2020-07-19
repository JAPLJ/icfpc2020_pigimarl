# HTTP Proxy でやり取りするデータと、AI が扱うデータの相互変換を行う

from common_interface import *
from ai_interface import *


def game_response_to_state(resp):
    """
    HTTP で返ってきた GameResponse を AI に渡す State にしてくれる
    resp: Python list にデコードされた状態のサーバからのレスポンス
    """
    assert resp[0] == 1 # Success
    game_stage = GameStage(resp[1])
    game_info = resp[2] # unknown list A
    my_side = Side(game_info[1])
    game_state = resp[3]

    if len(game_state) == 0:
        # (side, limit)
        return (my_side, game_info[2][0])

    # game_state = [ turn, gravity, ships ]
    current_turn = game_state[0]
    (planet_radius, gravity_radius) = game_state[1]
    ships = game_state[2]

    # ships = [ def_ships, atk_ships ]
    def_ships = convert_ships(ships[0])
    atk_ships = convert_ships(ships[1])

    return State(game_stage=game_stage,
                 planet_radius=planet_radius,
                 gravity_radius=gravity_radius,
                 current_turn=current_turn,
                 my_side=side,
                 my_ships=def_ships if my_side == DEFENSE else atk_ships,
                 enemy_ships=atk_ships if my_side == ATTACK else def_ships)


def convert_ships(resp):
    """ふね変換くん"""
    ships = []
    for ship in resp:
        (ship_info, _) = ship   # commands: unsupported
        side = ship_info[0]
        id = ship_info[1]
        (x, y) = ship_info[2]
        (vx, vy) = ship_info[3]
        params = ShipParameter(*ship_info[4])
        temp = ship_info[5]
        ships.append(Ship(id=id, side=side, x=x, y=y, vx=vx, vy=vy, params=params, temp=temp))
    return ships


def actions_to_commands(actions):
    """
    AI の出力 Dict[int, List[Command]] を受け取って、HTTP Proxy に渡すべきリストを作ってくれる君
    戻り値は普通の Python list
    """
    res = []
    for ship_id in actions:
        for cmd in actions[ship_id]:
            if cmd['command'] == 'move':    # 推進
                res.append([0, ship_id, [-cmd['x'], -cmd['y']]])
            elif cmd['command'] == 'suicide':   # 自爆
                res.append([1, ship_id])
            elif cmd['command'] == 'laser': # レーザー
                res.append([2, ship_id, [cmd['x'], cmd['y']], cmd['power']])
            elif cmd['split'] == 'split':   # 分裂
                res.append([3, ship_id, [cmd['p1'], cmd['p2'], cmd['p3'], cmd['p4']]])
    return res
