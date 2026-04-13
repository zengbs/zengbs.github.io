---
title: "Perfect Passing with `auto&&`"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

---
title: Perfect Passing with `auto&&`
tags: [CPP]

---

# Default Perfect Passing

If you pass a return value to another function directly, the value is passed perfectly, keeping its type and value category. For example:
```c++
#include <iostream>
#include <string>

// To avoid overloading ambiguous, we comment out this
//void process(std::string&) {
//   std::cout << "std::string&\n";
//}

void process(std::string&) {
   std::cout << "std::string&\n";
}
void process(const std::string&) {
   std::cout << "const std::string&\n";
}
void process(std::string&&) {
   std::cout << "std::string&&\n";
}

const std::string retConstByValue(std::string& s) {
   return s;
}
std::string retByValue(std::string& s) {
   return s;
}
std::string& retByRef(std::string& s) {
   return s;
}
const std::string& retByConstRef(const std::string& s) {
   return s;
}
std::string&& retByRefRef(std::string&& s) {
   return std::move(s);
}
const std::string&& retConstRefRef(const std::string&& s) {
   return std::move(s);
}

int main() {
   std::string s;
   const std::string cs;

   // Disable perfect forwarding
   process(retConstByValue(s));            // const std::string&
   process(retConstRefRef(std::move(cs))); // const std::string&

   // Perfect forwarding
   process(retByValue(s));             // std::string&&
   process(retByRef(s));               // std::string&
   process(retByConstRef(s));          // const std::string&
   process(retByRefRef(std::move(s))); // std::string&&
}
```
Therefore, (1) do not mark returned by value with `const`; (2) do not mark returned non-const rvalue reference with `const`. Otherwise, it disables move semantics and perfect forwarding.

# Universal References with `auto&&`

Why we need `auto&&`? Passing a return value ***later*** but keeping its type and value category. For example:


```c++
#include <iostream>
#include <string>

void process(std::string&&) {
   std::cout << "std::string&&\n";
}
std::string retByValue(std::string& s) {
   return s;
}

int main() {
   std::string s;

   auto&& ret = retByValue(s);

   // do something for ret ...

   process(std::forward<decltype(ret)>(ret)); // std::string&&
}
```


## Type Deduction of `auto&&`
* If you declare something with `auto&&`, you also declare a universal reference.


```c++
auto&& r{X};
```

| Value Category of `r` | Decuced expression type of `r`<br>`decltype((r))`    | Deduced Declared Type of `r`<br>`decltype(r)` | Expression Type of `X`<br>`decltype((X))` | Value Category of `X` | Declared Type of `X`<br>`decltype(X)` |
|:---------------------:| --- |:-------------------------------------------------:|:-----------------------------------------:|:---------------------:| ------------------------------------- |
|        lvalue         |   Type&  |            lvalue reference<br>(Type&)            |                   Type&                   |        lvalue         | Type, Type&, Type&&                   |
|        lvalue         |   Type&  |           rvalue reference<br>(Type&&)            |                   Type                    |        prvalue        | Type, Type&, Type&&                   |
|        lvalue         |   Type&  |           rvalue reference<br>(Type&&)            |                  Type&&                   |        xvalue        | Type, Type&, Type&&                   |


For example:

```c++
// forward declaration
std::string retPRValue();
std::string& retLValue();
std::string&& retXValue();
const std::string& retConstLValue();
const std::string&& retConstXValue();

auto&& r1{retPRValue()};     // The type of r1: std::string&&
auto&& r2{retLValue()};      // The type of r2: std::string&
auto&& r3{retXValue()};      // The type of r3: std::string&&
auto&& r4{retConstLValue()}; // The type of r4: const std::string&
auto&& r5{retConstXValue()}; // The type of r5: const std::string&&


std::string s;
const std::string cs;

auto&& r6{s};             // The type of r6: std::string&
auto&& r7{std::move(s)};  // The type of r7: std::string&&
auto&& r8{cs};            // The type of r8: const std::string&
auto&& r9{std::move(cs)}; // The type of r9: const std::string&&
```


# `auto&&` as Non-Forwarding Reference

## Universal References and the Range-Based `for` loop


```c++
std::vector<std::string> coll;

for (const auto& s : coll) {
 ...
}
```

is equivalent to the following:
```c++
std::vector<std::string> coll;

auto&& range = coll; // initialize a universal reference
auto pos = range.begin();
auto end = range.end();

for ( ; pos != end; ++pos ) {
   const auto& s = *pos;
}
```

The reason we declare `range` as a universal reference is that we want to be able to bind it to every `range` so that we can use it twice (once to ask for its beginning, and once to ask for its end) without creating a copy or losing the information about whether or not the `range` is `const`.

The loop should work for:
* non-const lvalue
   ```c++
   std::vector<int> coll;
   
   for (int& i : coll) {
      // ...
   }
   ```
* const lvalue
   ```c++
   const std::vector<int> coll;
   
   for (int i : coll) {
      // ...
   }
   ```
* prvalue
   ```c++
   for (int i : std::vector<int>{0,8,3}) {
      // ...
   }
   ```


## Using the Range-Based `for` Loop: temporary object

* Do no apply range-based for loop to a temporary object. For example:
   ```c++
   // return value
   std::vector<std::string> createStrings();
   
   for (char c : createStrings().at(0)) {
     ...
   }
   ```
   becomes:
   ```c++
    // return value
    std::vector<std::string> createStrings();
    
    // range is a reference extending
    // the lifetime of the reference to the first element
    auto&& range = createStrings().at(0);
    
    // all strings are destroyed here
    auto pos = range.begin();
    auto pos = rnage.end();
    
    for (; pos != end; ++pos) {
       char c = *pos;
    }
   ```
   `std::string& range` extends the lifetime of the refernece returned by `at()`  but not the return value of `createString()`.
* However, the following case is okay:
  ```c++
  #include <iostream>
  #include <string>
  #include <vector>
  
  std::string bar(const std::string& s) {
     return s;
  }
  
  int main() {
     for (char c : bar("644346")) {
        std::cout << c;
     }
     std::cout << "\n";
  }
  ```
  because
  ```c++
  auto&& range = bar("644346");
  ```
  the type of `range` is an rvalue reference (`std::sting&&`) binding to the return value (prvalue) of `bar()`, sucessfully extending the lifetime of the return value of `bar()`.

## Using the Range-Based `for` Loop: proxy object

```c++
#include <iostream>
#include <string>
#include <vector>

template<class Coll, class T>
void assign(Coll& coll, const T& value) {
   for (auto& elem : coll) {
       elem = value;
   }
}

int main() {
   std::vector<int> coll1{1,2,3};
   std::vector<std::string> coll2{"hello", "world"};
   std::vector<bool> coll3{false, true};

   assign(coll1, 0);
   assign(coll2, "ok");
   assign(coll3, false); // Error
}
```

This is because:
The range-based for loop is equivalent to
```c++
auto&& range = coll;
auto pos = coll.begin();
auto end = coll.end();

for (; pos != end; ++pos) {
   auto& elem = *pos; // Error
   elem = value
}
```
When using `std::vector<std::string>`, dereferencing iterator, `*pos` , returns lvalue reference. However, for `std::vector<bool>`, `*pos` returns a prvalue of a proxy object.

The solution is:
```c++
template<class Coll, class T>
void assign(Coll& coll, const T& value) {
   for (auto&& elem : coll) {
      elem = value;
   }
}
```



# Perfect Forwarding in Lambdas

# Using `auto&&` in C++20 Function Declarations