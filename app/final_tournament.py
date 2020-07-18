import requests
import sys

from tools.mod_dem import *


def final_tournament():
    server_url = sys.argv[1]
    player_key = int(sys.argv[2])
    print('ServerUrl: %s; PlayerKey: %s' % (server_url, player_key))

    send(server_url, [2, player_key, []])  # とりあえず nil
    send(server_url, [3, player_key, [1, 1, 1, 1]])
    while True:
        send(server_url, [4, player_key, []])  # とりあえず nil


def send(server_url, python_list):
    print('Request:', python_list)
    print('Modulated request:', enc(python_list))

    res = requests.post(server_url, data=enc(python_list))

    if res.status_code != 200:
        print('Unexpected server response:')
        print('HTTP code:', res.status_code)
        print('Response body:', res.text)
        exit(2)

    print('Server response:', res.text)


if __name__ == '__main__':
    main()
