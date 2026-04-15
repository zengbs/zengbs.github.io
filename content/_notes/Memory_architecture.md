---


---


# Memory Architecture

<img src="https://i.imgur.com/jvnHYcB.png" width="50%">
<img src="https://i.imgur.com/M5hkYLy.png" width="70%">


|          |   Name   | Access |         Scope         |  Life time   | Cached | Bandwidth (GB/s) |      Name      |   Specifier    |
|:--------:|:--------:|:------:|:---------------------:|:------------:|:------:|:----------------:|:--------------:|:--------------:|
| Off-chip |  Global  |  R/W   | All cuda threads+host | Application  |   Y*   |       100        |   float var†   |  `__device__`  |
| Off-chip | Surface  |  R/W   |                       |              |        |                  |                |                |
| Off-chip |  Local   |  R/W   |      Per-thread       | CUDA thread  |   Y*   |       100        | float var[100] |                |
| Off-chip  | Constant |   R    | All cuda threads+host | Application  |   Y    |     200-300      |   float var†   | `__constant__` |
| Off-chip  | Texture  |   R    | All cuda threads+host | Application  |   Y    |     200-300      |                |                |
| On-chip  |  Shared  |  R/W   |       Per-block       | Thread block |  N/A   |       200        |   float var†   |  `__shared__`  |
| On-chip  | Register |  R/W   |      Per-thread       | CUDA Thread  |  N/A   |                  |   float var    |                |

\* Depend on compute capability (see [here](https://en.wikipedia.org/wiki/CUDA#Multiprocessor_Architecture)).
† Can be either scalar variable or array variable

## Register (32-bit regular registers)
* Registers are the fastest memory space on a GPU.
* Arrays declared in a kernel may also be stored in registers, but only if the indices used to reference the array are constant and can be determined at compile time.
* Register variables are private to each thread.
* Registers are scarce resources that are partitioned among active warps in a streaming multiprocessor (SM).
* Using fewer registers in your kernels may allow more thread blocks to reside on an SM.
* See [here](https://en.wikipedia.org/wiki/CUDA#Technical_Specification) for the number of registers in each compute capability.
* If a kernel uses more registers than the hardware limit, the excess registers will spill over to local memory. This register spilling can have adverse performance consequences.
## Local memory
* Local memory resides in the same physical location as global memory.
* Variables in a kernel that are eligible for registers but cannot fit into the register space allocated for that kernel will spill into local memory.
* Variables that the compiler is likely to place in local memory are:
    * Local arrays referenced with indices whose values cannot be determined at compile-time.
    * Large local structures or arrays that would consume too much register space.
## Shared memory
* Each SM has limited amount of shared memory that is partitioned among thread blocks.
* When a thread block is finished executing, its allocation of shared memory will be released and assigned to other thread blocks.
* `cudaFuncSetCacheConfig()` can dynamically adjust the amount of shared memory and L1 cache.
    * `cudaFuncCachePreferNone`: no preference (default)
    * `cudaFuncCachePreferShared`: prefer 48KB shared memory and 16KB L1 cache
    * `cudaFuncCachePreferL1`: prefer 48KB L1 cache and 16KB shared memory
    * `cudaFuncCachePreferEqual`: Prefer equal size of L1 cache and shared memory, both 32KB
## Constant memory
* Constant variables must be declared with global scope, outside of any kernels with specifier `__constant__`.
* Constant memory must therefore be initialized by the host using: `cudaMemcpyToSymbol()`.
* Constant memory performs best when all threads in a warp read from the same memory address.
    * A coefficient for a mathematical formula is a good use case for constant memory because all threads in a warp will use the same coeffi cient to conduct the same calculation on different data.
    * A single read from constant memory broadcasts to all threads in a warp.
## Texture memory
* Texture memory is optimized for 2D spatial locality, so threads in a warp that use texture memory to access 2D data will achieve the best performance.
## Global memory
* Variables can either be decalred statically (`__device__`) or dynamically (e.g., `cudaMalloc`).
    * Static variable/aray in the global memory must initialized by the host using: `cudaMemcpyToSymbol()`.
* Memory transactions must be aligned to 32 bytes, 64 bytes, or 128 bytes.

## Caches
* There is one L1 cache per-SM and one L2 cache shared by all SMs.
* Both L1 and L2 caches are used to store data in local and global memory, including register spills.
* On the CPU, both memory loads and stores can be cached. However, on the GPU only memory load operations can be cached; memory store operations cannot be cached.
* The CPU L1 cache is optimized for both spatial and temporal locality. The GPU L1 cache is designed for spatial but not temporal locality.
* Frequent access to a cached L1 memory location does not increase the probability that the data will stay in cache.