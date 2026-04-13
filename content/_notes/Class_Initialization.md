---
date: 2026-04-13T15:32:36+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---

1. If all members in a class are public, the class is not required to provide a constructor.
2. The values are resolved positionally based on the declaration order of the data members.
   ```c++
   #include <iostream>
   
   class Foo {
   public:
      int ival;
      const char* ptr;
   };
   
   int main() {
       Foo foo = {1, "abc"};
       // Foo foo = {"abc", 1}; // Error
       std::cout << foo.ival << std::endl;
       std::cout << foo.ptr  << std::endl;
       return 0;
   }
   ```
3. Two primary drawbacks to the explicit initialization list are that:
    * It can only be applied to class objects for which all the data members are public
    * It requires the explicit intervention of the programmer, adding to the possibility of accident.
{% endraw %}