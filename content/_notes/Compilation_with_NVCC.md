---


---

<img src="https://hackmd.io/_uploads/ry96CCPHA.png" width="80%">

---
<img src="https://hackmd.io/_uploads/HynXl1drR.png" width="80%">

---
<img src="https://hackmd.io/_uploads/BJt_yGOSC.png" width="70%" alt="cuda-compilation-from-cu-to-cu-cpp-ii-1">


<img src="https://hackmd.io/_uploads/S1cSbMuBA.png" width="60%">

<img src="https://hackmd.io/_uploads/rJUiZzuSR.png" width="60%">


# Just-In-Time Compilation

# Binary Compatibility
Binary compatibility is guaranteed from one minor revision to the next one, but not from one minor revision to the previous one or across major revisions.

e.g., `nvcc -code=sm_80`: generate `cubin` object for CC 8.0.

# PTX Compatibility
The `-arch` compiler option specifies the compute capability that is assumed when compiling C++ to PTX code.

e.g., `nvcc -arch=compute_50`: generate RTX code.