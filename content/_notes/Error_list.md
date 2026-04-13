---
title: Error list


---

# Error list
###### tags: `C`
# Compile-time error


## 1
```
Compilation fails with "relocation R_X86_64_32 against `.rodata.str1.8' can not be used when making a shared object"
```
Compile the dependent library as shared library instead of static.

## 2

* `foo.cpp:3:10: fatal error: gsl/gsl_math.h: No such file or directory #include <gsl/gsl_math.h>`

  * See if `INCLUDE_PATH` is defined as path of GSL headers.
  * See if GSL is installed.
  * See if `INCLUDE_PATH` is added at compile step. i.e. `$gcc -I$(INCLUDE_PATH) foo.c`
    
* `foo.c:62:4: warning: implicit declaration of function ‘bar’`
  * See if `bar()` is declared as prototype in the header or at the top of file.

# Link-time error
* `foo.c:568: undefined reference to foo()`

  * See if `foo.o`(shared library) is compiled successfully.
  * See if the definetion of `foo()` is dropped by preprocessor.
  * See if execute `make clean` before `make`.
  * See if `foo.o` is in target list at linking step. (i.e. `$gcc foo.o`)

* `foo.cpp:138: undefined reference to 'gsl_root_fdfsolver_root'`

  * See if `LIBRARY_PATH` is defined as path of GSL library.
  * See if GSL is installed.
  * See if `LIBRARY_PATH` is added at linking step. (i.e.`gcc -L$(LD_LIBRARY_PATH) foo.o`)

* `/usr/bin/ld: cannot find -lfoo`
    * See if `LIBRARY_PATH` is added at linking step. (i.e.`gcc -L$(LIBRARY_PATH) foo.o`)
# Run-time error

