import requests

from tools.cons_list import *
from tools.mod_dem import *
from tools.multiple_draw import multipul_draw


def modulate(a):
    """
    modulatable な何かを modulate し、01 文字列を返す。
    :param a: modulatable な何か
    :return: 01 文字列
    """
    return enc(cons_list_to_python_list(a))


def demodulate(s):
    """
    01 文字列を demodulate し、modulatable な何かを返す。
    :param s: 01 文字列
    :return: modulatable な何か
    """
    return python_list_to_cons_list(dec(s))


def interact(server_url, pictures_path, initial_data, initial_res):
    """
    初期データと初期レスポンスを元に、Galaxy の実行およびサーバーとの通信を行い、最終的に画像を出力する。
    :param server_url: サーバー URL
    :param pictures_path: 画像の出力先
    :param initial_data: 初期データ
    :param initial_res: 初期レスポンス
    :return: None
    """
    data = initial_data
    res = initial_res

    while True:
        print('[Galaxy] Input data:', data)
        print('[Galaxy] Input response:', res)
        continue_flag, data, req = galaxy([data, res])
        print('[Galaxy] Output continue flag:', continue_flag)
        print('[Galaxy] Output data:', data)
        print('[Galaxy] Output request:', req)

        if continue_flag == 0:
            print('[Draw] Pictures:', res)
            draw_pictures(pictures_path, res)
            break

        print('[Send] Request:', req)
        res = send(server_url, req)
        print('[Send] Response:', res)


def send(server_url, req):
    """
    リクエストをサーバーへ送り、レスポンスを返す。
    https://icfpc2020-api.testkontur.ru/aliens/send?apiKey=c16bab7da69d411da59ce8227e5d9034
    :param server_url サーバー URL
    :param req: リクエスト
    :return: レスポンス
    """
    mod_req = modulate(req)
    http_res = requests.post(server_url, data=mod_req)

    if http_res.status_code != 200:
        print('Unexpected server response:')
        print('HTTP code:', http_res.status_code)
        print('Request:', req)
        print('Modulated request:', mod_req)
        print('Response body:', http_res.text)
        exit(2)

    mod_res = http_res.text
    res = demodulate(mod_res)
    return res


def galaxy(data, res):
    """
    データとレスポンスを受け取り、次の (継続フラグ, データ, リクエスト) を返す。
    japlj さんが書いてくれてる。
    :param data: データ
    :param res: レスポンス
    :return: 長さ 3 の リスト (継続フラグ, データ, リクエスト)
    """
    pass


def draw_pictures(pictures_path, pictures_cons_list):
    """
    指定のパスに画像たちを出力する。
    :param pictures_path: 画像の出力先のパス
    :param pictures_cons_list: 画像たちの cons 形式のリスト
    :return:
    """
    pictures = cons_list_to_python_list(pictures_cons_list)
    plot_vectors_list = [cons_list_to_python_list(picture) for picture in pictures]
    multipul_draw(plot_vectors_list, output_dir=pictures_path)
