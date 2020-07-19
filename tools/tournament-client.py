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
    solver: action(state: State) -> Dict[int, List[Command]]
    """
    req_join = make_req_join(player_key)
    res = send(server_url, req_join)


def send(server_url, req):
    mod_req = enc_from_cons_obj(req)
    http_res = requests.post(server_url, data=mod_req)
    if http_res.status_code != 200:
        print('Unexpected server response:')
        print('HTTP code:', http_res.status_code)
        print('Request:', req)
        print('Modulated request:', mod_req)
        print('Response body:', http_res.text)
        exit(2)
    return None


def make_req_join(player_key):
    # ただのlist（cons形式でない）を返す
    return [2, player_key, []]

def make_req_start(player_key, ship_parameter):
    # ただのlist（cons形式でない）を返す
    return [3, player_key, ship_parameter.list()]

def make_req_commands(commands):
    # ただのlist（cons形式でない）を返す


def main():
    server_url = sys.argv[1]
    player_key = sys.argv[2]
    

if __name__ == '__main__':
    main()
