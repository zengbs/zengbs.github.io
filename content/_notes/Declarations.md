---
title: Declarations
tags: [C]

---

###### tags: `C`

# Declarations

# Must-read
* [Clockwise/Spiral rule](http://c-faq.com/decl/spiral.anderson.html)
* [Interpreting More Complex Declarators](https://docs.microsoft.com/en-us/cpp/c-language/interpreting-more-complex-declarators?view=msvc-170)
* [Complex pointer declarations](https://stackoverflow.com/questions/46856869/complex-pointer-declarations)
* [C Operator Precedence](https://en.cppreference.com/w/c/language/operator_precedence)
  1. `()` Parentheses
  2. `()` Function call
  3. `[]` Array subscripting 
  4. `*` Indirection (dereference)
# Array
* `double x[3];`
   An array of three `double` values.
* `double *x[3];`
   An array of three pointers to `double`.
* `double (*x)[3];`
   A pointer to an array of three `double`.
```c=
  int (*ptr)[2];
  int array[2] = {1, 20};
  
  ptr = &array;
  
  printf("%d\n", *(*ptr+0));
  printf("%d\n", *(*ptr+1));
```


# Function pointer
* `int func(int)`
   <span style="color:blue">A function that takes an `int` as an argument and returns an `int`.</span>
* `int *func(int)`
   <span style="color:blue">A function that takes an `int` as argument and returns a pointer to an `int`.</span>
* `int (*func)(int)`
   <span style="color:blue">A pointer to the function that takes `int` as argument and returns `int`.</span>
* `int *func(int)[3]`
   <span style="color:blue">A function that takes `int` as argument and returns a pointer to an array of three pointers to `int`.</span>
* `int (*func[10])(int)`
   <span style="color:blue">An array of 10 pointers to a function that takes `int` as argument and returns `int`.</span>
* `int (*func(int))(double)`
<span style="color:blue">A pointer to a function that takes `int` as argument and returns a pointer to another function that takes `double` as argument and returns `int`.</span>
* `int (*(*func)[3])(int, int)`
* `void (*signal(int, void (*fp)(int)))(int)`
   1. <span style="color:blue">`signal` is a function passing `int` and the pointer `fp` returning a pointer to a function passing `int` returning `void`.</span>
   2. <span style="color:blue">`fp` is a pointer to a function passing `int` returning `void`.</span>
* `unsigned int *(* const *name[5][10] ) ( void )`
* `double ( *var( double (*)[3] ) )[3]`
* `int *(* const *name[5][10] ) ( void )`
* `char *( *(*var)() )[10]`
   <span style="color:blue">A pointer to a function returns a pointer to an array of 10 pointers to `char`.</span>
* `char *(*func)( int, float *)`
   <span style="color:blue">A pointer to the function that takes `int` and `float*` as arguments and returns the pointer to a `char`.</span>

# Pointer
* `double *x;`
   A pointer to `double`.
* `double **x;`
   A pointer to pointer to `double`.

## The pointer itself is constant
A constant pointer to `char`. For example:
* `(char*) const pContent;`
* `const (char*) pContent;`
 
## The value pointed by a pointer is a constant
A pointer to constant `char`.
* `const char *pContent;`
* `char const *pContent;`

## The value pointed by a pointer and the pointer itself are constant
A constant pointer to constant `char`.
* `const char* const pContent;`




# Use `typedef` to simplify function pointer
See [here](https://riptutorial.com/c/example/31818/typedef-for-function-pointers).
```c=
// prototype
void (*signal(int sig, void (*func)(int)))(int);

// typedef
typedef void (*SigCatcher)(int);

// simplfied delaration
SigCatcher signal( int sig, SigCatcher func );
```


```c=
// prototype
void(*(*papf)[3])(char *);
// papf is a pointer to an array of 3 pointers to a function passing char* returning void

// typedef
typedef void (*pf)(char*);
// pf is a pointer to a function passing char* and returning void

// simplified declaration
pf (*papf)[3];
```
---
## Usage
```c=
#include <stdio.h>

int add(int a, int b) {
  return a+b;
}


int main() {

  int (*fptr1)(int a, int b);
  fptr1 = add;
  printf("fptr1(3,5)=%d\n", fptr1(3,5));

  int (*fptr2)(int a, int b);
  fptr2 = &add;
  printf("(*fptr2)(3,5)=%d\n", (*fptr2)(3,5));


  typedef int (*fptr_t)(int a, int b);
  fptr_t fptr3 = add;
  fptr3 = add;
  printf("op(3,5)=%d\n", fptr3(3,5));

}
```