---
title: "decltype(auto)"
date: 2026-04-13T15:32:36+08:00
draft: false
---

---
title: decltype(auto)
tags: [CPP]

---

# Perfect Returning

C++14 introduced a new placeholder type for perfect returning: `decltype(auto)`. For example:

```c++
template<typename T>
decltype(auto) callFoo(T&& arg)
{
   return foo(std::forward<T>(arg));
}
```
With this declaration, `callFoo()` returns by value, if `foo()` returns by value, and `callFoo()` returns by reference if `foo()` returns by reference. In all cases, both the type and the value category are retained.

# `decltype(auto)`

```c++
std::string s = "hello";
std::string& r = s;

// initialized with name:
decltype(auto) da1 = s; // std::string
decltype(auto) da2(s);  // same
decltype(auto) da3{s};  // same
decltype(auto) da4 = r; // std::string&


// initialized with expression:
decltype(auto) da5 = std::move(s); // std::string&&
decltype(auto) da6 = s+s;          // std::string
decltype(auto) da7 = s[0];         // char&
decltype(auto) da8 = (s);          // std::string&
```

In contrast to `auto&&`, which is always a reference, `decltype(auto)` is sometimes just a value (if initialized with the name of an object of a value type or with a prvalue expression).

# Return Type `decaltype(auto)`

`decltype(auto)` is deduced as `decltype(returned expr)` instead of `decltype((returned expr))`.


| `expr`  | `decltype(auto) var = expr`<br>`decltype(var)` is ... | `auto&& var = expr`<br>`decltype(var)` is ... |
|:-------:|:-------------------------------------------------------:|:-----------------------------------------------:|
| lvalue  |                          Type&                          |                      Type&                      |
| xvalue  |                         Type&&                          |                     Type&&                      |
| prvalue |                          Type                           |                     Type&&                      |


As a more general example, consider a helper function of a framework that (after some initialization or logging) transparently calls a function as if we were to call it directly:
```c++
template<class Func, class ... Args>
decltype(auto) call(Func f, Args&& ... args) {
   // ...
   return f(std::forward<Args>(args)...);
}
```
For example:
```c++
#include <iostream>
#include <string>
#include <utility>

template<class Func, class... Args>
decltype(auto) call( Func f, Args&& ... args )
{
   return f(std::forward<Args>(args) ...);
}

std::string nextString()
{
   return "Hi";
}

std::ostream& print(std::ostream& strm, const std::string& val)
{
   return strm << "value: " << val;
}

std::string&& returnArg(std::string&& arg)
{
   return std::move(arg);
}

int main()
{
   // type of s: std::string
   // value category of call(...): prvalue
   // value category of s: lvalue
   auto s = call(nextString);

   // 100
   std::cout << std::is_same_v<std::string,decltype(s)> << "\n";
   std::cout << std::is_same_v<std::string&,decltype(s)> << "\n";
   std::cout << std::is_same_v<std::string&&,decltype(s)> << "\n";

   // 100
   std::cout << std::is_same_v<std::string,decltype(call(nextString))> << "\n";
   std::cout << std::is_same_v<std::string&,decltype(call(nextString))> << "\n";
   std::cout << std::is_same_v<std::string&&,decltype(call(nextString))> << "\n";

   // 010
   std::cout << std::is_same_v<std::string,decltype((s))> << "\n";
   std::cout << std::is_same_v<std::string&,decltype((s))> << "\n";
   std::cout << std::is_same_v<std::string&&,decltype((s))> << "\n";

   // type of ref: std::string&&
   // value category of call(...): xvalue
   // value category of ref: lvalue
   auto&& ref = call(returnArg, std::move(s));

   std::cout << "s: " << s << '\n'; // s: Hi
   std::cout << "ref: " << ref << '\n'; // ref: Hi

   // 001
   std::cout << std::is_same_v<std::string,decltype(ref)> << "\n";
   std::cout << std::is_same_v<std::string&,decltype(ref)> << "\n";
   std::cout << std::is_same_v<std::string&&,decltype(ref)> << "\n";

   // 001
   std::cout << std::is_same_v<std::string,decltype(call(returnArg, std::move(s)))> << "\n";
   std::cout << std::is_same_v<std::string&,decltype(call(returnArg, std::move(s)))> << "\n";
   std::cout << std::is_same_v<std::string&&,decltype(call(returnArg, std::move(s)))> << "\n";

   // 010
   std::cout << std::is_same_v<std::string,decltype((ref))> << "\n";
   std::cout << std::is_same_v<std::string&,decltype((ref))> << "\n";
   std::cout << std::is_same_v<std::string&&,decltype((ref))> << "\n";

   // type of str: std::string
   // value category of call(...): xvalue
   // value category of str: lvalue
   auto str = std::move(ref);

   // 100
   std::cout << std::is_same_v<std::string,decltype(str)> << "\n";
   std::cout << std::is_same_v<std::string&,decltype(str)> << "\n";
   std::cout << std::is_same_v<std::string&&,decltype(str)> << "\n";

   // 001
   std::cout << std::is_same_v<std::string,decltype(std::move(ref))> << "\n";
   std::cout << std::is_same_v<std::string&,decltype(std::move(ref))> << "\n";
   std::cout << std::is_same_v<std::string&&,decltype(std::move(ref))> << "\n";

   // 010
   std::cout << std::is_same_v<std::string,decltype((str))> << "\n";
   std::cout << std::is_same_v<std::string&,decltype((str))> << "\n";
   std::cout << std::is_same_v<std::string&&,decltype((str))> << "\n";

   std::cout << "s: " << s << '\n'; // s:
   std::cout << "ref: " << ref << '\n'; // ref:
   std::cout << "str: " << str << '\n'; // str: Hi

   call(print, std::cout, str) << '\n'; // value: Hi
}
```


# Deferred Perfect Returning


```c++
template<class Func, class... Args>
decltype(auto) call(Func f, Args&&.. args)
{
   decltype(auto) ret{f(std::forward<Args>(args)...)};
   
   if constexpr (std::is_rvlaue_reference_v<decltype(ret)>) {
      return std::move(ret);
   }else {
       return ret;
   }
}
```
## Plausible Solutions (Wrong):
* Returning `static_cast`:
   ```c++
   template<class Func, class... Args>
   decltype(auto) call(Func f, Args&&.. args)
   {
      decltype(auto) ret{f(std::forward<Args>(args)...)};
      return static_cast<decltype(ret)>(ret);
   }
   ```
   * If `f()` returns a prvalue:
     ```c++
     int call(Func f, Args&&.. args)
     {
        int ret{f(std::forward<Args>(args)...)};
        return static_cast<int>(ret);
     }
     ```
     An unnecessary copy occurs in the return statement. In this case, `static_cast<Type>(ret)` casts lvalue `ret` to a temporary prvalue, which in turn prevents copy elision.
   * If `f()` returns an lvalue:
      ```c++
     int& call(Func f, Args&&.. args)
     {
        int& ret{f(std::forward<Args>(args)...)};
        return static_cast<int&>(ret);
     }
     ```
   * If `f()` returns an xvalue:
      ```c++
     int&& call(Func f, Args&&.. args)
     {
        int&& ret{f(std::forward<Args>(args)...)};
        return static_cast<int&&>(ret);
     }
     ```
* Returning `ret`:
  ```c++
  template<class Func, class... Args>
  decltype(auto) call(Func f, Args&&.. args)
  {
     decltype(auto) ret{f(std::forward<Args>(args)...)};
     return ret;
  }
  ```
  * If `f()` returns xvalue, both the deduced type of `ret` and the return type of `call()` are `Type&&`. However, we cannot bind an lvalue to the type `Type&&`. The effective counterpart is something like this:
    ```c++
    int&& call(int& x){
       int&& ret{f(x)};
       return ret;
    }
    ```
* Using `auto&&` to declare `ret`:
  ```c++
  template<class Func, class... Args>
  decltype(auto) call(Func f, Args&&.. args)
  {
     auto&& ret{f(std::forward<Args>(args)...)};
     return ret; // Error
  }
  ```
    * If `f()` returns an lvalue: the type of `ret` will be `Type&`.
    * If `f()` returns a prvalue: the type of `ret` will be `Type&&`.
    * If `f()` returns a xvalue: the type of `ret` will be `Type&&`.
    Thus, we return a reference to a local object, leading to a fatal error.
* Returning a name with additional parentheses:
  ```c++
  template<class Func, class... Args>
  decltype(auto) call(Func f, Args&&.. args)
  {
     decltype(auto) ret{f(std::forward<Args>(args)...)};
     
     if constexpr (std::is_rvlaue_reference_v<decltype(ret)>) {
        return std::move(ret);
     }else {
         return (ret);
     }
  }
  ```
  In this case, `decltype(auto)` switches to the rules of expression and always deduces an lvalue reference (`Type&`).