---
title: "static_cast"
date: 2026-04-13T15:32:37+08:00
draft: false
---

---
title: static_cast
tags: [CPP]

---


*  If `T` is an lvalue reference type or an rvalue reference to function type, the result is an lvalue; if `T` is an rvalue reference to object type, the result is an xvalue; otherwise, the result is a prvalue. 

   |                              | `static_cast<Type>` | `static_cast<Type&>` | `static_cast<Type&&>` |
   | ---------------------------- | ------------------- | -------------------- |:---------------------:|
   | Value category of the result | prvalue             | lvalue               |        xvalue         |
   | Declared type of the result                             |      Type               |  Typr&                    |     Type&&                  |

* The `static_cast` operator shall not cast away constness.