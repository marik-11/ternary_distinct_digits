import random
from math import log

from distinct_digits import (at_most_below_power, count_exact, count_missing, distinct_digits, length_count, morphism_word,
                             nth_at_most, prefix_sum, prefix_sum_direct, sum_below_power, value_table)

def digit_set(n, b):
    s = set()
    while n:
        s.add(n % b)
        n //= b
    return s


oeis = [1, 1, 2, 1, 2, 2, 2, 1, 2, 2, 3, 2, 1, 2, 3, 2, 2, 2, 3, 2, 3, 2, 2, 2, 2, 1, 2, 2, 3, 2, 2, 3, 3, 3, 3, 2, 2, 3, 2, 1, 2, 3, 2, 2, 3, 3, 3, 3, 2, 2, 3, 2, 2, 2, 3, 2, 3, 3, 3, 2, 3, 2, 3, 3, 3, 3, 2, 2, 3, 2, 2, 2, 3, 2, 3, 2, 2, 2, 2, 1, 2, 2, 3, 2, 2, 3, 3, 3, 3, 2]
assert [distinct_digits(n) for n in range(1, 91)] == oeis
assert list(value_table(5)[1:91]) == oeis
table = value_table(10)
assert all(int(table[n]) == distinct_digits(n) for n in range(3 ** 10))
assert morphism_word(3 ** 6) == [distinct_digits(n) for n in range(3 ** 6)]
for b in range(2, 8):
    t = value_table(5 if b < 5 else 4, b)
    assert all(int(t[n]) == distinct_digits(n, b) for n in range(len(t)))
    for m in range(1, 8):
        cnt = [0] * (b + 1)
        for n in range(b ** (m - 1), b ** m):
            cnt[distinct_digits(n, b)] += 1
        assert [length_count(m, j, b) for j in range(1, b + 1)] == cnt[1:], (b, m)
    for k in range(1, 7):
        assert prefix_sum(b ** k - 1, b) == sum_below_power(k, b), (b, k)
        for j in range(1, b + 1):
            assert sum(count_exact(b ** k - 1, i, b) for i in range(1, j + 1)) == at_most_below_power(k, j, b)
    random.seed(b)
    for n in [random.randint(1, 20000) for _ in range(25)]:
        assert prefix_sum_direct(n, b) == sum(distinct_digits(m, b) for m in range(1, n + 1)), (b, n)
        assert [count_missing(n, d, b) for d in range(b)] == [sum(1 for m in range(1, n + 1) if d not in digit_set(m, b)) for d in range(b)], (b, n)
        cnt = [0] * (b + 1)
        for m in range(1, n + 1):
            cnt[distinct_digits(m, b)] += 1
        assert [count_exact(n, j, b) for j in range(1, b + 1)] == cnt[1:], (b, n)
    for j in range(1, b):
        low = [n for n in range(1, 30000) if distinct_digits(n, b) <= j]
        assert [nth_at_most(i, j, b) for i in range(1, len(low) + 1)] == low, (b, j)
for b in (3, 10, 16, 37):
    for e in (50, 200, 1000):
        assert prefix_sum_direct(10 ** e, b) == prefix_sum(10 ** e, b)
sigma = log(2) / log(3)
for x in [random.randint(10, 10 ** 12) for _ in range(200)]:
    e = count_exact(x, 1) + count_exact(x, 2)
    assert 2 * x ** sigma - 2 * log(x, 3) - 4 <= e <= 8 * x ** sigma
print("ok")
