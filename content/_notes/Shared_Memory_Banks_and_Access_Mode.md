---
title: Shared Memory Banks and Access Mode
tags: [CUDA]

---

# Configurations of Shared Memory
* Each SM has 64 KB of on-chip memory. The shared memory and L1 cache share this hardware resource.
*  For Kepler devices, L1 cache is used for register spills.
## Per-device Configuration
* API: `cudaDeviceSetCacheConfig`

## Per-kernel Configuration
* A per-kernel configuration can also override the device-wide setting.
* API: `cudaFuncSetCacheConfig`

# Configuration of Bank Size
* A large bank size may yield higher bandwidth for shared memory access, but may result in more bank conflicts depending on the application’s shared memory access patterns.
* You can use the following function to set a new bank size on devices with configurable shared memory banks: `cudaDeviceSetSharedMemConfig()`