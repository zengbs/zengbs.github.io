---


---


# Memory Management (global memory)
## Pageable memory

![image](https://hackmd.io/_uploads/rkakRkc86.png =40%x)

```cuda=
// Allocation
int *host_input_arr = (int*)malloc(sizeof(int) * elementSize);
int *host_output_arr = (int*)malloc(sizeof(int) * elementSize);
int *device_arr;
cudaMalloc((void**)&device_arr, sizeof(int) * elementSize);

// Data Transfer and Kernel Function
cudaMemcpy(device_arr, host_input_arr, sizeof(int) * elementSize, cudaMemcpyHostToDevice);
kernel<<<blockSize, threadsPerBlock>>>(device_arr, elementSize);
cudaDeviceSynchronize();
cudaMemcpy(host_output_arr, device_arr, sizeof(int) * elementSize, cudaMemcpyDeviceToHost);

// Free
cudaFree(device_arr);
free(host_input_arr);
free(host_output_arr);
```

## Pinned memory
Page-locking excessive amounts of memory with cudaMallocHost() may degrade system performance, since it reduces the amount of memory available to the system for paging. As a result, this function is best used sparingly to allocate staging areas for data exchange between host and device.
![image](https://hackmd.io/_uploads/SJ7zRy5Ua.png =40%x)

```c=
// Allocation
int *host_input_arr;
int *host_output_arr;
int *device_arr;
cudaMallocHost((void**)&host_input_arr, sizeof(int) * elementSize, cudaHostAllocDefault);
cudaMallocHost((void**)&host_output_arr, sizeof(int) * elementSize, cudaHostAllocDefault);
cudaMalloc((void**)&device_arr, sizeof(int) * elementSize);

// Data Transfer and Kernel Function
cudaMemcpy(device_arr, host_input_arr, sizeof(int) * elementSize, cudaMemcpyHostToDevice);
vecMultiply<<<blockSize, threadsPerBlock>>>(device_arr, elementSize);
cudaDeviceSynchronize();
cudaMemcpy(host_output_arr, device_arr, sizeof(int) * elementSize, cudaMemcpyDeviceToHost);

// Free
cudaFree(device_arr);
cudaFreeHost(host_input_arr);
cudaFreeHost(host_output_arr);

```

## Zero-copy memory

![image](https://hackmd.io/_uploads/r1xiLlx58p.png =40%x)

```c=
// Allocation
int *host_input_arr;
cudaHostAlloc((void**)&host_input_arr, sizeof(int) * elementSize, cudaHostAllocMapped);
cudaHostGetDevicePointer((void **)&device_input_arr,  (void *) host_input_arr , 0);

// Kernel Function
vecMultiply<<<blockSize, threadsPerBlock>>>(device_input_arr, elementSize);
cudaDeviceSynchronize();

// Free
cudaFree(device_input_arr);
```

## Unified Virtual Addressing

![image](https://hackmd.io/_uploads/S139WgcI6.png =40%x)

```c=
// Allocation
int *host_input_arr;
cudaMallocManaged((void**)&host_input_arr, sizeof(int) * elementSize);

// Kernel Function
vecMultiply<<<blockSize, threadsPerBlock>>>(host_input_arr, elementSize);
cudaDeviceSynchronize();

// Free
cudaFree(host_input_arr);
```

## Comparison
|                |   Pageable   |      Pinned      | Zero-copy | Unified Memory Access |
|:--------------:|:------------:|:----------------:| --------- |:-------:|
|   GPU cached   |    Y          |  Y                |      N     |     Y    |
| CPU allocation |   `malloc`   | `cudaHostAlloc` |        `cudaHostAlloc`</br>   |         |
| GPU allocaion  | `cudaMalloc` |   `cudaMalloc`   |         N/A  |         |
|      Copy      | `cudaMemcpy` |   `cudaMemcpy`</br>`cudaMemcpyAsync`   |        `cudaHostGetDevicePointer`   |         |
|      Pros      |      - Easy to use and manage.<br>- Abundant compared to other types.<br>- Managed automatically by OS.        |        - Fast data transfer to GPU.<br>- Allows asynchronous operations.<br>- Avoids paging overhead.         |   - Direct GPU access to host memory.<br>- No need to explicitly copy data.   |   - Simplifies memory management.<br>- Automatically migrates data between host and device.  |
|      Cons      |   - Slowest for GPU access due to copying overhead.<br>- Data might be paged out, causing further delays.           |         - Scarce resource; can lead to system performance issues if overused.<br>- Requires manual management.         |       - Slower than pinned memory for large data sets.<br>- May lead to performance issues in some architectures.   |  - Performance can be unpredictable.<br>- May not be optimal for all workloads or hardware configurations.  |

# Reference
* [EVERYTHING YOU NEED TO KNOW ABOUT UNIFIED MEMORY](https://on-demand.gputechconf.com/gtc/2018/presentation/s8430-everything-you-need-to-know-about-unified-memory.pdf)
