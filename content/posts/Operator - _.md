---
title: "Operator - _"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: Operator - >
tags: [CPP]

---

1.  `operator->` must be defined as a class member function.
2.  A definition for an object of type ScreenPtr must provide an initializer, an object of type Screen, to which the ScreenPtr object is made to refer, otherwise the ScreenPtr object definition is in error.
3.  The return type of an overloaded member access operator arrow must either be a pointer to a class type or an object of a class for which the member access operator arrow is defined.
4. If the return type is a pointer to class type, the semantics for the built-in member access operator arrow are then applied to the return value.
   ```c++
   #include <iostream>
   
   class Foo {
   public:
      Foo (int iv) : m_iv(iv){};
      void IntAbs(){  m_iv = ( m_iv > 0 ) ? m_iv : -m_iv; }
      int m_iv;
   };
   
   class FooPtr {
   public:
      FooPtr( Foo &f ) : ptr( &f ){};
      Foo* operator->(){ return ptr; };
      Foo& operator*() { return *ptr; }
   
   private:
      Foo* ptr;
   };
   
   int main(){
      Foo foo(-4);
      FooPtr ptr(foo);
      ptr->IntAbs();
      std::cout << foo.m_iv << "\n";
      return 0;
   }
   ```
5. If the return value is another class object or reference, the process is applied recursively until either a pointer type is returned or the statement is in error.
   ```c++
   #include <iostream>
   
   class D {
   public:
       void hello() {
           std::cout << "Hello from D\n";
       }
   };
   
   // The final operator->() in a chain must return
   // a pointer type (e.g., T*) for member access to succeed.
   class C {
       D d;
   public:
       D* operator->() {
           std::cout << "C::operator->() called\n";
           return &d;
       }
   };
   
   class B {
       C c;
   public:
       C& operator->() {
           std::cout << "B::operator->() called\n";
           return c;
       }
   };
   
   class A {
       B b;
   public:
       B operator->() {
           std::cout << "A::operator->() called\n";
           return b;
       }
   };
   
   int main() {
       A a;
       a->hello();
   }
   ```
{% endraw %}