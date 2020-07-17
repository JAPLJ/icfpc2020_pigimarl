import requests


def modulate(a):
    """
    modulatable な何かを modulate し、01 文字列を返す。
    https://message-from-space.readthedocs.io/en/latest/message13.html
    https://message-from-space.readthedocs.io/en/latest/message14.html
    https://message-from-space.readthedocs.io/en/latest/message35.html
    :param a: modulatable な何か
    :return: 01 文字列
    """
    return '01'


def demodulate(s):
    """
    01 文字列を demodulate し、modulatable な何かを返す。
    https://message-from-space.readthedocs.io/en/latest/message13.html
    https://message-from-space.readthedocs.io/en/latest/message14.html
    https://message-from-space.readthedocs.io/en/latest/message35.html
    :param s: 01 文字列
    :return: modulatable な何か
    """
    return [0]


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
            multipledraw(pictures_path, res)
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


def galaxy(input_list):
    """
    (データ, レスポンス) を受け取り、次の (継続フラグ, データ, リクエスト) を返す。
    japlj さんが書いてくれてる。
    :param input_list: 長さ 2 のリスト (データ, レスポンス)
    :return: 長さ 3 の リスト (停止フラグ, データ, リクエスト)
    """
    pass


def multipledraw(path, pictures):
    """
    指定のパスに画像を出力する。
    鈴木君が書いてくれてる。
    :param path: 画像の出力先
    :param pictures: List[List[Pair[Int, Int]]] で表現される画像たちのリスト
    :return: None
    """
    pass
