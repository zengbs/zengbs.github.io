---
title: "Initializer lists"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

---
title: Initializer lists
tags: [CPP]

---

* When there are constructors for both a speciﬁc number of arguments and an initializer list, the version with the initializer list is preferred:
  ```c++
  class P {
  public:
     P(int,int);
     P(std::initializer_list<int>);
  };
  
  P p(77,5);    // call P(int,int)
  P q{77,5};    // call P(initializer_list)
  P r{77,5,42}; // call P(initializer_list)
  P s = {77,5}; // call P(initializer_list)
  ```
  Without the constructor for the initializer list, the constructor taking two ints would be called to initialize `q` and `s`, while the initialization of `r` would be invalid.
* Passing an argument to a function parameter is copy-initialization instead of direct-initialization.
* `explicit` constructors are allowed only in direct-initialization, not in copy-initialization.

```c++
class P {
public:
   P(int a, int b);
   explicit P(int a, int b, int c);
};

P x(77,5);       // direct-initialization, ok
P y{77,5};       // direct-list-initialization, ok
P z{77,5,42};    // direct-list-initialization, ok
P v = {77,5};    // copy-list-initialization, ok
P w = {77,5,42}; // copy-list-initialization, error

void fp(const P&);

fp({47,11});     // copy-list-initialization, ok
fp({47,11,3});   // copy-list-initialization, error
fp(P{47,11});    // direct-list-initialization, ok
fp(P{47,11,3});  // direct-list-initialization, ok
```