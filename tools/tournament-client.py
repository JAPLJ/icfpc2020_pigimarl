import requests
import sys
from requests.exceptions import Timeout

from cons_list import *
from mod_dem import *
from common_interface import *
from conversion import *

API_KEY = 'c16bab7da69d411da59ce8227e5d9034'

def run(server_url, player_key, attacker_solver, defender_solver=None):
    """
    ゲームを一回分実行
    sideに応じてsolverを使い分ける
    使い分けの必要がない場合はdefender_solverを与えなくても良い
    solver:
        action func(State) -> Dict[int, List[Command]]
        set_specs func(limit: int, side: int) -> ShipParameter

    """
    print('[RUNNER] join game')
    req_join = make_req_join(player_key)
    (side, limit) = send(server_url, req_join)

    solver = attacker_solver
    if side == Side.DEFENSE and defender_solver is not None:
        solver = defender_solver

    ship_parameter = solver.set_specs(limit, side)
    print('[RUNNER] start game, parameter:', ship_parameter.list())
    req_start = make_req_start(player_key, ship_parameter)
    state = send(server_url, req_start)

    while True:
        commands = solver.action(state)
        print('[RUNNER] send commands:', commands)
        req_commands = make_req_commands(player_key, commands)
        state = send(server_url, req_commands)

        if state.game_stage == GameStage.FINISHED:
            break

    print('[RUNNER] game finished')

def send(server_url, list_req):
    """
    リクエスト送信
    req: list（cons形式でない）
    return: state: GameResponseをパースしたもの
    """
    print('[Send] req:', list_req)
    cons_req = python_list_to_cons_list_recurse(list_req)
    mod_req = enc_from_cons_obj(cons_req)
    try:
        http_res = requests.post(f'{server_url}/aliens/send?apiKey={API_KEY}', data=mod_req, timeout=10.0)
    except Timeout:
        print('[Send] timeout')
        exit(2)
    if http_res.status_code != 200:
        print('[Send] Unexpected server response:')
        print('[Send] HTTP code:', http_res.status_code)
        print('[Send] Request:', mod_req)
        print('[Send] Modulated request:', mod_req)
        print('[Send] Response body:', http_res.text)
        exit(2)

    mod_res = http_res.text
    cons_res = dec_to_cons_obj(mod_res)
    list_res = cons_list_to_python_list_recurse(cons_res)
    print('[Send] res:', list_res)
    return parse_game_response(list_res)

def parse_game_response(res):
    """
    GameResponseのlistをパースする
    """
    return game_response_to_state(res)


def make_req_join(player_key):
    # ただのlist（cons形式でない）を返す
    return [2, player_key, []]

def make_req_start(player_key, ship_parameter):
    # ただのlist（cons形式でない）を返す
    return [3, player_key, ship_parameter.list()]

def make_req_commands(player_key, commands):
    # ただのlist（cons形式でない）を返す
    return [4, player_key, actions_to_commands(commands)]

def main():
    server_url = sys.argv[1]
    player_key = int(sys.argv[2])

    # sys.setrecursionlimit(1000000)

    class Solver:
        def action(self, state):
            def action(self, state):
                commands = {}
                for ship in state.my_ships:
                    commands[ship.id] = [{'command': 'suicide'}]
                return commands

        def set_specs(self, limit, side):
            return ShipParameter(1, 1, 1, 1)

    solver = Solver()

    run(server_url, player_key, solver)


if __name__ == '__main__':
    main()
