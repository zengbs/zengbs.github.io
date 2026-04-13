---
title: 2D dynamic memory allocations


---

# 2D dynamic memory allocations
###### tags:  `C`

## Method 1
* ### Memory allocation
![](https://i.imgur.com/eg8zFKX.png =300x)
```c=
int **array = (int **)malloc(nrows * sizeof(int *));

for (int i=0;i<nrows;i++) 
  array[i] = (int *) malloc(ncolumns * sizeof(int));
```
* ### Free memory
```c=
for (int i=0;i<nrows;i++) free((void*)array[i]);

free((void*)array);
```

## Method 2
### Reference: [Athena](https://www.astro.princeton.edu/~jstone/Athena/doxygen/html.with_source/ath__array_8c_source.html)
* ### Memory allocation
![](https://i.imgur.com/X3mbj1U.png)
Note: we shall retuen a non-void data type to avoid undefined behavior as `void**` is not a generic pointer.
```c=
typedef int32_t mytype;
   
mytype** calloc_2d_array(size_t nc, size_t nr) 
{  
  mytype **array;
    
  array = (mytype**)calloc(nr,sizeof(mytype*));
   
  array[0] = (mytype*)calloc(nr*nc,sizeof(mytype));
   
  for(size_t i=1; i<nr; i++)  array[i] = array[0] + i*nc;
   
  return array;
}
```

## Free memory
```c=
void free_2d_array(mytype **array)
{
   free(&array[0][0]);
   free(array);
} 
```

## Method 3 (pointer to the first element in 2D array)
* ### Memory allocation
```c=
int *array = (int *)malloc(nrows * ncolumns * sizeof(int));
```
* ### Free memory
```c=
free(array);
```

## Method 4 (A pointer to an array of `NCOLUMNS` integers)
* ### Memory allocation
```c=
int (*array)[NCOLUMNS] = (int(*)[NCOLUMNS])malloc(nrows*sizeof(*array));
int (*array)[NCOLUMNS] = (int(*)[NCOLUMNS])malloc(nrows*NCOLUMNS*sizeof(int));
```
* ### Free memory

```c=
free(array);
```

## Method 5 (a pointer to whole 2D array)
* ### Memory allocation
```c=
int (*array)[NROWS][NCOLUMNS] = (int(*)[NROWS][NCOLUMNS])malloc(sizeof(*array));
int (*array)[NROWS][NCOLUMNS] = (int(*)[NROWS][NCOLUMNS])malloc(NROWS*NCOLUMNS*sizeof(int));
```
* ### Free memory

```c=
free(array);
```

## Comparison of various methods
|          | Contiguous memory |      Access array       | Number of allocations |
| -------- |:-----------------:|:-----------------------:|:---------------------:|
| Method 1 |         No        |      `array[i][j]`      |       `nrows`+1       |
| Method 2 |        Yes        |      `array[i][j]`      |           2           |
| Method 3 |        Yes        | `*(array+i*ncolumns+j)` |           1           |
| Method 4 |        Yes        |      `array[i][j]`      |           1           |
| Method 5 |        Yes        |    `(*array)[i][j]`     |           1           |


## Pass `array[]` to a function
|          |                Prototype                 |    Do it     |
| -------- |:----------------------------------------:|:------------:|
| Method 1 |         `void fun(int **array)`          | `fun(array)` |
| Method 2 |         `void fun(int **array)`          | `fun(array)` |
| Method 3 |          `void fun(int *array)`          | `fun(array)` |
| Method 4 |    `void fun(int(*array)[NCOLUMNS])`     | `fun(array)` |
| Method 5 | `void fun(int(*array)[NROWS][NCOLUMNS])` | `fun(array)` |
