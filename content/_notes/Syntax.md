---


---


# Syntax
![](https://i.imgur.com/ZgriOZ0.png)
* The `__device__` and `__host__` qualifiers can be used together, in which case the function is compiled for both the host and the device.

# API
## `cudaMalloc`
`cudaError_t cudaMalloc ( void** devPtr, size_t size )`
* This function allocates a linear range of ***global*** memory with the specified size in bytes.


## `cudaMemcpy`
`cudaError_t cudaMemcpy ( void* dst, const void* src, size_t count, cudaMemcpyKind kind )`
* `kind` takes one of the following types:
    * `cudaMemcpyHostToHost`
    * `cudaMemcpyHostToDevice`
    * `cudaMemcpyDeviceToHost`
    * `cudaMemcpyDeviceToDevice`

This function exhibits ***synchronous*** behavior because the host application blocks until `cudaMemcpy` returns and the transfer is complete.

## `cudaMemset`
## `cudaFree`
## `__syncthreads`

## Thread configuration
1D block: `dim3 BlockDim(int Ntx)`
2D block: `dim3 BlockDim(int Ntx, int Nty)`
2D block: `dim3 BlockDim(int Ntx, int Nty, int Ntz)`

1D grid: `dim3 GridDim(int Nbx)`
2D grid: `dim3 GridDim(int Nbx, int Nby)`
2D grid: `dim3 GridDim(int Nbx, int Nby, int Nbz)`

`Nt[xyz]` is the number of threads in x/y/z direction.
`Nb[xyz]` is the number of blocks in x/y/z direction.


## Shared memory
### Dynamic shared memory
### Static shared Memory
See [here](https://developer.nvidia.com/blog/using-shared-memory-cuda-cc/#:~:text=Shared%20memory%20is%20a%20powerful,mechanism%20for%20threads%20to%20cooperate.)
## Kernel call
### Declaration
```c=
__global__ void Kernel(argument list)
```
### Do it
```c=
Kernel<<<dim3 GridDim, dim3 BlockDim, size_t Ns, cudaStream_t S>>>(argument list)
```
* `Ns` specifies the number of bytes in shared memory that is dynamically allocated per block for this call in addition to the statically allocated memory; this dynamically allocated memory is used by any of the variables declared as an external array as mentioned in __shared__; Ns is an optional argument which defaults to 0;
* `S` specifies the associated stream, default is 0.
:::info
A kernel call is ***asynchronous*** with respect to the host thread. After a kernel is invoked, control returns to the host side immediately. You can call the following function to force the host application to wait for all kernels to complete. `cudaError_t cudaDeviceSynchronize(void)`
:::

:::info
1. Access to device memory only
2. Must have `void` return type
3. No support for a variable number of arguments
4. No support for `static` variables
5. No support for function pointers
6. Exhibit an ***asynchronous*** behavior
:::

# Built-in variables
## `gridDim`
## `blockIdx`
## `blockDim`
## `threadIdx`
## `warpSize`
## Handling errors
```c=
#define CHECK(call)                                                        \
{                                                                          \
   const cudaError_t error = call;                                         \
   if (error != cudaSuccess)                                               \
   {                                                                       \
       printf("Error: %s:%d, ", __FILE__, __LINE__);                       \
       printf("code:%d, reason: %s\n", error, cudaGetErrorString(error));  \
       exit(1);                                                            \
   }                                                                       \
}
```
Built-in API usage:
```c=
CHECK(cudaMemcpy(d_C, gpuRef, nBytes, cudaMemcpyHostToDevice));
```
Kernel call usage:
```c=
kernel_function<<<grid, block>>>(argument list);
CHECK(cudaDeviceSynchronize());
```

## Timing with CPU timer
```c=
double cpuSecond() {
    struct timeval tp;
    gettimeofday(&tp,NULL);
    return ((double)tp.tv_sec +(double)tp.tv_usec*1.e-6);
}
```
Timing kernel:
```c=
double iStart = cpuSecond();
kernel_name<<<grid, block>>>(argument list);
cudaDeviceSynchronize();
double iElaps = cpuSecond() - iStart;
```