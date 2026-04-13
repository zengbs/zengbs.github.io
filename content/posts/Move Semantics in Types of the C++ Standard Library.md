---
title: "Move Semantics in Types of the C++ Standard Library"
date: 2026-04-13T15:32:37+08:00
draft: false
---

---
title: Move Semantics in Types of the C++ Standard Library
tags: [CPP]

---

# Move Semantics for Strings
The capacity of strings (the memory currently available for the value) does usually not shrink. Only move operations, `swap()`, or `shrink_to_fit()` might shrink the capacity.
# Move Semantics for Containers
All containers define a move constructor and move assignment operator to support move semantics for unnamed temporary objects and objects marked with `std::move()`.

## Container Guarantees for Move Constructors
The C++ standard specifies the move constructor of all containers except for `std::array` is constant time complexity. See the expression `X u(rv);` and `X u = rv;` in the  table [tab:container.req].
## Container Guarantees for Move Assignment Operators
The C++ standard specifies the move assignemnt operator of all containers is linear time complexity. See the expression `a = rv` in the  table [tab:container.req].

There are only two ways to implement a move assignment:
* Destroy the old elements and move the whole contents of the source to the destination (i.e., move the pointer to the memory from the source to the destination).
* Move element by element from the source cont1 to the destination cont2 and destroy all remaining elements not overwritten in the destination.

Both ways require linear complexity. The first way needs O(N) to destroy the old element; the second way needs O(N) to move all elements one by one.

That's why the C++ standard specifies O(N) for move assignment.

## Insert Functions
All containers support moving a new element into the container. For example:

```c++
template<typename T, typename Allocator = allocator<T>>
class vector {
public:
   // insert a copy of elem:
   void push_back (const T& elem);
   // insert elem when the value of elem is no longer needed:
   void push_back (T&& elem);
};
```
Or 
```c++
template<typename Key, typename T, typename Compare = less<Key>,
typename Allocator = allocator<pair<const Key, T>>>
class map {
public:
   pair<iterator, bool> insert(const value_type& x);
   pair<iterator, bool> insert(value_type&& x);
};
```

## Emplace Functions
Functions like `emplace_back()` use perfect forwarding to avoid creating copies of the passed arguments. For example:
```c++
template<typename T, typename Allocator = allocator<T>>
class vector {
public:
   // insert a new element with perfectly forwarded arguments:
   template<typename... Args>
   constexpr T& emplace_back(Args&&... args) 
   {
      // call the constructor with the perfectly forwarded arguments:
      place_element_in_memory(T(std::forward<Args>(args)...));
   }
};
```
## Move Semantics for `std::array<>`
`std::array<>` is the only container that does not allocate memory on the heap. In fact, it is implemented as a templified C data structure with an array member:
```c++
template<typename T, size_t N>
struct array {
   T elems[N];
};
```
As a consequence:
* The move constructor has linear complexity because it has to move element by element.
* The move assignment operator might always throw because it has to move assign element by element.


However, moving an array is still better than copying if moving the elements is cheaper than copying them. For example:
```c++
std::array<std::string, 1000> arr;
...
auto arr2{arr};
 // copies string by string
auto arr3{std::move(arr)}; // moves string by string
```
If the strings allocate heap memory (i.e., they have a significant size if the small string optimization (SSO) is used), moving the array of strings is usually significantly faster.

# Move Semantics for Vocabulary Types

## Move Semantics for Pairs

```c++
template<typename T1, typename T2>
struct pair {
   // types of each member:
   using first_type = T1;
    // same as: typedef T1 first_type
   using second_type = T2;
   
   // the members:
   T1 first;
   T2 second;
   
   // default constructor
   constexpr pair();
   // constructor
   constexpr pair(const T1& x, const T2& y);
   // templated constructor
   template<typename U, typename V> constexpr pair(U&& x, V&& y);
   
   // ==== constructors ====
   // copy constructor
   pair(const pair&) = default;
   // move constructor
   pair(pair&&) = default;
   
   // ==== templated constructors ====
   // copy constructor
   template<typename U, typename V> constexpr pair(const pair<U, V>& p);
   // move constructor
   template<typename U, typename V> constexpr pair(pair<U, V>&& p);
   
   
   // ==== assignments ====:
   // copy assignment
   pair& operator=(const pair& p);
   // move assignment
   pair& operator=(pair&& p) noexcept( ... );
   
   // ==== templated assignments ====:
   // copy assignment
   template<typename U, typename V> pair& operator=(const pair<U, V>& p);
   // move assignment
   template<typename U, typename V> pair& operator=(pair<U, V>&& p);
   
   // other:
   void swap(pair& p) noexcept( ... );
};
```
* We need templated constructor/assignement, which is not generated by default, so that we can construct/assign an object from a different but convertible type. For example:
   ```c++
   std::pair<std::string,std::string> p{"Hello","World"};
   ``` 
* We can use move semantics when initializing a pair. For exmaple:
   ```c++
   int val = 42;
   std::string s1{"value of s1"};
   std::pair<std::string, std::string> p4{std::to_string(val), std::move(s1)};
   ```



## `std::make_pair()`

* In C++98, `make_pair<>()` was declared inside namespace std using call-by-reference to avoid unnecessary copying:
  ```c++
  template<typename T1, typename T2>
  pair<T1,T2> make_pair (const T1& a, const T2& b)
  {
     return pair<T1,T2>(a,b);
  }
  ```
  This, however, almost immediately caused significant problems when using pairs of string literals or raw arrays. For example, when `"hello"` was passed as the second argument, the type of the corresponding parameter `b` became a reference to an array of `const chars` (`const char(&)[6]`). Therefore, type `char[6]` was deduced as type `T2` and used as type of the second member. However, initializing an array member with an array is not possible because you cannot copy arrays.
  In this case the decayed type should be used as member type, which is the type you get when you would pass the argument by value (`const char*` for string literals).
* As a consequence, with C++03, the function definition was changed to use call-by-value:
   ```c++
   template<typename T1, typename T2>
   pair<T1,T2> make_pair (T1 a, T2 b)
   {
      return pair<T1,T2>(a,b);
   }
   ```
* With C++11, `make_pair()` had to support move semantics, which meant that the arguments had to become universal/forwarding references. Again, we have the problem that for references the type of the arguments does not decay. Therefore, the definition changed as follows:
   ```c++
   template<typename T1, typename T2>
   constexpr pair<typename decay<T1>::type, typename decay<T2>::type>
   make_pair (T1&& a, T2&& b)
   {
      return pair<typename decay<T1>::type,typename decay<T2>::type>
      (forward<T1>(a), forward<T2>(b));
   }
   ```
* Note that `std::decay<T>::type` performs three transformations:
   1. Remove references
   `int& → int`
   `const int&& → int`
   2. Remove cv-qualifiers
   `const int → int`
   `volatile int → int`
   3. Convert arrays/functions into pointers
`int[3] → int*`
`void(int) → void(*)(int)`
  This ensures the stored types inside the pair are value types (or decayed pointer types), never raw references or arrays.

## Move Semantics for `std::optional<>`
* `std::optional<T>` is a C++17 utility that represents an object that may or may not contain a value. It provides a safer alternative to using sentinel values (like -1 or `nullptr`) to indicate “no result”.
  ```c++
  #include <optional>
  #include <iostream>
  #include <string>
  
  std::optional<std::string> find_user(int id) {
      if (id == 1)
          return "Alice";
      return std::nullopt;   // No value
  }
  
  int main() {
      auto result = find_user(2);
  
      if (result) {                     // or result.has_value()
          std::cout << "User: " << *result << "\n";
      } else {
          std::cout << "User not found\n";
      }
  }
  ```
* Optional objects support move semantics. If you move the object as a whole, the state is copied and the contained object (if there is one) is moved. For example:
   ```c++
   std::optional<std:string> os;
   std::string s = "a long long long long long string";
   
   os = std::move(s); // Ok, moves
   std::string s1 = *os; // Ok, copies
   std::string s2 = std::move(*os); // Ok, moves
   ```
* `std::optional` supports moving contained object from a temporary optional. For example:
   ```c++
   std::optional<std::string> func();
   
   std::string s4 = func().value(); // OK, moves
   std::string s5 = *func(); // OK, moves
   ```
   This behavior is possible because reference qualifiers provides rvalue overloads:
   ```c++
   namespace std {
      template<typename T>
      class optional {
         ...
         constexpr T& operator*() &;
         constexpr const T& operator*() const&;
         constexpr T&& operator*() &&;
         constexpr const T&& operator*() const&&;
         constexpr T& value() &;
         constexpr const T& value() const&;
         constexpr T&& value() &&;
         constexpr const T&& value() const&&;
      };
   }
   ```
  | Feature           | `operator*`                    | `value()`                           |
  | ----------------- | ------------------------------ | ----------------------------------- |
  | Runtime check     | No                             | Yes                                 |
  | On empty optional | Undefined behavior             | Throws exception                    |
  | Use case          | Fast, when value is guaranteed | Safe, when failure must be detected |
  | Analogy           | Like dereferencing `T*`        | Like calling a checked getter       |


# Move Semantics for Smart Pointers


## Move semantics for `std::shared_ptr<>`
Shared pointers have the concept of shared ownership. Multiple shared pointers can “own” the same object and when the last owner is destroyed (or gets a new value), a “deleter” for the owned object is called.


While raw pointers do not benefit from move semantics (their address values are always copies), smart pointers can benefit from move semantics.
* Shared pointers (`std::shared_ptr<>`) support move semantics, which is helpful because moving a shared pointer is significantly cheaper than copying one.
* Unique pointers (`std::unique_ptr<>`) even support only move semantics because copying a unique pointer is not possible.

Note that copying the ownership is a pretty expensive operation. This is because a counter has to track the number of owners:
* Each time we copy a shared pointer, the owner counter is incremented
* Each time we destroy a shared pointer or assign a new value, the owner counter is decremented Furthermore, modifying the value of the counter is expensive because the modification is an ***atomic*** operation to avoid problems when multiple threads deal with shared pointers that own the same object.

It is therefore better to move shared pointers instead of copying them:

```c++
std::shared_ptr<int> lastPtr;
while(...){
   auto ptr{std::make_shared<int>(getValue())};
   lastPtr = std::move(ptr); // cheap
} // ptr destroyed, lastPtr is the only owner
```
It would significantly cheaper to iterate over a collection of shared pointers by reference:
```c++
std::vector<std::shared_ptr<...>> coll;

for (auto p : coll){ // expensive
   ...
}

for (const auto& p : coll) { // cheap
   ...
}
```

## Move semantics for `std::uniqu_ptr<>`
* The class template `std::unique_ptr<>` implements the concept of exclusive ownership. The type system ensures that there can be only one owner of an object at any one time. The trick is to use the type system to disable any attempt to copy a unique pointer. Because this check is done at compile time this approach does not introduce any significant performance overhead at runtime.
  ```c++
  #include<iostream>
  #include<string>
  #include<memory>
  
  std::unique_ptr<std::string> source() {
     static long id{0};
     auto ptr = std::make_unique<std::string>("obj"+std::to_string(++id));
     return ptr;
  }
  
  int main() {
     std::unique_ptr<std::string> ptr;
     for (int i=0;i<10;i++) {
        ptr = source(); // move assign
        std::cout << *ptr << "\n";
     }
  }
  ```
* As usual for moved-from types, to pass ownership to a sink function you can only pass it with `std::move()`:
  ```c++
  std::vector<std::unique_ptr<std::string>> coll;
  
  auto up = std::make_unique<std::string>("Hello");
  
  coll.push_back(up); // Error
  coll.push_back(std::move(up); // Ok, move
  ```
* If you pass a unique pointer to a potential sink function that takes the argument by reference, you do not know whether the ownership was moved. Whether the ownership was moved depends on the implementation of the function. In that case, you can double-check the state with `operator bool()`:
  ```c++
  auto up = std::make_unique<std::string>("Hello");
  sink(std::move(up)); // might move ownership to sink()
  if (up){ // check if up still has ownership
   ...
  }
  ```
  Alternatively,
  ```c++
  auto up = std::make_unique<std::string>("Hello");
  sink(std::move(up)); // might move ownership to sink()
  up.reset(); // ensure ownership is gone
  ```
# Move Semantics for IOStreams

Since C++11, the IOStreams library also provides function overloads (`operator<<() &&`) to take rvalue references, which allows us to take temporary objects. For example:
```c++
std::string s="hello";
std::ofstream("file.txt") << s << '\n';
```
Or even
```c++
std::ofstream("file.txt") << "hello" << '\n';
```
In the same way, you can parse a given string using a temporary string stream with `operator<<() &&`:
```c++
#include<iostream>
#include<string>
#include<sstream>

int main() {
   std::string name, firstname, lastname;
   name = "Tina Turner";
   std::istringstream{name} >> firstname >> lastname;  // OK since C++11
   std::cout << firstname << " " << lastname << '\n';
}
```
# Move Semantics for Multithreading