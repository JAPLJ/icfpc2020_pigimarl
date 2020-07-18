import requests
import sys

from mod_dem import *

prev_res = None


def main():
    server_url = sys.argv[1]
    player_key = int(sys.argv[2])
    print('ServerUrl: %s; PlayerKey: %s' % (server_url, player_key))

    health_check(server_url, player_key)

    send(server_url, [2, player_key, []])  # とりあえず nil
    send(server_url, [3, player_key, [1, 1, 1, 1]])
    while True:
        send(server_url, [4, player_key, []])  # とりあえず nil


def health_check(server_url, player_key):
    res = requests.post(server_url, data=str(player_key))
    if res.status_code != 200:
        print('Unexpected server response:')
        print('HTTP code:', res.status_code)
        print('Response body:', res.text)
        exit(2)
    print('Server response:', res.text)


def send(server_url, python_list):
    global prev_res

    print('Request:', python_list)
    # print('Modulated request:', enc(python_list))

    res = requests.post(server_url + '/aliens/send?apiKey=c16bab7da69d411da59ce8227e5d9034', data=enc(python_list))

    if res.status_code != 200:
        # print('Previous server response:', dec(prev_res))
        print('Unexpected server response:')
        print('HTTP code:', res.status_code)
        print('Response body:', res.text)
        exit(2)

    # print('Modulated server response:', res.text)
    print('Server response:', dec(res.text))

    prev_res = res.text


if __name__ == '__main__':
    main()
