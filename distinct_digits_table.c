#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

int main(int argc, char **argv)
{
    int k = argc > 1 ? atoi(argv[1]) : 18;
    uint64_t n = 1;
    for (int i = 0; i < k; i++)
        n *= 3;
    uint8_t *a = malloc(n);
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    a[0] = 0;
    uint64_t size = 1;
    for (int level = 0; level < k; level++) {
        for (uint64_t m = size; m-- > 0;) {
            uint8_t v = a[m];
            a[3 * m] = v | 1;
            a[3 * m + 1] = v | 2;
            a[3 * m + 2] = v | 4;
        }
        a[0] = 0;
        size *= 3;
    }
    static const uint8_t pop[8] = {0, 1, 1, 2, 1, 2, 2, 3};
    uint64_t sum = 1;
    for (uint64_t i = 1; i < n; i++) {
        a[i] = pop[a[i]];
        sum += a[i];
    }
    a[0] = 1;
    clock_gettime(CLOCK_MONOTONIC, &t1);
    printf("k=%d n=%llu time=%.3fs sum=%llu\n", k, (unsigned long long)n, (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) * 1e-9, (unsigned long long)sum);
    return 0;
}
