---
title: Linear Memory
tags: [CUDA]

---

# Linear Memory
* Linear memory is typically allocated using `cudaMalloc()` and freed using `cudaFree()` and data transfer between host memory and device memory are typically done using `cudaMemcpy()`.
* Linear memory can also be allocated through `cudaMallocPitch()` and `cudaMalloc3D()`. These functions are recommended for allocations of 2D or 3D arrays as it makes sure that the allocation is appropriately padded to meet the alignment requirements described in Device Memory Accesses, therefore ensuring best performance when accessing the row addresses or performing copies between 2D arrays and other regions of device memory (using the `cudaMemcpy2D()` and `cudaMemcpy3D()` functions).


# L2 Cache Access Management

## L2 cache Set-Aside for Persisting Accesses
* When a CUDA kernel accesses a data region in the global memory repeatedly, such data accesses can be considered to be *persisting*.
* If the data is only accessed once, such data accesses can be considered to be *streaming*.
* A portion of the L2 cache can be set aside to be used for persisting data accesses to global memory.

```cudaa=
cudaGetDeviceProperties(&prop, device_id);
size_t size = min(int(prop.l2CacheSize * 0.75), prop.persistingL2CacheMaxSize);
cudaDeviceSetLimit(cudaLimitPersistingL2CacheSize, size); 
```
## L2 Policy for Persisting Accesses
### L2 Access Properties
### L2 Persistence Example
### Reset L2 Access to Normal
### Manage Utilization of L2 set-aside cache
### Query L2 cache Properties
### Control L2 Cache Set-Aside Size for Persisting Memory Access