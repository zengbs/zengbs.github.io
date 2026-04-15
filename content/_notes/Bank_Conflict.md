---


---





## Bank
* Shared memory is divided into 32 equally-sized memory modules, called ***banks***, which can be accessed simultaneously.
* Shared memory are organized such that successive 32-bit words map to successive banks.
* There are 32 banks because there are 32 threads in a warp.
* Shared memory is a **1D** address space.
* **bank index = (byte address ÷ 4 bytes/bank) % 32 banks** i.e., Elements in shared memory belonging to different banks are also stored consecutively, by word offset.
* Threads in the same warp can be identified by consecutive values of `threadIdx.x`.
* **When multiple threads in a single warp read/write differ words in the same bank, conflict occurred.** See [Will bank conflict occur between different warps?](https://forums.developer.nvidia.com/t/cc5-0-will-bank-conflict-occur-between-different-warps/35548)
* One way to resolve this type of bank conflict is to add a word of padding after every N elements, where N is the number of banks.


## Example: Accessing Row-Major versus Column-Major

Row-major write/column-major read:
```cuda=
__global__ void setRowReadRow(int *out) {
   // static shared memory
   __shared__ int tile[BDIMY][BDIMX];
    
   // mapping from thread index to global memory index
   unsigned int idx = threadIdx.y * blockDim.x + threadIdx.x;
    
   // shared memory store operation (conflict-free)
   tile[threadIdx.y][threadIdx.x] = idx;
    
   // wait for all threads to complete
   __syncthreads();
    
   // shared memory load operation (bank conflict)
   out[idx] = tile[threadIdx.x][threadIdx.y] ;
}
```
* Conflict-free:
<img src="https://hackmd.io/_uploads/S1k6o2TL6.png" width="25%">
* Bank conflict:
<img src="https://hackmd.io/_uploads/H1sen3aUT.png" width="25%">
* Threads in the same warp can be identified by consecutive values of `threadIdx.x`.
* Elements in shared memory belonging to different banks are also stored consecutively, by word offset.
* Therefore, it is best to have threads with consecutive values of `threadIdx.x` accessing consecutive locations in shared memory.

## Padding Statically Declared Shared Memory

```cuda=
__global__ void setRowReadColPad(int *out) {
    
    // static shared memory
    __shared__ int tile[BDIMY][BDIMX+IPAD];
    
    // mapping from thread index to global memory offset
    unsigned int idx = threadIdx.y * blockDim.x + threadIdx.x;
    
    // shared memory store operation
    tile[threadIdx.y][threadIdx.x] = idx;
    
    // wait for all threads to complete
    __syncthreads();
    
    // shared memory load operation
    out[idx] = tile[threadIdx.x][threadIdx.y];
}
```

* Suppose we have only five shared memory banks.
* The left configuration is the one we imagine.
* The right configuration is real in hardware.

<img src="https://hackmd.io/_uploads/S1H0uaaIT.png" width="35%">


| Conflict-free                        | Conflict-free                        |            Conflict-free             |       Conflict-free (broadcast)       |            Bank conflict             |
| ------------------------------------ | ------------------------------------ |:------------------------------------:|:------------------------------------:|:------------------------------------:|
| ![](https://i.imgur.com/CUWLbQI.png) | ![](https://i.imgur.com/GnJ7sMu.png) | ![](https://i.imgur.com/yOYWjxL.png) | ![](https://i.imgur.com/zLHwtHx.png) | ![](https://i.imgur.com/EZPtRmN.png) |