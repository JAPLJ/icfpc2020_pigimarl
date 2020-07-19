import requests

from cons_list import *
from mod_dem import *

class ShipParameter:
    def __init__(self, energy, laser_power, cooling_rate, soul):
        self.energy = energy
        self.laser_power = laser_power
        self.cooling_rate = cooling_rate
        self.soul = soul

    def list():
        return [self.energy, self.laser_power, self.cooling_rate, self.soul]

def run(server_url, player_key, ship_parameter, solver):
    """
    ゲームを一回分実行
    ship_parameter: ゲーム開始時の初期パラメータ
    solver: func: action(state: State) -> Dict[int, List[Command]]
    """
    print('[RUNNER] join game')
    req_join = make_req_join(player_key)
    state = send(server_url, req_join)

    if state.game_stage != 0:
        print('[RUNNER] invalid game stage:', state.game_stage)
        exit(2)

    print('[RUNNER] start game, parameter:', ship_parameter)
    req_start = make_req_join(player_key, ship_parameter)
    state = send(server_url, req_start)

    while True:
        commands = solver(state)
        print('[RUNNER] send commands:', command)
        req_commands = make_req_commands(commands)
        state = send(server_url, req_commands)

        if state.game_stage == 2:
            break

    print('[RUNNER] game finished')


def send(server_url, list_req):
    """
    リクエスト送信
    req: list（cons形式でない）
    return: state: GameResponseをパースしたもの
    """
    cons_req = python_list_to_cons_list(list_req)
    mod_req = enc_from_cons_obj(cons_req)
    http_res = requests.post(server_url, data=mod_req)
    if http_res.status_code != 200:
        print('Unexpected server response:')
        print('HTTP code:', http_res.status_code)
        print('Request:', req)
        print('Modulated request:', mod_req)
        print('Response body:', http_res.text)
        exit(2)

    mod_res = http_res.text
    cons_res = dec_to_cons_obj(mod_res)
    list_res = cons_list_to_python_list(cons_res)
    return parse_game_response(list_res)

def parse_game_response(res):
    """
    GameResponseのlistをパースする
    """
    return {} # tekitou


def make_req_join(player_key):
    # ただのlist（cons形式でない）を返す
    return [2, player_key, [None]]

def make_req_start(player_key, ship_parameter):
    # ただのlist（cons形式でない）を返す
    return [3, player_key, ship_parameter.list()]

def make_req_commands(player_key, commands):
    # ただのlist（cons形式でない）を返す
    return [4, player_key, [None]]

def main():
    server_url = sys.argv[1]
    player_key = sys.argv[2]


if __name__ == '__main__':
    main()
