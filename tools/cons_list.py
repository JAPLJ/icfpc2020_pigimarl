"""
Python 形式のリストと cons 形式のリストを相互に変換する。
cons は 2 要素の tuple で、nil は None で表現する。

例: [1, 2, 3] <-> (1, (2, (3, None)))
"""


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


def cons_list_to_python_list_recurse(cons_list):
    if cons_list is None:
        return []
    elif (type(cons_list) is tuple) and (len(cons_list) == 2):
        head = cons_list_to_python_list_recurse(cons_list[0])
        tail = cons_list_to_python_list_recurse(cons_list[1])
        if type(tail) is not list:
            # 末尾に nil がないリスト対応
            return [head] + [tail]
        else:
            return [head] + tail
    elif type(cons_list) is int:
        return cons_list
    else:
        print('Error! Not a cons list:', cons_list)
        exit(2)


def python_list_to_cons_list(python_list):
    """
    Python 形式の (普通の) リストを cons 形式のリストへ変換する。
    :param python_list: Python 形式のリスト
    :return: cons 形式のリスト
    """
    if type(python_list) is list:
        if len(python_list) == 0:
            return None
        else:
            return python_list[0], python_list_to_cons_list(python_list[1:])
    else:
        print('Error! Not a Python list:', python_list)
        exit(2)

def python_list_to_cons_list_recurse(python_list):
    if type(python_list) is list:
        if len(python_list) == 0:
            return None
        else:
            head = python_list_to_cons_list_recurse(python_list[0])
            tail = python_list_to_cons_list_recurse(python_list[1:])
            return (head, tail)
    elif type(python_list) is int:
        return python_list
    else:
        print('Error! Not a Python list:', python_list)
        exit(2)
