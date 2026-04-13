---


---



# Warp Reduction
- See [Warp Shuffles](/Lr3-m6jiReydZjZPlQjsaQ).
# Block Reduction
## Interleaved Pairs with Warp Divergence

![image](https://hackmd.io/_uploads/HytTWeyd6.png)

1. Each iteration suffers warp divergence.
2. Access non-contiguous global memory.

```c=
__global__ void ReduceNeighbored( int *g_array, int *g_output, int arrayLength ){
    
   int tid = blockIdx.x*blockDim.x + threadIdx.x;
    
   if (tid >= arrayLength) return;
    
   int *idata = g_array + blockIdx.x*blockDim.x;
    
   for ( int offset = 1; offset < blockDim.x; offset *= 2 ){
    
      if (threadIdx.x % ( 2*offset ) == 0){
         idata[threadIdx.x] += idata[threadIdx.x+offset];
      }
      __syncthreads();
   }
    
   if (threadIdx.x == 0) g_output[blockIdx.x] = g_array[blockIdx.x*blockDim.x];   
}
```

## Interleaved Pairs with Non-coalesced Access

![image](https://hackmd.io/_uploads/rJtKy-yOT.png)
1. Warp divergence only occurs in the last five rounds when the number of active threads is less than a warp size.
2. Access non-contiguous global memory.

```c=
__global__ void ReduceNeighboredLess( int *g_array, int *g_output, int arrayLength ){
 
   int tid = blockIdx.x*blockDim.x + threadIdx.x;
 
   if (tid >= arrayLength) return;
 
   int *idata = g_array + blockIdx.x*blockDim.x;
 
   for ( int offset = 1; offset < blockDim.x; offset *= 2 ){
 
      if ( threadIdx.x < blockDim.x/2/offset ){
         idata[threadIdx.x*offset*2] += idata[threadIdx.x*offset*2 + offset];
      }
      __syncthreads();
   }
 
   if (threadIdx.x == 0) g_output[blockIdx.x] = g_array[blockIdx.x*blockDim.x];
 
}
```

## Interleaved Pairs with Coalesced Access

![image](https://hackmd.io/_uploads/Hkv1Kmg_6.png)

1. Warp divergence only occurs in the last five rounds when the number of active threads is less than a warp size.
2. Access contiguous global memory.

```c=
__global__ void ReduceInterleaved( int *g_array, int *g_output, int arrayLength ){
 
   int tid = blockIdx.x*blockDim.x + threadIdx.x;
 
   if (tid >= arrayLength) return;
 
   int *idata = g_array + blockIdx.x*blockDim.x;
 
   for ( int offset = blockDim.x/2; offset > 0; offset /= 2 ){
 
      if (threadIdx.x < offset){
         idata[threadIdx.x] += idata[threadIdx.x+offset];
      }
      __syncthreads();
   }
 
   if (threadIdx.x == 0) g_output[blockIdx.x] = g_array[blockIdx.x*blockDim.x];
}
```



## Unrolling with Two Blocks

![image](https://hackmd.io/_uploads/H1EEtmlOT.png)


```c=
__global__ void ReduceUnrolling2( int *g_array, int *g_output, int arrayLength ){
 
   int *idata = g_array + 2*blockIdx.x*blockDim.x;
 
   if ( threadIdx.x + blockDim.x < arrayLength ){
      int a0 = idata[threadIdx.x           ];
      int a1 = idata[threadIdx.x+blockDim.x];
      idata[threadIdx.x] = a0 + a1;
   }
 
   __syncthreads();
 
   for ( int offset = blockDim.x/2; offset > 0; offset /= 2 ){
 
      if (threadIdx.x < offset){
         idata[threadIdx.x] += idata[threadIdx.x+offset];
      }
      __syncthreads();
   }
 
   if (threadIdx.x == 0) g_output[blockIdx.x] = idata[0];
}
```

## Unrolling with Three Blocks

![image](https://hackmd.io/_uploads/BJ2rYXe_a.png)


```c=
__global__ void ReduceUnrolling3( int *g_array, int *g_output, int arrayLength ){                         
 
   int *idata = g_array + 3*blockIdx.x*blockDim.x;
 
   if ( threadIdx.x + 2*blockDim.x < arrayLength ){
      int a0 = idata[threadIdx.x             ];
      int a1 = idata[threadIdx.x+  blockDim.x];
      int a2 = idata[threadIdx.x+2*blockDim.x];
      idata[threadIdx.x] = a0 + a1 + a2;
   }
 
   __syncthreads();
 
 
   for ( int offset = blockDim.x/2; offset > 0; offset /= 2 ){
 
      if (threadIdx.x < offset){
         idata[threadIdx.x] += idata[threadIdx.x+offset];
      }
 
      __syncthreads();
   }
 
   if (threadIdx.x == 0) g_output[blockIdx.x] = idata[0];
}
```
## Block Reduction with Warp Shuffle
See [Block Reduction with Warp Shuffle](https://hackmd.io/Lr3-m6jiReydZjZPlQjsaQ#Block-Reduction-with-Warp-Shuffle).

# Grid Reduction
```c=
__device__ unsigned int count = 0;
__shared__ bool isLastBlockDone;
__global__ void sum(const float* array, unsigned int N,
                    volatile float* result)
{
    // Each block sums a subset of the input array.
    float partialSum = calculatePartialSum(array, N);

    if (threadIdx.x == 0) {

        // Thread 0 of each block stores the partial sum
        // to global memory. The compiler will use
        // a store operation that bypasses the L1 cache
        // since the "result" variable is declared as
        // volatile. This ensures that the threads of
        // the last block will read the correct partial
        // sums computed by all other blocks.
        result[blockIdx.x] = partialSum;

        // Thread 0 makes sure that the incrementation
        // of the "count" variable is only performed after
        // the partial sum has been written to global memory.
        __threadfence();

        // Thread 0 signals that it is done.
        unsigned int value = atomicInc(&count, gridDim.x);

        // Thread 0 determines if its block is the last
        // block to be done.
        isLastBlockDone = (value == (gridDim.x - 1));
    }

    // Synchronize to make sure that each thread reads
    // the correct value of isLastBlockDone.
    __syncthreads();

    if (isLastBlockDone) {

        // The last block sums the partial sums
        // stored in result[0 .. gridDim.x-1]
        float totalSum = calculateTotalSum(result);

        if (threadIdx.x == 0) {

            // Thread 0 of last block stores the total sum
            // to global memory and resets the count
            // varialble, so that the next kernel call
            // works properly.
            result[0] = totalSum;
            count = 0;
        }
    }
}
```

# Reference
[Optimizing Parallel Reduction in CUDA](https://developer.download.nvidia.com/assets/cuda/files/reduction.pdf)
[Memory Fence Function](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html?highlight=__syncthreads#memory-fence-functions)