---


---


# Memory Access Pattern
An individual CUDA thread can access 1,2,4,8,or 16 bytes in a single instruction or transaction. When considered warp-wide, that translates to 32 bytes all the way up to 512 bytes. The GPU memory controller can typically issue requests to memory in granularities of 32 bytes, up to 128 bytes. Larger requests (say, 512 bytes, considered warp wide) will get issued via multiple "transactions" of typically no more than 128 bytes.
## Global Memory
### Aligned and coalesced access
* **Aligned memory accesses**: the first address of device memory is an multiple of 32, 64, or 128 bytes. Performing a misaligned load will cause wasted bandwidth.
* **Coalesced memory accesses**: all 32 threads in a warp access a contiguous chunk of memory.
* **Aligned coalesced memory accesses**
![](https://i.imgur.com/7Y9h2ir.png =70%x)
* **Misaligned uncoalesced memory accesses**
![](https://i.imgur.com/rfndahT.png =70%x)

#### Read

Assuming each thread in a warp read 4-byte element in cache/memory:

|                            |                128-byte granularity    (cached load)                |                 32-byte granularity     (uncached load)                 |
|:--------------------------:|:-------------------------------------------------------------------:|:-----------------------------------------------------------------------:|
|   Aligned and coalesced    |                ![](https://i.imgur.com/9AlMfEG.png)                 |                  ![](https://i.imgur.com/CdandUN.png)                   |
|  Aligned and uncoalesced   |                ![](https://i.imgur.com/HJkNlcg.png)                 |                  ![](https://i.imgur.com/dyzxE9W.png)                   |
|  Misaligned and coalesced  |  ![](https://i.imgur.com/c7uGy5R.png) Bus utilization: 128/256=50%  | ![](https://i.imgur.com/5g2wVQp.png) Bus utilization: 128/(224-64)=80%  |
| Misaligned and uncoalesced | ![](https://i.imgur.com/stJMYLh.png) Bus utilization: 128/384=33.3% | ![](https://i.imgur.com/nftNih7.png) Bus utilization: 128/(32\*6)=66.6% |
|         Broadcast          | ![](https://i.imgur.com/iQBu1VQ.png) Bus utilization: 4/128=3.125%  |     ![](https://i.imgur.com/udQE72y.png) Bus utilization:4/32=12.5%     |

Check the size of the granularity on the L1/L1 cache:
`nvprof --metrics l1_cache_line_size my_gpu_application`
`nvprof --metrics l2_cache_line_size my_gpu_application`

Keep in mind that the size of the granularity on the L1/L2 cache can vary depending on the specific GPU model and architecture. Additionally, the size of the granularity may also be affected by the specific configuration of the GPU and the operating system.
* What is the size of the granularity of global memory?


### Examples

1. Misalignment read/write occurs when `offset` is not a multiple of the size of granuality.

```cuda=
__global__ void readOffset(float *A, float *B, float *C, float *D, const int n) {
    unsigned int i = blockIdx.x * blockDim.x + threadIdx.x;
    int offset, k;
    
    offset = 11;
    k = i + offset;
    if (k < n) C[i] = A[k] + B[k]; // misalignment read
    if (k < n) D[k] = A[i] + B[i]; // misalignment write
    
    offset = 128;
    k = i + offset;
    if (k < n) C[i] = A[k] + B[k]; // alignment read
    if (k < n) D[k] = A[i] + B[i]; // alignment write
}
```

2. Uncoalesce read/write occurs when all 32 threads in a warp do not access a contiguous chunk of memory.
```cuda=
__global__ void readOffset(float *A, float *B, float *C, const int n, int offset) {
    unsigned int i = blockIdx.x * blockDim.x + threadIdx.x;
    unsigned int k = (i%2==0) ? (2*i) : (i);
    if (k < n) C[i] = A[k] + B[k]; // uncoaleased read
    if (k < n) C[k] = A[i] + B[i]; // uncoaleased read
}
```

3. Array copy
```cuda=
#include <stdio.h>

// Kernel that processes an array
__global__ void processArray(float *array, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        // Each thread does some simple operation
        array[idx] = array[idx] * 2.0f;
    }
}

int main() {
    const int numElements = 1024; // Number of elements in the array
    const int elementSize = sizeof(float); // Size of each element
    const int blockSize = 128; // Block size, chosen based on memory transaction size

    // Ensure the array size is a multiple of the memory transaction size for alignment
    const int arraySize = numElements * elementSize;
    const int transactionSize = 128; // Transaction size in bytes, could be 32, 64, or 128
    const int padding = (transactionSize - (arraySize % transactionSize)) % transactionSize;
    const int totalArraySize = arraySize + padding;

    float *d_array;

    // Allocate aligned device memory
    cudaMalloc(&d_array, totalArraySize);

    // Initialize array on host
    float *h_array = new float[numElements + padding / elementSize];
    for (int i = 0; i < numElements; i++) {
        h_array[i] = 1.0f; // Example initialization
    }

    // Copy data to device
    cudaMemcpy(d_array, h_array, arraySize, cudaMemcpyHostToDevice);

    // Configure blocks and grid
    dim3 blocks(blockSize);
    dim3 grid((numElements + blocks.x - 1) / blocks.x);

    // Launch the kernel
    processArray<<<grid, blocks>>>(d_array, numElements);

    // Copy back the results to host
    cudaMemcpy(h_array, d_array, arraySize, cudaMemcpyDeviceToHost);

    // Free memory
    cudaFree(d_array);
    delete[] h_array;

    return 0;
}
```
4. The starting address of device memory is neither a multiple of 32, 64, nor 128 bytes.
```cuda=
#include <cuda_runtime.h>
#include <iostream>

__global__ void processMisalignedArray(float *array, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n) {
        array[idx] = array[idx] * 2.0f;  // Simple operation to demonstrate access
    }
}

int main() {
    const int numElements = 1024;
    const int elementSize = sizeof(float);
    const int misalignmentOffset = 7; // Deliberately misalign by 7 bytes

    char *d_base; // Allocate as char* for byte-wise manipulation
    float *d_misalignedArray;

    // Allocate more memory than needed to ensure we can misalign manually
    cudaMalloc((void**)&d_base, numElements * elementSize + misalignmentOffset);

    // Intentionally create a misaligned float pointer
    d_misalignedArray = reinterpret_cast<float*>(d_base + misalignmentOffset);

    // Initialize array on host
    float *h_array = new float[numElements];
    for (int i = 0; i < numElements; i++) {
        h_array[i] = 1.0f;  // Initialize with some values
    }

    // Copy data to device (to the misaligned address)
    cudaMemcpy(d_misalignedArray, h_array, numElements * elementSize, cudaMemcpyHostToDevice);

    // Configure blocks and grid
    dim3 blocks(256);
    dim3 grid((numElements + blocks.x - 1) / blocks.x);

    // Launch the kernel
    processMisalignedArray<<<grid, blocks>>>(d_misalignedArray, numElements);

    // Copy back the results to host
    cudaMemcpy(h_array, d_misalignedArray, numElements * elementSize, cudaMemcpyDeviceToHost);

    // Output the first few elements for demonstration
    for (int i = 0; i < 10; i++) {
        std::cout << "Element " << i << ": " << h_array[i] << std::endl;
    }

    // Clean up
    cudaFree(d_base);
    delete[] h_array;

    return 0;
}
```

### SoA vs. AoS
#### SoA: structure of array

```cuda=
struct innerStruct {
    float x;
    float y;
};
```


```cuda=
__global__ void testInnerStruct(innerStruct *data,
 	innerStruct *result, const int n) {
 	unsigned int i = blockIdx.x * blockDim.x + threadIdx.x;
 	if (i < n) {
                // read a structure with one thread
 		innerStruct tmp = data[i];
 		tmp.x += 10.f;
 		tmp.y += 20.f;
                // write a structure with one thread
 		result[i] = tmp;
 	}
}
```

The above code shows uncoalesced reading/writing, since `t0` reads at `data[0]`, `t1` reads `data[1]`, but the memory locations of `data[0]` and `data[1]` are not contiguous.

#### AoS: array of structure

```cuda=
struct innerArray {
    float x[N];
    float y[N];
};
```


```cuda=
__global__ void testInnerArray(InnerArray *data, InnerArray *result, const int n) {
	unsigned int i = blockIdx.x * blockDim.x + threadIdx.x;
	if (i<n) {
		float tmpx = data->x[i];
		float tmpy = data->y[i];
		tmpx += 10.f;
		tmpy += 20.f;
		result->x[i] = tmpx;
		result->y[i] = tmpy;
	}
}
```

![image](https://hackmd.io/_uploads/H1f7ukcU6.png)

# Reference
![image](https://hackmd.io/_uploads/BJaIYUZW0.png)

https://www.cs.nthu.edu.tw/~cherung/teaching/2010gpucell/CUDA02.pdf