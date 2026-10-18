// ЛР №3, вариант 4. Классификация изображений методом спектрального угла (CUDA).
// Сборка: nvcc -Werror cross-execution-space-call -lm -o lab3 lab3.cu
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define CSC(call)                                                          \
do {                                                                       \
    cudaError_t res = (call);                                              \
    if (res != cudaSuccess) {                                              \
        fprintf(stderr, "ERROR: CUDA failure in %s:%d. Message: %s\n",     \
                __FILE__, __LINE__, cudaGetErrorString(res));              \
        exit(0);                                                           \
    }                                                                      \
} while (0)

#define MAX_CLASSES 32

// Нормированные векторы средних avg_j / |avg_j| для всех классов.
// Лежат в константной памяти: все потоки читают одни и те же данные.
__constant__ double c_unit[MAX_CLASSES][3];

// Один поток обрабатывает пиксели с шагом, равным общему числу потоков (1D-сетка).
// Класс пикселя p: jc = argmax_j ( p^T * avg_j / |avg_j| ).
// Сравнение строгое (>), классы перебираются по возрастанию номера,
// поэтому при равенстве выбирается класс с наименьшим номером.
// Номер класса записывается в альфа-канал; обработка идёт "на месте".
__global__ void classify(uchar4 *img, long long n, int nc) {
    long long idx = (long long)blockIdx.x * blockDim.x + threadIdx.x;
    long long offset = (long long)blockDim.x * gridDim.x;
    while (idx < n) {
        uchar4 p = img[idx];
        int best = 0;
        double best_val = 0.0;
        for (int j = 0; j < nc; j++) {
            double val = p.x * c_unit[j][0] + p.y * c_unit[j][1] + p.z * c_unit[j][2];
            if (j == 0 || val > best_val) {
                best_val = val;
                best = j;
            }
        }
        p.w = (unsigned char)best;
        img[idx] = p;
        idx += offset;
    }
}

int main() {
    char in_path[4096], out_path[4096];
    if (scanf("%4095s %4095s", in_path, out_path) != 2) {
        fprintf(stderr, "ERROR: cannot read file paths\n");
        return 0;
    }

    FILE *fp = fopen(in_path, "rb");
    if (fp == NULL) {
        fprintf(stderr, "ERROR: cannot open input file %s\n", in_path);
        return 0;
    }
    int w, h;
    if (fread(&w, sizeof(int), 1, fp) != 1 || fread(&h, sizeof(int), 1, fp) != 1 ||
        w <= 0 || h <= 0) {
        fprintf(stderr, "ERROR: invalid image header\n");
        fclose(fp);
        return 0;
    }
    long long count = (long long)w * (long long)h;
    uchar4 *data = (uchar4 *)malloc(sizeof(uchar4) * (size_t)count);
    if (data == NULL) {
        fprintf(stderr, "ERROR: not enough host memory\n");
        fclose(fp);
        return 0;
    }
    if (fread(data, sizeof(uchar4), (size_t)count, fp) != (size_t)count) {
        fprintf(stderr, "ERROR: input file is truncated\n");
        free(data);
        fclose(fp);
        return 0;
    }
    fclose(fp);

    int nc;
    if (scanf("%d", &nc) != 1 || nc < 1 || nc > MAX_CLASSES) {
        fprintf(stderr, "ERROR: invalid number of classes (must be 1..%d)\n", MAX_CLASSES);
        free(data);
        return 0;
    }

    // Оценка вектора средних для каждого класса: avg_j = (1/np_j) * sum(ps_i^j).
    // Суммы целочисленные (точные), деление выполняется один раз.
    double unit[MAX_CLASSES][3];
    for (int j = 0; j < nc; j++) {
        long long np;
        if (scanf("%lld", &np) != 1 || np < 1) {
            fprintf(stderr, "ERROR: invalid sample size for class %d\n", j);
            free(data);
            return 0;
        }
        long long sum[3] = {0, 0, 0};
        for (long long i = 0; i < np; i++) {
            int x, y;
            if (scanf("%d %d", &x, &y) != 2) {
                fprintf(stderr, "ERROR: cannot read sample coordinates of class %d\n", j);
                free(data);
                return 0;
            }
            if (x < 0 || x >= w || y < 0 || y >= h) {
                fprintf(stderr, "ERROR: sample pixel (%d, %d) of class %d is outside the image\n",
                        x, y, j);
                free(data);
                return 0;
            }
            uchar4 p = data[(long long)y * w + x];   // x -- столбец, y -- строка
            sum[0] += p.x;
            sum[1] += p.y;
            sum[2] += p.z;
        }
        double avg[3] = {(double)sum[0] / (double)np,
                         (double)sum[1] / (double)np,
                         (double)sum[2] / (double)np};
        double len = sqrt(avg[0] * avg[0] + avg[1] * avg[1] + avg[2] * avg[2]);
        for (int k = 0; k < 3; k++)
            unit[j][k] = (len > 0.0) ? avg[k] / len : 0.0;   // нулевой вектор -> оценка 0
    }

    CSC(cudaMemcpyToSymbol(c_unit, unit, sizeof(unit)));

    uchar4 *dev_img = NULL;
    CSC(cudaMalloc(&dev_img, sizeof(uchar4) * (size_t)count));
    CSC(cudaMemcpy(dev_img, data, sizeof(uchar4) * (size_t)count, cudaMemcpyHostToDevice));

    classify<<<256, 256>>>(dev_img, count, nc);
    CSC(cudaGetLastError());
    CSC(cudaDeviceSynchronize());

    CSC(cudaMemcpy(data, dev_img, sizeof(uchar4) * (size_t)count, cudaMemcpyDeviceToHost));
    CSC(cudaFree(dev_img));

    fp = fopen(out_path, "wb");
    if (fp == NULL) {
        fprintf(stderr, "ERROR: cannot open output file %s\n", out_path);
        free(data);
        return 0;
    }
    fwrite(&w, sizeof(int), 1, fp);
    fwrite(&h, sizeof(int), 1, fp);
    fwrite(data, sizeof(uchar4), (size_t)count, fp);
    fclose(fp);

    free(data);
    return 0;
}
