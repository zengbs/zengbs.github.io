---
title: "Memory alignment (1)"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: Memory alignment
tags: [CPP]

---

```c++
#include <iostream>

class A {
public:
  A(int i1, int i2, double d1) : _i1(i1), _i2(i2), _d1(d1) {}
  int _i1;
  int _i2;
  double _d1;
};


class B {
public:
  B(int i1, int i2, double d1) : _i1(i1), _i2(i2), _d1(d1) {}
  int _i1;
  double _d1;
  int _i2;
};

class C {
public:
  C(char c1, char c2, int i) : _c1(c1), _c2(c2), _i(i) {}
  char _c1;
  char _c2;
  int _i;
};


class D {
public:
  D(char c1, char c2, int i) : _c1(c1), _c2(c2), _i(i) {}
  char _c1;
  int _i;
  char _c2;
};


int main(){

   A a(1, 2, 2.0);
   B b(1, 2, 2.0);
   C c('1', '2', 3);
   D d('1', '2', 3);
   
   std::cout << "&a       = " << &a << "\n";
   std::cout << "&(a._i1) = " << &(a._i1) << "\n";
   std::cout << "&(a._i2) = " << &(a._i2) << "\n";
   std::cout << "&(a._d1) = " << &(a._d1) << "\n\n";


   std::cout << "&b       = " << &b << "\n";
   std::cout << "&(b._i1) = " << &(b._i1) << "\n";
   std::cout << "&(b._d1) = " << &(b._d1) << "\n";
   std::cout << "&(b._i2) = " << &(b._i2) << "\n\n";


   std::cout << "&c       = " << &c << "\n";
   std::cout << "&(c._c1) = " << (void*)&(c._c1) << "\n";
   std::cout << "&(c._c2) = " << (void*)&(c._c2) << "\n";
   std::cout << "&(c._i)  = " << &(c._i) << "\n\n";

   std::cout << "&d       = " << &d << "\n";
   std::cout << "&(d._c1) = " << (void*)&(d._c1) << "\n";
   std::cout << "&(d._i)  = " << &(d._i) << "\n";
   std::cout << "&(d._c2) = " << (void*)&(d._c2) << "\n\n";

   std::cout << "sizeof(a) = " << sizeof(a)<< ", " << "alignof(a) = " << alignof(a)<< "\n";
   std::cout << "sizeof(b) = " << sizeof(b)<< ", " << "alignof(b) = " << alignof(b)<< "\n";
   std::cout << "sizeof(c) = " << sizeof(c)<< ", " << "alignof(c) = " << alignof(c)<< "\n";
   std::cout << "sizeof(d) = " << sizeof(d)<< ", " << "alignof(d) = " << alignof(d)<< "\n";


   return 0;
}
```


```
&a       = 0x7ffc07820cc0
&(a._i1) = 0x7ffc07820cc0
&(a._i2) = 0x7ffc07820cc4
&(a._d1) = 0x7ffc07820cc8

&b       = 0x7ffc07820cd0
&(b._i1) = 0x7ffc07820cd0
&(b._d1) = 0x7ffc07820cd8
&(b._i2) = 0x7ffc07820ce0

&c       = 0x7ffc07820cac
&(c._c1) = 0x7ffc07820cac
&(c._c2) = 0x7ffc07820cad
&(c._i)  = 0x7ffc07820cb0

&d       = 0x7ffc07820cb4
&(d._c1) = 0x7ffc07820cb4
&(d._i)  = 0x7ffc07820cb8
&(d._c2) = 0x7ffc07820cbc

sizeof(a) = 16, alignof(a) = 8
sizeof(b) = 24, alignof(b) = 8
sizeof(c) = 8, alignof(c) = 4
sizeof(d) = 12, alignof(d) = 4
```

https://nimrod.blog/posts/what-does-cpp-object-layout-look-like/

https://dev.to/visheshpatel/memory-layout-of-c-object-1p17

https://selfboot.cn/en/2024/05/10/c++_object_model/
{% endraw %}