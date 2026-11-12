import numpy as np
from math import comb


def surjections(m, j):
    return sum((-1) ** i * comb(j, i) * (j - i) ** m for i in range(j + 1))


def distinct_digits(n, b=3):
    if n == 0:
        return 1
    seen = 0
    while n:
        seen |= 1 << (n % b)
        n //= b
    return bin(seen).count("1")


def mask_table(k, b=3):
    dtype = np.uint8 if b <= 8 else np.uint16
    masks = np.zeros(1, dtype=dtype)
    bits = (1 << np.arange(b)).astype(dtype)
    for _ in range(k):
        masks[0] = 0
        masks = (masks[:, None] | bits[None, :]).reshape(-1)
    masks[0] = 1
    return masks


def value_table(k, b=3):
    lut = np.array([bin(x).count("1") for x in range(1 << b)], dtype=np.uint8)
    return lut[mask_table(k, b)]


def length_count(m, j, b=3):
    if j < 1 or j > b or j > m:
        return 0
    full = surjections(m, j)
    without_zero = comb(b - 1, j) * full
    with_zero = comb(b - 1, j - 1) * (full - surjections(m - 1, j) - surjections(m - 1, j - 1))
    return without_zero + with_zero


def completions(q, t, r):
    return sum((-1) ** i * comb(t, i) * (q + t - i) ** r for i in range(t + 1))


def to_digits(n, b):
    digits = []
    while n:
        digits.append(n % b)
        n //= b
    return digits[::-1]


def count_exact(limit, j, b=3):
    if limit < 1:
        return 0
    digits = to_digits(limit, b)
    length = len(digits)
    total = sum(length_count(l, j, b) for l in range(1, length))
    prefix = 0
    for i, d in enumerate(digits):
        r = length - i - 1
        for c in range(1 if i == 0 else 0, d):
            q = bin(prefix | (1 << c)).count("1")
            t = j - q
            if 0 <= t <= b - q:
                total += comb(b - q, t) * completions(q, t, r)
        prefix |= 1 << d
    if bin(prefix).count("1") == j:
        total += 1
    return total


def prefix_sum(limit, b=3):
    return sum(j * count_exact(limit, j, b) for j in range(1, b + 1))


def count_missing(limit, d, b=3, powers=None):
    if limit < 1:
        return 0
    digits = to_digits(limit, b)
    length = len(digits)
    if powers is None:
        powers = [1] * (length + 1)
        for i in range(1, length + 1):
            powers[i] = powers[i - 1] * (b - 1)
    if d == 0:
        total = sum(powers[l] for l in range(1, length))
    else:
        total = sum((b - 2) * powers[l - 1] for l in range(1, length))
    blocked = False
    for i, di in enumerate(digits):
        lo = 1 if i == 0 else 0
        allowed = (di - lo) - (1 if lo <= d < di else 0)
        total += allowed * powers[length - i - 1]
        if di == d:
            blocked = True
            break
    if not blocked:
        total += 1
    return total


def prefix_sum_direct(limit, b=3):
    if limit < 1:
        return 0
    length = len(to_digits(limit, b))
    powers = [1] * (length + 1)
    for i in range(1, length + 1):
        powers[i] = powers[i - 1] * (b - 1)
    return sum(limit - count_missing(limit, d, b, powers) for d in range(b))


def sum_below_power(k, b=3):
    if b == 2:
        return 2 ** (k + 1) - 2 - k
    return b * (b ** k - 1) - (b - 1) ** 2 * ((b - 1) ** k - 1) // (b - 2)


def at_most_below_power(k, j, b=3):
    return sum(length_count(m, i, b) for m in range(1, k + 1) for i in range(1, j + 1))


def free_words(q, r, j, b):
    if q > j:
        return 0
    return sum(comb(b - q, t) * completions(q, t, r) for t in range(j - q + 1))


def nth_at_most(index, j, b=3):
    length = 1
    while True:
        block = sum(length_count(length, i, b) for i in range(1, j + 1))
        if index <= block:
            break
        index -= block
        length += 1
    prefix = 0
    value = 0
    for i in range(length):
        r = length - i - 1
        for c in range(1 if i == 0 else 0, b):
            q_set = prefix | (1 << c)
            ways = free_words(bin(q_set).count("1"), r, j, b)
            if index <= ways:
                prefix = q_set
                value = value * b + c
                break
            index -= ways
    return value


MORPHISM = {0: (0, 1, 2), 1: (3, 1, 4), 2: (5, 4, 2), 3: (3, 3, 6), 4: (6, 4, 4), 5: (5, 6, 5), 6: (6, 6, 6)}


def morphism_word(length):
    word = [0]
    while len(word) < length:
        word = [x for s in word for x in MORPHISM[s]]
    return [1 + s // 3 for s in word[:length]]
