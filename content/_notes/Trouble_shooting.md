---


---


# Trouble shooting

## The reasons for a CUDA kernel launch fail
1. If there are insufficient registers or shared memory on each SM to process at least one block, the kernel launch will fail.

## `compute-sanitizer`

Memory check:
compute-sanitizer  --tool  memcheck  ./a.out

Shared memory race check:
compute-sanitizer  --tool  racecheck  ./a.out

Initialization check:
compute-sanitizer --tool   initcheck  ./a.out

Synchronization check:
compute-sanitizer --tool   synccheck  ./a.out

# Reference
[NVIDIA/compute-sanitizer-samples](https://github.com/NVIDIA/compute-sanitizer-samples)