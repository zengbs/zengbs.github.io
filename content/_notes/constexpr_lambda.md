---
date: 2026-04-13T15:32:36+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---

# `constexpr` Lambdas


```mermaid
graph TD
    A[Implicit constexpr Lambda] --> B{Does the Lambda body<br/>allow constexpr?}
    B -->|Yes| C
    B -->|No| D
    C[Case1: Enable constexpr]
    D[Case2: Disable constexpr]
 ```
 ```mermaid
graph TD
    A[Explicit constexpr Lambda] --> B{Does the Lambda body<br/>allow constexpr?}
    B -->|Yes| C
    B -->|No| D
    C[Case3: Enable constexpr]
    D[Case4: Compile error]
 ```
 
# Case1
```c++
auto squared = [](auto val) {
   return val*val;
};
std::array<int,squared(5)> a;
```
# Case2
```c++
auto squared2 = [](auto val) {
   static int calls = 0; // Okay, but disable constexpr
   return val*val;
};
std::array<int,squared2(5)> a; // compile error
std::cout << squared2(5) << "\n"; // Okay, runtime calculation
```
# Case3
```c++
auto squared3 = [](auto val) constexpr {
   return val*val;
};
```
# Case4
```c++
auto squared4 = [](auto val) constexpr {
   static calls = 0; // compile error
   return val*val;
};
```

# Closure object of lambda
For an implicit or explicit `constexpr` lambda, the function call `operator()` is `constexpr`. That is the definition of
```c++
auto squared = [](auto val) {
   // implicitly constexpr since C++17
   return val*val;
};
```
converts into the closure type:
```c++
class CompilerSpecificName {
public:
   ...
   template<typename T>
      constexpr auto operator() (T val) const {
      return val*val;
   }
};
```

# `constexpr` lambda vs. `constexpr` closure object
## `constexpr` lambda
```c++
// compile-time lambda calls
auto squared1 = [](auto val) constexpr {
   return val*val;
};
```
* `constexpr` applies to the lambda’s `operator()`.
* The lambda is a normal object.
* The lambda can be evaluated at compile time.
* It does not force compile-time evaluation.
* Its call operator is explicitly `constexpr`.

## `constexpr` closure object
```c++
// compile-time initialization
constexpr auto squared2 = [](auto val) {
   return val*val;
};
```
* `constexpr` applies to the lambda object variable.
* The lambda’s `operator()` is implicitly `constexpr` (since C++17, if possible).

For example:
```c++
// C++17
#include<iostream>

          auto squared1 = [](auto val) constexpr{ return val*val; };
constexpr auto squared2 = [](auto val)          { static int a=1; return val*val; };

int main(){

   // x is required to be determined at compile time
   // --> `operator()` must be constexpr
   constexpr int  x = squared1(5);  // OK

   // f1 must be initialized by a constant expression
   // --> the lambda has no captures, so its closure type is a literal type
   // --> therefore the lambda object can be constexpr
   constexpr auto f1 = squared1;    // OK
   std::cout << f1(6) << "\n";


   // y must be a constant expression
   // --> squared2::operator() is NOT constexpr
   //     (its body contains a static local variable, which is not allowed
   //      in a constant expression)
   constexpr int  y  = squared2(5); // Error

   // f2 must be initialized by a constant expression
   // --> the lambda has no captures, so its closure type is a literal type
   // --> therefore the lambda object itself can be constexpr,
   //     even though operator() is not constexpr
   constexpr auto f2 = squared2;    // OK
   std::cout << f2(6) << "\n";

}
```

# Static initialization order fiasco
The fiasco only occurs when:
1. A global object requires dynamic initialization.
2. And another global object in a different translation unit depends on it.

See [What’s the “static initialization order ‘fiasco’](https://isocpp.org/wiki/faq/ctors#static-init-order).

For example:
```c++
// file1.cc
#include<cstdlib>
#include<limits.h>

auto squared = [](auto val) {
    return val*val;
};

int squared_global = squared(5);
```

```c++
// file2.cc
#include <iostream>

extern int squared_global;

int global = squared_global;

int main() { std::cout << global+1 << "\n"; }
```

* `g++ file2.cc file1.cc -std=c++14 && ./a.out` results int `x = 0`.
* `g++ file1.cc file2.cc -std=c++14 && ./a.out` results int `x = 626`.


If (only) the lambda is `constexpr` it can be used at compile time, but `squared1` might be initialized at run time, which means that some problems might occur if the static initialization order matters (e.g., causing the static initialization order fiasco). If the (closure) object initialized by the lambda is `constexpr`, the object is initialized when the program starts but the lambda might still be a lambda that can only be used at run time (e.g., using `static` variables). Therefore, you might consider declaring:
```c++
constexpr auto squared = [](auto val) constexpr {
   return val*val;
};
```
{% endraw %}