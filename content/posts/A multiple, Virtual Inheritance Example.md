---
title: "A multiple, Virtual Inheritance Example"
date: 2026-04-13T15:32:36+08:00
draft: false
render_with_liquid: false
---

---
title: 'A multiple, Virtual Inheritance Example'
tags: [CPP]

---

* An instance of a class template can serve as an explicit base class.
   ```c++
   class Derived : public Base<T> {...}
   ```
* A class template can be derived from a nontemplate base class.
   ```c++
   template<class T>
   class Derived : private Base {...}
   ```
* A class template can also serve as both a derived and base class of a derivation.
   ```c++
   template<class T>
   class Derived : public Base<T>{...}
   ```
* The template parameter itself can serve as a base class.
   ```c++
   template <typename T>
   class Derived : public T{...}
   ```
   But `T` must be a class type. A built-in type `T` results in compile-time error.
* When serving as a base class, a class template must be qualified with its full parameter list.
   ```c++
   template < class Type >
   class Derived : public Base<Type> {};
   
   // error: Base is a template so template arguments must be specified
   template < class Type >
   class Derived : public Base{};
   ```
   
   
```c++
#include <iostream>
#include <cassert>

template <typename T>
class Base {
public:
    int _size = 10;
};

template <typename T>
class Derived : public Base<T> {
public:
    void printSize() {
        // std::cout << _size << "\n"; //  Error: _size is unqualified and lookup fails
        std::cout << this->_size << "\n";             // OK: via 'this' makes it dependent
        std::cout << Base<T>::_size << "\n";          // OK: qualified name also works
    }

    void checkIndex(int ix) {
        // assert(ix >= 0 && ix < _size); //  Error without qualification
        assert(ix >= 0 && ix < this->_size);          //  OK
        std::cout << "Index " << ix << " is valid.\n";
    }
};

int main() {
    Derived<int> d;
    d.printSize();       // Output: 10 (twice)
    d.checkIndex(5);     // Output: Index 5 is valid.
}
```