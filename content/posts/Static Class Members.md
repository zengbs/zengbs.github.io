---
title: "Static Class Members"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

---
title: Static Class Members
tags: [CPP]

---

> [ISO 1998 1.8 §5] Unless it is a bit-field, a most derived object shall have a non-zero size and shall occupy one or more bytes of storage.
```c++
#include<iostream>
class Empty {};
int main() {
    Empty e;
    std::cout << sizeof(e) << "\n";
}
```

> [ISO 1998 1.8 §5] Base class sub-objects may have zero size.
```c++
class Empty {};
class Derived : public Empty {
    int x;
};

int main() {
    // Empty Base Optimization (EBO) 
    // Usually 4, not 5
    std::cout << sizeof(Derived) << "\n";
}
```

> [ISO 1998 9.4.2 §1] A static data member is not part of the subobjects of a class. There is only one copy of a static data member shared by all the objects of the class.
```c++
#include<iostream>
class Bar {
   static Bar mem1;
};

int main() {
    Bar b;
    // Output: 1
    std::cout << sizeof(b) << "\n"; 
}
```

0. A non-const and non-inline static data member is not allowed to have an in-class initializer. Because a non-inline static data member is not actually “defined” inside the class, and giving it an initializer would implicitly make it a definition — which creates multiple-definition problems when the class is in a header.
   ```c++
   class MyClass {
   public:
      inline static std::string msg2{"OK"};  // OK, since C++17
      const static std::string msg3{"OK"};   // Error
      static std::string msg1{"OK"};         // Error
      inline static int a1{1};               // OK
      const static int a2{2};                // OK
      static int a3{3};                      // Error
      const static std::string msg4;         // OK
   };
   
   // OK
   const std::string MyClass::msg4{"ddd"};
   ```

1. A static data member can be of the same class type as that of which it is a member. A nonstatic data member is restricted to being declared as a pointer or a reference to an object of its class.
    ```c++
    class Bar {
       static Bar mem1;
       Bar& mem2;
       Bar* mem3;
       Bar mem4;
    }
    ```
2. A static data member can appear as a default argument to a member function of the class, but a nonstatic member cannot.
   ```c++
   class Bar {
      int mem0;
      static int mem1;
      void fun(int = mem1);
      void fun(int = mem0);
   };
   // must define at compile time
   Bar::mem1 = 1;
   ```
   Because the expressions used as default parameters must be defined at compile time, only static member can be used.


# Static Member Functions
A member function requires an object to be called; however if the member function only operates on static members, creating an object solely for this purpose is unnecessary. A better way is to declared the member function itself as static, allowing it to directly access static members without needing an object.

```c++
#include <iostream>

class Foo{
public:
    static int i;
    static void bar(int inc){
        i += inc;
    }
};

int Foo::i = 0;

int main() {
    Foo::bar(1);
    std::cout << Foo::i;
    return 0;
}
```

1. The function definition that appears outside of the class body must not specify the keyword static.
   ```c++
   #include <iostream>
   
   class Foo{
   public:
       static int i;
       static void bar(int inc);
   };
   
   void Foo::bar(int inc){
       Foo::i += 1;
   }
   
   int Foo::i = 0;
   
   int main() {
       Foo::bar(1);
       std::cout << Foo::i;
       return 0;
   }
   ```
2. Static member functions have no `this` pointer. This makes sense when you think about it -- the `this` pointer always points to the object that the member function is working on. Static member functions do not work on an object, so the `this` pointer is not needed.
3. Static member functions can directly access other static members (variables or functions), but not non-static members. This is because non-static members must belong to a class object, and static member functions have no class object to work with!