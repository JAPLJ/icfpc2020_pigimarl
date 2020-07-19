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
    if len(game_state[1]) > 0:
        (planet_radius, gravity_radius) = game_state[1]
    else:
        (planet_radius, gravity_radius) = (None, None)
    ships = game_state[2]

    (atk_ships, def_ships) = convert_ships(ships)

    return State(game_stage=game_stage,
                 planet_radius=planet_radius,
                 gravity_radius=gravity_radius,
                 current_turn=current_turn,
                 my_side=my_side,
                 my_ships=def_ships if my_side == Side.DEFENSE else atk_ships,
                 enemy_ships=def_ships if my_side == Side.ATTACK else atk_ships)


def convert_ships(resp):
    """ふね変換くん"""
    ships = [[], []]
    for ship in resp:
        (ship_info, rcmds) = ship
        side = ship_info[0]
        id = ship_info[1]
        (x, y) = ship_info[2]
        (vx, vy) = ship_info[3]
        params = ShipParameter(*ship_info[4])
        temp = ship_info[5]
        max_temp = ship_info[6]
        max_accel = ship_info[7]
        cmds = []
        for rc in rcmds:
            r = ResponseCommand()
            r.kind = rc[0]
            if r.kind == 0:  # 推進
                r.x, r.y = rc[1][0], rc[1][1]
            elif r.kind == 1:   # 自爆
                r.v = rc[1]
            elif r.kind == 2:   # LASER
                r.x, r.y = rc[1][0], rc[1][1]
                r.p2 = rc[2]
                r.v = rc[3]
            elif r.kind == 3:   # 分裂
                r.p1, r.p2, r.p3, r.p4 = rc[1]
            cmds.append(r)
        ships[side].append(Ship(id=id, side=side, x=x, y=y, vx=vx, vy=vy, params=params, temp=temp,
                                max_temp=temp, max_accel=max_accel, commands=cmds))
    return ships


def actions_to_commands(actions):
    """
    AI の出力 Dict[int, List[Command]] を受け取って、HTTP Proxy に渡すべきリストを作ってくれる君
    戻り値は普通の Python list
    """
    res = []
    for ship_id in actions:
        for cmd in actions[ship_id]:
            if cmd['command'] == 'accel':    # 推進
                res.append([0, ship_id, Pt(-cmd['x'], -cmd['y'])])
            elif cmd['command'] == 'suicide':   # 自爆
                res.append([1, ship_id])
            elif cmd['command'] == 'laser': # レーザー
                res.append([2, ship_id, Pt(cmd['x'], cmd['y']), cmd['power']])
            elif cmd['command'] == 'split':   # 分裂
                res.append([3, ship_id, [cmd['p1'], cmd['p2'], cmd['p3'], cmd['p4']]])
    return res
