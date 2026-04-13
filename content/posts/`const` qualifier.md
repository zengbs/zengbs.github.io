---
title: "`const` qualifier"
date: 2026-04-13T15:32:38+08:00
draft: false
---

---
title: '`const` qualifier'
tags: [CPP]

---

# Reference and `const`

## A reference to `const`
`const T&` can bind to a either l-value or r-value.
`const T&` can bind to a `const` l-value.
`T&` cannot bind to a `const` l-value and r-value.
`T&` can only bind to a l-value.
See [Reference](/czbMYeWBRAOpRXzgf_M4RQ).

# Pointer and `const`
A pointer to `const T` can point to plain `T`.
A pointer to `const T` can point to `const T`.
A pointer cannot point to `const T`.


## The pointer itself is constant
A constant pointer to `T`. For example:
* `T * const ptr`:
* `T * volatile * const * * ptr`:
   `ptr` is a pointer to pointer to const pointer to volatile pointer
 
## The value pointed by a pointer is a constant
A pointer to constant `T`.
* `T const *ptr` (recommended syntax):
   `ptr` is a pointer to const `T`
* `const T *ptr`

## The value pointed by a pointer and the pointer itself are constant
A constant pointer to constant `T`.
* `const T* const ptr;`

# Internal Linkage
`const` variables by default have **internal linkage**, meaning their scope is limited to the file in which they are defined. If using `const` across multiple files must use `extern` even on the definition.
Usage:
```c++
//header.h
extern const int var;
```
```c++
// main.cc
extern const int var = 2;
```

# `constexpr`
1. `constexpr` computes and creates a compile-time constant; `const` simply means that value cannot be changed.
2. `return` type and the type of each parameter must be a literal type.
3. function body must contain exactly one `return`.
4. `constexpr` functions are implicitly `inline`.
5. `constexpr` applies to the pointer, not the type to which the pointer points:
`constexpr int *q = nullptr`: `q` is a `const` pointer to `int`. 

# Copy `const` object

* Top-level const: the objet itself is `const`.
* Low-level const: the value which object points to is `const`.
    * I.e., the `const` in an expression without pointer or reference must be top-level.
### General Rule of `const` assignment
If the giver has a low-level const qualifier, then the receiver must also have a low-level const qualifier; all other conditions are allowed. (I.e., Always keep the information of low-level const)

![image](https://hackmd.io/_uploads/rJxxh4cYkl.png =60%x)



|        Type        | Top-level | Low-level |
|:------------------:|:---------:|:---------:|
|       `int`        |           |           |
|    `const int`     |   const   |           |
|    `int* const`    |   const   |           |
|    `const int*`    |           |   const   |
| `const int* const` |   const   |   const   |
|       `int*`       |           |           |
|       `int&`       |           |           |
|    `const int&`    |           |   const   |


# `decltype`
* When we apply `decltype` to an expression that is not a variable, we get the type that that expression yields.
* `decltype((variable))` is always a reference type.
* `decltype(variable)` is a reference type only if variable is a reference.
* `decltype(*pointer)` is always a reference type.
* `decltype` retains top-, low-level `const`, and reference from .