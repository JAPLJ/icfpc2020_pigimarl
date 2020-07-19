"""
2P対戦用スクリプト
注意：本番では必要そうなヘルスチェックは除いてください
eg: python run_local_battle.py ai1 ./run_ai1.sh ai2 ./run_ai2.sh
    log/ai1.log, log/ai2.log にログが保存される

コンソールにもログを出したい
"""
import os
import sys
from subprocess import Popen

import requests

from tools.mod_dem import dec, enc_from_cons_obj


def get_two_player_keys(server_url, api_key):
    url = f"{server_url}/aliens/send?apiKey={api_key}"
    data = enc_from_cons_obj((1, (0, None)))
    response = requests.post(url, data)
    decoded = dec(response.text)
    p1_key = decoded[1][0][1]
    p2_key = decoded[1][1][1]
    return p1_key, p2_key


def execute(
        p1_name, p1_command, p1_key,
        p2_name, p2_command, p2_key,
        server_url):
    with open(os.path.join('log', f'{p1_name}.log'), "w") as f:
        p = Popen([p1_command, server_url, p1_key, '1.json'], stdout=f)
    with open(os.path.join('log', f'{p2_name}.log'), "w") as g:
        q = Popen([p2_command, server_url, p2_key, '2.json'], stdout=g)
    p.wait()
    q.wait()


if __name__ == '__main__':
    p1_name = sys.argv[1]
    p1_command = sys.argv[2]
    p2_name = sys.argv[3]
    p2_command = sys.argv[4]

    print("Player1:", p1_name, p1_command)
    print("Player2:", p2_name, p2_command)

    SERVER_URL = "https://icfpc2020-api.testkontur.ru"
    API_KEY = "c16bab7da69d411da59ce8227e5d9034"

    print("get player keys")
    p1_key, p2_key = get_two_player_keys(SERVER_URL, API_KEY)
    p1_key, p2_key = str(p1_key), str(p2_key)
    print("Player1Key:", p1_key)
    print("Player2Key:", p2_key)
    print("execute")
    execute(p1_name, p1_command, p1_key, p2_name, p2_command, p2_key, SERVER_URL)
