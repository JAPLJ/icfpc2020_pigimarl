# 整数と list を modulate/demodulate する

def dec(s):
    def dec_inner(s, k):
        if s[k:k + 2] == '11':  # cons
            (h, k) = dec_inner(s, k + 2)
            (t, k) = dec_inner(s, k)
            if type(t) is not list:
                # nil なし対応
                return ([h] + [t], k)
            else:
                return ([h] + t, k)
        elif s[k:k + 2] == '00':  # nil
            return ([], k + 2)
        else:
            sgn = +1 if s[k:k + 2] == '01' else -1
            bits = 0
            k = k + 2
            while s[k] == '1':
                bits += 1
                k += 1
            return (0 if bits == 0 else sgn * int(s[k + 1:k + bits * 4 + 1], 2), k + bits * 4 + 1)

    return dec_inner(s, 0)[0]


def enc(l):
    if type(l) == int:
        res = []
        if l >= 0:
            res.append('01')
        else:
            res.append('10')
        bits = '' if l == 0 else bin(abs(l))[2:]
        bits4 = (len(bits) + 3) // 4
        res.append('1' * bits4 + '0')
        res.append('0' * (bits4 * 4 - len(bits)) + bits)
        return ''.join(res)
    else:
        if len(l) == 0:
            return '00'
        else:
            res = []
            res.append('11')
            res.append(enc(l[0]))
            res.append(enc(l[1:]))
            return ''.join(res)


def dec_to_cons_obj(s):
    """
    01 文字列を demodulate し、modulatable なオブジェクトを返す。
    :param s: 01 文字列
    :return: modulatable なオブジェクト
    """

    def dec_inner(s, k):
        if s[k:k + 2] == '11':  # cons
            (h, k) = dec_inner(s, k + 2)
            (t, k) = dec_inner(s, k)
            return ((h, t), k)
        elif s[k:k + 2] == '00':  # nil
            return (None, k + 2)
        else:
            sgn = +1 if s[k:k + 2] == '01' else -1
            bits = 0
            k = k + 2
            while s[k] == '1':
                bits += 1
                k += 1
            return (0 if bits == 0 else sgn * int(s[k + 1:k + bits * 4 + 1], 2), k + bits * 4 + 1)

    return dec_inner(s, 0)[0]


def enc_from_cons_obj(l):
    """
    modulatable なオブジェクトを modulate し、01 文字列を返す。
    :param l: modulatable なオブジェクト
    :return: 01 文字列
    """
    if type(l) == int:
        res = []
        if l >= 0:
            res.append('01')
        else:
            res.append('10')
        bits = '' if l == 0 else bin(abs(l))[2:]
        bits4 = (len(bits) + 3) // 4
        res.append('1' * bits4 + '0')
        res.append('0' * (bits4 * 4 - len(bits)) + bits)
        return ''.join(res)
    else:
        if l is None:
            return '00'
        else:
            res = []
            res.append('11')
            res.append(enc_from_cons_obj(l[0]))
            res.append(enc_from_cons_obj(l[1]))
            return ''.join(res)
