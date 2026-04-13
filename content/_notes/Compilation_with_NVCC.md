---
title: Compilation with NVCC


---

![image](https://hackmd.io/_uploads/ry96CCPHA.png =80%x)

---
![image](https://hackmd.io/_uploads/HynXl1drR.png =80%x)

---
![cuda-compilation-from-cu-to-cu-cpp-ii-1](https://hackmd.io/_uploads/BJt_yGOSC.png =70%x)


![image](https://hackmd.io/_uploads/S1cSbMuBA.png =60%x)

![image](https://hackmd.io/_uploads/rJUiZzuSR.png =60%x)


# Just-In-Time Compilation

# Binary Compatibility
Binary compatibility is guaranteed from one minor revision to the next one, but not from one minor revision to the previous one or across major revisions.

e.g., `nvcc -code=sm_80`: generate `cubin` object for CC 8.0.

# PTX Compatibility
The `-arch` compiler option specifies the compute capability that is assumed when compiling C++ to PTX code.

e.g., `nvcc -arch=compute_50`: generate RTX code.