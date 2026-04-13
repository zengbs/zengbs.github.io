---
title: "Class Scope under Inheritance"
date: 2026-04-13T15:32:36+08:00
draft: false
---

---
title: Class Scope under Inheritance
tags: [CPP]

---

# Class Scope under Single Inheritance
* Under inheritance, the scope of the derived class is nested within the scope of its immediate base classes. If a name is unresolved within the scope of the derived class, the enclosing base class scope is searched for a definition of the name.
* Although a base class member can be accessed directly as if it were a member of the derived class, in practice it retains its base class membership.
   ```c++
   #include <iostream>
   #include <string>
   
   int ival = 3;
   
   class Base {
   public:
      Base(int val) : ival(val){}
      int ival;
   };
   
   class Derived : public Base {
   public:
      Derived(int val) : Base(val+1), ival(val) {}
   
      void show(){
         std::cout << "ival = " << ival << "\n"; // 1
         std::cout << "Base::ival = " << Base::ival << "\n"; // 2
         std::cout << "::ival = " << ::ival << "\n"; // 3
      }
   
      int ival;
   };
   
   int main() {
   
      Derived d(1);
   
      d.show();
   
      return 0;
   }
   ```
* The actual process of name resolution is as follows:
    1. `d` is an object of the `Derived` class. The scope of the `Base` class is searched for `ival` first. It is not
found.
    2. Since `Derived` is derived from `Base`, the `Base` class scope is next examined to find a declaration of `ival`. It is found to be a member of the `Base` base class. The reference is resolved successfully.
   ```c++
   #include <iostream>
   #include <string>
   
   int ival = 3;
   
   class Base {
   public:
      Base(int val) : ival(val){}
      int ival;
   };
   
   class Derived : public Base {
   public:
      Derived(int val) : Base(val+1){}
   
      void show(){
         std::cout << "ival = " << ival << "\n"; // 2
      }
   };
   
   int main() {
   
      Derived d(1);
   
      d.show();
   
      return 0;
   }
   ```
* In effect, a derived class member with the same name as a member of the base class hides direct access of the base class member. To access the base class member, we must qualify it with the class scope operator. If the class used to qualify the member does not define the member, a compilation error emits.
   ```c++
   #include <iostream>
   #include <string>
   
   int ival = 3;
   
   class Base {
   public:
   };
   
   class Derived : public Base {
   public:
      Derived(int val) : Base(){}
   
      void show(){
         // Error: ival is not a member of Base
         std::cout << "ival = " << Base::ival << "\n";
      }
   };
   
   int main() {
   
      Derived d(1);
   
      d.show();
   
      return 0;
   }
   ```
* The resolution of a class member is always performed prior to determining whether the access is actually legal, which may at first seem counterintuitive. 
* Why is this design chosen? Because if C++ didn’t follow this rule, changing only the access level of a base class member could change which variable is chosen, leading to unexpected behavior. For example, suppose we have:
   ```c++
   int dval; // global variable
   
   class ZooAnimal {
   private:
       int dval;  // private member
   };
   
   int Bear::mumble(int ival) {
       foo(dval);
   }
   ```
   The `dval` in `foo(dval)` resolves to the private `ZooAnimal::dval`, even though it's inaccessible — so the code will give a compile-time error.
But imagine the class designer later changes this to:
   ```c++
   class ZooAnimal {
   protected:  // just changed access
       int dval;
   };
   ```
   Now suddenly, `ZooAnimal::dval` is accessible, so `foo(dval) `now calls a different overload of `foo()`, because the argument is now an `int` from the class instead of the global `int` `dval`.

# Class Scope under Multiple Inheritance

```c++
#include <iostream>

class ZooAnimal {
public:
   void gender(){
      std::cout << "ZooAnimal::gender()\n";
   }
   void color(){
      std::cout << "ZooAnimal::color()\n";
   };
   void highlight() {
      std::cout << "ZoomAnimal::highlight()\n";
   };
};

class Endangered {
public:
   void highlight() {
      std::cout << "Endangered::highlight()\n";
   };
   void print() {
      std::cout << "Endangered::print()\n";
   }
};

class Bear : public ZooAnimal {
public:
   void color(){
      std::cout << "Bear::color()\n";
   }
};

class Panda : public Bear, public Endangered {
public:
};

int main() {

   Panda p;

   p.color(); // Bear::color()
   p.gender(); // ZooAnimal::gender()
   p.print(); // Endangered::print()
   //p.highlight(); // Error: ambiguous
   p.ZooAnimal::highlight(); // ZoomAnimal::highlight()
   p.Endangered::highlight(); // Endangered::highlight()
}
```
* Although there are two latent ambiguities in the inheritance of `highlight()` functions from the `ZooAnimal` and `Endangered` base classes, no error message is issued until an ambiguous attempt to reference either of those functions occurs.
* A lookup of an identifier begins with a search of the immediate scope in which the reference occurs.
* Under multiple inheritance, the search simulates the simultaneous examination of each base class inheritance subtree — in our example, both the `Endangered` and the `Bear/ZooAnimal` subtrees. If a declaration is found in only one base class subtree, the identifier is resolved and the lookup algorithm concludes. This is what happens with the invocation of `gender()`.
* If a declaration is found in two or more base class subtrees, the reference is ambiguous, and a compile-time error message is generated. This is what happens with the unqualified invocation of `highlight()`.
* A program-level solution to the member ambiguity is to qualify explicitly the instance we wish to invoke using the class scope operator. For example:
   ```c++
   p.ZooAnimal::highlight(); // ZoomAnimal::highlight()
   p.Endangered::highlight(); // Endangered::highlight()
   ```
   While this solves the problem, in general it is not a satisfactory solution. The reason is that the user has now been placed in the position of having to decide what the right behavior is for the Panda class. This burden of responsibility should never be placed on the user of a class.
* The simplest way to do this is to define a named instance within the derived class that provides the desired behavior. For example:
   ```c++
   inline void Panda::highlight() {
      Endangered::highlight();
   }
   
   inline ostream&
   Panda::print( ostream &os ) const
   {
      Bear::print( os );
      Endangered::print( os );
      return os;
   }
   ```