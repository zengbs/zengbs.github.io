---
title: "const_cast"
date: 2026-04-13T15:32:36+08:00
draft: false
---

---
title: const_cast
tags: [CPP]

---

* `const_cast` removes only a low-level `const` from an object. i.e., object can be modified after casting.


```c++=
  const int a = 10; 
  const int* b = &a; 
        
  // Function f() expects int*, not const int*
  //   f(b);
  int* c = const_cast<int*>(b);
  f(c);  // 10
        
  // Error: lvalue is const
  //  *b = 20;
        
  // Error: Undefined behavior
  //  *c = 30;
        
  int a1 = 40; 
  const int* b1 = &a1;
  int* c1 = const_cast<int*>(b1);
        
  // Integer a1, the object referred to by c1, has not been declared const
  *c1 = 50;
  cout << a1 << endl; // 50
```