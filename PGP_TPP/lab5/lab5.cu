// ЛР №5, вариант 2. Сортировка подсчётом для int из диапазона [0, 2^24 - 1] (CUDA).
// Гистограмма на атомарных операциях + сканирование Блеллока любого размера
// с рекурсией и бесконфликтным использованием разделяемой памяти.
// Сборка: nvcc -Werror cross-execution-space-call -lm -o lab5 lab5.cu
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

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
#define RANGE (1 << RANGE_BITS)  // значения лежат в [0, RANGE - 1], RANGE = 2^24

// ----- параметры запуска (фиксированы, не зависят от размера данных) --------
#ifndef SCAN_BLOCK
#define SCAN_BLOCK 512           // потоков в блоке сканирования
#endif
#ifndef SCAN_GRID
#define SCAN_GRID 256            // блоков в сетке сканирования
#endif
#ifndef STREAM_BLOCK
#define STREAM_BLOCK 256
#endif
#ifndef STREAM_GRID
#define STREAM_GRID 1024
#endif
#ifndef CHUNK
#define CHUNK 64                 // длина участка выхода, обрабатываемого одним потоком
#endif

#define ELEMS (2 * SCAN_BLOCK)   // элементов, сканируемых одним блоком
#define LOG_NUM_BANKS 5          // 32 банка разделяемой памяти
// Смещение для устранения конфликтов банков: после каждых 32 элементов
// вставляется один пропуск, обращения вида 2^k * (2t+1) - 1 расходятся по банкам.
#define CFO(x) ((x) >> LOG_NUM_BANKS)

// ----------------------------------------------------------------------------
// Гистограмма: hist[a[i]]++ на атомарных операциях.
// ----------------------------------------------------------------------------
__global__ void histogram(const int *a, int *hist, int n) {
    long long idx = (long long)blockIdx.x * blockDim.x + threadIdx.x;
    long long offset = (long long)blockDim.x * gridDim.x;
    for (long long i = idx; i < n; i += offset)
        atomicAdd(&hist[a[i]], 1);
}

// ----------------------------------------------------------------------------
// Исключающее сканирование Блеллока внутри блока из ELEMS элементов.
// Суммы блоков записываются в sums[]. Блоки обходятся циклом с шагом gridDim.x,
// поэтому число блоков в сетке фиксировано.
// ----------------------------------------------------------------------------
__global__ void scan_blocks(int *data, int *sums, int len, int nblocks) {
    __shared__ int temp[ELEMS + (ELEMS >> LOG_NUM_BANKS)];
    int tid = threadIdx.x;

    for (int b = blockIdx.x; b < nblocks; b += gridDim.x) {
        long long base = (long long)b * ELEMS;
        int ai = tid, bi = tid + SCAN_BLOCK;
        int offA = CFO(ai), offB = CFO(bi);

        temp[ai + offA] = (base + ai < len) ? data[base + ai] : 0;
        temp[bi + offB] = (base + bi < len) ? data[base + bi] : 0;

        // Восходящий проход (свёртка).
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

        // Сумма блока -> sums[b], последний элемент обнуляется.
        if (tid == 0) {
            int last = (ELEMS - 1) + CFO(ELEMS - 1);
            sums[b] = temp[last];
            temp[last] = 0;
        }

        // Нисходящий проход.
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
        __syncthreads();   // temp будет использован следующим блоком
    }
}

// Добавление просканированных сумм блоков ко всем элементам своих блоков.
__global__ void add_offsets(int *data, const int *sums, int len) {
    long long idx = (long long)blockIdx.x * blockDim.x + threadIdx.x;
    long long offset = (long long)blockDim.x * gridDim.x;
    for (long long i = idx; i < len; i += offset)
        data[i] += sums[i / ELEMS];
}

// Сканирование массива любого размера, рекурсивно:
// 1) сканируем блоки, 2) рекурсивно сканируем их суммы, 3) добавляем смещения.
static void scan(int *dev, int len) {
    int nblocks = (len + ELEMS - 1) / ELEMS;
    int *sums = NULL;
    CSC(cudaMalloc(&sums, sizeof(int) * nblocks));
    scan_blocks<<<SCAN_GRID, SCAN_BLOCK>>>(dev, sums, len, nblocks);
    CSC(cudaGetLastError());
    if (nblocks > 1) {
        scan(sums, nblocks);
        add_offsets<<<STREAM_GRID, STREAM_BLOCK>>>(dev, sums, len);
        CSC(cudaGetLastError());
    }
    CSC(cudaFree(sums));
}

// ----------------------------------------------------------------------------
// Запись отсортированного массива по просканированной гистограмме.
// ex[v] -- число элементов, меньших v (исключающее сканирование гистограммы),
// значит элемент выхода с номером pos равен наибольшему v, для которого ex[v] <= pos.
// Выход разбит на участки по CHUNK элементов: поток бинарным поиском находит
// значение для начала участка и дальше идёт по значениям вперёд. Работа делится
// поровну по выходным позициям, поэтому перекоса нагрузки нет даже если
// почти все числа одинаковы.
// ----------------------------------------------------------------------------
__global__ void write_sorted(int *out, const int *ex, int n) {
    long long idx = (long long)blockIdx.x * blockDim.x + threadIdx.x;
    long long offset = (long long)blockDim.x * gridDim.x;
    long long nchunks = ((long long)n + CHUNK - 1) / CHUNK;

    for (long long c = idx; c < nchunks; c += offset) {
        long long s = c * CHUNK;
        long long e = s + CHUNK;
        if (e > n) e = n;

        int lo = 0, hi = RANGE - 1;                 // наибольшее v: ex[v] <= s
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

int main() {
    int n;
    if (fread(&n, sizeof(int), 1, stdin) != 1) {
        fprintf(stderr, "ERROR: cannot read array length\n");
        return 0;
    }
    if (n < 0) {
        fprintf(stderr, "ERROR: negative array length %d\n", n);
        return 0;
    }
    if (n == 0) return 0;

    size_t bytes = sizeof(int) * (size_t)n;
    int *h = (int *)malloc(bytes);
    if (h == NULL) {
        fprintf(stderr, "ERROR: not enough host memory\n");
        return 0;
    }
    if (fread(h, sizeof(int), (size_t)n, stdin) != (size_t)n) {
        fprintf(stderr, "ERROR: input is shorter than the declared length\n");
        free(h);
        return 0;
    }
    for (int i = 0; i < n; i++) {
        if (h[i] < 0 || h[i] >= RANGE) {
            fprintf(stderr, "ERROR: element %d = %d is outside [0, %d]\n", i, h[i], RANGE - 1);
            free(h);
            return 0;
        }
    }

    int *dev_data = NULL, *dev_hist = NULL;
    CSC(cudaMalloc(&dev_data, bytes));
    CSC(cudaMalloc(&dev_hist, sizeof(int) * (size_t)RANGE));
    CSC(cudaMemcpy(dev_data, h, bytes, cudaMemcpyHostToDevice));
    CSC(cudaMemset(dev_hist, 0, sizeof(int) * (size_t)RANGE));

    histogram<<<STREAM_GRID, STREAM_BLOCK>>>(dev_data, dev_hist, n);
    CSC(cudaGetLastError());

    scan(dev_hist, RANGE);

    // Исходные данные больше не нужны: результат пишется в тот же буфер.
    write_sorted<<<STREAM_GRID, STREAM_BLOCK>>>(dev_data, dev_hist, n);
    CSC(cudaGetLastError());
    CSC(cudaDeviceSynchronize());

    CSC(cudaMemcpy(h, dev_data, bytes, cudaMemcpyDeviceToHost));
    CSC(cudaFree(dev_data));
    CSC(cudaFree(dev_hist));

    fwrite(h, sizeof(int), (size_t)n, stdout);
    fflush(stdout);

    free(h);
    return 0;
}
