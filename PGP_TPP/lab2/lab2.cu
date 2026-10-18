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

__device__ float brightness(uchar4 p) {
    return 0.299f * p.x + 0.587f * p.y + 0.114f * p.z;
}

__global__ void sobel(cudaTextureObject_t tex, uchar4 *out, int w, int h) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int idy = blockIdx.y * blockDim.y + threadIdx.y;
    int offsetx = blockDim.x * gridDim.x;
    int offsety = blockDim.y * gridDim.y;

    for (int y = idy; y < h; y += offsety) {
        for (int x = idx; x < w; x += offsetx) {
            float fx = x + 0.5f, fy = y + 0.5f;
            float y11 = brightness(tex2D<uchar4>(tex, fx - 1.0f, fy - 1.0f));
            float y12 = brightness(tex2D<uchar4>(tex, fx,        fy - 1.0f));
            float y13 = brightness(tex2D<uchar4>(tex, fx + 1.0f, fy - 1.0f));
            float y21 = brightness(tex2D<uchar4>(tex, fx - 1.0f, fy));
            float y23 = brightness(tex2D<uchar4>(tex, fx + 1.0f, fy));
            float y31 = brightness(tex2D<uchar4>(tex, fx - 1.0f, fy + 1.0f));
            float y32 = brightness(tex2D<uchar4>(tex, fx,        fy + 1.0f));
            float y33 = brightness(tex2D<uchar4>(tex, fx + 1.0f, fy + 1.0f));

            float gx = (y13 + 2.0f * y23 + y33) - (y11 + 2.0f * y21 + y31);
            float gy = (y31 + 2.0f * y32 + y33) - (y11 + 2.0f * y12 + y13);
            float g = sqrtf(gx * gx + gy * gy);
            if (g > 255.0f) g = 255.0f;

            uchar4 src = tex2D<uchar4>(tex, fx, fy);
            unsigned char v = (unsigned char)g;
            out[y * w + x] = make_uchar4(v, v, v, src.w);
        }
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
    size_t count = (size_t)w * (size_t)h;
    uchar4 *data = (uchar4 *)malloc(sizeof(uchar4) * count);
    if (data == NULL) {
        fprintf(stderr, "ERROR: not enough host memory\n");
        fclose(fp);
        return 0;
    }
    if (fread(data, sizeof(uchar4), count, fp) != count) {
        fprintf(stderr, "ERROR: input file is truncated\n");
        free(data);
        fclose(fp);
        return 0;
    }
    fclose(fp);

    cudaArray *arr = NULL;
    cudaChannelFormatDesc ch = cudaCreateChannelDesc<uchar4>();
    CSC(cudaMallocArray(&arr, &ch, w, h));
    CSC(cudaMemcpy2DToArray(arr, 0, 0, data, w * sizeof(uchar4),
                            w * sizeof(uchar4), h, cudaMemcpyHostToDevice));

    cudaResourceDesc resDesc = {};
    resDesc.resType = cudaResourceTypeArray;
    resDesc.res.array.array = arr;

    cudaTextureDesc texDesc = {};
    texDesc.addressMode[0] = cudaAddressModeClamp;   
    texDesc.addressMode[1] = cudaAddressModeClamp;
    texDesc.filterMode = cudaFilterModePoint;        
    texDesc.readMode = cudaReadModeElementType;
    texDesc.normalizedCoords = 0;                    

    cudaTextureObject_t tex = 0;
    CSC(cudaCreateTextureObject(&tex, &resDesc, &texDesc, NULL));

    uchar4 *dev_out = NULL;
    CSC(cudaMalloc(&dev_out, sizeof(uchar4) * count));

    sobel<<<dim3(16, 16), dim3(32, 32)>>>(tex, dev_out, w, h);
    CSC(cudaGetLastError());
    CSC(cudaDeviceSynchronize());

    CSC(cudaMemcpy(data, dev_out, sizeof(uchar4) * count, cudaMemcpyDeviceToHost));

    CSC(cudaDestroyTextureObject(tex));
    CSC(cudaFreeArray(arr));
    CSC(cudaFree(dev_out));

    fp = fopen(out_path, "wb");
    if (fp == NULL) {
        fprintf(stderr, "ERROR: cannot open output file %s\n", out_path);
        free(data);
        return 0;
    }
    fwrite(&w, sizeof(int), 1, fp);
    fwrite(&h, sizeof(int), 1, fp);
    fwrite(data, sizeof(uchar4), count, fp);
    fclose(fp);

    free(data);
    return 0;
}
