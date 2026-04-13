---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---

# Candidate functions
Candidate functions are the set of functions that (1) have the same name as the function being called, and (2) are visible (i.e., in scope and accessible) at the point of the call.


# Viable functions
From the set of candidate functions constructed for a given context (13.3.1), a set of viable functions is chosen, from which the best function will be selected by comparing argument conversion sequences for the best fit (13.3.3). The selection of viable functions considers relationships between arguments and function parameters other than the ranking of conversion sequences. 

First, to be a viable function, a candidate function shall have enough parameters to agree in number with the arguments in the list.
— If there are `m` arguments in the list, all candidate functions having exactly `m` parameters are viable.
— A candidate function having fewer than `m` parameters is viable only if it has an ellipsis in its parameter list (8.3.5). For the purposes of overload resolution, any argument for which there is no corresponding parameter is considered to ‘‘match the ellipsis’’ (13.3.3.1.3) .
— A candidate function having more than `m` parameters is viable only if the `(m+1)`–st parameter has a default argument (8.3.6). For the purposes of overload resolution, the parameter list is truncated on the right, so that there are exactly `m` parameters.

Second, for `F` to be a viable function, there shall exist for each argument an implicit conversion sequence (13.3.3.1) that converts that argument to the corresponding parameter of `F`. If the parameter has reference type, the implicit conversion sequence includes the operation of binding the reference, and the fact that a reference to non-const cannot be bound to an rvalue can affect the viability of the function (see 13.3.3.1.4).

```c++
#include <iostream>
#include <vector>
void manip( vector<int> & ) {std::cout<<"A\n"};
void manip( const vector<int> & )std::cout<<"B\n"};
vector<int> f();
extern vector<int> vec;
int main() {
   // manip( vector<int> & ) is selected
   manip( vec );
   
   // the argument is an rvalue, and that cannot be bound to lvalue reference
   // The only one viable function is the second one
   manip( f() );
}
```
```c++
#include<iostream>

void print( int& ){std::cout<<"B\n";};
void print( char ){std::cout<<"C\n";};

int main() {
   // The only viable function is print(char)
   print( 1 );
   return 0;
}
```
```c++
#include<iostream>

void print( int& ){std::cout<<"B\n";};
void print( int ){std::cout<<"C\n";};

int main() {
               // candidate functions: print(int&), print(int)
   print( 1 ); // viable functions: print(int)
               // C
   return 0;
}
```



```c++
#include<iostream>

void print( unsigned int ){std::cout<<"A\n";};
void print( char* ){std::cout<<"B\n";};
void print( char ){std::cout<<"C\n";};
class SmallInt { /* ... */ };

int main() {
   int ia = 1;
   int *ip = &ia;
   SmallInt si;
   print( ip ); // error: no viable function: no match
   print( si ); // error: no viable function: no match
   return 0;
}
```
```c++
void f();
void f( int );
void f( double );
void f( char*, char* );

int main() {
   // Two viable functions: f( int ) and f( double ) at here
   f(1);
   return 0;
}
```

```c++
char* format( int );
void g() {
   // global function format( int ) is hidden
   char* format( double );
   char* format( char* );
   
   // Only one viable function: format( double ) at here
   format(1.2);
}
```
```c++
namespace libs_R_us {
   int max( int, int );
   double max( double, double );
}

// using declaration
using libs_R_us::max;
char max( char, char );
void func()
{
   // the three max() functions are viable functions
   max( 87, 65 );
}
```
```c++
extern double min( double, double );
extern int min( char*, int );
void func()
{
   // one candidate function min( double, double )
   min( 87, 65 ); // calls min( double, double )
}
```

# Flowchart
![The best viable function](https://hackmd.io/_uploads/rymFKDxDex.jpg =70%x)

# The best viable functions
ICS = Implicit Conversion Sequence.

Define ICSi(F) as follows:
— if F is a static member function, ICS1(F) is defined such that ICS1(F) is neither better nor worse than ICS1(G) for any function G, and, symmetrically, ICS1(G) is neither better nor worse than ICS1(F); otherwise,
— let ICSi(F) denote the implicit conversion sequence that converts the i-th argument in the list to the type of the i-th parameter of viable function F. 13.3.3.1 defines the implicit conversion sequences and 13.3.3.2 defines what it means for one implicit conversion sequence to be a better conversion sequence or worse conversion sequence than another.

Given these definitions, a viable function F1 is defined to be a better function than another viable function F2 if ***for all arguments i***, ICSi(F1) is not a worse conversion sequence than ICSi(F2), and then
— for some argument j, ICSj(F1) is a better conversion sequence than ICSj(F2), or, if not that,
— F1 is a non-template function and F2 is a template function specialization, or, if not that,

— F1 and F2 are template functions, and the function template for F1 is more specialized than the template for F2 according to the partial ordering rules described in 14.5.5.2, or, if not that,

— the context is an initialization by user-defined conversion (see 8.5, 13.3.1.5) and the standard conversion sequence from the return type of F1 to the destination type (i.e., the type of the entity being initialized) is a better conversion sequence than the standard conversion sequence from the return type of F2 to the destination type.

# Example
## 1st Path
![The best viable function.-1](https://hackmd.io/_uploads/rkNL-FgDge.jpg =50%x)
```c++
#include<iostream>

void print( const int& ){std::cout<<"B\n";};
void print( int ){std::cout<<"C\n";};

int main() {
               // candidate functions: print(int), print(const int&)
   print( 1 ); // viable functions: print(int), print(const int&)
               // ambiguous
   return 0;
}
```
```c++
#include<iostream>

void print( int& ){std::cout<<"B\n";};
void print( int ){std::cout<<"C\n";};

int main() {
   int ia = 1;
                // candidate functions: print(int&), print(int)
   print( ia ); // viable functions: print(int&), print(int)
                // ambiguous
   return 0;
}
```
```c++
#include <iostream>

void foo(int, float,          int) { std::cout<<"A\n"; }
void foo(double, int,       short) { std::cout<<"C\n"; }

int main() {
    short s = 1;
    // error: ambiguous
    // --> since no candidate is better than others in "every" argument.
    foo(1, 1.0f, s);

    return 0;
}
```
## 2nd Path
![The best viable function.-2](https://hackmd.io/_uploads/SyqdZKgDel.jpg =50%x)
```c++
#include <iostream>

void foo(int, float,   int) { std::cout<<"A\n"; }
void foo(int, float, short) { std::cout<<"C\n"; }

int main() {
    unsigned short s = 1;

    foo(1, 1.0f, s);

    return 0;
}
```
```c++
#include <iostream>
void extract( void * ){std::cout<<"A\n";};
void extract( const void * ){std::cout<<"B\n";};

int main() {
   int* pi;
   extract( pi ); // A
   return 0;
}
```
## 3rd Path
![The best viable function-3](https://hackmd.io/_uploads/rkgMtWtxPex.jpg =50%x)

```c++
#include <iostream>

void foo(int, float, unsigned short) { std::cout<<"A\n"; }

template<class T>
void foo(int, float, T) { std::cout<<"C\n"; }

template<>
void  foo<unsigned short>(int, float, unsigned short) { std::cout<<"Specialized C\n"; }

int main() {

    unsigned short s = 1;
    foo(1, 1.0f, s);
    return 0;
}
```
```c++
#include <iostream>

template<typename T>
void foo(T t) {
    std::cout << "Template foo\n";
}

template<>
void foo<int>(int t) {
    std::cout << "Template specialization for int\n";
}

void foo(int t) {
    std::cout << "Non-template foo\n";
}

int main() {
    foo(42); // "Non-template foo"
    return 0;
}
```

## 4th Path
![The best viable function-4](https://hackmd.io/_uploads/rJ5KbKgDgx.jpg =50%x)
```c++
#include <iostream>

template<class T, class U, class V>
void foo(T, U, V) { std::cout<<"A\n"; }
template<>
void foo<int, float, unsigned short>(int, float, unsigned short) {
std::cout<<"Specialized A\n";
}

template<class T, class U>
void foo(T, U, unsigned short) { std::cout<<"C\n"; }
template<>
void  foo<int, float>(int, float, unsigned short) { std::cout<<"Specialized C\n"; }

int main() {
    unsigned short s = 1;
    foo(1, 1.0f, s); // Specialized C
    return 0;
}
```
```c++
#include <iostream>

template<class T>
void foo(T) {
    std::cout << "Template A\n";
}

template<class T>
void foo(T*) {
    std::cout << "Template B\n";
}


int main() {
    int a[10];
    foo(a); // "Template B"
    return 0;
}
```
## 5th Path
![The best viable function-5](https://hackmd.io/_uploads/BJJqZKxPxx.jpg =50%x)

```c++
#include <iostream>

struct A {
   A(unsigned short x) : _x(x) {}

   operator int() {
      std::cout << "Calls operator int()\n";
      return _x;
   }
   operator short() {
      std::cout << "Calls operator short()\n";
      return _x;
   }
   unsigned short _x;
};

int main() {
    int x = A(2); // Calls operator int()
    std::cout << x << "\n";
    return 0;
}
```

## 6th Path
![The best viable function-6](https://hackmd.io/_uploads/By7cZKlvex.jpg =50%x)

```c++
#include <iostream>

struct A {
   A(unsigned short x) : _x(x) {}

   operator int() {
      std::cout << "Calls operator int()\n";
      return _x;
   }
   operator short() {
      std::cout << "Calls operator short()\n";
      return _x;
   }
   unsigned short _x;
};

int main() {
    float y = A(2); // ambiguous
    std::cout << y << "\n";
    return 0;
}
```





![936825-20210316030907126-2015925917](https://hackmd.io/_uploads/Bkg_L6o0h1l.png)

{% endraw %}