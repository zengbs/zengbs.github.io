---
title: "Overloading function template"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

---
title: Overloading function template
tags: [CPP]

---

# Partial ordering of specializations
1. Between two templates that both match, the one that can handle **fewer** types is chosen as **more specialized**.
2. Partial ordering does not provide a complete (total) order among all templates; it only establishes a relative order among the candidates that are viable for the function call.
# Example
```c++
#include <iostream>

template<typename T>
void foo(T, T){
   std::cout << "Version 1" << std::endl;
}
template<typename T, typename U>
void foo(T, U){
   std::cout << "Version 2" << std::endl;
}

int main(){

   // Call "Version 1" due to partial ordering.
   // I.e, the Version 1 is more specialied than "Version 2"
   foo(4, 1);

   // Call "Version 2"
   foo(1, 2U);

   return 0;
}
```

```c++
#include <iostream>

template<typename T>
void foo(T*){
   std::cout << "Version 1" << std::endl;
}
template<typename T>
void foo(T){
   std::cout << "Version 2" << std::endl;
}

int main(){

   int ia[10];

   // Call "Version 1" due to partial ordering.
   // I.e, the Version 1 is more specialied than "Version 2"
   foo(ia);

   return 0;
}
```

```c++
#include <iostream>

template<typename T, typename U>
void foo(T*){
   std::cout << "Version 1" << std::endl;
}

template<typename T>
void foo(T&){
   std::cout << "Version 2" << std::endl;
}

int main(){

   // Call version 2
   // Since we cannot deduce temlplate parameter U 
   int ia[10];
   foo(ia);

   return 0;
}
```

```c++
#include <iostream>

template<typename T>
void foo(T*){
   std::cout << "Version 1" << std::endl;
}

template<typename T>
void foo(T&){
   std::cout << "Version 2" << std::endl;
}

int main(){

   // Call "Version 1"
   int ia[10];
   foo(ia);

   return 0;
}
```
```c++
#include <iostream>

template<typename T>
void foo(T){
   std::cout << "Version 1" << std::endl;
}

template<typename T>
void foo(T&){
   std::cout << "Version 2" << std::endl;
}

int main(){

   // Ambiguous call
   int ia[10];
   foo(ia);

   return 0;
}
```