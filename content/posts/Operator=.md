---
title: "Operator="
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

---
title: Operator=
tags: [CPP]

---

1. If objects of a class type are to be assigned values of a type other than their own class type, assignment operators accepting a parameter of this other type can be defined. For example: `String s = "Sfwrlff";`.
5. What shall the return type of an operator assignment be?
    * The reference to the current object. Because assignment operators are meant to allow chaining assignments, like this: `a = b = c`. This work correctly only if `b = c` returns a reference to `b`, so that `a = b = c` becomes valid.
    * Return by value would break assignment chaining and be less efficient.
    * Return by const reference (`const ClassName&`) is bad because it would prevent doing things like `(a = b) = c;` (i.e., reassigning after assignment).