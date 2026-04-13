---
title: "Structured bindings"
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

---
title: Structured bindings
tags: [CPP]

---

# Structured Bindings
To iterate over the elements of a `std::map<>` without structured bindings, you would have to program:
```c++
for (const auto& e : mymap) {
   std::cout << e.first << ": " << e.second << "\n";
}
```
By using structured bindings, the code becomes a lot more readable:
```c++
for (const auto& [key,val] : mymap) {
   std::cout << key << ": " << val << "\n";
}
```

## Structured Bindings in Detail


### Binding to an Anonymous Entity

The expression
```c++
auto [u,v] = ms;
```
is as if the following code:
```c++
auto e = ms;
auto u = e.i;
auto v = e.s;
```
Note that (1) `u` and `v` are not references to `e.i` and `e.s` repectively. (2) `decltype(u)` and `decltype(v)` are the types of the member `i` and `s` respectively. As a result,
```c++
std:cout << u << ' ' << v << '\n';
```
prints the copies of `ms.i` and `ms.s`.


* `e` exists as long as the structured bindings to it exist. Thus, it is destroyed when the structured bindings go out of scope. As a consequence:
  ```c++
  MyStruct ms{42,"hello"};
  auto [u,v] = ms;
  std::cout << u << "\n"; // print 42
  u = 31;
  std::cout << ms.i << "\n"; // print 42
  ```
* When using structured bindings for return values, the same principle applies.
  ```c++
  auto [u,v] = getStruct();
  ```
  It behaves as if we had initialized a new entity `e` with the return value of `getStruct()` so that the structured bindings `u` and `v` become alias names for the two members/elements of `e`, similar to defining:
  ```c++
  auto e = getStruct();
  auto u = e.i; // the type of u is the same as i
  auto v = e.s; // the type of v is the same as s
  ```
  That is, structured bindings bind to a new entity, which is initialized from a return value, instead of binding to the return value directly.
  
### Using Qualifiers
Declaring structured bindings to a `const` reference means that an entire anonymous `const` entity binds to `ms`. As a result, any change to members of `ms` affect the value of `u` and `v`;
```c++
const auto& [u,v] = ms;
ms.i = 2; // affects u
std::cout << u; // print 2
u = 3; // Error:  assignment of read-only variable ‘u’
```
```c++
auto& [u,v] = ms;
ms.i = 2; // affect u
std::cout << u; // print 2
u = 3; // affect ms.i
std::cout << ms.i; //print 3
```
If the value used to initialize a structured bindings reference is a temporary object, as usual, the lifetime of the temporary is extended to the lifetime of the bound structure:
```c++
MyStruct getStruct();

const auto& [a,b] = getStruct();
std::cout << a;
```

### Qualifiers Do Not Necessarily Apply to the Structured Bindings
1. `const` reference: the entire anonymous entity is `const` reference, but `u` and `v` are not declared as being references.
   ```c++
   const auto& [u,v] = ms;
   ```
   is as if the following:
   ```c++
   const auto& e = ms;
   
   const auto u = e.i; // u is not a reference
   const auto v = e.s; // v is not a reference
   ```
2. Alignment: if we align the initialized anonymous entity and not the structured bindings `u` and `v`, `u` as the first member is forced to be aligned to 16, while `v` is not.
   ```c++
   alignas(16) auto [u,v] = ms; // align the object, not v
   ```
3. Structured bindings do not decay even though `auto` is used.
   ```c++
   struct S{
      const char x[6];
      const char y[6];
   };
   
   S s;
   auto& [u,v] = s;
   ```
   , where the type of `u`/`v` is still `const char x[6]`/`const char y[6]` instead of `const char*`.

### Move Semantics


```c++
MyStruct ms = {42, "Jim"};
auto&& [v,n] = std::move(ms);

std::cout << ms.s; // prints "Jim"

std::string s = std::move(n);

std::cout << ms.s; // prints unspecified value
std::cout << n;    // prints unspecified value
std::cout << s;    // print "Jim"
```

```c++
MyStruct ms = {42,"Jim"};
auto [v,n] = std::move(ms);

std::cout << ms.s; // prints unspecified value
std::cout << n;    // prints "Jim"

std::string s = std::move(n);
std::cout << n;    // prints unspecified value
n = "Lara";
std::cout << n;    // prints "Lara"
std::cout << s;    // print "Jim"
```

## Where Structured Bindings Can Be Used

### Structures and Classes
Note that only limited use of inheritance is possible. All non-static data members must be members of the same class definition . For example:
```c++
struct B {
   int a = 1;
   int b = 2;
};

struct D1 : B {
};

auto [x,y] = D1{}; // OK

struct D2 : B {
   int c = 3;
};
auto [i,j,k] = D2{}; // Error
```
Note that you should use structured bindings on public members only if their order is guaranteed to be stable. Otherwise, if the order of `int a` and `int b` inside `B` changes, `x` and `y` suddenly are initialized with different values.

### Raw Arrays
```c++
```

```c++
#include <iostream>

int main() {

   int arr[] = {1,2,3,4,};
   auto [a,b,c,d] = arr;

   std::cout << a << "\n"; // 1
   std::cout << b << "\n"; // 2
   std::cout << c << "\n"; // 3
   std::cout << d << "\n"; // 4
   
   // ERROR: number of elements doesn't fit
   auto [x,y] = arr; 
}
```

Note that C++ allows us to return arrays with size by reference, so that this feature also applies to functions that return an array, provided the size of the array is part of the return type:
```c++
auto getArr() -> int(&)[2];
...
auto [x,y]=getArr();
```
### `std::pair`,`std::tuple`,`std::array`

#### `std::array`

```c++
std::array<int,4> stdarr { 1, 2, 3, 4 };
...
auto& [a,b,c,d] = stdarr;
a += 10; // OK: modifies stdarr[0]

const auto& [e,f,g,h] = stdarr;
e += 10; // ERROR: reference to constant object

auto&& [i,j,k,l] = stdarr;
i += 10; // OK: modifies stdarr[0]

auto [m,n,o,p] = stdarr;
m += 10; // OK: but modifies copy of stdarr[0]

auto& [a,b,c,d] = getArray(); // ERROR
```

#### `std::tuple`
```c++
std::tuple<char,float,std::string> getTuple();
// ...
auto [a,b,c] = getTuple(); // OK
```
#### `std::pair`
Without structured binding, you may handle the exception as follows:
```c++
std::map<std::string,int> coll;
auto ret = coll.insert({"new",42});

if (!ret.second){
   // if insertion failed, handle error using iterator ret.first
}
```
With structured binding, the code is more readable:
```c++
std::map<std::string,int> coll;
auto [pos,ok] = coll.insert({"new",42});

if (!ok){
   // if insertion failed, handle error using iterator pos
}
```
