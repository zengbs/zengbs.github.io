---
title: "Operator()"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

---
title: Operator()
tags: [CPP]

---

1. If a class type is defined to represent an operation, the function call operator can be overloaded for this class type to invoke this operation. For example:
   ```c++
   #include <iostream>
   #include <vector>
   #include <algorithm>
   
   struct absInt {
      int operator()( int iv ){
         return (iv > 0) ? iv : -iv;
      }
   };
   
   int main(){
      std::vector<int> ia = {-1, 3, -31, 6};
      std::transform( ia.begin(), ia.end(), ia.begin(), absInt() );
      for ( const int& e : ia ){
         std::cout << e << "\n";
      }
   }
   ```
2. An overloaded `operator()` must be declared as a member function.
3. The fourth argument of `transform()` is a temporary object of class `absInt` created by invoking the default constructor of `absInt`. 