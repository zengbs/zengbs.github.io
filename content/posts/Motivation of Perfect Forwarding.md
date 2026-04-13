---
title: "Motivation of Perfect Forwarding"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

---
title: Motivation of Perfect Forwarding
tags: [CPP]

---

Given a function with 1 parameter of class type `X`, we need 3 overloads to fulfill all value category. This mean having 9 overloads for 2 generic arguments and 27 overloads for 3 generic arguments. For example:
```c++
class X {...};
class Y {...};

// 1 generic argument needs 3 overloads
void foo(const X&);
void foo(X&);
void foo(X&&);

// 2 generic arguments need 9 overloads
void bar(const X&, const Y&);
void bar(const X&, Y&);
void bar(const X&, Y&&);
void bar(X&, const Y&);
void bar(X&, Y&);
void bar(X&, Y&&);
void bar(X&&, const Y&);
void bar(X&&, Y&);
void bar(X&&, Y&&);
```
Therefore, C++11 introduced "perfect forwarding" without any overloads but still keeping the type and the value category.