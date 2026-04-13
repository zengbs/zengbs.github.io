---
title: "Implementing Perfect Forwarding"
date: 2026-04-13T15:32:37+08:00
draft: false
---

---
title: Implementing Perfect Forwarding
tags: [CPP]

---

# Forwarding References
To avoid overloading functions for parameters with different value categories, C++ introduced a special mechanism for perfect forwarding. You need three things:
1. Take the call parameter as a pure rvalue reference (declared with `&&` but without `const` or `volatile`).
2. The type of the parameter has to be a template parameter of the function.
3. When forwarding the parameter to another function, use a helper function called `std::forward<>()`, which is declared in `<utility>`.

For example:
```c++
// for single argument
template<class T>
void callFoo(T&& arg) {
   foo(std::forward<T>(arg));
}

// for a pair of arguments
template<class T, class U>
void callFoo(T&& arg1, U&& arg2) {
   foo(std::forward<T>(arg1), std::forward<U>(arg2));
}

// for variadic number of arguments
template<class ... Ts>
void callFoo(Ts&& ... args) {
   foo(std::forward<Ts>(args) ... );
}
```


## `std::forward<>()`
`std::forward<>()` is effectively a conditional `std::move()` so that we get the same behavior:
* If we pass an rvalue to arg, we have the same effect as calling `foo(std::move(arg))`.
* If we pass an lvalue to arg, we have the same effect as calling `foo(arg)`.

```c++
template<class T>
void callFoo(T&& arg);

X v;
const X c;
callFoo(v);            // type of arg is X&, calls foo(X&)
callFoo(c);            // type of arg is const X&, calls foo(const X&)
callFoo(X{});          // type of arg is X&&, calls foo(X&&)
callFoo(std::move(v)); // type of arg is X&&, calls foo(X&&)
callFoo(std::move(c)); // type of arg is const X&&, calls foo(const X&)
```
Note that 
1) A generic rvalue reference that is qualified with `const` (or `volatile`) is not a universal reference.
2) Generic arguments preserve the constness and type of argument.


# Using `std::forward<>()` to Member Functions
```c++
class X {
private:
   std::string name;
public:
   std::string getName() && {
      return std::move(name);
   }
   const std::string& getName() const& {
      return name;
   }
};


template<class T>
void foo(T&& x){

   // x is always an lvalue
   // --> calls getName() const&
   x.getName();

   // If the argument (not parameter) is lvalue, calls getName() const&
   // If the argument (not parameter) is rvalue, calls getName() &&
   std::forward<T>(x).getName();
}
```


# Rvalue References versus Universal References

```c++
usgin Coll = std::vector<std::string>;

void foo(Coll&& arg)
{
 ...
}

Coll v;
const Coll c;

foo(v); // Error
foo(c); // Error
foo(Coll{}); // OK, arg binds to non-const prvalue
foo(std::move(v)); // OK, arg binds to non-const xvalue
foo(std::move(c)); // Error
```

```c++
template<class Coll>
void foo(Coll&& arg)
{
 ...
}

Coll v;
const Coll c;

foo(v); // OK, arg binds to non-const lvalue
foo(c); // OK, arg binds to const lvalue
foo(Coll{}); // OK, arg binds to non-const prvalue
foo(std::move(v)); // OK, arg binds to non-const xvalue
foo(std::move(c)); // OK, arg binds to const xvalue
```

# Overload Resolution with Universal References

|              | lvalue reference | const lvalue reference | rvalue reference | const rvalue reference |  Universal reference   |
| ------------ | ---------------- | ---------------------- | ---------------- | ---------------------- | --- |
| lvalue       | 1                | 3                      | n/a              | n/a                    |   2  |
| const lvalue | n/a              | 1                      | n/a              | n/a                    |   2  |
| prvalue      | n/a              | 4                      | 1                | 3                      |   2  |
| xvalue       | n/a              | 4                      | 1                | 3                      |    2 |
| const xvalue | n/a              | 3                      | n/a              | 1                      |    2 |

