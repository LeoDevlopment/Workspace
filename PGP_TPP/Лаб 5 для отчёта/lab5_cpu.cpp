// ЛР №5, вариант 2. CPU-версия для сравнения с GPU (для отчёта, не для сдачи).
// Замеряет два алгоритма на одном ядре процессора:
//   std::sort            -- обычная сортировка из стандартной библиотеки;
//   сортировка подсчётом -- тот же алгоритм, что на GPU (гистограмма, префиксные суммы, запись).
// Результаты обоих сравниваются между собой.
//
// Сборка:  g++ -O2 -o lab5_cpu lab5_cpu.cpp
// Запуск:  ./lab5_cpu [--noout] < data.bin
// Результат замера -- одна строка CPUTIME=... в stderr.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <algorithm>
#include <vector>
#include <chrono>

#ifndef RANGE_BITS
#define RANGE_BITS 24
#endif
#define RANGE (1 << RANGE_BITS)

static double now_ms() {
    using namespace std::chrono;
    return duration<double, std::milli>(steady_clock::now().time_since_epoch()).count();
}

int main(int argc, char **argv) {
    bool noout = false;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--noout")) noout = true;
        else { fprintf(stderr, "ERROR: unknown argument %s\n", argv[i]); return 0; }
    }

    double t0 = now_ms();
    int n;
    if (fread(&n, sizeof(int), 1, stdin) != 1 || n < 0) {
        fprintf(stderr, "ERROR: invalid array length\n");
        return 0;
    }
    if (n == 0) return 0;
    std::vector<int> a(n);
    if (fread(a.data(), sizeof(int), (size_t)n, stdin) != (size_t)n) {
        fprintf(stderr, "ERROR: input is shorter than the declared length\n");
        return 0;
    }
    for (int i = 0; i < n; i++)
        if (a[i] < 0 || a[i] >= RANGE) {
            fprintf(stderr, "ERROR: element %d = %d is outside [0, %d]\n", i, a[i], RANGE - 1);
            return 0;
        }
    double read_ms = now_ms() - t0;

    // 1. std::sort
    std::vector<int> s(a);
    double t1 = now_ms();
    std::sort(s.begin(), s.end());
    double std_sort_ms = now_ms() - t1;

    // 2. Сортировка подсчётом
    std::vector<int> c(a.size());
    double t2 = now_ms();
    std::vector<int> cnt(RANGE, 0);
    for (int i = 0; i < n; i++) cnt[a[i]]++;
    size_t pos = 0;
    for (int v = 0; v < RANGE; v++)
        for (int k = cnt[v]; k > 0; k--) c[pos++] = v;
    double count_sort_ms = now_ms() - t2;

    int same = (s == c) ? 1 : 0;

    double out_ms = 0.0;
    if (!noout) {
        double t3 = now_ms();
        fwrite(s.data(), sizeof(int), (size_t)n, stdout);
        fflush(stdout);
        out_ms = now_ms() - t3;
    }
    fprintf(stderr, "CPUTIME= n=%d std_sort_ms=%.4f count_sort_ms=%.4f same=%d read_ms=%.4f out_ms=%.4f\n",
            n, std_sort_ms, count_sort_ms, same, read_ms, out_ms);
    return 0;
}
