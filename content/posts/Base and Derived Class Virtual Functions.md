---
title: "Base and Derived Class Virtual Functions"
date: 2026-04-13T15:32:36+08:00
draft: false
---

---
title: Base and Derived Class Virtual Functions
tags: [CPP]

---

# Introduction
* By default, the member functions of a class are nonvirtual. When a member function is nonvirtual, the function invoked is the one defined in the static type of the class object (or pointer or reference) through which it is invoked.
   ```c++
   #include <iostream>
   
   class A {
   public:
      void foo( ){
         std::cout << "Calls A::foo()\n";
      }
   };
   
   class B : public A {
   public:
      void foo( ){
         std::cout << "Calls B::foo()\n";
      }
   };
   
   int main() {
   
      A* obj1 = new B;
   
      obj1->foo(); // Calls A::foo()
   
      obj1->A::foo(); // Calls A::foo()
   
      A* obj2 = new A;
      obj2->foo(); // Calls A::foo()
   
      B* obj3 = new B;
      obj3->foo(); // Calls B::foo()
   
      return 0;
   }
   ```
* Polymorphism is enabled only when a derived class subtype is addressed indirectly through either a base class reference or pointer. The use of a base class object does not preserve the type-identity of the derived class.
   ```c++
   #include <iostream>
   using namespace std;
   
   // Base class
   class Query {
   public:
       virtual void display() const {
           cout << "Query::display()" << endl;
       }
   };
   
   // Derived class
   class NameQuery : public Query {
   public:
       void display() const override {
           cout << "NameQuery::display()" << endl;
       }
       void extra() const {
           cout << "Extra function in NameQuery" << endl;
       }
   };
   
   int main() {
   
       NameQuery nq;
   
       // Call through derived object – correct behavior
       nq.display();  // Output: NameQuery::display()
   
       // Object slicing: only Query part is copied
       Query q = nq;
   
       // Call through base object – slicing has occurred
       q.display();   // Output: Query::display() ← wrong if you expected polymorphism
   
       // Error: q has no member of extra()
       q.extra();
   
   
       return 0;
   }
   ```

# Virtual Input/Output
* The base class first introducing a virtual function must specify the `virtual` keyword within the class declaration. If the definition is placed outside the class, the keyword `virtual` must not again be specified.
   ```c++
   #include<iostream>
   
   class Base {
   public:
      virtual void foo();
   };
   
   class Derived : public Base {
   public:
      void foo() override {
         std::cout << "Calls Derived::foo()\n";
      }
   };
   
   // Correct
   void Base::foo(){
     std::cout << "Calls Bar::foo()\n";
   }
   
   // Incorrect
   virtual void Base::foo(){
     std::cout << "Calls Bar::foo()\n";
   }
   
   int main(){
      Base* ptr = new Derived;
      ptr->foo();
      return 0;
   }
   ```
* In order for a derived class instance of a virtual function to override the instance active in its base class, its prototype must match that of the base class exactly. For example, if we left off the `const`, or declared a second parameter, the derived instance would not override the active base class instance. The return value must also be the same, with one exception: The return value of the derived instance can be a covariant type of the return value of the base instance. 
   ```c++
   #include <iostream>
   using namespace std;
   
   class Animal {
   public:
       virtual Animal* clone() const {
           cout << "Cloning Animal" << endl;
           return new Animal(*this);
       }
       virtual void speak() const {
           cout << "Animal speaks" << endl;
       }
       virtual ~Animal() {}
   };
   
   class Dog : public Animal {
   public:
       // Covariant return type: returns Dog* instead of Animal*
       Dog* clone() const override {
           cout << "Cloning Dog" << endl;
           return new Dog(*this);
       }
       void speak() const override {
           cout << "Woof!" << endl;
       }
   };
   
   int main() {
       Animal* a1 = new Dog();
       Animal* a2 = a1->clone(); // Calls Dog::clone, returns Dog*, but assigned to Animal*
   
       a1->speak(); // Woof!
       a2->speak(); // Woof!
   
       delete a1;
       delete a2;
       return 0;
   }
   ```
# Pure Virtual Functions
* A class containing (or inheriting) one or more **pure** virtual functions is recognized as an abstract base class by the compiler. An attempt to create an independent class object of an abstract base class results in a compile-time error. An abstract base class can only occur as a subobject in subsequently derived classes.
   ```c++
   #include <iostream>
   #include <vector>
   
   class A {
   public:
      virtual void foo( ) = 0;
   };
   
   class B : public A {
   public:
      void foo( ){
         std::cout << "Calls B::foo()\n";
      }
   };
   
   int main() {
   
      A* obj = new B;
   
      // invoke B::foo() dynamically through virtual mechanism
      obj->foo(); // Calls B::foo()
   
      // Error: undefined reference
      obj->A::foo();
   
      // invalid new-expression of abstract class type ‘A’
      A* obja = new A;
   
      return 0;
   }
   ```



# Static Invocation of a Virtual Function
* When we invoke a virtual function using the class scope operator, we override the virtual mechanism, causing the virtual function to be resolved statically at compile-time.
   ```c++
   #include <iostream>
   #include <vector>
   
   class A {
   public:
      virtual void foo( ){
         std::cout << "Calls A::foo()\n";
      }
   };
   
   class B : public A {
   public:
      void foo( ){
         std::cout << "Calls B::foo()\n";
      }
   };
   
   
   int main() {
   
      A* obj = new B;
   
      // invoke B::foo() dynamically through virtual mechanism
      obj->foo(); // Calls B::foo()
   
      // invoke A::foo() statically at compile-time
      obj->A::foo(); // Calls A::foo()
   
      return 0;
   }
   ```
   Why might we wish to override the virtual mechanism? Often, for efficiency.

# Virtual Functions and Default Arguments

* The default argument to be passed to `foo()`, however, is not determined at run-time; rather, it is determined at compile-time and is based on the type of the object through which the function is being invoked. When `foo()` is invoked through `obj1`, the default argument is determined by the declaration of `A::foo()`, which is 1. When `foo()` is invoked through `obj2`, the default argument is determined by the declaration of `B::foo()`, which is 2.
   ```c++
   #include <iostream>
   #include <vector>
   
   class A {
   public:
      virtual void foo( int a = 1 ){
         std::cout << "Calls A::foo(int a = " << a << ")\n";
      }
   };
   
   class B : public A {
   public:
      void foo( int a = 2 ){
         std::cout << "Calls B::foo(int a = " << a << ")\n";
      }
   };
   
   class C : public B {
   public:
      void foo( int a = 3 ){
         std::cout << "Calls C::foo(int a = " << a << ")\n";
      }
   };
   
   int main() {
   
      A* obj1 = new B;
      obj1->foo(); // a = 1
   
      B* obj2 = new C;
      obj2->foo(); // a = 2
   
      return 0;
   }
   ```
   But what if we really wish for the actual default argument passed to `foo()` to be based on the actual instance of the function invoked? Unfortunately, the virtual mechanism does not support this directly. One programming solution is:
   ```c++
   void
   base::foo( int ival = base_default_value )
   {
      int real_default_value = 1024;
      if ( ival == base_default_value )
      ival = real_default_value;
      // ...
   }
   
   void
   derived::foo( int ival = base_default_value )
   {
      int real_default_value = 2048;
      if ( ival == base_default_value )
      ival = real_default_value;
      // .
   }
   ```
# Virtual Destructors
* It ensures that when an object is deleted through a pointer to the base class, both the base and derived classes' destructor are also called correctly. If the destructor of the base class is non-virtual, only the base destructor is called. The recource allocated by derived constuctor will cause memory leakage. For example:
   ```c++
   #include <iostream>
   
   class Root {
   public:
       virtual ~Root() {
           std::cout << "Root destructor\n";
       }
   };
   
   class Base : public Root {
   public:
       ~Base() {
           std::cout << "Base destructor\n";
       }
   };
   
   class Derived : public Base {
   public:
       ~Derived() {
           std::cout << "Derived destructor\n";
       }
   };
   
   int main() {
       Root* obj = new Derived();
       delete obj;
       // Output:
       // Derived destructor
       // Base destructor
       // Root destructor
   }
   ```
* As a general rule of thumb, we recommend that the root base class of a class hierarchy declaring one or more virtual functions declare its destructor virtual as well. However, unlike the base class constructor, the base class destructor, in general, should not be made protected.

# Virtually a Virtual new Operator
* Because operator `new` is called before the object exists, there's no object instance and no vtable — so you cannot make the operator `new` virtual.
* Since `new` cannot be virtual, creating a duplicate of an object through pointer is considerably less trivial. The solution is:
   ```c++
   #include<iostream>
   class Base {
   public:
      virtual Base* clone() const = 0;
      virtual ~Base(){};
      virtual int get() = 0;
   };
   
   class Derived : public Base{
   public:
      Derived(int m) : _m(m) {}
      Base* clone() const override {
         return new Derived(*this);
      }
      int get() override { return _m; }
      int _m;
   };
   
   
   int main() {
   
       Base* obj1 = new Derived(-1);
   
       // using static_cast
       // --> Cons: the type of obj1 must be known at compile time
       Base* copy = new Derived(*static_cast<Derived*>(obj1));
       std::cout << copy->get() << "\n";
       delete copy;
   
       // using dynamic_cast
       // --> Cons: must check all derived types at runtime
       Base* obj2 = new Derived(-1);
   
       Derived* derivedPtr = dynamic_cast<Derived*>(obj2);
       if (derivedPtr) {
           Base* copy = new Derived(*derivedPtr);  // safe deep copy
           std::cout << copy->get() << "\n";
           delete copy;
       } else {
           std::cout << "obj1 is not a Derived\n";
       }
   
       delete obj2;
   
       // using clone
       // --> Best solution
       Base* copy2 = obj1->clone();
       std::cout << copy2->get() << "\n";
       delete copy2;
   }
   ```

# Virtual Functions, Constructors, and Destructors
Virtual functions do not behave polymorphically during base class construction or destruction. Because during construction, the derived part of the object does not yet exist. And during destruction, the derived part of the object has already been destroyed.
So:
   * Inside a base class constructor, virtual function calls resolve to base versions only.
   * Inside a base class destructor, virtual function calls also resolve to base versions only.

This prevents accessing uninitialized or destroyed data in derived classes, which could lead to crashes or undefined behavior.

```c++
#include <iostream>

class Base {
public:
    Base() {
        std::cout << "Base constructor\n";
        call();  // virtual function call inside constructor
    }

    virtual ~Base() {
        std::cout << "Base destructor\n";
        call();  // virtual function call inside destructor
    }

    virtual void call() const {
        std::cout << "Base::call()\n";
    }
};

class Derived : public Base {
public:
    Derived() {
        std::cout << "Derived constructor\n\n";
    }

    ~Derived() {
        std::cout << "Derived destructor\n";
    }

    void call() const override {
        std::cout << "Derived::call()\n";
    }
};

int main() {

    Derived d;

    return 0;
}
```
Output:
```
Base constructor
Base::call()
Derived constructor

Derived destructor
Base destructor
Base::call()
```