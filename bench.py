import subprocess
import sys
import time

from distinct_digits import distinct_digits, prefix_sum, prefix_sum_direct, value_table


def best(f, *a, r=5):
    t = []
    for _ in range(r):
        s = time.perf_counter()
        f(*a)
        t.append(time.perf_counter() - s)
    return min(t)


print("table: n, loop, numpy table")
for k in (8, 10, 12, 13):
    n = 3 ** k
    print(n, round(best(lambda: [distinct_digits(i) for i in range(n)], r=1), 4), round(best(value_table, k, r=3), 4))
print("numpy table 3^18", round(best(value_table, 18, r=1), 3))
if len(sys.argv) > 1:
    for k in (14, 18):
        print(subprocess.run([sys.argv[1], str(k)], capture_output=True, text=True).stdout.strip())
print("prefix sums: base, N, inclusion-exclusion, direct")
for b in (3, 10):
    for e in (6, 18, 100, 1000):
        N = 10 ** e
        print(b, "10^%d" % e, round(best(prefix_sum, N, b), 6), round(best(prefix_sum_direct, N, b), 6))
print(prefix_sum_direct(10 ** 18), prefix_sum_direct(10 ** 18, 10))
