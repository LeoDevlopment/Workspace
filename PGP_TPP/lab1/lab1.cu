#include <stdio.h>
#include <stdlib.h>

#define CSC(call)                                                          \
do {                                                                       \
    cudaError_t res = (call);                                              \
    if (res != cudaSuccess) {                                              \
        fprintf(stderr, "ERROR: CUDA failure in %s:%d. Message: %s\n",     \
                __FILE__, __LINE__, cudaGetErrorString(res));              \
        exit(0);                                                           \
    }                                                                      \
} while (0)

__global__ void kernel(const double *a, const double *b, double *res, long long n) {
    long long idx = (long long)blockIdx.x * blockDim.x + threadIdx.x;
    long long offset = (long long)blockDim.x * gridDim.x;
    while (idx < n) {
        res[idx] = a[idx] - b[idx];
        idx += offset;
    }
}

int main() {
    long long n;
    if (scanf("%lld", &n) != 1) {
        fprintf(stderr, "ERROR: cannot read vector size n\n");
        return 0;
    }
    if (n < 0 || n >= (1LL << 25)) {
        fprintf(stderr, "ERROR: n must satisfy 0 <= n < 2^25, got %lld\n", n);
        return 0;
    }
    if (n == 0) {
        printf("\n");
        return 0;
    }

    size_t bytes = sizeof(double) * (size_t)n;
    double *a = (double *)malloc(bytes);
    double *b = (double *)malloc(bytes);
    if (a == NULL || b == NULL) {
        fprintf(stderr, "ERROR: not enough host memory\n");
        free(a);
        free(b);
        return 0;
    }

    for (long long i = 0; i < n; i++) {
        if (scanf("%lf", &a[i]) != 1) {
            fprintf(stderr, "ERROR: cannot read element %lld of the first vector\n", i);
            free(a); free(b);
            return 0;
        }
    }
    for (long long i = 0; i < n; i++) {
        if (scanf("%lf", &b[i]) != 1) {
            fprintf(stderr, "ERROR: cannot read element %lld of the second vector\n", i);
            free(a); free(b);
            return 0;
        }
    }

    double *dev_a = NULL, *dev_b = NULL, *dev_res = NULL;
    CSC(cudaMalloc(&dev_a, bytes));
    CSC(cudaMalloc(&dev_b, bytes));
    CSC(cudaMalloc(&dev_res, bytes));
    CSC(cudaMemcpy(dev_a, a, bytes, cudaMemcpyHostToDevice));
    CSC(cudaMemcpy(dev_b, b, bytes, cudaMemcpyHostToDevice));

    kernel<<<256, 256>>>(dev_a, dev_b, dev_res, n);
    CSC(cudaGetLastError());
    CSC(cudaDeviceSynchronize());

    CSC(cudaMemcpy(a, dev_res, bytes, cudaMemcpyDeviceToHost));

    CSC(cudaFree(dev_a));
    CSC(cudaFree(dev_b));
    CSC(cudaFree(dev_res));

    for (long long i = 0; i < n; i++)
        printf("%.10e%c", a[i], i + 1 < n ? ' ' : '\n');

    free(a);
    free(b);
    return 0;
}
