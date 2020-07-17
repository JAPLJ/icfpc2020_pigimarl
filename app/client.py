import requests

from app.multiple_draw import multipul_draw


def modulate(a):
    """
    modulatable な何かを modulate し、01 文字列を返す。
    https://message-from-space.readthedocs.io/en/latest/message13.html
    https://message-from-space.readthedocs.io/en/latest/message14.html
    https://message-from-space.readthedocs.io/en/latest/message35.html
    :param a: modulatable な何か
    :return: 01 文字列
    """
    if a is None:
        return '00'
    elif type(a) is int:
        res = []
        if a >= 0:
            res.append('01')
        else:
            res.append('10')
        bits = '' if a == 0 else bin(abs(a))[2:]
        bits4 = (len(bits) + 3) // 4
        res.append('1' * bits4 + '0')
        res.append('0' * (bits4 * 4 - len(bits)) + bits)
        return ''.join(res)
    elif (type(a) is tuple) and (len(a) == 2):
        return '11' + modulate(a[0]) + modulate(a[1])
    else:
        print('Error! Not a modulatable object:', a)
        exit(2)


def demodulate(s):
    """
    01 文字列を demodulate し、modulatable な何かを返す。
    https://message-from-space.readthedocs.io/en/latest/message13.html
    https://message-from-space.readthedocs.io/en/latest/message14.html
    https://message-from-space.readthedocs.io/en/latest/message35.html
    :param s: 01 文字列
    :return: modulatable な何か
    """

    def dem_inner(s, k):
        if s[k:k + 2] == '11':  # cons
            (h, k) = dem_inner(s, k + 2)
            (t, k) = dem_inner(s, k)
            return (h, t), k
        elif s[k:k + 2] == '00':  # nil
            return None, k + 2
        else:
            sgn = +1 if s[k:k + 2] == '01' else -1
            bits = 0
            k = k + 2
            while s[k] == '1':
                bits += 1
                k += 1
            num = 0 if bits == 0 else sgn * int(s[k + 1:k + bits * 4 + 1], 2)
            return num, k + bits * 4 + 1

    return dem_inner(s, 0)[0]


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


def cons_list_to_python_list(cons_list):
    """
    cons 形式のリストを Python 形式の (普通の) リストへ変換する。
    :param cons_list: cons 形式のリスト
    :return: Python 形式のリスト
    """
    if cons_list is None:
        return []
    elif (type(cons_list) is tuple) and (len(cons_list) == 2):
        head = cons_list[0]
        tail = cons_list[1]
        return [head] + cons_list_to_python_list(tail)
    else:
        print('Error! Not a cons list:', cons_list)
        exit(2)
