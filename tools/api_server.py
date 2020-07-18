import json

from flask import Flask, request

import deep_tuple
from client import *

api = Flask(__name__)

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
