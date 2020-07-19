# ネストの深いタプルを頑張って読み込んでくれる君

def read(s):
    """めちゃくちゃネストの深いタプルを表す文字列 s を評価してくれる"""
    res = []
    i = 0
    cur = []
    while i < len(s):
        if s[i] == ' ' or s[i] == ',':
            i += 1
        elif s[i] == '(':
            res.append(cur)
            cur = []
            i += 1
        elif s[i] == ')':
            res[-1].append(tuple(cur))
            cur = res.pop()
            i += 1
        elif s[i] == 'N':
            cur.append(None)
            i += 4
        else:
            v = 0
            sgn = +1
            if s[i] == '-':
                sgn = -1
                i += 1
            while s[i].isdigit():
                v = v * 10 + ord(s[i]) - ord('0')
                i += 1
            cur.append(v * sgn)
    return cur[0]
