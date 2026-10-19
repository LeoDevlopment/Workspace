// ЛР №4, вариант 2. CPU-версия для сравнения с GPU (для отчёта, не для сдачи).
// Тот же алгоритм: Гаусс-Жордан "на месте" с выбором главного элемента по столбцу,
// один поток, матрица хранится по строкам (так цикл по j векторизуется компилятором).
//
// Сборка:  g++ -O2 -o lab4_cpu lab4_cpu.cpp
// Запуск:  ./lab4_cpu [--noout] < matrix.txt
// Результат замера -- одна строка CPUTIME=... в stderr.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <chrono>

#define MAX_N 10000

static double now_ms() {
    using namespace std::chrono;
    return duration<double, std::milli>(steady_clock::now().time_since_epoch()).count();
}

static unsigned char ibuf[1 << 16];
static size_t ipos = 0, ilen = 0;

static int next_char() {
    if (ipos == ilen) {
        ilen = fread(ibuf, 1, sizeof(ibuf), stdin);
        ipos = 0;
        if (ilen == 0) return -1;
    }
    return ibuf[ipos++];
}

static int read_token(char *tok, int cap) {
    int c;
    do { c = next_char(); } while (c == ' ' || c == '\n' || c == '\r' || c == '\t');
    if (c < 0) return 0;
    int len = 0;
    while (c >= 0 && c != ' ' && c != '\n' && c != '\r' && c != '\t') {
        if (len < cap - 1) tok[len++] = (char)c;
        c = next_char();
    }
    tok[len] = '\0';
    return 1;
}

static int read_double(double *x) {
    char tok[128];
    if (!read_token(tok, sizeof(tok))) return 0;
    char *end;
    *x = strtod(tok, &end);
    return *end == '\0';
}

int main(int argc, char **argv) {
    bool noout = false;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--noout")) noout = true;
        else { fprintf(stderr, "ERROR: unknown argument %s\n", argv[i]); return 0; }
    }

    double t0 = now_ms();
    char tok[128];
    char *end;
    if (!read_token(tok, sizeof(tok))) { fprintf(stderr, "ERROR: invalid matrix size\n"); return 0; }
    long long nll = strtoll(tok, &end, 10);
    if (*end != '\0' || nll < 1 || nll > MAX_N) {
        fprintf(stderr, "ERROR: invalid matrix size (must be 1..%d)\n", MAX_N);
        return 0;
    }
    int n = (int)nll;
    double *A = (double *)malloc(sizeof(double) * (size_t)n * n);
    int *piv = (int *)malloc(sizeof(int) * n);
    if (A == NULL || piv == NULL) { fprintf(stderr, "ERROR: not enough host memory\n"); return 0; }
    for (size_t i = 0; i < (size_t)n * n; i++)
        if (!read_double(&A[i])) { fprintf(stderr, "ERROR: cannot read matrix element %zu\n", i); return 0; }
    double read_ms = now_ms() - t0;

    double t1 = now_ms();
    for (int k = 0; k < n; k++) {
        int r = k;
        double best = fabs(A[(size_t)k * n + k]);
        for (int i = k + 1; i < n; i++) {
            double v = fabs(A[(size_t)i * n + k]);
            if (v > best) { best = v; r = i; }
        }
        piv[k] = r;
        if (r != k)
            for (int j = 0; j < n; j++) {
                double t = A[(size_t)k * n + j];
                A[(size_t)k * n + j] = A[(size_t)r * n + j];
                A[(size_t)r * n + j] = t;
            }
        double p = A[(size_t)k * n + k];
        if (p == 0.0) { fprintf(stderr, "ERROR: matrix is singular\n"); return 0; }

        double *rk = A + (size_t)k * n;
        for (int j = 0; j < n; j++) rk[j] /= p;
        rk[k] = 1.0 / p;
        for (int i = 0; i < n; i++) {
            if (i == k) continue;
            double *ri = A + (size_t)i * n;
            double f = ri[k];
            for (int j = 0; j < n; j++) ri[j] -= f * rk[j];
            ri[k] = -f / p;
        }
    }
    for (int k = n - 1; k >= 0; k--) {
        if (piv[k] == k) continue;
        for (int i = 0; i < n; i++) {
            double t = A[(size_t)i * n + k];
            A[(size_t)i * n + k] = A[(size_t)i * n + piv[k]];
            A[(size_t)i * n + piv[k]] = t;
        }
    }
    double compute_ms = now_ms() - t1;

    double write_ms = 0.0;
    if (!noout) {
        double t2 = now_ms();
        static char outbuf[1 << 20];
        setvbuf(stdout, outbuf, _IOFBF, sizeof(outbuf));
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                printf("%.10e%c", A[(size_t)i * n + j], j + 1 < n ? ' ' : '\n');
        fflush(stdout);
        write_ms = now_ms() - t2;
    }

    fprintf(stderr, "CPUTIME= n=%d compute_ms=%.4f read_ms=%.4f write_ms=%.4f\n",
            n, compute_ms, read_ms, write_ms);
    free(A);
    free(piv);
    return 0;
}
