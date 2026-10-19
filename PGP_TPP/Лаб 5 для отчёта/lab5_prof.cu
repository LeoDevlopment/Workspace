// ЛР №5, вариант 2. ПРОФИЛИРУЮЩАЯ версия (для отчёта, не для сдачи).
// Алгоритм тот же, что в lab5.cu, плюс замеры по фазам через cudaEvent и
// настраиваемые конфигурации запуска.
//
// Сборка:  nvcc -arch=sm_75 -O2 -o lab5_prof lab5_prof.cu
// Запуск:  ./lab5_prof [--noout] [--stream-grid G] [--stream-block B] [--scan-grid G] < data.bin
//   --noout          не выводить отсортированный массив
//   --stream-grid/-block  конфигурация ядер histogram, add_offsets, write_sorted (1024 и 256)
//   --scan-grid      число блоков ядра scan_blocks (256); потоков в блоке 512 (константа)
// Результат замеров -- одна строка TIMING=... в stderr.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <chrono>

#define CSC(call)                                                          \
do {                                                                       \
    cudaError_t res = (call);                                              \
    if (res != cudaSuccess) {                                              \
        fprintf(stderr, "ERROR: CUDA failure in %s:%d. Message: %s\n",     \
                __FILE__, __LINE__, cudaGetErrorString(res));              \
        exit(0);                                                           \
    }                                                                      \
} while (0)

#ifndef RANGE_BITS
#define RANGE_BITS 24
#endif
#define RANGE (1 << RANGE_BITS)

#ifndef SCAN_BLOCK
#define SCAN_BLOCK 512
#endif
#ifndef CHUNK
#define CHUNK 64
#endif
#define ELEMS (2 * SCAN_BLOCK)
#define LOG_NUM_BANKS 5
#define CFO(x) ((x) >> LOG_NUM_BANKS)

// Конфигурации запуска (меняются из командной строки).
static int g_stream_grid = 1024, g_stream_block = 256, g_scan_grid = 256;

__global__ void histogram(const int *a, int *hist, int n) {
    long long idx = (long long)blockIdx.x * blockDim.x + threadIdx.x;
    long long offset = (long long)blockDim.x * gridDim.x;
    for (long long i = idx; i < n; i += offset)
        atomicAdd(&hist[a[i]], 1);
}

__global__ void scan_blocks(int *data, int *sums, int len, int nblocks) {
    __shared__ int temp[ELEMS + (ELEMS >> LOG_NUM_BANKS)];
    int tid = threadIdx.x;
    for (int b = blockIdx.x; b < nblocks; b += gridDim.x) {
        long long base = (long long)b * ELEMS;
        int ai = tid, bi = tid + SCAN_BLOCK;
        int offA = CFO(ai), offB = CFO(bi);
        temp[ai + offA] = (base + ai < len) ? data[base + ai] : 0;
        temp[bi + offB] = (base + bi < len) ? data[base + bi] : 0;
        int offset = 1;
        for (int d = ELEMS >> 1; d > 0; d >>= 1) {
            __syncthreads();
            if (tid < d) {
                int i = offset * (2 * tid + 1) - 1;
                int j = offset * (2 * tid + 2) - 1;
                i += CFO(i);
                j += CFO(j);
                temp[j] += temp[i];
            }
            offset <<= 1;
        }
        if (tid == 0) {
            int last = (ELEMS - 1) + CFO(ELEMS - 1);
            sums[b] = temp[last];
            temp[last] = 0;
        }
        for (int d = 1; d < ELEMS; d <<= 1) {
            offset >>= 1;
            __syncthreads();
            if (tid < d) {
                int i = offset * (2 * tid + 1) - 1;
                int j = offset * (2 * tid + 2) - 1;
                i += CFO(i);
                j += CFO(j);
                int t = temp[i];
                temp[i] = temp[j];
                temp[j] += t;
            }
        }
        __syncthreads();
        if (base + ai < len) data[base + ai] = temp[ai + offA];
        if (base + bi < len) data[base + bi] = temp[bi + offB];
        __syncthreads();
    }
}

__global__ void add_offsets(int *data, const int *sums, int len) {
    long long idx = (long long)blockIdx.x * blockDim.x + threadIdx.x;
    long long offset = (long long)blockDim.x * gridDim.x;
    for (long long i = idx; i < len; i += offset)
        data[i] += sums[i / ELEMS];
}

static void scan(int *dev, int len) {
    int nblocks = (len + ELEMS - 1) / ELEMS;
    int *sums = NULL;
    CSC(cudaMalloc(&sums, sizeof(int) * nblocks));
    scan_blocks<<<g_scan_grid, SCAN_BLOCK>>>(dev, sums, len, nblocks);
    CSC(cudaGetLastError());
    if (nblocks > 1) {
        scan(sums, nblocks);
        add_offsets<<<g_stream_grid, g_stream_block>>>(dev, sums, len);
        CSC(cudaGetLastError());
    }
    CSC(cudaFree(sums));
}

__global__ void write_sorted(int *out, const int *ex, int n) {
    long long idx = (long long)blockIdx.x * blockDim.x + threadIdx.x;
    long long offset = (long long)blockDim.x * gridDim.x;
    long long nchunks = ((long long)n + CHUNK - 1) / CHUNK;
    for (long long c = idx; c < nchunks; c += offset) {
        long long s = c * CHUNK;
        long long e = s + CHUNK;
        if (e > n) e = n;
        int lo = 0, hi = RANGE - 1;
        while (lo < hi) {
            int mid = (lo + hi + 1) >> 1;
            if (ex[mid] <= s) lo = mid; else hi = mid - 1;
        }
        int v = lo;
        int next = (v + 1 < RANGE) ? ex[v + 1] : INT_MAX;
        for (long long pos = s; pos < e; pos++) {
            while (next <= pos) {
                v++;
                next = (v + 1 < RANGE) ? ex[v + 1] : INT_MAX;
            }
            out[pos] = v;
        }
    }
}

// ---- секундомер на cudaEvent -----------------------------------------------
struct Stopwatch { cudaEvent_t a, b; };
static void sw_init(Stopwatch *s) { CSC(cudaEventCreate(&s->a)); CSC(cudaEventCreate(&s->b)); }
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

int main(int argc, char **argv) {
    bool noout = false;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--noout")) noout = true;
        else if (!strcmp(argv[i], "--stream-grid") && i + 1 < argc) g_stream_grid = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--stream-block") && i + 1 < argc) g_stream_block = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--scan-grid") && i + 1 < argc) g_scan_grid = atoi(argv[++i]);
        else { fprintf(stderr, "ERROR: unknown or incomplete argument %s\n", argv[i]); return 0; }
    }
    if (g_stream_grid < 1 || g_scan_grid < 1 || g_stream_block < 1 || g_stream_block > 1024) {
        fprintf(stderr, "ERROR: invalid launch configuration\n");
        return 0;
    }

    CSC(cudaFree(0));   // инициализация контекста вне замеров

    double t0 = now_ms();
    int n;
    if (fread(&n, sizeof(int), 1, stdin) != 1 || n < 0) {
        fprintf(stderr, "ERROR: invalid array length\n");
        return 0;
    }
    if (n == 0) return 0;
    size_t bytes = sizeof(int) * (size_t)n;
    int *h = (int *)malloc(bytes);
    if (h == NULL) { fprintf(stderr, "ERROR: not enough host memory\n"); return 0; }
    if (fread(h, sizeof(int), (size_t)n, stdin) != (size_t)n) {
        fprintf(stderr, "ERROR: input is shorter than the declared length\n");
        return 0;
    }
    for (int i = 0; i < n; i++)
        if (h[i] < 0 || h[i] >= RANGE) {
            fprintf(stderr, "ERROR: element %d = %d is outside [0, %d]\n", i, h[i], RANGE - 1);
            return 0;
        }
    double read_ms = now_ms() - t0;

    int *dev_data = NULL, *dev_hist = NULL;
    CSC(cudaMalloc(&dev_data, bytes));
    CSC(cudaMalloc(&dev_hist, sizeof(int) * (size_t)RANGE));

    Stopwatch sw_total, sw_h2d, sw_hist, sw_scan, sw_write, sw_d2h;
    sw_init(&sw_total); sw_init(&sw_h2d); sw_init(&sw_hist);
    sw_init(&sw_scan); sw_init(&sw_write); sw_init(&sw_d2h);

    sw_start(&sw_total);

    sw_start(&sw_h2d);
    CSC(cudaMemcpy(dev_data, h, bytes, cudaMemcpyHostToDevice));
    CSC(cudaMemset(dev_hist, 0, sizeof(int) * (size_t)RANGE));
    double h2d_ms = sw_stop(&sw_h2d);

    sw_start(&sw_hist);
    histogram<<<g_stream_grid, g_stream_block>>>(dev_data, dev_hist, n);
    CSC(cudaGetLastError());
    double hist_ms = sw_stop(&sw_hist);

    sw_start(&sw_scan);
    scan(dev_hist, RANGE);
    double scan_ms = sw_stop(&sw_scan);

    sw_start(&sw_write);
    write_sorted<<<g_stream_grid, g_stream_block>>>(dev_data, dev_hist, n);
    CSC(cudaGetLastError());
    double write_ms = sw_stop(&sw_write);

    sw_start(&sw_d2h);
    CSC(cudaMemcpy(h, dev_data, bytes, cudaMemcpyDeviceToHost));
    double d2h_ms = sw_stop(&sw_d2h);

    double gpu_total_ms = sw_stop(&sw_total);

    CSC(cudaFree(dev_data));
    CSC(cudaFree(dev_hist));

    double out_ms = 0.0;
    if (!noout) {
        double t1 = now_ms();
        fwrite(h, sizeof(int), (size_t)n, stdout);
        fflush(stdout);
        out_ms = now_ms() - t1;
    }

    fprintf(stderr,
            "TIMING= n=%d stream_grid=%d stream_block=%d scan_grid=%d h2d_ms=%.4f hist_ms=%.4f "
            "scan_ms=%.4f write_ms=%.4f d2h_ms=%.4f gpu_total_ms=%.4f read_ms=%.4f out_ms=%.4f\n",
            n, g_stream_grid, g_stream_block, g_scan_grid, h2d_ms, hist_ms, scan_ms, write_ms,
            d2h_ms, gpu_total_ms, read_ms, out_ms);
    free(h);
    return 0;
}
