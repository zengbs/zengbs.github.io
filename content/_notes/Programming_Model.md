---
title: Programming Model


---

###### tags: `CUDA`


# CUDA Programming Model
![](https://i.imgur.com/fG2HjlE.png =60%x)
Figure: The layout of streaming multiprocessor (SM) on Fermi
![](https://developer.ridgerun.com/wiki/images/9/9e/Nvidia-microarchitecture.png =60%x)
Figure: The memory layouts of device and streaming multiprocessor (SM) are shown on the left and right side, respectively.
![](https://i.imgur.com/XxYakNo.png =60%x)



## Warp
* A warp is composed of 32 threads.
* When you launch a grid of thread blocks, the thread blocks in the grid are distributed among SMs. Once a thread block is scheduled to an SM, threads in the thread block are further partitioned into warps.
* A warp consists 32 threads and all threads in a warp are executed in Single Instruction Multiple Thread (SIMT) fashion.
* A warp is never split between different thread blocks.
## Thread block
* Thread blocks are required to execute independly.
* If thread block size is not a multiple of warp size, some CUDA cores in the last warp are left inactive.
* Each SM features two warp schedulers and two instruction dispatch units. When a thread block is assigned to an SM, all threads in a thread block are divided into warps. The two warp schedulers select **two** warps and issue one or two instructions on two warps.
* When a kernel grid is launched, the thread blocks of that kernel grid are distributed among available SMs for execution.
* Once scheduled on an SM, the threads of a thread block execute concurrently only on that assigned SM.
* A single Streaming Multiprocessor (SM) can only execute one block at a time. If you have a block whose size (in terms of the number of threads) is greater than the number of CUDA cores on an SM, the SM will execute the block in multiple batches, serially.
* Multiple thread blocks may be assigned to the same SM at once and are scheduled based on the availability of SM resources.
    * If the SM has enough resources (such as registers and shared memory) and the thread blocks are small enough, the SM can execute multiple thread blocks concurrently by interleaving the threads from different blocks on the cores. It allows the SM to hide latencies and increase instruction-level parallelism, resulting in higher performance.
        * Concurrent Execution vs. Interleaving: A single SM typically cannot execute multiple thread blocks simultaneously in the sense of parallel execution on different cores. However, it can interleave the execution of threads from different blocks. This interleaving is a form of concurrent execution, but it's not parallel execution in the strictest sense. It's more like rapidly switching between different thread blocks.
        * Hiding Latencies: The primary advantage of this interleaving is the ability of the SM to hide latencies. While one thread block is waiting (for example, for a memory fetch), the SM can switch to executing another thread block. This keeps the cores busy and improves overall throughput.
        * Instruction-Level Parallelism: By interleaving threads from different blocks, the SM can increase instruction-level parallelism. This means that the SM can execute instructions from different threads in a way that optimizes the use of the GPU’s computational resources.
        * Resource Limitations: The extent to which an SM can interleave thread blocks depends on the available resources, such as registers and shared memory. If the thread blocks are small (i.e., they use fewer resources), it's more feasible for an SM to handle multiple blocks concurrently.
        * On the other hand, if the SM does not have sufficient resources or the thread blocks are too large, it may not be possible to execute multiple thread blocks concurrently on the SM. In this case, the SM will execute each thread block one at a time, switching between thread blocks as resources become available.
        * ![Peek 2023-12-14 07-02](https://hackmd.io/_uploads/B10Cj3wUa.gif)
* When a warp idles for any reason (for example, waiting for values to be read from device memory), the SM is free to schedule another available warp from any thread block that is resident on the same SM.
* Switching between concurrent warps has no overhead because **hardware resources are partitioned among all threads and blocks on an SM**, so the state of the newly scheduled warp is already stored on the SM. But note that **a warp is never split between different thread blocks.**
* CUDA provides a runtime [API](https://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__DEVICE.html#group__CUDART__DEVICE_1g6c9cc78ca80490386cf593b4baa35a15) that can be used to adjust the amount of shared memory and L1 cache.
* **Shared memory is partitioned among thread blocks resident on the SM, and registers are partitioned among threads.**
* Limited hardware resouce on SM (see [Technical Specification](https://en.wikipedia.org/wiki/CUDA#Technical_Specification))
    1. <span style="color:red">Maximum number of threads per block</span>
    2. <span style="color:red">Maximum number of concurrent blocks per SM</span>
    3. <span style="color:blue">Maximum number of concurrent warps (within concureent blocks) per SM</span>
        * Maximum number of concurrent threads * 32 = Maximum number of concurrent warps per SM.
    5. Maximum number of concurrent threads (within concurrent blocks) per SM
        * (<span style="color:red">the number of threads per block</span>) * (<span style="color:red">the number of concurrent blocks</span>) = <span style="color:red">number of concurrent threads per SM</span>.
    6. **Number of 32-bit registers per SM**
    7. **Maximum number of 32-bit registers per thread**
        * (<span style="color:red">number of register per thread</span>) * (<span style="color:red">number of threads per block</span>) * (<span style="color:red">number of concureent blocks per SM</span>) < <span style="color:red">number of register per SM</span>.
    8. **Maximum amount of shared memory per SM**
        * (required shared memory per block) * (<span style="color:red">number of concurrent blocks per SM</span>) < <span style="color:red">amount of shared memory per SM</span>.
* If there are `N` blocks in a SM, `x` registers per thread, `y` bytes of shareed memory per block, then the amount of blocks that are concurrently running on a SM would be `min(N, min( floor(f/(x*BLOCK_SIZE)), floor(size of shared memory per SM/y) ))`

## Thread block cluster
![圖片](https://hackmd.io/_uploads/rkU49FLBC.png =70%x)
