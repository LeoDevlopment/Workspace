// ЛР №4, вариант 2. ПРОФИЛИРУЮЩАЯ версия (для отчёта, не для сдачи).
// Алгоритм тот же, что в lab4.cu, плюс замеры времени через cudaEvent и
// настраиваемая конфигурация запуска двумерного ядра update.
//
// Сборка:  nvcc -arch=sm_75 -O2 -o lab4_prof lab4_prof.cu
// Запуск:  ./lab4_prof [--grid GX GY] [--block BX BY] [--noout] [--detail] < matrix.txt
//   --grid / --block  конфигурация ядра update (по умолчанию 16 16 и 32 32)
//   --noout           не печатать обратную матрицу (замер без вывода)
//   --detail          замер по фазам (поиск максимума, обмен строк, подготовка, update);
//                     добавляет накладные расходы на события на каждом шаге
// Результат замеров -- одна строка TIMING=... в stderr.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <chrono>
#include <thrust/extrema.h>
#include <thrust/device_ptr.h>

#define CSC(call)                                                          \
do {                                                                       \
    cudaError_t res = (call);                                              \
    if (res != cudaSuccess) {                                              \
        fprintf(stderr, "ERROR: CUDA failure in %s:%d. Message: %s\n",     \
                __FILE__, __LINE__, cudaGetErrorString(res));              \
        exit(0);                                                           \
    }                                                                      \
} while (0)

#define MAX_N 10000
#define CHUNK 64

const int GRID1 = 256, BLOCK1 = 256;

struct abs_less {
    __host__ __device__ bool operator()(double a, double b) const {
        return fabs(a) < fabs(b);
    }
};

__global__ void swap_rows(double *A, int n, int r1, int r2) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int offset = blockDim.x * gridDim.x;
    for (int j = idx; j < n; j += offset) {
        double t = A[(long long)j * n + r1];
        A[(long long)j * n + r1] = A[(long long)j * n + r2];
        A[(long long)j * n + r2] = t;
    }
}

__global__ void swap_cols(double *A, int n, int c1, int c2) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int offset = blockDim.x * gridDim.x;
    for (int i = idx; i < n; i += offset) {
        double t = A[(long long)c1 * n + i];
        A[(long long)c1 * n + i] = A[(long long)c2 * n + i];
        A[(long long)c2 * n + i] = t;
    }
}

__global__ void prepare(const double *A, double *col, double *row, int n, int k, double p) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int offset = blockDim.x * gridDim.x;
    for (int t = idx; t < n; t += offset) {
        col[t] = A[(long long)k * n + t];
        row[t] = A[(long long)t * n + k] / p;
    }
}

__global__ void update(double *A, const double *col, const double *row, int n, int k, double p) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int idy = blockIdx.y * blockDim.y + threadIdx.y;
    int offsetx = blockDim.x * gridDim.x;
    int offsety = blockDim.y * gridDim.y;
    for (int j = idy; j < n; j += offsety) {
        double rj = row[j];
        for (int i = idx; i < n; i += offsetx) {
            long long pos = (long long)j * n + i;
            if (i == k && j == k)  A[pos] = 1.0 / p;
            else if (i == k)       A[pos] = rj;
            else if (j == k)       A[pos] = -col[i] / p;
            else                   A[pos] -= col[i] * rj;
        }
    }
}

// ---- секундомер на cudaEvent ----------------------------------------------
struct Stopwatch { cudaEvent_t a, b; };

static void sw_init(Stopwatch *s) {
    CSC(cudaEventCreate(&s->a));
    CSC(cudaEventCreate(&s->b));
}
static void sw_start(Stopwatch *s) { CSC(cudaEventRecord(s->a, 0)); }
static double sw_stop(Stopwatch *s) {
    CSC(cudaEventRecord(s->b, 0));
    CSC(cudaEventSynchronize(s->b));
    float ms = 0.0f;
    CSC(cudaEventElapsedTime(&ms, s->a, s->b));
    return (double)ms;
}

static double now_ms() {
    using namespace std::chrono;
    return duration<double, std::milli>(steady_clock::now().time_since_epoch()).count();
}

// ---- быстрый ввод ----------------------------------------------------------
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

static int read_int(long long *x) {
    char tok[128];
    if (!read_token(tok, sizeof(tok))) return 0;
    char *end;
    *x = strtoll(tok, &end, 10);
    return *end == '\0';
}

int main(int argc, char **argv) {
    int gx = 16, gy = 16, bx = 32, by = 32;
    bool noout = false, detail = false;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--grid") && i + 2 < argc) {
            gx = atoi(argv[i + 1]); gy = atoi(argv[i + 2]); i += 2;
        } else if (!strcmp(argv[i], "--block") && i + 2 < argc) {
            bx = atoi(argv[i + 1]); by = atoi(argv[i + 2]); i += 2;
        } else if (!strcmp(argv[i], "--noout")) {
            noout = true;
        } else if (!strcmp(argv[i], "--detail")) {
            detail = true;
        } else {
            fprintf(stderr, "ERROR: unknown or incomplete argument %s\n", argv[i]);
            return 0;
        }
    }
    if (gx < 1 || gy < 1 || bx < 1 || by < 1 || bx * by > 1024) {
        fprintf(stderr, "ERROR: invalid launch configuration\n");
        return 0;
    }
    dim3 grid2(gx, gy), block2(bx, by);

    CSC(cudaFree(0));   // инициализация контекста CUDA вне замеров

    double t_start = now_ms();

    long long nll;
    if (!read_int(&nll) || nll < 1 || nll > MAX_N) {
        fprintf(stderr, "ERROR: invalid matrix size (must be 1..%d)\n", MAX_N);
        return 0;
    }
    int n = (int)nll;
    size_t total = (size_t)n * (size_t)n;

    double *h = (double *)malloc(sizeof(double) * total);
    double *buf = (double *)malloc(sizeof(double) * (size_t)CHUNK * n);
    if (h == NULL || buf == NULL) {
        fprintf(stderr, "ERROR: not enough host memory\n");
        return 0;
    }
    for (int i0 = 0; i0 < n; i0 += CHUNK) {
        int rows = (n - i0 < CHUNK) ? (n - i0) : CHUNK;
        for (int r = 0; r < rows; r++)
            for (int j = 0; j < n; j++)
                if (!read_double(&buf[(size_t)r * n + j])) {
                    fprintf(stderr, "ERROR: cannot read matrix element (%d, %d)\n", i0 + r, j);
                    return 0;
                }
        for (int j = 0; j < n; j++)
            for (int r = 0; r < rows; r++)
                h[(size_t)j * n + i0 + r] = buf[(size_t)r * n + j];
    }
    double read_ms = now_ms() - t_start;

    double *dev_A = NULL, *dev_col = NULL, *dev_row = NULL;
    CSC(cudaMalloc(&dev_A, sizeof(double) * total));
    CSC(cudaMalloc(&dev_col, sizeof(double) * n));
    CSC(cudaMalloc(&dev_row, sizeof(double) * n));
    int *piv = (int *)malloc(sizeof(int) * n);

    Stopwatch sw_total, sw_h2d, sw_gauss, sw_d2h, sw_step;
    sw_init(&sw_total); sw_init(&sw_h2d); sw_init(&sw_gauss);
    sw_init(&sw_d2h); sw_init(&sw_step);
    double t_pivot = 0, t_swap = 0, t_prep = 0, t_update = 0;

    sw_start(&sw_total);

    sw_start(&sw_h2d);
    CSC(cudaMemcpy(dev_A, h, sizeof(double) * total, cudaMemcpyHostToDevice));
    double h2d_ms = sw_stop(&sw_h2d);

    sw_start(&sw_gauss);
    for (int k = 0; k < n; k++) {
        if (detail) sw_start(&sw_step);
        thrust::device_ptr<double> first = thrust::device_pointer_cast(dev_A + (size_t)k * n + k);
        thrust::device_ptr<double> last = thrust::device_pointer_cast(dev_A + (size_t)k * n + n);
        thrust::device_ptr<double> it = thrust::max_element(first, last, abs_less());
        int r = k + (int)(it - first);
        piv[k] = r;
        if (detail) t_pivot += sw_stop(&sw_step);

        if (r != k) {
            if (detail) sw_start(&sw_step);
            swap_rows<<<GRID1, BLOCK1>>>(dev_A, n, k, r);
            CSC(cudaGetLastError());
            if (detail) t_swap += sw_stop(&sw_step);
        }

        double p;
        CSC(cudaMemcpy(&p, dev_A + (size_t)k * n + k, sizeof(double), cudaMemcpyDeviceToHost));
        if (p == 0.0) {
            fprintf(stderr, "ERROR: matrix is singular\n");
            return 0;
        }

        if (detail) sw_start(&sw_step);
        prepare<<<GRID1, BLOCK1>>>(dev_A, dev_col, dev_row, n, k, p);
        CSC(cudaGetLastError());
        if (detail) t_prep += sw_stop(&sw_step);

        if (detail) sw_start(&sw_step);
        update<<<grid2, block2>>>(dev_A, dev_col, dev_row, n, k, p);
        CSC(cudaGetLastError());
        if (detail) t_update += sw_stop(&sw_step);
    }
    for (int k = n - 1; k >= 0; k--) {
        if (piv[k] != k) {
            swap_cols<<<GRID1, BLOCK1>>>(dev_A, n, k, piv[k]);
            CSC(cudaGetLastError());
        }
    }
    double gauss_ms = sw_stop(&sw_gauss);

    sw_start(&sw_d2h);
    CSC(cudaMemcpy(h, dev_A, sizeof(double) * total, cudaMemcpyDeviceToHost));
    double d2h_ms = sw_stop(&sw_d2h);

    double gpu_total_ms = sw_stop(&sw_total);

    CSC(cudaFree(dev_A));
    CSC(cudaFree(dev_col));
    CSC(cudaFree(dev_row));

    double write_ms = 0.0;
    if (!noout) {
        double t_w = now_ms();
        static char outbuf[1 << 20];
        setvbuf(stdout, outbuf, _IOFBF, sizeof(outbuf));
        for (int i0 = 0; i0 < n; i0 += CHUNK) {
            int rows = (n - i0 < CHUNK) ? (n - i0) : CHUNK;
            for (int j = 0; j < n; j++)
                for (int r = 0; r < rows; r++)
                    buf[(size_t)r * n + j] = h[(size_t)j * n + i0 + r];
            for (int r = 0; r < rows; r++)
                for (int j = 0; j < n; j++)
                    printf("%.10e%c", buf[(size_t)r * n + j], j + 1 < n ? ' ' : '\n');
        }
        fflush(stdout);
        write_ms = now_ms() - t_w;
    }

    fprintf(stderr,
            "TIMING= n=%d gx=%d gy=%d bx=%d by=%d h2d_ms=%.4f gauss_ms=%.4f d2h_ms=%.4f "
            "gpu_total_ms=%.4f pivot_ms=%.4f swap_ms=%.4f prep_ms=%.4f update_ms=%.4f "
            "read_ms=%.4f write_ms=%.4f\n",
            n, gx, gy, bx, by, h2d_ms, gauss_ms, d2h_ms, gpu_total_ms,
            t_pivot, t_swap, t_prep, t_update, read_ms, write_ms);

    free(h);
    free(buf);
    free(piv);
    return 0;
}
