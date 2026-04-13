---
title: Warp Shuffles


---

# Definitions
`laneID = threadIdx.x % warpSize` or`laneID = threadIdx.x & 0x1f`
`warpID = threadIdx.x / warpSize`


* Threads within a warp are referred to as lanes, and may have an index between 0 and `warpSize-1` (inclusive).
* The `__shfl_*sync()` intrinsics permit exchanging of a variable between threads within a warp without use of shared memory. The exchange occurs **simultaneously** for all active threads within the warp.

# Broadcast
```c=
T __shfl_sync(unsigned mask, T var, int srcLane, int width=warpSize);
```
`__shfl_sync(0xffffffff, var, 2, warpSize)`, where `var=input[2]`.
![image](https://hackmd.io/_uploads/rJax7dePp.png =70%x)
`__shfl_sync(0xffffffff, var, 2, warpSize/2)`, where `var=input[2]` or `var=input[18]`.
![image](https://hackmd.io/_uploads/Hy_ZmOlwT.png =70%x)


* `mask`: The new *_sync shfl intrinsics take in a mask indicating the threads participating in the call. A bit, representing the thread’s lane id, must be set for each participating thread to ensure they are properly converged before the intrinsic is executed by the hardware. Each calling thread must have its own bit set in the mask and all non-exited threads named in mask must execute the same intrinsic with the same mask, or the result is undefined.
* `var`: input values to be broadcast. i.e., `var=input[srcLane]`.
* `srcLane`: all threads get the same value from the thread at lane `srcLane`. For instance, if `srcLane` is set to 5, each participating thread in the warp will receive the value of var from the thread whose lane ID is 5. `srcLane = (srcLane % width) + k*width`, `k=0,...,(warpSize/width)`.
* `width`: . Value must have a power of two in the range `[1, warpSize]` (i.e., 1, 2, 4, 8, 16 or 32)
* Return: the value of `var` held by the thread whose ID is given by `srcLane`.

# Shuffle Up
```c=
T __shfl_up_sync(unsigned mask, T var, unsigned int delta, int width=warpSize);
```
`__shfl_up_sync(0xffffffff, var, 2, warpSize)`, where `var=input[2]`.
![image](https://hackmd.io/_uploads/B1qjV_evT.png =70%x)
`__shfl_up_sync(0xffffffff, var, 2, warpSize/2)`, where `var=input[2]`.
![image](https://hackmd.io/_uploads/SkShE_lD6.png =70%x)

# Shuffle Down

```c=
T __shfl_down_sync(unsigned mask, T var, unsigned int delta, int width=warpSize);
```
`__shfl_down_sync(0xffffffff, var, 3, warpSize)`
![image](https://hackmd.io/_uploads/rya4H_xPp.png =70%x)
`__shfl_down_sync(0xffffffff, var, 3, warpSize/4)`
![image](https://hackmd.io/_uploads/By_HB_gPp.png =70%x)



# XOR Shuffle
```c=
T __shfl_xor_sync(unsigned mask, T var, int laneMask, int width=warpSize);
```

The table below shows the XOR result between `tid` and `laneMask`:
![image](https://hackmd.io/_uploads/SyYKmQbDT.png)



`__shfl_xor_sync(0xffffffff, var, 1, warpSize)`


![image](https://hackmd.io/_uploads/rkJwr_lwa.png =70%x)
`__shfl_xor_sync(0xffffffff, var, 3, warpSize)`
![image](https://hackmd.io/_uploads/HyYPHdxvp.png =70%x)



# Examples
## Local Reduction with XOR shuffle
```c=
for (int i=1; i<warpSize; i*=2)
   value += __shfl_xor_sync(0xffffffff, value, i);
```

![image](https://hackmd.io/_uploads/HyFZkCCUa.png =40%x)


## Local Reduction with Down Shuffle
```c=
for (int i=warpSize/2; i>0; i=i/2)
   value += __shfl_down_sync(0xffffffff, value, i);
```

![image](https://hackmd.io/_uploads/Hy_fy0ALa.png =40%x)


## Block Reduction with Warp Shuffle
```c=
__inline__ __device__
int WarpReduceMin(int value)                                                               
{  
   for ( int offset=warpSize/2; offset>0; offset/=2 ){
      int value = max(value, __shfl_down_sync( 0xffffffff, value, offset, warpSize));                       
   }
   return value;
}
```

```c=
__inline__ __device__                                                                          
int BlockReduceMin(int value)                                                                  
{                                                                                              
   // size of array must have a constant value                                                 
   static __shared__ int buffer[32];                                                           
                                                                                               
   int laneID = threadIdx.x % warpSize;                                                        
   int warpID = threadIdx.x / warpSize;                                                        
                                                                                               
   // assumming number of warps <= 32                                                          
   int numWarp = blockDim.x / warpSize;                                                        
                                                                                               
   // execute warp shuffle for each thread; the result will be at the thread with laneID = 0                                             
   value = WarpShuffle(value);                                                                 
                                                                                               
   if (laneID==0)  buffer[warpID] = value;                                                     
                                                                                               
   __syncthreads();                                                                            
                                                                                               
   // fill the rest of warps with INT_MAX in case numWarp is less than 32                      
   value = (threadIdx.x < numWarp) ? buffer[threadIdx.x] : INT_MAX;                            
                                                                                               
   if (threadIdx.x < warpSize){                                                                 
      value = WarpShuffle(value);                                                              
   }
    
   return value;                                 
}
```


# Reference
* [CUDA C++ Programming Guide (Warp Shuffle Functions)](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#warp-shuffle-functions)
* [Faster Parallel Reductions on Kepler](https://developer.nvidia.com/blog/faster-parallel-reductions-kepler/)