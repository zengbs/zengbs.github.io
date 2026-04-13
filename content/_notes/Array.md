---
title: Array


---

# Array
###### tags:  `C`

Question: What's difference between array and pointer?

|                                                                            |    Static array    | Auto array  |       Variable-length array       |            Dynamic array             |            Static dynamic array             |
|:--------------------------------------------------------------------------:|:------------------:|:-----------:|:---------------------------------:|:------------------------------------:|:-------------------------------------------:|
|                                  Declare                                   | `static int a[5];` | `int a[5];` | `int size=5; int a[size];` | `int *a;a=malloc(size*sizeof(int));` | `static int *a;a=malloc(size*sizeof(int));` |
|                                   Scope                                    |                    |             |                                   |                                      |                                             |
|                                Memory block                                |                    |             |                                   |                                      |                                             |
| Can the array return to main function if it is declared in other function? |                    |             |                                   |                                      |                                             |

