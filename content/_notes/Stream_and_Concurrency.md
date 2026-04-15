---


---

# Stream
* A **stream** in CUDA is a sequence of operations that execute on the device in the order in which they are issued by the host code.


## Default Stream
* Most operations added to the NULL-stream cause the host to block on all preceding operations, the main exception being kernel launches.

## Non-default Stream
* For non-default stream, all operations are non-blocking with respect to the host.
```cuda=
#include <cuda_runtime.h>

int main() {
    cudaStream_t stream;
    cudaError_t result = cudaStreamCreate(&stream);

    // Use the stream for operations...

    // Clean up and destroy the stream
    cudaStreamDestroy(stream);
    
    return 0;
}

```
### Non-default blocking stream
*  Non-default blocking stream can be blocked waiting for earlier operations in the NULL stream to complete.
*  Default stream can be blocked waiting for earlier operations in the non-default blocking stream to complete.
* Non-default blocking stream is equivalent to the stream created by `cudaStreamCreate(&stream)`.
```cuda=
#include <cuda_runtime.h>

int main() {
    cudaStream_t stream;
    cudaError_t result = cudaStreamCreateWithFlags(&stream, cudaStreamDefault);

    // Use the stream for operations...

    // Clean up and destroy the stream
    cudaStreamDestroy(stream);

    return 0;
}
```
### Non-default non-blocking stream
* Non-default non-blocking stream will not be blocked on operations in the NULL stream. 


```cuda=
#include <cuda_runtime.h>

int main() {
    cudaStream_t stream;
    cudaError_t result = cudaStreamCreateWithFlags(&stream, cudaStreamNonBlocking);

    // Use the stream for operations...

    // Clean up and destroy the stream
    cudaStreamDestroy(stream);

    return 0;
}
```



|                                 |              Host' view              | Can be blocked by a defaul stream? |  Creation   |
|:-------------------------------:|:------------------------------------:|:----------------------------------:| --- |
|         Default stream          | Synchronous</br>(except kenel calls) |                N/A                 |   N/A  |
|       Non-default stream        |             Asynchronous             |                Yes                 |   `cudaStreamCreateWithFlags(&stream, cudaStreamDefault)`</br>or</br>`cudaStreamCreate(&stream1)`  |
|   Non-default blocking stream   |             Asynchronous             |                Yes                 |  `cudaStreamCreateWithFlags(&stream, cudaStreamDefault)`   |
| Non-default non-blocking stream |             Asynchronous             |                 No                 | `cudaStreamCreateWithFlags(&stream, cudaStreamNonBlocking)`    |

## Example
```cuda=
K1<<<1, 1, 0, stream_1>>>();
K2<<<1, 1>>>();
K3<<<1, 1, 0, stream_2>>>();
```



| Non-default blocking | Non-default non-blocking |                 Execution timeline                 |
| -------------------- | ------------------------ |:--------------------------------------------------:|
| K1, K3               |                          | <img src="https://hackmd.io/_uploads/HkdkW-Vw6.png" width="80%"> |
|                      | K1,K3                    | <img src="https://hackmd.io/_uploads/r1g_mZZEPp.png" width="40%">
| K1                   | K3                       |          <img src="https://hackmd.io/_uploads/SkrBZZNDp.png" width="60%">
| K3                   | K1                       |          <img src="https://hackmd.io/_uploads/S1YUZZNPa.png" width="60%">



# Synchronization with Streams
## Synchronize everything
* `cudaDeviceSynchronize()` blocks the host thread until all previously issued operations on the device have completed.
## Synchronize w.r.t. a specific stream
* `cudaStreamSynchronize(stream)` blocks the host thread until all previously issued operations in the specified stream have completed.
## Synchronize Using Events
* ` cudaEventSynchronize(cudaEvent_t event)`

# Hyper-Q
Hyper-Q is a feature introduced in the Kepler architecture. It expands the capability of a single GPU to handle work from multiple CPU cores simultaneously. Traditionally, a single CPU core would queue tasks to the GPU. Hyper-Q allows multiple CPU cores to place tasks in the GPU's queue, which increases GPU utilization and reduces CPU idle times. It essentially allows for more concurrent operations to be processed by the GPU, making it significantly more efficient in multi-threaded and parallel computing environments.

# Grid Management Unit (GMU)

# Concurrent Kernels Executions
* Under the condition of not violating the issue order:
    * Each hardware (work/copy) queue is capable of sequentially (executing/copying) a single work in a stream, or concurrently (executing/copying) multiple works in different stream.
## Depth-first
```cuda=
for (int i = 0; i < n_streams; i++) {
   kernel_1<<<grid, block, 0, streams[i]>>>();
   kernel_2<<<grid, block, 0, streams[i]>>>();
   kernel_3<<<grid, block, 0, streams[i]>>>();
   kernel_4<<<grid, block, 0, streams[i]>>>();
}
```
<img src="https://hackmd.io/_uploads/HyJdHb4wa.png" width="80%">



|                       with Hyper-Q</br>(multiple hardware work queues)                       |                     without Hyper-Q</br>(single hardware work queue)                      |
|:--------------------------------------------------------:|:--------------------------------------------------------:|
| <img src="https://hackmd.io/_uploads/B1puPW4vT.png" width="70%"> | <img src="https://hackmd.io/_uploads/S1G4DZ4v6.png" width="80%"> |





## Breadth-first
```cuda=
for (int i = 0; i < n_streams; i++)
   kernel_1<<<grid, block, 0, streams[i]>>>();
for (int i = 0; i < n_streams; i++)
   kernel_2<<<grid, block, 0, streams[i]>>>();
for (int i = 0; i < n_streams; i++)
   kernel_3<<<grid, block, 0, streams[i]>>>();
for (int i = 0; i < n_streams; i++)
   kernel_4<<<grid, block, 0, streams[i]>>>();
```
<img src="https://hackmd.io/_uploads/rJ2dHZVPa.png" width="80%">

|                       with Hyper-Q</br>(multiple hardware work queues)                       |                     without Hyper-Q</br>(single hardware work queue)                      |
|:--------------------------------------------------------:|:--------------------------------------------------------:|
| <img src="https://hackmd.io/_uploads/B1puPW4vT.png" width="40%"> | <img src="https://hackmd.io/_uploads/B1puPW4vT.png" width="40%"> |




# Overlapping Kernel Execution and Data Transfers
## Requirements
* The device must be capable of "concurrent copy and execution". 
* The kernel execution and the data transfer to be overlapped must both occur in different, non-default streams.
* The host memory involved in the data transfer must be pinned memory.


## Depth-first
```cuda=
for (int i = 0; i < NSTREAM; ++i) {
   int ioffset = i * iElem;
   cudaMemcpyAsync(&d_A[ioffset], &h_A[ioffset], iBytes, cudaMemcpyHostToDevice, stream[i]);
   cudaMemcpyAsync(&d_B[ioffset], &h_B[ioffset], iBytes, cudaMemcpyHostToDevice, stream[i]);
   sumArrays<<<grid, block,0,stream[i]>>>(&d_A[ioffset], &d_B[ioffset], &d_C[ioffset],iElem);   
   cudaMemcpyAsync(&gpuRef[ioffset],&d_C[ioffset],iBytes, cudaMemcpyDeviceToHost, stream[i]);
}
```
<img src="https://hackmd.io/_uploads/BkHUgzHw6.png" width="90%">


|                  | w/ GMU | w/o GMU |
|:----------------:| ------ | ------- |
|  One work queue  |  ![image](https://hackmd.io/_uploads/ryuwMfrD6.png) | ![image](https://hackmd.io/_uploads/ryuwMfrD6.png) |
| Eight work queue |  ![image](https://hackmd.io/_uploads/rJcwzMBw6.png) |  |

## Breadth-first

```cuda=
// initiate all asynchronous transfers to the device
for (int i = 0; i < NSTREAM; ++i) {
   int ioffset = i * iElem;
   cudaMemcpyAsync(&d_A[ioffset], &h_A[ioffset], iBytes, cudaMemcpyHostToDevice, stream[i]);
   cudaMemcpyAsync(&d_B[ioffset], &h_B[ioffset], iBytes, cudaMemcpyHostToDevice, stream[i]);
}

// launch a kernel in each stream
for (int i = 0; i < NSTREAM; ++i) {
   int ioffset = i * iElem;
   sumArrays<<<grid, block, 0, stream[i]>>>(&d_A[ioffset], &d_B[ioffset], &d_C[ioffset],iElem);
}

// queue asynchronous transfers from the device
for (int i = 0; i < NSTREAM; ++i) {
   int ioffset = i * iElem;
   cudaMemcpyAsync(&gpuRef[ioffset],&d_C[ioffset], iBytes,
   cudaMemcpyDeviceToHost, stream[i]);
}
```
<img src="https://hackmd.io/_uploads/SJu_lzrw6.png" width="90%">




|                  | w/ GMU | w/o GMU |
|:----------------:| ------ | ------- |
|  One work queue  |  ![image](https://hackmd.io/_uploads/ryuwMfrD6.png) | ![image](https://hackmd.io/_uploads/BkV3ffrvT.png) |
| Eight work queue |  ![image](https://hackmd.io/_uploads/rJcwzMBw6.png) |  |


# Overlapping GPU and CPU Execution


# The Limit of Speedup
<img src="https://hackmd.io/_uploads/r1Pz4d9D6.png" width="70%">



# Reference
* [How to Overlap Data Transfers in CUDA C/C++](https://developer.nvidia.com/blog/how-overlap-data-transfers-cuda-cc/)
* [CUDA C/C++ Streams and Concurrency](https://developer.download.nvidia.com/CUDA/training/StreamsAndConcurrencyWebinar.pdf)
* [CUDA Streams Best Practices and Common Pitfalls](https://on-demand.gputechconf.com/gtc/2014/presentations/S4158-cuda-streams-best-practices-common-pitfalls.pdf)