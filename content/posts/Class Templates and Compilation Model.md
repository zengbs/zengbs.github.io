---
title: "Class Templates and Compilation Model"
date: 2026-04-13T15:32:36+08:00
draft: false
render_with_liquid: false
---

---
title: Class Templates and Compilation Model
tags: [CPP]

---

# Inclusion Model (implicit instantiations)
```c++
// header.h
#include<iostream>

template<class T>
struct MyClass {
   MyClass(T m) : _m(m){}
   void show(){ std::cout << _m << "\n"; }
   T _m;
};
```
```c++
// foo.cc
# include "header.h"

void foo(){
   MyClass<double> objd(-5.2);
   objd.show();

   MyClass<int> obji(-5);
   obji.show();
}
```
```c++
// main.cc
# include "header.h"

void foo();

int main(){
   MyClass<int> obj(1);
   obj.show();
   foo();
   return 0;
}
```
![image](https://hackmd.io/_uploads/B1uQY2pblx.png)

# Exclusion Model (explicit instantiations )
```c++
// header.h
template<class T, int size, int weight=1>
struct MyClass {
   MyClass(T m);
   void show();
   T _m;
};
```
```c++
// header.cc
#include<iostream>
#include"header.h"

template<class T, int size, int weight>
MyClass<T,size,weight>::MyClass(T m) : _m(m){ }

template<class T, int size, int weight>
void MyClass<T,size,weight>::show(){
   std::cout << _m << "\n";
}

template class MyClass<int, 10, 10>;
template class MyClass<double, 10>;
```
```c++
// foo.cc
# include "header.h"

void foo(){
   MyClass<double,10> objd(-5.2);
   objd.show();

   MyClass<int,10,10> obji(-5);
   obji.show();
}
```
```c++
// main.cc
#include "header.h"

void foo();

int main(){
   MyClass<int,10,10> obj(1);
   obj.show();
   foo();
   return 0;
}
```
![image](https://hackmd.io/_uploads/BJqwq3p-ee.png)


# Exclusion Model (extern template)
```c++
// header.h
#include<iostream>

template<class T>
struct MyClass {
   MyClass(T m) : _m(m){}
   void show(){ std::cout << _m << "\n"; }
   T _m;
};
```
```c++
// foo.cc
# include "header.h"

void foo(){
   MyClass<double> objd(-5.2);
   objd.show();

   MyClass<int> obji(-5);
   obji.show();
}
```
```c++
// main.cc
#include "header.h"

void foo();
extern template class MyClass<int>;

int main(){
   MyClass<int> obj(1);
   obj.show();
   foo();
   return 0;
}
```
![image](https://hackmd.io/_uploads/Sy9Pi36-ee.png)
