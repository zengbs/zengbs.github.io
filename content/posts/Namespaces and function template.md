---
title: "Namespaces and function template"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

---
title: Namespaces and function template
tags: [CPP]

---

# Example
```c++
#include <iostream>

namespace db {
   template <typename T>
   void foo(T) { std::cout << "Called generic template" << std::endl; }
}

// First way
namespace db {
   template<>
   void foo(double) { std::cout << "Called specialized template for double" << std::endl; }
}

// Second way
template<> void db::foo(float) { std::cout << "Called specialized template for float" << std::endl; }

int main(){
   foo(1); // Error: foo is not found
   db::foo(1); // Called generic template
   db::foo(1.2); // Called specialized template for double
   db::foo(1.2f); // Called specialized template for float
   return 0;
}
```