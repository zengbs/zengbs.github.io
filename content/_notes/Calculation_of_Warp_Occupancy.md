---


---



# Limited by Number of Warps per SM

$\displaystyle X=\text{# available blocks per SM} =  \text{ floor}\left( \frac{\text{Max # active warps per SM}}{\text{# warps per block}} \right)$



# Limited by Number of Registers per SM

$\displaystyle \text{warp limit per SM due to per-warp register} = \text{floor}\left[\frac{\text{Max # registers per SM}}{\text{ceiling}(\text{# registers per thread}\times\text{warpSize}, \text{register allocation unit size})}, \text{warp allocation granuality}\right]$


$\displaystyle Y=\text{# available blocks per SM} = \text{ floor}\left(\frac{\text{warp limit per SM due to per-warp register}}{\text{# warps per block}}\right)$


# Limited by Shared Memory

$\displaystyle \text{amount of allocated shared memory per block}=\text{ceiling}\left(\text{shared memory per block}, \text{ shared memory allocation unit size}\right)$

$\displaystyle Z=\text{# available blocks per SM} =  \text{ floor}\left(\frac{\text{Max amount of shared memory per SM}}{\text{amount of allocated shared memory per block}}\right)$

# Summary

$\displaystyle A=\text{Max # active blocks per SM}$
$\displaystyle B=\text{Max # active warps per SM}$

$\displaystyle\text{# active blocks per SM} = \min\left[X, Y, Z, A\right]$

$\displaystyle\text{# active warps per SM} =\min\left[\left(\text{# active blocks per SM}\times\text{# warps per block}\right), B\right]$

$\displaystyle \text{warp occupancy}=\frac{\text{# active warps per SM}}{\text{Max # warps per SM}}$


# Examples
For CC = 8.0

![image](https://hackmd.io/_uploads/S18R2afu6.png)
![image](https://hackmd.io/_uploads/SkbXJ0GOT.png)
![image](https://hackmd.io/_uploads/H14VkCfua.png)

# Grid/Block Size vs. GPU Throughput

To understand how grid/block size affects GPU throughput, we use a CUDA kernel below to give a demonstration. The kernel adds two one-dimensional (1D) vectors on global memory and combines them to form another third 1D vector.

```cuda=
// Kernel
__global__ void kernel(double *a, double *b, double *c, long length)
{
    int id = blockDim.x * blockIdx.x + threadIdx.x;

    while(id < length){
       c[id] = a[id] + b[id] + sqrt(a[id]) + sqrt(b[id]);
       c[id] = sqrt(c[id]);
       id += gridDim.x*blockDim.x;
    }
}
```

The kernel systematically iterates through a range of grid sizes and block sizes, executing the kernel function with each combinations.

Before and after each kernel execution, the script calls `Start()` and `Stop()` functions for timing the excution. The `cudaDeviceSynchronize()` function ensures the kernal function is completed before proceeding on the host side. Without calling `cudaDeviceSynchronize()`, the thread on CPU will  proceed to execute the `Stop()` immediately after the kernel function is called. This premature execution leads to inaccurate timing results, as it doesn't account for the actual completion time of the kernel's execution on the GPU.
```cuda=
// Launch kernel
for ( gridSize = 1; gridSize<=1024; gridSize++ ){
   for ( blockSize = 1; blockSize<=1024; blockSize++ ){
      Start();
      kernel<<< gridSize, blockSize >>>(d_A, d_B, d_C, N); 
      cudaDeviceSynchronize();
      Stop();
      printf("%d, %d, %e\n", gridSize, blockSize, GetValue());
   }   
   printf("\n");
}
```

The figure below illustrates the timing results derived from the benchmark script on NVIDIA A10, represented as a function of both grid size and block size. At first glance, the figure shows that the time spent on the kernel execution increases as either the block size or grid size decreases.

<img src="https://hackmd.io/_uploads/HygxYnQKp.png" width="70%">

To conduct detailed analysis, we plot the profiles in the top row panels, the right panel shows how the kernel's execution time varies with grid size at a fixed block size, while the left panel shows the variation with block size at a fixed grid size. These two profiles are based on the time as a function of both grid and block size showing the above figure.


![fig__occupancy](https://hackmd.io/_uploads/Sk73r-ntp.png)


$\begin{equation}
\displaystyle
\text{Warp occupancy}=\frac{\text{Number of threads per block}}{\text{ceiling(Number of threads per block, warp size)}}
\end{equation}$




$\begin{equation}
\displaystyle
\text{SM occupancy}=\frac{\text{Number of blocks per grid}}{\text{ceiling(Number of blocks per grid, Number of SMs per GPU)}}
\end{equation}$





| gridSize | blockSize | Time ($10^{-4}$ sec) |
| -------- | -------- | -------- |
| 1024     |    32  |      |
| 1024     |    64  |      |
| 1024     |    96  |      |
| 1024     |      |      |
| 1024     |      |      |
| 1024     |      |      |


# Tool
[Warp Occupancy Calculator](https://docs.google.com/spreadsheets/d/1sqRu1hZdnCKiMbaWQWbsC_DKg9qg3O98Hm-57hW7ZgI/edit#gid=2071872559)


# Reference
[Better Performance at Lower Occupancy](https://www.nvidia.com/content/gtc-2010/pdfs/2238_gtc2010.pdf)