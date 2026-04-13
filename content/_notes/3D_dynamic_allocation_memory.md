---
title: 3D dynamic allocation memory


---

# 3D dynamic allocation memory
###### tags:  `C`

## Memory allocation
```c=
#include <stdlib.h>
#include <stdio.h>
#include "include/macro.h"


void ***calloc_3d_array (size_t nt, size_t nr, size_t nc, size_t size)
{
  void ***array;
  size_t i, j;

  if ((array = (void ***) calloc (nt, sizeof (void **))) == NULL)
    {
      printf ("[calloc_3d] failed to allocate memory for %d 1st-pointers\n", (int) nt);
      return NULL;
    }

  if ((array[0] = (void **) calloc (nt * nr, sizeof (void *))) == NULL)
    {
      printf ("[calloc_3d] failed to allocate memory for %d 2nd-pointers\n", (int) (nt * nr));
      free ((void *) array);
      return NULL;
    }

  for (i = 1; i < nt; i++)
    {
      array[i] = (void **) ((unsigned char *) array[0] + i * nr * sizeof (void *));
    }

  if ((array[0][0] = (void *) calloc (nt * nr * nc, size)) == NULL)
    {
      printf ("[calloc_3d] failed to alloc. memory (%d X %d X %d of size %d)\n",
      (int) nt, (int) nr, (int) nc, (int) size);
      free ((void *) array[0]);
      free ((void *) array);
      return NULL;
    }
  for (j = 1; j < nr; j++)
    {
      array[0][j] = (void **) ((unsigned char *) array[0][j - 1] + nc * size);
    }
for (i = 1; i < nt; i++)
    {
      array[i][0] = (void **) ((unsigned char *) array[i - 1][0] + nr * nc * size);
      for (j = 1; j < nr; j++)
        {
          array[i][j] = (void **) ((unsigned char *) array[i][j - 1] + nc * size);
        }
    }

  return array;
}
```
## Free memory
```c=
void free_3d_array(void ***array){

  free(array[0][0]);
  free(array[0]);
  free(array);
}
```