#
# decode されたプログラムを実行する処理系
# 評価戦略として全ての計算に遅延評価を採用
#

import sys

##
## basic definitions
##

symbols = dict()


class Thunk:
    def __init__(self, v):
        self.v = v


class Lambda:
    def __init__(self, fn):
        self.fn = fn


class App:
    def __init__(self, fn, arg):
        self.fn = fn
        self.arg = arg


class Cons:
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr
    
    def __repr__(self):
        res = []
        res.append('Cons(')
        res.append(str(ev(self.car)))
        res.append(',')
        res.append(str(ev(self.cdr)))
        res.append(')')
        return ''.join(res)


class Nil:
    def __repr__(self):
        return 'Nil'


def ev(v):
    while isinstance(v, Thunk):
        v = v.v()
        if isinstance(v, App):
            v = peel(ev(v.fn))(v.arg)
    return v


def peel(l):
    return l.fn


def apply(fn):
    return lambda arg: Thunk(lambda: App(fn, arg))


##
## primitives
##

# arithmetic
p_add = Lambda(lambda x: Lambda(lambda y: Thunk(lambda: ev(x) + ev(y))))
p_mul = Lambda(lambda x: Lambda(lambda y: Thunk(lambda: ev(x) * ev(y))))
p_div = Lambda(lambda x: Lambda(lambda y: Thunk(lambda: ev(x) // ev(y))))
p_neg = Lambda(lambda x: Thunk(lambda: -ev(x)))

# comparison
p_lt = Lambda(lambda x: Lambda(lambda y: Thunk(lambda: p_t if ev(x) < ev(y) else p_f)))
p_eq = Lambda(lambda x: Lambda(lambda y: Thunk(lambda: p_t if ev(x) == ev(y) else p_f)))

# combinators
p_b = Lambda(lambda x: Lambda(lambda y: Lambda(lambda z: Thunk(lambda: apply(x)(apply(y)(z))))))
p_c = Lambda(lambda x: Lambda(lambda y: Lambda(lambda z: Thunk(lambda: apply(apply(x)(z))(y)))))
p_t = Lambda(lambda x: Lambda(lambda y: Thunk(lambda: x)))
p_f = Lambda(lambda x: Lambda(lambda y: Thunk(lambda: y)))
p_i = Lambda(lambda x: Thunk(lambda: x))
p_s = Lambda(lambda x: Lambda(lambda y: Lambda(lambda z: Thunk(lambda: apply(apply(x)(z))(apply(y)(z))))))

# list
p_cons = Lambda(lambda x: Lambda(lambda xs: Thunk(lambda: Cons(x, xs))))
p_car = Lambda(lambda x: Thunk(lambda: ev(x).car))
p_cdr = Lambda(lambda x: Thunk(lambda: ev(x).cdr))
p_nil = Thunk(lambda: Nil())
p_isnil = Lambda(lambda x: Thunk(lambda: p_t if isinstance(ev(x), Nil) else p_f))


PRIMITIVES = {
    'add': p_add,
    'mul': p_mul,
    'div': p_div,
    'neg': p_neg,

    'lt': p_lt,
    'eq': p_eq,

    'b': p_b,
    'c': p_c,
    't': p_t,
    'f': p_f,
    'i': p_i,
    's': p_s,

    'cons': p_cons,
    'car': p_car,
    'cdr': p_cdr,
    'nil': p_nil,
    'isnil': p_isnil
}

##
## parser
##

def parse(toks):
    def parse_inner(ptr):
        if toks[ptr] == 'ap':
            (fn, ptr) = parse_inner(ptr + 1)
            (arg, ptr) = parse_inner(ptr)
            return (apply(fn)(arg), ptr)
        elif toks[ptr] in PRIMITIVES:
            return (PRIMITIVES[toks[ptr]], ptr + 1)
        elif toks[ptr][0] == '-' or toks[ptr].isdigit():
            return (Thunk(lambda: int(toks[ptr])), ptr + 1)
        else:
            return (Thunk(lambda: symbols[toks[ptr]]), ptr + 1)
    return parse_inner(0)[0]

##
## main
##

def main(filename):
    sys.setrecursionlimit(1000000)
    
    with open(filename) as f:
        for line in f.readlines():
            toks = line.split()
            symbols[toks[0]] = parse(toks[2:])
    print('Successfully parsed')
    
    while True:
        try:
            sym = input()
            print(ev(symbols[sym]))
        except EOFError:
            break

if __name__ == '__main__':
    main(sys.argv[1])
