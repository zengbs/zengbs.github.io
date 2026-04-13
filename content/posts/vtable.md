---
title: "vtable"
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

---
title: vtable
tags: [CPP]

---


## Creating a vtable for each class
Given a member function in a class...

* If the function is declared as `virtual` in the class, it appears in the vtable (the converse is false, see beow).
* If a derived class defines a virtual function with **the same name and signature** as one in its base class, the derived class's version will replace the base's version in the vtable, regardless of whether the function in the derived class uses the `override` or `virtual` keyword. Otherwise, the function does not replace the base class's virtual function in the vtable. Instead, it is treated as a new function.
* If a function in the derived class is declared as `override` in the derived class, then there must be a virtual function with the same name and signature in its base class, and of course in the vtable.
* Otherwise, the function do not participate in the vtable and are resolved at compile time based on the static type.

## Creating a pointer by `A* ptr_A = new C()` or by `C c; A* ptr_A = &c;`
* `A` **must** be any intermediate or direct base class of `C` (upcasting); otherwise, the code will not compile.

## Dynamic casting a pointer: `C* ptr_C = dynamic_cast<C*>(ptr_A);`
* Check if `ptr_C` is null. If (1) `ptr_A` does not hold the instance of `C` or if (2) all ancestors of `C` are non-polymorphic, then `dynamic_cast` returns null.
* Why `dynamic_cast` does not only work for upcasting? The example below demostrates that downcasting is safe (not always):
	```c++
	A* basePtr = new B(); // B is derived from polymorphic A
	B* derivedPtr = dynamic_cast<B*>(basePtr);
	```

## Calling a function via a pointer
* Say, `A* ptr_A = new C();`
* `ptr_A` holds a `vptr` to the vtable corresponding to `C`.
* Neither downcasting nor upcasting alters the vtable that `vptr` points to in `ptr_A`.
* The function name `func` should be declared in `A`; otherwies, `ptr_A->func()` results in compile error.
* If `func()` does not appear in the vtable, `ptr->func()` calls the `func()` in `A`.
* If `func()` does appear in the vtable, `ptr->func()` calls the `func()` in the vtable.
## Calling a function via an object
* When calling a function on an object directly (e.g., `B b;` `b.func();`), without using a pointer, the vtable lookup is not used — even if `B` and its ancestors have virtual functions.