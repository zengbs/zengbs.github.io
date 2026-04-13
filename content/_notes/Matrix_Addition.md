---


---

# Original Version

```c=
__global__ void MatrixAddition(unsigned short *input, unsigned short *mean, int n, int m) {
    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    int idy = threadIdx.y + blockIdx.y * blockDim.y;
    int index = idy * m + idx;
 
    if (idx < m && idy < m) {
        int sum = 0;
        for (int i = 0; i < n; i++) {
            sum += input[i * m * m + index];
        }   
        mean[index] = sum;
    }   
}
```

# Optimized Versions

```c=
#define ELEMENTS_PER_THREAD_2 2

__global__ void MatrixAdditionOptimized2(unsigned short *input, unsigned short *mean, int n, int m) {

    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    int idy = threadIdx.y + blockIdx.y * blockDim.y;
    int index = idy * m + idx;
    unsigned int *input2 = (unsigned int*)input;


    if ( index % ELEMENTS_PER_THREAD_2 == 0 && index < m*m ){

        unsigned int sum[ELEMENTS_PER_THREAD_2] = {0};

        for (int i = 0; i < n; i++) {

           unsigned long fourInt = input2[(i * m * m + index)/ELEMENTS_PER_THREAD_2];

           unsigned short a = ( fourInt & 0x0000ffff ) >>  0;
           unsigned short b = ( fourInt & 0xffff0000 ) >> 16;

           sum[0] += a;
           sum[1] += b;
        }

        mean[index+0] = sum[0];
        mean[index+1] = sum[1];
    }
}
```


```c=
#define ELEMENTS_PER_THREAD_4 4

__global__ void MatrixAdditionOptimized4(unsigned short *input, unsigned short *mean, int n, int m) {

    int idx = threadIdx.x + blockIdx.x * blockDim.x;
    int idy = threadIdx.y + blockIdx.y * blockDim.y;
    int index = idy * m + idx;
    unsigned long *input4 = (unsigned long*)input;


    if ( index % ELEMENTS_PER_THREAD_4 == 0 && index < m*m ){

        unsigned int sum[ELEMENTS_PER_THREAD_4] = {0};

        for (int i = 0; i < n; i++) {

           unsigned long fourInt = input4[(i * m * m + index)/ELEMENTS_PER_THREAD_4];

           unsigned short a = ( fourInt & 0x000000000000ffff ) >>  0;
           unsigned short b = ( fourInt & 0x00000000ffff0000 ) >> 16;
           unsigned short c = ( fourInt & 0x0000ffff00000000 ) >> 32;
           unsigned short d = ( fourInt & 0xffff000000000000 ) >> 48;

           sum[0] += a;
           sum[1] += b;
           sum[2] += c;
           sum[3] += d;
        }

        mean[index+0] = sum[0];
        mean[index+1] = sum[1];
        mean[index+2] = sum[2];
        mean[index+3] = sum[3];
    }
}
```



![image](https://hackmd.io/_uploads/ByrWr1QTp.png)

![image](https://hackmd.io/_uploads/r1xzdkX6a.png)

![image](https://hackmd.io/_uploads/rJkuIbmT6.png)

![image](https://hackmd.io/_uploads/HygKjG7aa.png)


Version 1 operates on unsigned short values, which are 16 bits each. The GPU's memory subsystem is optimized for accessing wider chunks of data (e.g., 32-bit, 64-bit, or even larger blocks) at a time. When threads access 16-bit values, the potential for coalescing is reduced compared to accessing 32-bit or 64-bit values directly, as fewer values can be fetched in a single memory transaction


Note that the right shift will be arithmetic when the left operand is signed integer. In this case, we can mask out the heading bits to convert arithmetic shift to logical shift. See [here](https://stackoverflow.com/questions/17893901/perform-logical-shift-using-arithmetic-shift-operator-in-c).

# `main` function
```c=
int main() {

    int N = 200; // Number of matrices
    int M = 256; // Size of each matrix (MxM)
    size_t size = N * M * M * sizeof(unsigned short);

    // Allocate host memory
    unsigned short *h_input = (unsigned short *)malloc(size);
    unsigned short *h_mean1 = (unsigned short *)malloc(M * M * sizeof(unsigned short));
    unsigned short *h_mean2 = (unsigned short *)malloc(M * M * sizeof(unsigned short));
    unsigned short *h_mean3 = (unsigned short *)malloc(M * M * sizeof(unsigned short));
    unsigned short *h_mean4 = (unsigned short *)malloc(M * M * sizeof(unsigned short));

    // Initialize input matrices (example)
    for (int i = 0; i < N * M * M; i++) {
        h_input[i] = i;
    }

    // Allocate device memory
    unsigned short *d_input, *d_mean;
    cudaMalloc(&d_input, size);
    cudaMalloc(&d_mean, M * M * sizeof(unsigned short));

    // Copy matrices from host to device
    cudaMemcpy(d_input, h_input, size, cudaMemcpyHostToDevice);

    // Define block and grid sizes
    dim3 blockSize(16, 16);
    dim3 gridSize((M + blockSize.x - 1) / blockSize.x, (M + blockSize.y - 1) / blockSize.y);

    dim3 gridSize2((M/2 + blockSize.x - 1) / blockSize.x, (M + blockSize.y - 1) / blockSize.y);

    dim3 gridSize4((M/4 + blockSize.x - 1) / blockSize.x, (M + blockSize.y - 1) / blockSize.y);




    MatrixAddition<<<gridSize, blockSize>>>(d_input, d_mean, N, M);
    cudaMemcpy(h_mean1, d_mean, M * M * sizeof(unsigned short), cudaMemcpyDeviceToHost);


    // Case 2:
    Start();
    MatrixAdditionCPU(h_input, h_mean2, N, M);
    Stop();
    printf("CPU: %e\n", GetValue());



    // Copy the mean matrix back to host
    MatrixAdditionOptimized4<<<gridSize4, blockSize>>>(d_input, d_mean, N, M);
    cudaMemcpy(h_mean3, d_mean, M * M * sizeof(unsigned short), cudaMemcpyDeviceToHost);

    MatrixAdditionOptimized2<<<gridSize2, blockSize>>>(d_input, d_mean, N, M);
    cudaMemcpy(h_mean4, d_mean, M * M * sizeof(unsigned short), cudaMemcpyDeviceToHost);



    if( isTwoMatrixEqual(h_mean4, h_mean1, M)){
       printf("Success!\n");
    }else{
       printf("Fail!\n");
    }


    // Free device memory
    cudaFree(d_input);
    cudaFree(d_mean);

    // Free host memory
    free(h_input);
    free(h_mean1);
    free(h_mean2);

    return 0;
}
```