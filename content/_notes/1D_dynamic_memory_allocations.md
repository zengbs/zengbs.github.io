---


---

# 1D dynamic memory allocations
###### tags:  `C`


## Method 1 (pointer to the first element in 1D array)
* ### Memory allocation

  ```c=
  int *array = (int *)malloc(size * sizeof(int));
  ```

* ### Free memory

  ```c=
  free(array);
  ```



## Comparison of various methods
|          | Contiguous memory |        Access array         | Number of allocations |
| -------- |:-----------------:|:---------------------------:|:---------------------:|
| Method 1 |        Yes        | `*(array+i)`<br/>`array[i]` |           1           |



## Pass `array[]` to a function
|          |                Prototype                 |    Do it     |
| -------- |:----------------------------------------:|:------------:|
| Method 3 |          `void fun(int *array)`          | `fun(array)` |
