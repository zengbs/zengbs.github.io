---
title: "Auto"
date: 2026-04-13T15:32:36+08:00
draft: false
---

---
title: Auto
tags: [CPP]

---

* `auto` disregards reference from giver:
   ```c++
   int i = 0, &r = i;
   auto a = r; // a is an int
   ```
* `auto` disregards top-level const from giver but keep low-level const (i.e., always keep the information of low-level const):
   ```c++
   const int ci = i, &cr = ci;
   auto b = ci; // b is an int (top-level const in ci is dropped)
   auto c = cr; // c is an int (cr is an alias for ci whose const is top-level)
   auto d = &i; // d is an int* (& of an int object is int*)
   auto e = &ci; // e is const int* (& of a const object is low-level const)
   ```
* `auto` keeps pointer from giver:
   ```c++
   int i =1;
   
   // p1 is int*
   auto  p1 = &i;
   
   // p2 is also int*
   auto *p2 = &i;
   ```
* If we want the deduced type to have a top-level const, we must say so explicitly:
   ```c++
    // deduced type of ci is int; f has type const int
   const auto f = ci;
   ```
* We can also specify that we want a reference to the auto-deduced type. Normal initialization rules still apply:
   ```c++
    // g is a const int& that is bound to ci
   auto &g = ci;
   
    // error: we can’t bind a plain reference to a literal
   auto &h = 42;
   
   // ok: we can bind a const reference to a literal
   const auto &j = 42; 
   ```
* When we define several variables in the same statement, it is important to remember that a reference or pointer is part of a particular declarator and not part of the base type for the declaration.
   ```c++
   // ‘auto’ is ‘int’
   // k is int; l is int&
   auto k = ci, &l = i;
   
   // ‘auto’ is ‘int’
   // m is a const int&; p is a pointer to const int
   auto &m = ci, *p = &ci;
   
   // error: inconsistent deduction for ‘auto’: ‘int’ and then ‘const int’
   auto &n = i, *p2 = &ci;
   ```