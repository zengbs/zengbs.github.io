---
title: "emplace_back vs. push_back"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: emplace_back vs. push_back
tags: [CPP]

---

```c++
#include<vector>
#include<iostream>

class MyClass {
public:

MyClass(const std::string& s) : _s(s)
{
   std::cout << "Ctor\n";
}

// copy ctor
MyClass(const MyClass& rhs)
: _s(rhs._s)
{
   std::cout << "COPY ctor\n";
}

// move ctor
MyClass(MyClass&& rhs) noexcept
: _s(rhs._s)
{
   std::cout << "MOVE ctor\n";
}

// copy assignment
MyClass& operator=( const MyClass& rhs )
{
   std::cout << "COPY assignment\n";
   if ( this != &rhs ){
      _s = rhs._s;
   }
   return *this;
}

// move assignment
MyClass& operator=( MyClass&& rhs ) noexcept
{
   std::cout << "MOVE assignment\n";
   if ( this != &rhs ){
      _s = rhs._s;
   }
   return *this;
}

private:
std::string _s;

};

int main () {

   int len = 5;

   std::vector<MyClass> v1, v2;
   v1.reserve(len);
   v2.reserve(len);

   std::cout << "====== PUSH_BACK ======\n";

   for (int i=0;i<len;i++)
   {
      v1.push_back(MyClass(std::to_string(i)));
   }

   std::cout << "\n====== EMPLACE ======\n";

   for (int i=0;i<len;i++)
   {
      v2.emplace_back(std::to_string(i));
   }

   return 0;
}
```



`len = 3`:
|                   | No `noexcept`                                       | `noexcept`                                          |
| ----------------- | --------------------------------------------------- | --------------------------------------------------- |
| `reserve(len)`    | ![image](https://hackmd.io/_uploads/S1P4sY0see.png) | ![image](https://hackmd.io/_uploads/rJGwjYAixg.png) |
| No `reserve(len)` | ![image](https://hackmd.io/_uploads/H1_zoY0see.png) | ![image](https://hackmd.io/_uploads/S1T0oFRjxe.png) |

# Summary
* `emplace_back()` constructs an element directly in place at the end of the vector, eliminating the need for an extra copy or move operation.
* The presence of a `noexcept` specifier in move semantics determines whether the existing data can be moved or must be copied into newly allocated memory.
{% endraw %}