---
title: Note on CUDA programming
---
# Note on CUDA programming


CUDA execution model
---
- [Programming Model]({{ "/notes/Programming_Model" | relative_url }})
- [Compilation Workflow]({{ "/notes/Compilation_with_NVCC" | relative_url }})



Global memory
---
- [Memory architecture]({{ "/notes/Memory_architecture" | relative_url }})
- [Memory management]({{ "/notes/Memory_management_global_memory" | relative_url }})
- [Memory access pattern]({{ "/notes/Memory_access_pattern" | relative_url }})

Shared memory and constant memory
---
- [Configurations of Shared Memory]({{ "/notes/Shared_Memory_Banks_and_Access_Mode" | relative_url }})
- [Bank conflict]({{ "/notes/Bank_Conflict" | relative_url }})
- [Synchronization of Shared Memory]({{ "/notes/Synchronization_of_Memory" | relative_url }})
- [Warp Shuffles]({{ "/notes/Warp_Shuffles" | relative_url }})


Texture memory
---
- [Texture Memory]({{ "/notes/Texture_Memory" | relative_url }})

Streams and concurrency
---
- [Stream and Concurrency]({{ "/notes/Stream_and_Concurrency" | relative_url }})
- [Triple Buffering]()


Worked Examples
---
- [Parallel Reduction]({{ "/notes/Parallel_Reduction" | relative_url }})
- [Matrix Addition]({{ "/notes/Matrix_Addition" | relative_url }})
- [Matrix Transpose]({{ "/notes/Matrix_Transpose" | relative_url }})
- [Matrix Multiplcation]({{ "/notes/Matrix_Multiplcation" | relative_url }})


Tensor core
---
- [Tensor core]({{ "/notes/Tensor_core" | relative_url }})

Profiling
---
- [Calculation of Warp Occupancy]({{ "/notes/Calculation_of_Warp_Occupancy" | relative_url }})
- [Performance tuning]({{ "/notes/Performance_tuning" | relative_url }})
- [Nsight compute]({{ "/notes/Nsight_compute" | relative_url }})
- [Nsight system]({{ "/notes/Nsight_system" | relative_url }})

Debugging
---
- [cuda-gdb]({{ "/notes/cuda-gdb" | relative_url }})

Mannual
---
[nvcc](https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/)
[CUDA C++ Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html)
[CUDA C++ Best Practices Guide](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html)
[Parallel Thread Execution ISA Version 8.5](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html)
[CUDA runtime API](https://docs.nvidia.com/cuda/cuda-runtime-api/index.html)
[CUDA driver API](https://docs.nvidia.com/cuda/cuda-driver-api/index.html)
[Thrust](https://developer.nvidia.com/thrust)
[CUDA-GDB](https://docs.nvidia.com/cuda/cuda-gdb/index.html)
[Compute Sanitizer](https://docs.nvidia.com/compute-sanitizer/index.html)
[Nsight System](https://docs.nvidia.com/nsight-systems/index.html)
[Nsight compute](https://docs.nvidia.com/nsight-compute/index.html)
[Profiler](https://docs.nvidia.com/cuda/profiler-users-guide/index.html)
[CUDA binary utilities](https://docs.nvidia.com/cuda/cuda-binary-utilities/index.html)

Miscellaneous
---
- [Nvidia Technical Blog]({{ "/notes/Nvidia_Technical_Blog" | relative_url }})
- [CUDA FAQ]({{ "/notes/CUDA_FAQ" | relative_url }})
- [Syntax]({{ "/notes/Syntax" | relative_url }})
- [Thread indexing cheatsheet]({{ "/notes/Thread_indexing_cheatsheet" | relative_url }})
- [Trouble shooting]({{ "/notes/Trouble_shooting" | relative_url }})
- [NVIDIA A10]({{ "/notes/NVIDIA_A10" | relative_url }})
- [kriegalex](https://github.com/kriegalex/wrox-pro-cuda-c/tree/master)
- [HangJie720 ](https://github.com/HangJie720/Professional-CUDA-C-Programming/tree/master)
- [deeplearning](https://github.com/deeperlearning/professional-cuda-c-programming)
- [Good articles](https://siboehm.com/)
