import requests
import sys
from dataclasses import asdict
from requests.exceptions import Timeout
import datetime

from cons_list import *
from conversion import *
from mod_dem import *
from multiship import Multiship

API_KEY = 'c16bab7da69d411da59ce8227e5d9034'

import time
import threading

class TimestampLogger(threading.Thread):
    def __init__(self):
        super().__init__()
        self.alive = True
        self.start()

    def __del__(self):
        self.kill()

    def kill(self):
        self.alive = False
        self.join()

    def run(self):
        while self.alive:
            time.sleep(0.2)
            print(f"[{datetime.datetime.now()} TIMESTAMPER] STAMP")


def run(server_url, player_key, ai_selector, json_log_path=None):
    """
    ゲームを一回分実行
    君だけの ai_selector: AISelector を作って最高の AI を選択しよう！

    solver:
        action func(State) -> Dict[int, List[Command]]
        set_specs func(limit: int, side: int) -> ShipParameter
    """
    json_logging = json_log_path is not None
    json_logs = []

    print('[RUNNER] join game', flush=True)
    req_join = make_req_join(player_key)
    (side, limit, enemy_params) = send(server_url, req_join)

    ai_info = ai_selector.select(side, limit, enemy_params)
    solver = Multiship(ai_info, ai_info)

    ship_parameter = solver.set_specs(limit, side)
    print('[RUNNER] start game, parameter:', ship_parameter.list(), flush=True)
    req_start = make_req_start(player_key, ship_parameter)
    state = send(server_url, req_start)
    if json_logging:
        json_logs.append(asdict(state))

    while True:
        print(f'[{datetime.datetime.now()} RUNNER] call solver.action', flush=True)
        commands = solver.action(state)
        print(f'[{datetime.datetime.now()} RUNNER] send commands:', commands, flush=True)
        req_commands = make_req_commands(player_key, commands)
        state = send(server_url, req_commands)
        if json_logging:
            json_logs.append(asdict(state))

        if state.game_stage == GameStage.FINISHED:
            break

    if json_logging:
        import json
        with open(json_log_path, 'w') as f:
            f.write(json.dumps(json_logs))
            # f.write(f'[{",".join(json_logs)}]')

    print('[RUNNER] game finished', flush=True)


def send(server_url, list_req):
    """
    リクエスト送信
    req: list（cons形式でない）
    return: state: GameResponseをパースしたもの
    """
    print(f'[{datetime.datetime.now()} Send] req:', str(list_req)[:100], flush=True)
    cons_req = python_list_to_cons_list_recurse(list_req)
    mod_req = enc_from_cons_obj(cons_req)
    try:
        http_res = requests.post(f'{server_url}/aliens/send?apiKey={API_KEY}', data=mod_req, timeout=10.0)
    except Timeout:
        print('[Send] timeout', flush=True)
        exit(2)
    if http_res.status_code != 200:
        print('[Send] Unexpected server response:', flush=True)
        print('[Send] HTTP code:', http_res.status_code, flush=True)
        print('[Send] Request:', mod_req, flush=True)
        print('[Send] Modulated request:', mod_req, flush=True)
        print('[Send] Response body:', http_res.text, flush=True)
        exit(2)

    mod_res = http_res.text
    cons_res = dec_to_cons_obj(mod_res)
    list_res = cons_list_to_python_list_recurse(cons_res)
    print(f'[{datetime.datetime.now()} Send] res:', str(list_res)[:100], flush=True)
    return parse_game_response(list_res)


def parse_game_response(res):
    """
    GameResponseのlistをパースする
    """
    return game_response_to_state(res)


def make_req_join(player_key):
    # ただのlist（cons形式でない）を返す
    return [2, player_key, [103652820, 192496425430]]


def make_req_start(player_key, ship_parameter):
    # ただのlist（cons形式でない）を返す
    return [3, player_key, ship_parameter.list()]


def make_req_commands(player_key, commands):
    # ただのlist（cons形式でない）を返す
    return [4, player_key, actions_to_commands(commands)]


def main():
    x = TimestampLogger()
    server_url = sys.argv[1]
    player_key = int(sys.argv[2])
    json_log_path = None if len(sys.argv) < 4 else sys.argv[3]

    # sys.setrecursionlimit(1000000)
    from ai_selector import AISelector
    
    try:
        run(server_url, player_key, AISelector(), json_log_path=json_log_path)
    except:
        import traceback
        traceback.print_exc()
        sys.stdout.flush()
        sys.stderr.flush()
    
    x.kill()


if __name__ == '__main__':
    main()
