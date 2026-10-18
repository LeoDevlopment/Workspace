// ЛР №4, вариант 2. Вычисление обратной матрицы методом Гаусса-Жордана
// с выбором главного элемента по столбцу (CUDA + Thrust только для поиска максимума).
// Сборка: nvcc -Werror cross-execution-space-call -lm -o lab4 lab4.cu
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
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

#define MAX_N 10000     // n <= 10^4
#define CHUNK 64        // число строк, обрабатываемых за раз при вводе/выводе

// Конфигурации запуска фиксированы и не зависят от размера матрицы.
const int  GRID1 = 256, BLOCK1 = 256;                // одномерные ядра
const dim3 GRID2(16, 16), BLOCK2(32, 32);            // двумерное ядро

// Компаратор для Thrust: сравнение по модулю.
struct abs_less {
    __host__ __device__ bool operator()(double a, double b) const {
        return fabs(a) < fabs(b);
    }
};

// ---------------------------------------------------------------------------
// Матрица хранится по столбцам: элемент (i, j) -- A[j * n + i].
// Столбец лежит в памяти подряд, поэтому поиск главного элемента по столбцу
// (Thrust) идёт по непрерывному участку, а потоки с соседними номерами по x
// обращаются к соседним адресам (объединение запросов к глобальной памяти).
// ---------------------------------------------------------------------------

// Обмен строк r1 и r2 во всех столбцах.
__global__ void swap_rows(double *A, int n, int r1, int r2) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int offset = blockDim.x * gridDim.x;
    for (int j = idx; j < n; j += offset) {
        double t = A[(long long)j * n + r1];
        A[(long long)j * n + r1] = A[(long long)j * n + r2];
        A[(long long)j * n + r2] = t;
    }
}

// Обмен столбцов c1 и c2 (столбцы непрерывны в памяти).
__global__ void swap_cols(double *A, int n, int c1, int c2) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int offset = blockDim.x * gridDim.x;
    for (int i = idx; i < n; i += offset) {
        double t = A[(long long)c1 * n + i];
        A[(long long)c1 * n + i] = A[(long long)c2 * n + i];
        A[(long long)c2 * n + i] = t;
    }
}

// Копия ведущего столбца k и ведущей строки k (делённой на ведущий элемент).
// Копии нужны, чтобы основное ядро не читало то, что само же перезаписывает.
__global__ void prepare(const double *A, double *col, double *row, int n, int k, double p) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int offset = blockDim.x * gridDim.x;
    for (int t = idx; t < n; t += offset) {
        col[t] = A[(long long)k * n + t];        // A[t][k]
        row[t] = A[(long long)t * n + k] / p;    // A[k][t] / p
    }
}

// Один шаг Гаусса-Жордана "на месте" (обратная матрица замещает исходную):
//   A[k][k]  = 1 / p
//   A[k][j]  = A[k][j] / p                      (j != k)
//   A[i][k]  = -A[i][k] / p                     (i != k)
//   A[i][j] -= A[i][k] * A[k][j] / p            (i != k, j != k)
// Двумерная сетка: x -- строки (соседние адреса), y -- столбцы.
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

// ---------------------------------------------------------------------------
// Быстрый ввод: чтение блоками и разбор токенов (scanf слишком медленный
// для 10^8 чисел).
// ---------------------------------------------------------------------------
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

int main() {
    long long nll;
    if (!read_int(&nll) || nll < 1 || nll > MAX_N) {
        fprintf(stderr, "ERROR: invalid matrix size (must be 1..%d)\n", MAX_N);
        return 0;
    }
    int n = (int)nll;
    size_t total = (size_t)n * (size_t)n;

    double *h = (double *)malloc(sizeof(double) * total);        // по столбцам
    double *buf = (double *)malloc(sizeof(double) * (size_t)CHUNK * n);
    if (h == NULL || buf == NULL) {
        fprintf(stderr, "ERROR: not enough host memory\n");
        free(h); free(buf);
        return 0;
    }

    // Чтение по строкам блоками по CHUNK строк, запись в хранение по столбцам.
    for (int i0 = 0; i0 < n; i0 += CHUNK) {
        int rows = (n - i0 < CHUNK) ? (n - i0) : CHUNK;
        for (int r = 0; r < rows; r++)
            for (int j = 0; j < n; j++)
                if (!read_double(&buf[(size_t)r * n + j])) {
                    fprintf(stderr, "ERROR: cannot read matrix element (%d, %d)\n", i0 + r, j);
                    free(h); free(buf);
                    return 0;
                }
        for (int j = 0; j < n; j++)
            for (int r = 0; r < rows; r++)
                h[(size_t)j * n + i0 + r] = buf[(size_t)r * n + j];
    }

    double *dev_A = NULL, *dev_col = NULL, *dev_row = NULL;
    CSC(cudaMalloc(&dev_A, sizeof(double) * total));
    CSC(cudaMalloc(&dev_col, sizeof(double) * n));
    CSC(cudaMalloc(&dev_row, sizeof(double) * n));
    CSC(cudaMemcpy(dev_A, h, sizeof(double) * total, cudaMemcpyHostToDevice));

    int *piv = (int *)malloc(sizeof(int) * n);
    if (piv == NULL) {
        fprintf(stderr, "ERROR: not enough host memory\n");
        return 0;
    }

    for (int k = 0; k < n; k++) {
        // Главный элемент по столбцу k среди строк k..n-1 (Thrust).
        thrust::device_ptr<double> first = thrust::device_pointer_cast(dev_A + (size_t)k * n + k);
        thrust::device_ptr<double> last = thrust::device_pointer_cast(dev_A + (size_t)k * n + n);
        thrust::device_ptr<double> it = thrust::max_element(first, last, abs_less());
        int r = k + (int)(it - first);
        piv[k] = r;

        if (r != k) {
            swap_rows<<<GRID1, BLOCK1>>>(dev_A, n, k, r);
            CSC(cudaGetLastError());
        }

        double p;
        CSC(cudaMemcpy(&p, dev_A + (size_t)k * n + k, sizeof(double), cudaMemcpyDeviceToHost));
        if (p == 0.0) {
            fprintf(stderr, "ERROR: matrix is singular\n");
            CSC(cudaFree(dev_A)); CSC(cudaFree(dev_col)); CSC(cudaFree(dev_row));
            free(h); free(buf); free(piv);
            return 0;
        }

        prepare<<<GRID1, BLOCK1>>>(dev_A, dev_col, dev_row, n, k, p);
        CSC(cudaGetLastError());
        update<<<GRID2, BLOCK2>>>(dev_A, dev_col, dev_row, n, k, p);
        CSC(cudaGetLastError());
    }

    // Перестановки строк на шагах прямого хода превращаются в перестановки
    // столбцов результата; применяются в обратном порядке.
    for (int k = n - 1; k >= 0; k--) {
        if (piv[k] != k) {
            swap_cols<<<GRID1, BLOCK1>>>(dev_A, n, k, piv[k]);
            CSC(cudaGetLastError());
        }
    }
    CSC(cudaDeviceSynchronize());

    CSC(cudaMemcpy(h, dev_A, sizeof(double) * total, cudaMemcpyDeviceToHost));
    CSC(cudaFree(dev_A));
    CSC(cudaFree(dev_col));
    CSC(cudaFree(dev_row));

    // Вывод по строкам, блоками по CHUNK строк (чтение по столбцам блоками).
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

    free(h);
    free(buf);
    free(piv);
    return 0;
}
