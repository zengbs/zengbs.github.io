---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---

# Rules for Declaring Functions with `noexcept`
* The order of qualifiers in a function definition shall have the [form](/gaQ1pmssRMuFVEutIXwfWg).
* The `noexcept` operator performs a compile-time check that returns true if an expression is declared to not throw any exceptions.
* The noexcept condition must be a compile-time expression that yields a value convertible to `bool`.
* You cannot overload functions that have only different `noexcept` conditions.
* In class hierarchies, a `noexcept` condition is part of the specified interface. Overwriting a base class function that is `noexcept` in a derived class with a function that is not `noexcept` is an error (but not the other way around).
   ```c++
   class Ancestor {
   public:
      virtual void foo() noexcept {};
      virtual void foobar() noexcept {};
      virtual void bar() {};
      void baz() noexcept {};
   };
   
   class Descendant : public Ancestor {
   public:
       // OK
       void foo() noexcept override{}
   
       // ERROR, overriding cannot discard exception-specification
       //void foobar() override {};
   
       // OK, overriding can add except-specification
       void bar() noexcept override{}
   
       // OK, hiding instead of overriding
       void baz() {}
   };
   
   int main() { }
   ```
* Descendant class should relax exception guarantees.
   ```c++
   class Ancestor {
       virtual void foo1() noexcept(true) {};
       virtual void foo2() noexcept(true) {};
       virtual void foo3() noexcept(false) {};
       virtual void foo4() noexcept(false) {};
   };
   
   class Descendant : public Ancestor {
       void foo1() noexcept(true) override {};
       //void foo2() noexcept(false) override {}; // Error!
       void foo3() noexcept(true) override {};
       void foo4() noexcept(false) override {};
   };
   
   int main() { }
   ```
{% endraw %}