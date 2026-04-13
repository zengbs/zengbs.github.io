---
title: CUDA FAQ


---

###### tags:  `CUDA`

# CUDA FAQ
1. What do you mean by Cuda core?
<span style="color:blue"></span>
3. What are the components of gpu?
<span style="color:blue"></span>
4. What are the different memories used in gpu?
<span style="color:blue">Register: </span>
<span style="color:blue">Shared memory:</span>
<span style="color:blue">Local memory:</span>
<span style="color:blue">Global memory:</span>
<span style="color:blue">Constant memory:</span>
<span style="color:blue">Texture memory:</span>
5. What kind of memory is particular to each thread?
<span style="color:blue">Registers.</span>
6. Which memory is used by all threads in a single block?
<span style="color:blue">Shared memory.</span>
7. What is the use of Constant memory?
<span style="color:blue">Constant Memory is used to store constant values. The advantage of having separate Constant Memory is to ==reduce latency==. It is used in only those situation, when multiple threads has to access same value. Suppose there are 32 threads in one block. Let all of them are using the same variable. Hence there will be 32 accesses from global memory. Now if we store the variable in constant memory. 
    1. First thread will access the value of a variable
    2. First thread will broadcast this value to other threads in half warp.
    3. This value will be saved in a cache and will be provided to the threads of other half warp.
Hence total accesses will be just 1 instead of 32.</span>
8. What is the use of Texture memory?
<span style="color:blue">Texture memory is again used to reduce the latency. Texture memory is used in a special case. Consider an image. When we access a particular pixel, there are more chances that we will access surrounding pixels. Such a group of values which are accessed together are saved in texture memory.</span>
11. What do you mean by bock and grid in Cuda?
<span style="color:blue">Thread is a single instance of execution. 
    1. A group of threads is called a Block.
    2. A group of blocks is called a Grid. 
    3. One Grid is generated for one Kernel and on one GPU. However, mutiple kernels can run on a GPU at the same time(i.e., concurrent kernel), in this case, a GPU has multiple grids.</span>
12. What is the advantage of shared memory in CUDA?
<span style="color:blue">Shared memory is also used to reduce the latency (memory access delay). How? See, Global memory is very big in size as compared to shared memory. So definitely, search time for a location of variable is lesser for shared memory compared to global memory.</span>
14. What is warp in CUDA?
<span style="color:blue">CUDA employs a Single Instruction Multiple Thread (SIMT) architecture to manage and execute threads in groups of 32 called warps. All threads in a warp execute the same instruction at the same time. Each thread has its own instruction address counter and register state, and carries out the current instruction on its own data.</span>
15. What is the use of cudaMalloc() function and what arguments does it accept?
<span style="color:blue"></span>
16. What is the use of cudaMemcpy() function and what arguments does it accept?
<span style="color:blue"></span>
17. What is the use of cudaFree() function and what arguments does it accept?
<span style="color:blue"></span>
18. What is kernel in Cuda?
<span style="color:blue"></span>
19. How kernel is defined in Cuda?
<span style="color:blue"></span>
20. How to define a kernel which is called from another kernel?
<span style="color:blue"></span>
21. How kernels are called from main() function?
<span style="color:blue"></span>
22. What is dim3 in Cuda?
<span style="color:blue"></span>
23. How can we define a multi dimensional structure of grid?
<span style="color:blue"></span>
24. How can we define a multi dimensional structure of block?
<span style="color:blue"></span>
25. What are the keywords used for finding block id and thread id?
<span style="color:blue"></span>
26. What are keywords used for block size and grid size?
<span style="color:blue"></span>
27. Name any Nvidia gpu card which consists of two gpus?
<span style="color:blue"></span>
28. How to find out number of gpus in your system?
<span style="color:blue"></span>
29. How to find out id of current gpu on your system?
<span style="color:blue"></span>
30. What are the different properties of gpu?
<span style="color:blue"></span>
31. How to find out properties of gpu?
<span style="color:blue"></span>
32. Which properties of gpu are used to find its compute capability?
<span style="color:blue"></span>
33. How to set any gpu as current gpu when its id is given?
<span style="color:blue"></span>
34. What is the use of cudaChooseDevice() function and what arguments does it accept?
<span style="color:blue"></span>
35. What is the use of memset() function and what arguments does it accept?
<span style="color:blue"></span>
51. How many different kind of memories are in a GPU ?
<span style="color:blue"></span>
52. What means coalesced / uncoalesced?
<span style="color:blue"></span>
53. Can you implement a matrix transpose kernel?
<span style="color:blue"></span>
54. What is a warp ?
<span style="color:blue"></span>
55. How many warps can run simultaneously inside a multiprocessor?
<span style="color:blue"></span>
56. What is the difference between a block and a thread ?
<span style="color:blue"></span>
57. Can thread communicate between them? and blocks ?
<span style="color:blue"></span>
58. Can you describe how works a cache?
<span style="color:blue"></span>
59. What is the difference between shared memory and registers?
<span style="color:blue"></span>
60. Which algorithms perform better on the gpu? data bound or cpu bound?
<span style="color:blue"></span>
61. Which steps will you perform to port of an application to cuda ?
<span style="color:blue"></span>
62. What is a barrier ?
<span style="color:blue"></span>
63. What is a Stream ?
<span style="color:blue"></span>
64. Can you describe what means occupancy of a kernel?
<span style="color:blue"></span>
65. What means structure of array vs array of structures?
<span style="color:blue"></span>
# Advanced
1. matrix multiplication
2. parallel reduction
3. Warp divergence
4. global memory coalesce
5. shared memory bank conflict
# Reference
* [Interview Questions on CUDA Programming](https://www.comrevo.com/2017/05/interview-questions-on-cuda-programming.html)
* [GPU基础知识](https://zhuanlan.zhihu.com/p/33518322)
* [GPU programming interview](https://carpentries-incubator.github.io/lesson-gpu-programming/)