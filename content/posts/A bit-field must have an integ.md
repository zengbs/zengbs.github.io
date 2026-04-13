---
title: "A bit-field must have an integ"
date: 2026-04-13T15:32:36+08:00
draft: false
render_with_liquid: false
---

---
title: A bit-field must have an integ
tags: [CPP]

---

1. A bit-field must have an integral data type. It can be either signed or unsigned.
    * There will be no difference in the value stored. However, if your program later depends on how arithmetic or bitwise manipulations behave, or if you work with values that might exceed the positive range of a signed integer, then the distinction between unsigned int and int becomes important.
2. Bit-fields defined in consecutive order within the class body are, if possible, packed within adjacent bits
of the same integer, thereby providing for storage compaction.
3. The address-of operator (&) cannot be applied to a bit-field, and so there can be no pointers referring to class bit-fields. Nor can a bit-field be a static member of its class.
    * Static data members are associated with the class rather than with any particular object instance. Bit-fields, on the other hand, are designed to save storage in object instances by packing multiple members into the same underlying storage unit.


```c++
#include <iostream>

class MyClass {
public:
   unsigned int a : 5;
   unsigned int b : 8;
   unsigned int c : 2;
};

int main(){

   MyClass obj;

   obj.a = 2;
   obj.b = 0xFF;

   // 5 in binary is 101, doesn't fit 2 bits
   // the value is truncated to fit into 2 bits
   obj.c = 5;

   std::cout << obj.a << std::endl;
   std::cout << obj.b << std::endl;
   std::cout << obj.c << std::endl;

   return 0;
}
```