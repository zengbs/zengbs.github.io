---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---

# Non-static members
A pointer to a class member doesn’t store a memory address like a normal pointer does. Instead, it stores a kind of offset or internal identifier that tells the compiler "which member inside the object" to access.



# Static members
Static class members are global objects and functions that belong to the class. Pointers to these are ordinary pointers.

# Example
```c++
#include <iostream>

class MyClass {
public:
   int _mem;
   static int _s_mem;
   void foo(int);
   static void s_foo(int);
};

void MyClass::foo(int a){
   _mem = a;
}

void MyClass::s_foo(int a){
   _s_mem = a;
}

int MyClass::_s_mem = -1;

int main(){

   // pointer to class member
   typedef int MyClass::*p_MyClass;
   p_MyClass pMem = &MyClass::_mem;

   // pointer to class member function
   void (MyClass::* p_foo)(int) = &MyClass::foo;

   MyClass obj;

   (obj.*p_foo)(2);

   std::cout << obj.*pMem << std::endl;

   // pointer to static class member
   int *pi = &MyClass::_s_mem;
   *pi = -3;

   // pointer to static class member function
   void (*s_foo)(int) = &MyClass::s_foo;
   s_foo(*pi);

   std::cout << *pi << std::endl;

   return 0;
}
```
{% endraw %}