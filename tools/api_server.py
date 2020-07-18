"""
Galaxy との interaction を行うための API サーバー。
(state, vector) のペアを送ると、(次の state, 画像たちの情報) を返す。

起動方法:
icfpc2020_pigimarl ディレクトリで
python3 tools/api_server.py galaxy.txt 'https://icfpc2020-api.testkontur.ru/aliens/send?apiKey=c16bab7da69d411da59ce8227e5d9034'

エンドポイントの叩き方:
url -X POST -H "Content-Type: application/json" -d '{"state": "None", "vector":[0, 0]}' http://127.0.0.1:5000/interact
"""

import json

from flask import Flask, request
from flask_cors import CORS

import deep_tuple
from client import *

api = Flask(__name__)
CORS(api)

galaxy_path = sys.argv[1]
server_url = sys.argv[2]

sys.setrecursionlimit(1000000)

galaxy = LazyGalaxy(galaxy_path)


@api.route('/interact', methods=['POST'])
def interact():
    state_str = request.json['state']
    vector_list = request.json['vector']

    state = deep_tuple.read(state_str)
    vector = tuple(vector_list)

    while True:
        print('[Galaxy] Input state:', state)
        print('[Galaxy] Input vector:', vector)
        cons_list = galaxy.eval_galaxy(state, vector)
        continue_flag, state, data = cons_list_to_python_list(cons_list)
        print('[Galaxy] Output continue flag:', continue_flag)
        print('[Galaxy] Output state:', state)
        print('[Galaxy] Output data:', data)

        if continue_flag == 0:
            break

        print('[Send] Request data:', data)
        vector = send(server_url, data)
        print('[Send] Response vector:', vector)

    pictures = [
        [
            list(t)
            for t in cons_list_to_python_list(cl)
        ]
        for cl in cons_list_to_python_list(data)
    ]

    res = {'state': str(state), 'multiple_draw': pictures}

    return json.dumps(res)


if __name__ == '__main__':
    api.run()
