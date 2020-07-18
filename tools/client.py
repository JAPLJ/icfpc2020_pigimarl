import requests
import sys

from cons_list import *
from galaxy_lazy import LazyGalaxy
from mod_dem import *
from multiple_draw import *


def main():
    galaxy_path = sys.argv[1]
    server_url = sys.argv[2]
    pictures_path = sys.argv[3]

    sys.setrecursionlimit(1000000)

    galaxy = LazyGalaxy(galaxy_path)
    interact(server_url, pictures_path, galaxy)


def interact(server_url, pictures_path, galaxy, initial_data=(1, ((3, None), (0, (None, None)))), initial_res=(0, 0)):
    """
    初期データと初期レスポンスを元に、Galaxy の実行およびサーバーとの通信を行い、最終的に画像を出力する。
    :param server_url: サーバー URL
    :param pictures_path: 画像の出力先
    :param galaxy: Galaxy
    :param initial_data: 初期データ
    :param initial_res: 初期レスポンス
    :return: None
    """
    data = initial_data
    res = initial_res

    while True:
        print('[Galaxy] Input data:', data)
        print('[Galaxy] Input response:', res)
        cons_list = galaxy.eval_galaxy(data, res)
        continue_flag, data, req = cons_list_to_python_list(cons_list)
        print('[Galaxy] Output continue flag:', continue_flag)
        print('[Galaxy] Output data:', data)
        print('[Galaxy] Output request:', req)

        if continue_flag == 0:
            draw_pictures(pictures_path, req)
            break

        print('[Send] Request:', req)
        res = send(server_url, req)
        print('[Send] Response:', res)


def send(server_url, req):
    """
    リクエストをサーバーへ送り、レスポンスを返す。
    :param server_url サーバー URL
    :param req: リクエスト
    :return: レスポンス
    """
    mod_req = enc_from_cons_obj(req)
    http_res = requests.post(server_url, data=mod_req)

    if http_res.status_code != 200:
        print('Unexpected server response:')
        print('HTTP code:', http_res.status_code)
        print('Request:', req)
        print('Modulated request:', mod_req)
        print('Response body:', http_res.text)
        exit(2)

    mod_res = http_res.text
    res = dec_to_cons_obj(mod_res)
    return res


def draw_pictures(pictures_path, pictures_cons_list):
    """
    指定のパスに画像たちを出力する。
    :param pictures_path: 画像の出力先のパス
    :param pictures_cons_list: 画像たちの cons 形式のリスト
    :return:
    """
    pictures = cons_list_to_python_list(pictures_cons_list)
    plot_vectors_list = [cons_list_to_python_list(picture) for picture in pictures]
    print('[Draw] Pictures:', plot_vectors_list)
    multipul_draw(plot_vectors_list, output_dir=pictures_path)


if __name__ == '__main__':
    main()
