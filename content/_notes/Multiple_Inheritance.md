---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

![image](https://hackmd.io/_uploads/SyZM4biXeg.png)

* To support multiple inheritance, the derivation list, as in
  ```c++
  class Bear : public ZooAnimal { ... };
  ```
  is extended to support a comma-separated list of base classes. For example:
  ```c++
  class Panda : public Bear, public Endangered { ... };
  ```
  Each listed base class must also specify its access level, one of `public`, `protected`, or `private`. As with single inheritance, a base class under multiple inheritance can be listed only if its definition has already been seen.
* In practice, two base classes seems to be the most common, with one base class often representing a public abstract interface and the second base class providing a private implementation.
* Derived classes inheriting from three or more immediate base classes follow a mixin-based design style in which each base class represents a facet of the complete interface of the derived class.
* Under multiple inheritance, a derived class contains a base class subobject for each of its base classes.
* The base class constructors are invoked in the declaration order within the class derivation list.
* The order of constructor invocation is not affected by either the
presence of the base class within the member initialization list or the order in which they are listed. 
* Similarly, the order of destructor invocation is always the reverse of the constructor order.
* Under single inheritance, the public and protected members of the base class can be accessed directly as if they were members of the derived class. The same holds true with multiple inheritance.
* Under multiple inheritance, however, there is the possibility of inheriting a member with the same name from two or more base classes. In this case, direct access is ambiguous and results in a compile-time error even if the two inherited member functions define different parameter
types.
* The reason for this is that the inherited member functions do not form a set of overloaded functions within
the derived class. `print()`, therefore, is resolved only using name resolution on the name `print` rather than using overload resolution based on the actual argument types.
* Under single inheritance, a pointer, a reference, or an object of a derived class, if necessary, is converted automatically to a pointer, a reference, or an object of a publically derived base class. Again, the same holds true with multiple inheritance. 
   ```c++
   #include <iostream>
   
   class ZooAnimal {
   public:
      void gender(){
         std::cout << "ZooAnimal::gender()\n";
      }
      virtual void color() = 0;
   };
   
   class Endangered {
   public:
      void landAnimals() {
         std::cout << "Endangered::landAnimals()\n";
      }
      virtual void highlight() = 0;
   };
   
   
   class Bear : public ZooAnimal {
   public:
      virtual void color(){
         std::cout << "Bear::color()\n";
      }
      void hungry(){
         std::cout << "Bear::hungry()\n";
      }
   };
   
   class Panda : public Bear, public Endangered {
   public:
      void color() override {
         std::cout << "Panda::color()\n";
      }
   
      void highlight() override {
         std::cout << "Panda::highlight()\n";
      }
   };
   
   int main() {
   
      ZooAnimal* p = new Panda;
   
      p->gender(); // ZooAnimal::gender()
      p->color(); // Panda::color()
      //p->highlight(); // Error
      //p->hungry(); // Error
   
      Bear* q = new Panda;
      q->gender(); // ZooAnimal::gender()
      q->color(); // Panda::color()
      q->hungry(); // Bear::hungry()
   
      Endangered* r = new Panda;
   
      r->highlight(); // Panda::highlight()
      r->landAnimals(); // Endangered::landAnimals()
      
      Panda s;
      s.color(); // Panda::color()
      s.highlight(); // Panda::highlight()
      s.hungry(); // Bear::hungry()
      s.landAnimals(); // Endangered::landAnimals()
      s.gender(); // ZooAnimal::gender()
   }
   ```
   When a `Bear` or `ZooAnimal` pointer or reference is initialized with or assigned the address of a `Panda` class object, both the `Panda`-specific and `Endangered` portions of the `Panda` interface are no longer accessible. Similarly, when an `Endangered` pointer or reference is initialized with or assigned the address of a Panda class object, both the `Panda`-specific and `Bear` portions of the Panda interface are no longer accessible.
{% endraw %}