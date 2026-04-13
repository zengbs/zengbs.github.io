---
title: Optimization Techniques
tags: [CUDA]

---

# Memory Access

## Constant memory
Store read-only data in constant memory, and broadcast this data to multiple threads.
## Warp
1. Using warp shuffle function
## Shared memory
1. We can decrease the amount of shared memory per block to increase resident blocks per SM, mitigating the impact of stalled warps due to `__syncthreads()`.
2. Avoid back conflicting
    * Padding
    * reordering data
    * remap threads to data
## Register
1. Using pointer arithmetic
2. Minimizing temporary variables
    * Rewriting arithmetic operations
    * Moving temporary variables to shared memory
    * Packing small types into larger types. (e.g., pack 4 bytes into 1 integer)
    * Refraining from storing values that can be recalculated

## Global memory
1. Coalesced Access
     * Use "structure of array" instead of "array of structure".
3. Compress data


# Irregularity
## Loop unrolling 
Loop unrolling can increase the opportunity for ILP(why?)
1. Explicitly duplicating the body of the loop)
2. Macros
3. C++ template
4. compiler directives

## Reduce branch divergence
1. replacing them with arithmetic instructions
2. Using lookup-tables
3. kernel fission


# Balancing