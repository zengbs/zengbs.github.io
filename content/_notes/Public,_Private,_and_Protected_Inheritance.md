---
title: "Public, Private, and Protected Inheritance"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: 'Public, Private, and Protected Inheritance'
tags: [CPP]

---

![HkfKu3yayl](https://hackmd.io/_uploads/SysA9iCmee.jpg =45%x)

# Public Inheritance
* A public derivation is referred to as ***type inheritance***. The derived class is a subtype of the base class; it overrides the implementation of all type-specific member functions of the base class while inheriting those that are shared.
* The derived class in general reflects an ***is-a*** relationship; that is, it provides a specialization of its more general base class.

# Private Inheritance
* A private derivation is referred to as ***implementation inheritance***. The derived class does not support the public interface of the base class directly; rather, it wishes to reuse the implementation of the base class while providing its own public interface. 
# Protected Inheritance
* Under protected inheritance, all the public members of the base class become protected members of the derived class. This means they can be accessed from classes subsequently derived from the class, but not from outside the class hierarchy.

# Exempting Individual Members
* In this example, the class Derived was inherited from the class Base using private inheritance. As a result, all protected and public members of Base are inherited as private members. However, we can exempt individual members as follows:
  ```c++
  #include<iostream>
  
  class Base {
  public:
     void foo () { std::cout << "Calls Base::foo()\n"; }
     void bar () { std::cout << "Calls Base::bar()\n"; }
  };
  
  class Derived : private Base {
  public:
     // Exempting Base::foo()
     using Base::foo;
  };
  
  int main() {
  
     Derived d;
     d.foo();
     // d.bar(); // Error
  
     return 0;
  }
  ```
* Another reason to exempt individual members is to allow subsequent derivations access to the protected members of the private base class. For example,
   ```c++
   #include<iostream>
   
   class Base {
   public:
      Base( int m, int n ) : _m(m), _n(n){}
      void foo () { std::cout << "Calls Base::foo()\n"; }
      void bar () { std::cout << "Calls Base::bar()\n"; }
   protected:
      int _m;
   private:
      int _n;
   };
   
   class Derived : private Base {
   public:
      // Exempt Base::foo()
      using Base::foo;
   
      Derived( int m, int n ) : Base(m, n) {}
   
   protected:
      using Base::_m;
   private:
      // using Base::_n; // Error
   };
   
   class Derived2 : public Derived {
   public:
      Derived2(int m, int n) : Derived(m, n) {}
      void show_m(){
         std::cout << "m = " <<  _m << "\n";
      }
   };
   
   int main() {
   
      Derived2 d2(1, 2);
      d2.show_m(); // m = 2
   
      return 0;
   }
   ```
   The derived class can only restore the inherited member to its original access level. The access level cannot be made either more or less restrictive than the level originally specified within the base class.
* A common pattern of multiple inheritance is to inherit the public interface of one class and the private implementation of a second class. For example,
   ```c++
   #include <iostream>
   #include <string>
   
   // Public interface
   class Shape {
   public:
       virtual void draw() const = 0;  // Pure virtual
       virtual ~Shape() {}
   };
   
   // Private implementation
   class Logger {
   protected:
       void log(const std::string& msg) const {
           std::cout << "[LOG]: " << msg << std::endl;
       }
   };
   
   // Derived class uses both
   class Circle : public Shape, private Logger {
   public:
       void draw() const override {
           log("Drawing a circle");  // Use Logger internally
           std::cout << "Circle is drawn." << std::endl;
       }
   };
   
   int main() {
   
       Circle c;
       c.draw(); // Allowed: draw() is public
   
       // c.log("test"); // Error: 'log' is private through inheritance
       return 0;
   }
   ```
# Object Composition
* There are actually two forms of object composition:
    1. ***Composition by value***, in which an actual object of the class is declared to be a member, as illustrated two subsections ago by our revised PeekbackStack implementation.
    2. ***Composition by reference***, in which the object is addressed indirectly through either a reference or a pointer member to the class object.
* By generally we mean that composition by value is not necessarily the most efficient representation strategy for large class objects, particularly if they are copied often. Composition by reference, in this case, can allow us to avoid unnecessary copying when used in conjunction with a strategy of reference counting and what is called ***copy on write***.



# Summary

| Inheritance Type | Rule of Thumb                                                                               | Use Case                                                                                              |
| ---------------- | ------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `public`         | Use when you want to expose the base class’s public interface as part of the derived class. | "is-a" relationship: `class Dog : public Animal`                                                      |
| `protected`      | Rarely used. Use when only derived classes should access base members, but not clients.     | Internal derivation where public interface is not exposed.                                            |
| `private`        | Use when inheritance is purely an **implementation detail**, not visible to the client.     | "implemented-in-terms-of": e.g., stack implemented via vector: `class Stack : private std::vector<T>` |

| Composition Type | Rule of Thumb                                                                                   | Use Case                                                     |
| ---------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| by value     | Use when the composed object is **always required** and **has the same lifetime**.              | `Car` has `Engine` (always has one)                          |
| by reference | Use when the composed object is **shared**, **externally owned**, and **never null**.           | Injecting dependencies (e.g., reference to a logger)         |
| by pointer   | Use when the composed object is **optional**, **polymorphic**, or **shared/owned dynamically**. | Optional or changeable behavior: `std::unique_ptr<Strategy>` |

{% endraw %}