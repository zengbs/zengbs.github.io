---
title: "Lambda expressions"
date: 2026-04-13T15:32:37+08:00
draft: false
---

---
title: Lambda expressions
tags: [CPP]

---

# Syntax of Lambdas
* Call it directly:
  ```c++
  [] {
  std::cout << "hello lambda" << std::endl;
  } ();
  ```
* Pass a Lambda to an object:
  ```c++
  auto l = [] {
     std::cout << "Hi\n";
  };
  
  l();
  ```
* A lambda with parameters:
  ```c++
  auto l2 = [] (const std::string& s) {
     std::cout << s << "\n";
  };
  
  l2("Hello");
  ```
* A lambda can also return something. Without any speciﬁc deﬁnition of the return type, it is deduced from the return value:
  ```c++
  auto l3 = [] {
     return 42;
  };
  
  std::cout << l3() << "\n";
  ```
* To specify a return type, you can use the new syntax C++ also provides for ordinary functions:
   ```c++
   auto l4 = [] () -> double {
      return 42;
   };
   
   std::cout << l4() << "\n";
   ```
## Captures
Inside the lambda introducer (brackets at the beginning of a lambda), you can specify a capture to access data of outer scope that is not passed as an argument:
1. `[=]` means that the outer scope is passed to the lambda by value. Thus, you can read but not modify all data that was readable where the lambda was deﬁned.
2. `[&]` means that the outer scope is passed to the lambda by reference. Thus, you have write access to all data that was valid when the lambda was deﬁned, provided that you had write access there.

* You can also specify individually for each object that inside the lambda you have access to it by value or by reference:
  ```c++
  int x=0;
  int y=42;
  
  auto qq = [x, &y] {
     std::cout << "x=" << x << "\n";
     std::cout << "y=" << ++y << "\n";
  };
  
  qq();
  
  std::cout << "final y=" << y << "\n";
  ```
* Instead of `[x, &y]`, you could also have speciﬁed `[=, &y]` to pass y by reference and all other objects by value.
   ```c++
   auto q = [=, &y] {
      std::cout << "x=" << x << "\n";
      std::cout << "y=" << ++y << "\n";
   };
   
   q();
   
   std::cout << "final y=" << y << "\n";
   ```
* To have a mixture of passing by value and passing by reference, you can declare the lambda as mutable. In that case, objects are passed by value, but inside the function object deﬁned by the lambda, you have write access to the passed value. For example:
   ```c++
   auto f = [x] () mutable {
      std::cout << ++x << "\n";
      std::cout << ++x << "\n";
   };
   
   f();
   f();
   
   std::cout << "x=" << x << "\n";
   ```
   
## Type of Lambdas
 * `auto`: returns by value:
   ```c++
   auto returnLambda(){ // return by value
     return [] (int x, int y) {
        return x*y;
     };
   }
   
   auto m = returnLambda();
   std::cout << m(5,9) << "\n";
   ```
 * `decltype(auto)`: returns the exact expression in the return statement (i.e., return a prvalue):
   ```c++
   decltype(auto) returnLambda(){
     return [] (int x, int y) {
        return x*y;
     };
   }
   
   decltype(auto) m = returnLambda();
   std::cout << m(5,9) << "\n";
   ```
 * `std::function<>`: 
   ```c++
   std::function<int(int,int)> returnLambda(){
     return [] (int x, int y) {
        return x*y;
     };
   }
   
   auto m = returnLambda();
   std::cout << m(5,9) << "\n";
   ```
   
   
 


