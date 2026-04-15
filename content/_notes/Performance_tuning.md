---


---


# Performance Issues

## Warp divergence
All threads in a warp execute the same instruction at the same time. i.e. avoid threads in a warp take different logic paths.

If threads of warp diverge, the warp serially execuates each branch path.

1. Warp divergence (Example 1):
```cuda=
__global__ void warpDivergenceKernel(int *data) {
    int index = threadIdx.x + blockIdx.x * blockDim.x;
    
    // Conditional statement causing warp divergence
    if (index % 2 == 0) {
        data[index] = index;  // Path for even indices
    } else {
        data[index] = 0;        // Path for odd indices
    }
}
```

2. No warp divergence (Example 1):
```cuda=
__global__ void optimizedKernel(int *data) {
    int index = threadIdx.x + blockIdx.x * blockDim.x;

    // Using arithmetic operations to avoid conditional branching
    int isEven = index % 2;  // will be 1 for even indices, 0 for odd
    data[index] = (1-isEven) * index;
}
```

3. Warp divergence (Example 2):
```cuda=
__global__ void mathKernel1(float *c) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    float a, b;
    a = b = 0.0f;
    if (tid % 2 == 0) {
        a = 100.0f;
    } else {
        b = 200.0f;
    }
    c[tid] = a + b;
}
```

4. No warp divergence (Example 2):
```cuda=
__global__ void mathKernel2(void) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    float a, b;
    a = b = 0.0f;
    if ((tid / warpSize) % 2 == 0) {
        a = 100.0f;
    } else {
        b = 200.0f;
    }
    c[tid] = a + b;
}
```
Note that the two versions of Example 2 give the same output, but in differnt order.

```cuda=
int f(int x){
   
    if (0 <=x && x <= 10){
        return 1;
    }else{
        return 0;
    }
}
```

```cuda=
int f(int x){
    return (int)(0 <=x && x <= 10)
}
```

## Occupancy

$\displaystyle\text{Warp occupancy}=\frac{\text{number of active warps per SM}}{\text{maximum active warps per SM}}$

* Resources are allocated for the entire block.
* Utilizing too many resources per thread may limit the occupancy.

## Latency Hiding (Little's law)


### Stream Multiprocessors

$\text{Needed warps} = \text{throughput per warp} \times\text{latency}$.

Instruction latency = 20 cycles

Throughput per SM = 32 operations/cycle

Thread parallelism $= 32\times 20 = 640$ operations.

Thus, if the number of threads is less than 64, SM will sometimes be idle.



### Memory

$\displaystyle \text{Needed data} = \left(\frac{\text{memory bandwidth}}{\text{memory frequency}}\right)\times \text{instruction latency}$

* Instruction latency = 800 cycles
* Memory bandwidth = 144 GB/sec
* Memory frequency = 1.566 GHz\*cycle = 1.566G cycle/sec

Multiplying the above two, we can obtain how much data can be moved in a single cycle:

$\displaystyle\frac{ 144 \text{ GB/sec} }{1.566 \text{ G cycle/sec}} = 92$ Bytes/cycle


Thus, data parallelism $= 800\times 92$ Bytes = 74 KB

Suppose each thread moves 4 bytes from global memory to SM for computation, we need at least

$\displaystyle\frac{74 \text{ KB}}{ 4 \text{ bytes/thread} } =$ 18,500 threads

to hide memory latency or to fetch enough data to fulfill memory bandwidth.



## Bank conflict
64-bit machine:
$\displaystyle\text{Bank index}=\left(\frac{\text{byte addess}}{8 \text{ bytes per bank}}\right)\%32\text{ banks}$
## Coalesced and aligned memory access
## CUDA streaming
* All independent operations should be issued before dependent operations,
* Synchronization of any kind should be delayed as long as possible.

## Guidline for Grid and Block Size
1. Avoid small grid size and large block size.
    * Load Balancing: a single Streaming Multiprocessor (SM) can only execute one block at a time. If you have only a single block whose size (in terms of the number of threads) is much greater than the number of CUDA cores on an SM, the SM will execute the block in multiple batches, serially. That's why a grid size should be a multiple of the number of SMs in a device to make sure no inactive SMs.
    * Register Spilling: Large block size could risk the shortage of rigister on an SM. The excess memory will store on the local memory, which has much larger latency than register.
2. Avoid large grid size and small block size.
    * Load Balancing: a single Streaming Multiprocessor (SM) can only execute one block at a time. If you have a block whose size is much smaller than the number of CUDA cores on an SM, some CUDA cores are inactive. That's why a block size should be a multiple of the number of CUDA cores in an SM.
3. Keep the number of blocks per grid a multiple of the number of SM. e.g., 48 for Turing architecture.
4. Keep the number of threads per block a multiple of of the number of CUDA cores in an SM. i.e., 64
5. Keep the number of threads per block a power of 2.
    * [In order to ensure 100% warp occupancy](https://hackmd.io/nxg0xlLqQlyeJ5TE_b_YBQ?view).
## Guidline for performance tuning
1. Avoid warp divergence.
2. Avoid register spilling.
11. Enhance warp occupancy.
4. A large bank size may yield higher bandwidth for shared memory access, but may result in more bank conflicts depending on the application?�s shared memory access patterns.
12. Adjust the amount of shared memory and L2 cache
13. Avoid bank conflict
14. Coalesced and aligned memory access.
15. Make sure data size is a multiple of cache granularity.
16. Concurrent GPU/CPU executions
17. Concurrent GPU executions and data transfer
18. Use constant memory for data that does not change over the course of a kernel execution.
19. Loop Unrolling.
20. Kernel Fusion.
21. Dynamic Parallelism:
    Use dynamic parallelism to launch kernels from within other kernels where appropriate, reducing the need for CPU intervention and improving data locality.
21. Efficient Use of Atomic Operations:
    Use atomic operations judiciously as they can serialize access to memory, but they are essential for certain operations like reductions and histograms.
23. More computation per memory access
24. Re?�compute may be faster than re?�loading data
25. Minimize memory transfers from host to device
26. Check each [metric](https://docs.nvidia.com/cuda/profiler-users-guide/index.html#metrics-for-capability-7-x) with `nvprof` as you can as possible.
27. Turn on the [MPS](https://docs.nvidia.com/deploy/mps/index.html#topic_6_1) daemon.
    * Turn on:
        * `sudo nvidia-cuda-mps-control -d`
        * `ps -ef |grep mps # check mps status`
    * Turn off:
        * `echo quit | nvidia-cuda-mps-control`
28. Ensure that no one else is using GPU while you are:
    * Switch compute mode from "default" to "exclusive process".
    * `nvidia-smi  --query | grep 'Compute Mode'` (check the current compute mode).
    * `nvidia-smi -i 1 -c MODE` (set the compute mode `MODE` to default on the device 0).
        * `0/DEFAULT, 1/EXCLUSIVE_PROCESS, 2/PROHIBITED`


<img src="https://hackmd.io/_uploads/rJ3yCwNaT.png" width="50%">



# Reference:
* [Choosing the right Dimensions](http://selkie.macalester.edu/csinparallel/modules/CUDAArchitecture/build/html/2-Findings/Findings.html#)
* [How to Choose the Grid Size and Block Size for a CUDA Kernel?](https://oneflow2020.medium.com/how-to-choose-the-grid-size-and-block-size-for-a-cuda-kernel-d1ff1f0a7f92)
* [Better Performance at Lower Occupancy](https://www.nvidia.com/content/gtc-2010/pdfs/2238_gtc2010.pdf)
* [Demystifying GPU Microarchitecture through
Microbenchmarking](http://www.stuffedcow.net/files/gpuarch-ispass2010.pdf)
* [Register spilling](https://developer.download.nvidia.com/CUDA/training/register_spilling.pdf)
* [Bank conflict](https://www.itread01.com/content/1541908989.html)
* [GPU ?�硬體架構](https://kheresy.wordpress.com/2008/03/31/hotballs-hivegpu-%e7%9a%84%e7%a1%ac%e9%ab%94%e6%9e%b6%e6%a7%8b/)
* [Block ??Grid ?�設定�? Warp](https://kheresy.wordpress.com/2008/07/09/cuda-%E7%9A%84-threading%EF%BC%9Ablock-%E5%92%8C-grid-%E7%9A%84%E8%A8%AD%E5%AE%9A%E8%88%87-warp/)
* [cudaDeviceProp Struct Reference](https://docs.nvidia.com/cuda/cuda-runtime-api/structcudaDeviceProp.html)
* [How do I choose grid and block dimensions for CUDA kernels?](https://stackoverflow.com/questions/9985912/how-do-i-choose-grid-and-block-dimensions-for-cuda-kernels)
* [CUDA_Occupancy_Calculator](https://docs.google.com/spreadsheets/d/16Wgo2pONQdS0NQCFkW3-10M2OoAQeSvf5eQQPqMsy-M/edit?usp=sharing)
* [NVIDIA Nsight Compute](https://developer.nvidia.com/nsight-compute)
* [How to properly calculate CPU and GPU FLOPS performance?](https://scicomp.stackexchange.com/questions/36306/how-to-properly-calculate-cpu-and-gpu-flops-performance)
* [How to Access Global Memory Efficiently in CUDA C/C++ Kernels](https://developer.nvidia.com/blog/how-access-global-memory-efficiently-cuda-c-kernels/)
* [CUDA warps and occupancy](https://on-demand.gputechconf.com/gtc-express/2011/presentations/cuda_webinars_WarpsAndOccupancy.pdf)