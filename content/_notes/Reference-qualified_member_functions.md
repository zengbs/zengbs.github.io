---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

# Motivation
1. To prevent assigning to temporaries (rvalue). For example,
   ```c++
   basic_string& operator=(const basic_string& str) {...}
   std::string getName() { ... };
   
   // assign lvalue to rvalue
   // but compiler doesn't emit error at compile time
   getName() = "a string";
   ```
   ```c++
   basic_string& operator=(const basic_string& str) & {...}
   std::string getName() { ... };
   
   // compile error
   getName() = "a string";
   ```
2. To distinguish between lvalue and rvalue semantics.


# Usage
1. Ref-qualified member cannot coexist with non-ref-qualified one. Use one or the other.
2. The `&` and `&&` ref-qualifiers are used for member functions that are called on lvalue and rvalue object, respectively. For example:
   ```c++
   class C {
      void foo() const& {}
      void foo() && {}
      void foo() const&& {}
      void foo() & {}
   };
   
   
   C obj;
   obj.foo() // calls foo() &
   C{}.foo() // class foo() &&
   
   const C cx;
   cx.foo() // calls foo() const&
   std::move(cx).foo() // calls foo() const&&
   ```

# Rule of thumb
* Use reference qualifiers in assignment operators to prevent assigning to rvalue.
* Use reference qualifiers when references to objects are returned to prevent accessing destroyed temporary object. See [Define a Getter for a Movable Object](/CHxUWNWBT9uGaIc8IeDLuw) for more details.
{% endraw %}