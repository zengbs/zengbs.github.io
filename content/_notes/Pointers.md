---


---


# Pointers

`&`: address-of
`*` : dereference/indirection


* `*(ptr+3)`: the pointer `ptr` advances three times the size of the pointed-to element.
    * Compiler shall know the data type of `ptr` before advancing.
* `void*` is a generic pointer type for objects (i.e. only data, function pointer exclusive).
> A pointer to void may be converted to or from a pointer to any object type. A pointer to any object type may be converted to a pointer to void and back again; the result shall compare equal to the original pointer.
* The standard does not guarantee compiler can convert `void**` to any pointer to pointer to any data type other than `void`. [See here.](http://c-faq.com/ptrs/genericpp.html)
* Any `void **` value you play with must be the address of an actual `void *` value somewhere.
* A pointer to `void` will have the same representation and memory alignment as a pointer to `char`.
* A pointer to `void` will never be equal to another pointer. However, two `void` pointers assigned a `NULL` value will be equal.
* Any pointer can be assigned to a pointer to `void`. It can then be cast back to its original pointer type. When this happens the value will be equal to the original pointer value.


## Function pointer


## FAQ

1. <span style="color:blue">I have a `char *` pointer that happens to point to some `int`s, and I want to step it over them. Why doesn't `((int *)p)++;` work?</span> ([Origin](http://c-faq.com/ptrs/castincr.html))
Cast conversion yields an `rvalue`, which cannot be assigned to, or incremented with `++`.
a. `p = (char *)((int *)p + 1);`
b. `p += sizeof(int);`
c. `int *ip = (int *)p; p = (char *)(ip + 1);`

2. <span style="color:blue">Why can't I perform arithmetic on a `void *` pointer?</span> ([Origin](http://c-faq.com/ptrs/voidparith.html))
The compiler doesn't know the size of the pointed-to objects. Before performing arithmetic, convert the pointer either to char * or to the pointer type you're trying to manipulate

3. <span style="color:blue">I've got some code that's trying to unpack external structures, but it's crashing with a message about an ``unaligned access.'' What does this mean? The code looks like this: 

   ```c=
   struct mystruct {
      char c;
      long int i32;
      int i16;
   } s;
   
   char buf[7], *p;
   fread(buf, 7, 1, fp);
   p = buf;
   s.c = *p++;
   s.i32 = *(long int *)p;
   p += 4;
   s.i16 = *(int *)p;
   ```

4. <span style="color:blue">I have a function which accepts, and is supposed to initialize, a pointer: 

   ```c=
   void f(int *ip)
   {
      static int dummy = 5;
      ip = &dummy;
   }
   ```

<span style="color:blue">But when I call it like this:</span>
```c=
   int *ip;
   f(ip);
```
<span style="color:blue">the pointer in the caller remains unchanged.</span>
See [here.](https://hackmd.io/mQJCoGl4Qai_WmeCcJJcEw?view)

    
5. <span style="color:blue">Suppose I want to write a function that takes a generic pointer as an argument and I want to simulate passing it by reference. Can I give the formal parameter type `void **`, and do something like this? </span>

   ```c=
   void f(void **);
   double *dp;
   f((void **)&dp);
   ```

    
## Reference
[Everything you need to know about pointers in C](https://boredzo.org/pointers/)
[你所不知道的C語言：指標篇](https://hackmd.io/@sysprog/c-pointer#%E4%BD%A0%E6%89%80%E4%B8%8D%E7%9F%A5%E9%81%93%E7%9A%84C%E8%AA%9E%E8%A8%80%EF%BC%9A%E6%8C%87%E6%A8%99%E7%AF%87)

    
    
    
    
## Specifications

### 6.2.4 Storage durations of objects
> The value of a pointer becomes indeterminate when the object it points to (or just past) reaches the end of its lifetime.

See [Dangling pointer](https://en.wikipedia.org/wiki/Dangling_pointer).

```c=
#include <stdio.h>
#include <stdlib.h>

void foo(int **ptr){
   int a = 2;
   *ptr = &a;
}

int main(){
   int *ptr = malloc(sizeof(int));
   foo(&ptr);
   printf("%d\n", *ptr);
   return 0;
}
```

### 6.2.5 Types
> A *pointer* type may be derived from a function type or an object type, called the referenced type.

See [Usage of function pointers](https://hackmd.io/bESBSXqdSJa5H2OAI_1x_Q#Usage).
```c=
int add(int x, int y){ return x+y; }

int (*fptr)( int, int );
fptr = &add;
fptr = add;
```

```c=
int a = 1;
int *ptr = &a; 
```
> A pointer type describes an object whose value provides a reference to an entity of the referenced type.


> A pointer type derived from the referenced type T is sometimes called "pointer to T". The construction of a pointer type from a referenced type is called "pointer type derivation". A pointer type is a ***complete object type***.

> Arithmetic types and pointer types are collectively called *scalar types*. Array and structure types are collectively called *aggregate types*.

> Array, function, and pointer types are collectively called ***derived declarator types***. A ***declarator type derivation*** from a type $T$ is the construction of a derived declarator type from $T$ by the application of an array-type, a function-type, or a pointer-type derivation to $T$.

> A pointer to `void` shall have the same representation and [alignment requirements](https://en.cppreference.com/w/c/language/object#Alignment) as a pointer to a character type. Similarly, pointers to qualified or unqualified versions of compatible types shall have the same representation and alignment requirements. All pointers to structure types shall have the same representation and alignment requirements as each other. All pointers to union types shall have the same representation and alignment requirements as each other. Pointers to other types need not have the same representation or alignment requirements.
