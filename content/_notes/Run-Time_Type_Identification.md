---
title: "Run-Time Type Identification"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: Run-Time Type Identification
tags: [CPP]

---

* RTTI allows programs that manipulate objects as pointers or references to base classes to retrieve the actual derived types of the objects to which these pointers or references refer. Two operators are provided for the RTTI support in C++:
   1. A `dynamic_cast` operator that allows for type conversions that are performed at run-time and that allows programs to navigate through a class hierarchy safely, converting a pointer to a base class to a pointer to a derived class or converting an lvalue referring to a base class to a reference to a derived class, only when the conversion is actually guaranteed to succeed
   2. A `typeid` operator that indicates the actual derived type of the object referred to by a pointer or a reference.
* That is, the RTTI operators are run-time events for classes with virtual functions and compile-time events for all other types.
* The use of the RTTI operators should, however, be minimized. The C++ static type system (that is, compile-time type checking) should be used whenever possible because it is safer and more efficient.

# The `dynamic_cast` operator
* A `dynamic_cast` operator can be used to convert a pointer that refers to an object of class type to a pointer to a class in the same class hierarchy. A `dynamic_cast` operator can also be used to convert an lvalue for an object of class type to a reference to a class in the same class hierarchy.
* If a `dynamic_cast` to a pointer type fails, the result of the `dynamic_cast` is the value 0.
* If a `dynamic_cast` to a reference type fails, an exception is thrown.
* The `dynamic_cast` operator therefore performs two operations at once. It verifies that the requested cast is indeed valid, and then only if it is valid does it perform the cast.
* The `dynamic_cast` is safer than the other C++ cast operations because the other casts do not verify whether the cast can actually be performed.
* The `dynamic_cast` is used for safe casting from a pointer to a base class to a pointer to a derived class, often referred to as safe downcasting.
* The result of the `dynamic_cast` operator must always be tested to verify that the cast is sucessful before using the resulting pointer. For example:
   ```c++
   class employee {
   public:
         virtual int salary();
   };
   
   class manager : public employee {
   public:
      int salary();
   };
   
   class programmer : public employee {
   public:
      int salary();
      int bonus();
   };
   
   void company::payroll( employee *pe )
   {
      // dynamic_cast and test in condition expression
      if ( programmer *pm = dynamic_cast< programmer* >( pe ) ) {
         // use pm to call programmer::bonus()
      } else {
         // use of employee's member functions
      }
   }
   ```
   The true path of the if statement is executed if pm is not zero.
*  A `dynamic_cast` can also be used to convert an lvalue of a base class type to a reference to a derived class type. The syntax for such a `dynamic_cast` operation is the following,
   ```c++
   dynamic_cast< Type& >( lval )
   ```
   where `Type&` is the target type of the conversion and lval is the lvalue of base class type. The `dynamic_cast` operation converts the operand lval to the desired type `Type&` only if lval actually refers to an object that is of a type that has a base class or a derived class that is of type Type.
* A reference `dynamic_cast` that fails, throws an exception. For example:
   ```c++
   #include <typeinfo>
   
   void company::payroll( employee &re )
   {
      try {
         programmer &rm = dynamic_cast< programmer & >( re );
         // use re to call programmer::bonus()
      }
      catch ( std::bad_cast ) {
         // use of employee's member functions
      }
   }
   ```

# The `typeid` operator
* The typeid operator allows a program to ask of an expression: What type are you?
* For example:
  1. When the operand is not of class type, then the typeid operator indicates the type of the operand.
  2. When the operand of the typeid operator is of class type, but not of a class type with virtual functions, then the typeid operator indicates the type of the operand as well, not the type of the underlying object.
  2. When the operand of the typeid operator is a pointer/reference to a class type with virtual functions, then the typeid operator indicates the type of the underlying object.
  3. When the operand of the typeid opeator is a pointer to class/non-class type, the typeid operator indicate the type of the pointer itself.
   ```c++
   #include <typeinfo>
   #include <iostream>
   
   class employee {
   public:
      virtual void salary(){ std::cout << "employee::salary()\n"; }
   
   };
   
   class manager : public employee {
   public:
      manager() : employee() {}
      void salary(){ std::cout << "manager::salary()\n"; }
   };
   
   int main(){
   
      employee* ep = new manager;
   
      if( typeid(ep) == typeid(employee*)  )  // 1
      {
          std::cout << "1\n";
      }
      else {
          std::cout << "0\n";
      }
      if( typeid(ep) == typeid(manager*)   )  // 0
      {
          std::cout << "1\n";
      }
      else {
          std::cout << "0\n";
      }
      if( typeid(*ep) == typeid(employee)  )  // 0
      {
          std::cout << "1\n";
      }
      else {
          std::cout << "0\n";
      }
      if( typeid(*ep) == typeid(manager)   )  // 1
      {
          std::cout << "1\n";
      }
      else {
          std::cout << "0\n";
      }
      if( typeid(&ep) == typeid(employee*) )  // 0
      {
          std::cout << "1\n";
      }
      else {
          std::cout << "0\n";
      }
      if( typeid(&ep) == typeid(manager*)  )  // 0
      {
          std::cout << "1\n";
      }
      else {
          std::cout << "0\n";
      }
   
      employee& re = *ep;
   
      if( typeid(re) == typeid(employee)  )  // 0
      {
          std::cout << "1\n";
      }
      else {
          std::cout << "0\n";
      }
      if( typeid(re) == typeid(manager)   )  // 1
      {
          std::cout << "1\n";
      }
      else {
          std::cout << "0\n";
      }
   
   }
   ```
{% endraw %}