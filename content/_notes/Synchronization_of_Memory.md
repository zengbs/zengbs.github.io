---
title: Synchronization of Memory


---

* GPUs typically implement a weak or relaxed memory [consistency model](https://en.wikipedia.org/wiki/Consistency_model). In such a model, there is less guarantee about the order in which memory operations (reads and writes) by one thread are observed by other threads (including the calling thread). This means that without explicit synchronization, different threads may see shared/global memory updates in different orders.
*  If you are only dealing with registers within a single thread and not interacting with shared or global memory, then you typically don't need to use a memory fence. This is because the operations within a single thread are executed in order, and the values in the registers are not accessible to other threads.

# Explicit Barrier
`__syncthreads()` waits until all threads in the thread block have reached this point and all global and shared memory accesses made by these threads prior to `__syncthreads()` are visible to all threads in the block.

# Memory Fence
* Memory fence functions ensure that
    1. Any memory write before the fence is visible to other threads after the fence.
    2. All the read operations issued before the fence are completed before any read operations that come after it are executed.
* **Block level fence**
    * API: `__threadfence_block()`
    * **If writes to shared and global memory by "a single" thread have occurred**, `__threadfence_block` ensures that the writes are visible to "other threads" in the same block before proceeding. However, this does not guarantee that all threads in the block have completed their writes to shared/global memory before the fence. This means if threads are executing at different rates, some might reach the fence and proceed to read memory that other threads have not yet written to, potentially leading to a race condition.
 

* **Grid level fence**
    * Same as block-level memory fence, but extend to grid level.
    * API: `__threadfence()`
* **System level fence (host+device)**
    * Same as block-level memory fence, but extend to system level. i.e., global memory, page-locked host memory, and the memory of other devices.
    * API: `__threadfence_system()`


# Example 1
   * The code below could lead to race condition. If a thread (say `t0`) in the second half of the block starts executing `B[idx] = A[(BLOCK_SIZE-1) - idx];` before another thread in the first half has executed its write to `A[idx]`, the `t0` thread might read an initial value in `A[]`.
```c=
#define BLOCK_SIZE 512

__global__ void swap (int* A, int* B)
{  
  unsigned int idx = threadIdx.x + blockDim.x * blockIdx.x;
   
  // Reaplce "A[idx] = ( idx < BLOCK_SIZE/2 ) ? 1 : 2" by the line below to avoid warp divergence
  A[idx] = (idx-(idx%(BLOCK_SIZE/2))) / (BLOCK_SIZE/2) + 1;
   
  __threadfence_block();
   
  B[idx] = A[(BLOCK_SIZE-1) - idx];
} 
```
# Example 2
1. thread 1 executes `writeXY()`, while thread 2 executes `readXY()`.
```c=
__device__ int X = 1, Y = 2;

__device__ void writeXY()
{
    X = 10;
    Y = 20;
}

__device__ void readXY()
{
    int B = Y;
    int A = X;
}
```

There are 24 possible memory access orderings.



| Column 1 |    Access ordering*    | Number of combinations |    Results |
|:--------:|:-----------:| ---------------------- | --- |
|  Case 1  | A<X</br>B<Y | 6$\displaystyle=\frac{4!}{2!2!}$                      |   X=10</br>Y=20</br>A=1</br>B=2  |
|  Case 2  | X<A</br>B<Y | 6                      |    X=10</br>Y=20</br>A=10</br>B=2 |
|  Case 3  | A<X</br>Y<B | 6                      |    X=10</br>Y=20</br>A=1</br>B=20 |
|  Case 4  | X<A</br>Y<B | 6                      |    X=10</br>Y=20</br>A=10</br>B=20 |

\* A<X represents the thread 2 write `A` first, and then the thread 1 write `X`.

If we add memory fence as shown as below, we can only remove the case 3 but not also the case 1 since memory fence take effect only when initial writings have occurred.
```c=
__device__ int X = 1, Y = 2;

__device__ void writeXY()
{
    X = 10;
    __threadfence();
    Y = 20;
}

__device__ void readXY()
{
    int B = Y;
    __threadfence(); // why we need this line?
    int A = X;
}
```
* The `__threadfence()` in `writeXY()` ensures that the write to the global variable `X` is visible to all threads in the grid before the same thread proceeds to write the global variable `Y`.
* The `__threadfence()` in `readXY()` ensures that the read of `X` in `readXY()` sees the **most recent value** written to global memory by any thread, including the thread executing `writeXY()`.

# Example 3

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
* The key issue here is that when the thread 0 has executed the line `result[blockIdx.x] = partialSum` and going to move on to the next line, it typically means that the thread has just issued the command to write `partialSum` into memory. The write command would be placed in a queue to be executed by the memory subsystem. The thread itself does not wait for the write to physically complete in memory.



# Discussion
`__syncthreads()` would merely synchronise threads in the current block only, without enforcing the global memory writes for other block.