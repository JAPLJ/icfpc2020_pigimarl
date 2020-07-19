class Annotation:
    def __init__(self, val, min_y, max_y, min_x, max_x):
        self.val = val
        self.min_y = min_y
        self.max_y = max_y
        self.min_x = min_x
        self.max_x = max_x


class Bitmap:
    def __init__(self, min_y, max_y, min_x, max_x):
        self.min_y = min_y
        self.max_y = max_y
        self.min_x = min_x
        self.max_x = max_x

        height = max_y - min_y + 1
        width = max_x - min_x + 1
        self.a = [[False for _ in range(width)] for _ in range(height)]

    def get(self, y, x):
        if self.min_y <= y <= self.max_y and self.min_x <= x <= self.max_x:
            return self.a[y - self.min_y][x - self.min_x]
        else:
            return False

    def set(self, y, x, val):
        self.a[y - self.min_y][x - self.min_x] = val


def annotate_picture(vectors):
    if len(vectors) == 0:
        return []

    bitmap = vectors_to_bitmap(vectors)
    annotations = []
    annotations += annotate_numbers(bitmap)

    return annotations


def vectors_to_bitmap(vectors):
    min_x = 10000
    max_x = -10000
    min_y = 10000
    max_y = -10000
    for x, y in vectors:
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    bitmap = Bitmap(min_y, max_y, min_x, max_x)
    for x, y in vectors:
        bitmap.set(y, x, True)

    return bitmap


def annotate_numbers(a):
    annotations = []

    for y in range(a.min_y, a.max_y + 1):
        for x in range(a.min_x, a.max_x + 1):
            # .#
            # #?
            # 左上にこういう構造が必要
            if not (not a.get(y, x) and a.get(y, x + 1) and a.get(y + 1, x)):
                continue

            # 下方向にどれだけ白が続くか
            h = 0
            while a.get(y + h + 1, x):
                h += 1

            # 右方向にどれだけ白が続くか
            w = 0
            while a.get(y, x + w + 1):
                w += 1

            if not 0 <= h - w <= 1:
                continue

            d = w  # 正方形の一辺の長さ

            if not check_isolated(a, y, y + d, x, x + d):
                continue

            num = 0
            for dy in range(d):
                for dx in range(d):
                    if a.get(y + 1 + dy, x + 1 + dx):
                        num += 1 << (dy * d + dx)

            if h - w == 1:
                num *= -1

            annotations.append(Annotation(num, y, y + h, x, x + w))
            erase_rectangle(a, y, y + h, x, x + w)

    return annotations


def erase_rectangle(a, min_y, max_y, min_x, max_x):
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            a.set(y, x, False)


def check_isolated(a, min_y, max_y, min_x, max_x):
    """
    [min_y, max_y] × [min_x, max_x] の小長方形の周り 1 ピクセルがすべて黒であるかチェック。
    :param a:
    :param min_y:
    :param max_y:
    :param min_x:
    :param max_x:
    :return:
    """
    for y in range(min_y - 1, max_y + 2):
        if a.get(y, min_x - 1) or a.get(y, max_x + 1):
            return False
    for x in range(min_x - 1, max_x + 2):
        if a.get(min_y - 1, x) or a.get(max_y + 1, x):
            return False
    return True
