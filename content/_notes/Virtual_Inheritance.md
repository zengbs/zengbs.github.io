---
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---

* Inheritance is a specialized form of composition by value.
* Virtual inheritance is a specialized form of composition by reference.
* When we write
   ```c++
   class Bear : public ZooAnimal { ... };
   ```
    each Bear class object contains all the nonstatic data members of its ZooAnimal base class subobject together with the nonstatic data members declared within Bear. Similarly, when a derived class is itself an object of derivation, as in
    ```c++
    class PolarBear : public Bear { ... };
    ```
    each `PolarBear` class object contains all the nonstatic data members declared within `PolarBear` together with all the nonstatic data members of its `Bear` subobject and all the nonstatic data members of its `ZooAnimal` subobject.
* Take the diagram below as an example, each `Panda` object contains two `ZooAnimal` subobjects: the instance contained within its `Bear` subobject and the instance contained within its `Racoon` subobject.
![image](https://hackmd.io/_uploads/r1DFk8MEex.png =50%x)
It's a bad idea. Because:
  1. Storing two copies of the `ZooAnimal` subobject wastes storage, because `Panda` needs only one instance.
  2. The `ZooAnimal` constructor is invoked twice, once for each subobject.
  3. The ambiguity to which the two instances give rise. For example, any unqualified access to an `ZooAnimal` member is a compile-time error: Which instance is intended? What if the `Bear` and `Racoon` classes initialize their `ZooAnimal` subobjects slightly differently?
     ```c++
     #include <iostream>
     
     class ZooAnimal {
     public:
        virtual void foo(){ std::cout << "ZooAnimal::foo()\n"; }
     private:
     
     };
     
     class Bear : public ZooAnimal {
     public:
     private:
     
     };
     
     class Racoon : public ZooAnimal {
     public:
     private:
     
     };
     
     class Panda : public Bear, public Racoon {
     public:
     private:
     
     };
     
     int main (){
     
        Panda p;
        p.foo(); // ‘foo’ is ambiguous
     
        return 0;
     }
     ```


# Virtual Base Class Declaration

* A base class is specified as being derived through virtual inheritance by modifying its declaration with the keyword `virtual`. For example, the following declarations make `ZooAnimal` a virtual base class of both `Bear` and `Raccoon`:
   ```c++
   // the order of the keywords public and virtual
   // is not significant
   class Bear : public virtual ZooAnimal { ... };
   class Raccoon : virtual public ZooAnimal { ... };
   ```
* An object of the derived class can be manipulated through a pointer or a reference to a base class type even though the base class is virtual.
   ```c++
   #include <iostream>
   
   class ZooAnimal {
   public:
      virtual void foo(){ std::cout << "ZooAnimal::foo()\n"; }
   private:
   
   };
   
   class Bear : virtual public ZooAnimal {
   public:
   private:
   
   };
   
   class Racoon : virtual public ZooAnimal {
   public:
   private:
   
   };
   
   class Panda : public Bear, public Racoon, public Endangered {
   public:
      void foo() override { std::cout << "Panda::foo()\n"; }
   private:
   
   };
   
   int main (){
      ZooAnimal* ptr = new Panda;
      ptr->foo(); // Panda::foo()
      return 0;
   }
   ```
# Special Initialization Semantics
* In a nonvirtual derivation, a derived class can initialize explicitly only its immediate base classes.
* In the initialization of a virtual base class, if intermediate base classes each provide a constructor for the virtual base, it becomes ambiguous which constructor should be used. Therefore, it is the responsibility of the most derived class to explicitly initialize the virtual base class.
   ```c++
   #include <iostream>
   
   struct A {
       int value;
       A(int v) : value(v) {
           std::cout << "A constructed with value = " << value << '\n';
       }
   };
   
   struct B : virtual public A {
       B() : A(1) {}  // tries to init virtual base A
   };
   
   struct C : virtual public A {
       C() : A(2) {}  // also tries to init virtual base A
   };
   
   struct D : public B, public C {
       // D does NOT explicitly initialize A
       // Ambiguity: Should it use B's init or C's init?
   };
   
   int main() {
       D d; // This will fail to compile (ambiguous initialization of A)
   }
   ```
   ```c++
   #include <iostream>
   
   struct A {
       int value;
       A(int v) : value(v) {
           std::cout << "A constructed with value = " << value << '\n';
       }
   };
   
   struct B : virtual public A {
       B() : A(0) { // This call to A() is ignored because A is virtual
           std::cout << "B constructed\n";
       }
   };
   
   struct C : virtual public A {
       C() : A(0) { // Ignored too
           std::cout << "C constructed\n";
       }
   };
   
   struct D : public B, public C {
       D() : A(42), B(), C() { // Only D initializes A
           std::cout << "D constructed\n";
       }
   };
   
   int main() {
       D d;
       std::cout << "Final value in A: " << d.value << '\n';
   }
   ```
* When a `Panda` object is initialized, (1) the explicit invocations of the `ZooAnimal` constructor within `Raccoon` and `Bear` are no longer executed during the execution of their respective constructors, and (2) the `ZooAnimal` constructor is invoked with the arguments specified for the `ZooAnimal` constructor in the initialization list of the `Panda` constructor.
* If the `Panda` constructor does not specify arguments explicitly for the `ZooAnimal` constructor, one of two actions occurs: Either the `ZooAnimal` default constructor is called or, if there is no default constructor, the compiler issues an error message when the definition of Panda's constructor is compiled.
   ```c++
   #include <iostream>
   
   class ZooAnimal {
   public:
      ZooAnimal(int m): _m(m){}
      void get(){ std::cout << "_m = " << _m << "\n"; }
   private:
      int _m;
   };
   
   class Bear : virtual public ZooAnimal {
   public:
      Bear(int m): _m(m), ZooAnimal(m+1){}
   private:
      int _m;
   };
   
   class Racoon : virtual public ZooAnimal {
   public:
      Racoon(int m): _m(m), ZooAnimal(m+2){}
   private:
      int _m;
   };
   
   class Panda : public Bear, public Racoon {
   public:
      Panda(int m): _m(m), Bear(m), Racoon(m), ZooAnimal(m+3){}
   private:
      int _m;
   };
   
   int main (){
   
      Panda p(1);
      p.get(); // 4
   
      return 0;
   }
   ```
* You may perhaps have noticed that the two arguments being passed to both the `Bear` and `Raccoon` constructors are unnecessary when the classes serve as intermediate derived classes. A design solution to avoid the unnecessary argument passing is to provide an explicit constructor to be invoked when the class serves as an intermediate derived class.
   ```c++
   #include <iostream>
   
   class ZooAnimal {
   public:
      ZooAnimal() = default; // the default ctor is required
      ZooAnimal(int m, int n): _m(m), _n(n){}
      void get(){ std::cout << "_m = " << _m << ", _n = "<< _n <<"\n"; }
   private:
      int _m;
      int _n;
   };
   
   class Bear : virtual public ZooAnimal {
   public:
      // Use it when Base is the most base class
      Bear(int m, int n): _m(m), ZooAnimal(m+1, n){}
   protected:
      // Use it when Base is intermediate derived class
      Bear(int m): _m(m){}
   private:
      int _m;
   };
   
   class Racoon : virtual public ZooAnimal {
   public:
      // Use it when Racoon is the most derived class
      Racoon(int m, int n): _m(m), ZooAnimal(m+2, n){}
   protected:
      // Use it when Racoon is intermediate derived class
      Racoon(int m): _m(m){}
   private:
      int _m;
   };
   
   class Panda : public Bear, public Racoon {
   public:
      Panda(int m, int n): _m(m), Bear(m), Racoon(m), ZooAnimal(m+3, n){}
   private:
      int _m;
   };
   
   int main (){
   
      Panda p(1,2);
      p.get(); // _m = 4, _n = 2
   
      return 0;
   }
   ```
# Constructor and Destructor Order
* The immediate base classes are examined in the order of their declaration for the presence of virtual base classes.
* Each subtree is examined depth first; that is, the search begins with the root class and moves down.
* Virtual base classes are always constructed prior to nonvirtual base classes regardless of where they appear in the inheritance hierarchy.
* Once the virtual base class constructors are invoked, the nonvirtual base class constructors are invoked in the order of declaration.
![image](https://hackmd.io/_uploads/rkTfdYGExx.png =40%x)
   ```c++
   #include <iostream>
   
   class ZooAnimal {
   public:
      ZooAnimal(){ std::cout << "ZooAnimal()\n"; }
   private:
   };
   
   class ToyAnimal {
   public:
      ToyAnimal(){ std::cout << "ToyAnimal()\n"; }
   private:
   };
   
   class Character {
   public:
      Character(){ std::cout << "Character()\n"; }
   };
   
   class Bear : virtual public ZooAnimal {
   public:
      Bear(){ std::cout << "Bear()\n"; }
   };
   
   class BookCharacter : public Character {
   public:
      BookCharacter(){ std::cout << "BookCharacter()\n"; }
   };
   
   
   class TeddyBear : public BookCharacter, public Bear, virtual public ToyAnimal {
   public:
      TeddyBear(){ std::cout << "TeddyBear()\n"; }
   };
   
   int main (){
   
      TeddyBear bear;
   
      return 0;
   }
   ```
   The output:
   ````
   ZooAnimal()
   ToyAnimal()
   Character()
   BookCharacter()
   Bear()
   TeddyBear()
   ````
* The order of copy constructor invocations under memberwise initialization (and of copy assignment operators under memberwise assignment) are the same.
* The order of base class destructor calls is guaranteed to be the reverse order of constructor invocation.

# Visibility of Virtual Base Class Members

* Under a nonvirtual derivation, each inherited instance is given equal weight in resolving the reference, and so an unqualified reference results in a compile-time ambiguity error.
   ```c++
   #include <iostream>
   
   class ZooAnimal {
   public:
      void family_name(){ std::cout << "ZooAnimal::family_name()\n"; }
      void onExhibit() { std::cout << "ZooAnimal::onExhibit()\n"; }
      void print() { std::cout << "ZooAnimal::print()\n"; }
   };
   
   class Bear : public ZooAnimal {
   public:
      void print() { std::cout << "Bear::print()\n"; }
      void onExhibit() { std::cout << "Bear::onExhibit()\n"; }
   };
   
   class Racoon : public ZooAnimal {
   public:
      void print() { std::cout << "Racoon::print()\n"; }
   };
   
   class Panda : public Bear, public Racoon {
   public:
   };
   
   int main (){
   
      Panda p;
      // p.family_name(); // Error: ambiguous
      // p.onExhibit(); // Error: ambiguous
      // p.print(); // Error: ambiguous
   
      return 0;
   }
   ```
* Under a virtual derivation, the inheritance of a virtual base class member is given less weight than a subsequently redefined instance of that member.
* If two or more base classes at the same derivation level redefine a virtual base class member, they are accorded equal precedence within the derived class.
  ```c++
  #include <iostream>
  
  class ZooAnimal {
  public:
     void family_name(){ std::cout << "ZooAnimal::family_name()\n"; }
     void onExhibit() { std::cout << "ZooAnimal::onExhibit()\n"; }
     void print() { std::cout << "ZooAnimal::print()\n"; }
  };
  
  class Bear : virtual public ZooAnimal {
  public:
     void print() { std::cout << "Bear::print()\n"; }
     void onExhibit() { std::cout << "Bear::onExhibit()\n"; }
  };
  
  class Racoon : virtual public ZooAnimal {
  public:
     void print() { std::cout << "Racoon::print()\n"; }
  };
  
  class Panda : public Bear, public Racoon {
  public:
  };
  
  int main (){
  
     Panda p;
     p.family_name(); // ZooAnimal::family_name
     p.onExhibit(); // Bear::onExhibit
     p.print(); // Error: ambiguous
     p.Bear::print(); // Bear::print
  
     return 0;
  }
  ```
{% endraw %}