---
title: "Base and Derived Class Construction"
date: 2026-04-13T15:32:36+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: Base and Derived Class Construction
tags: [CPP]

---

* The order of constructor invocation is always the following:
    1. **The base class constructor.** If there is more than one base class, the constructors are invoked in the order the base classes appear in the class derivation list, not in the order in which they are listed in the member initialization list.
    2. **Member class object constructor.** If there is more than one member class object, the constructors are invoked in the order in which the objects are declared within the class, not the order in which they are listed in the member initialization list.
    3. **The derived class constructor.**
* As a general rule, the derived class constructor should never assign a value to a base class data member directly, but rather pass the value to the appropriate base class constructor. Otherwise, the implementations of the two classes become tightly coupled, and it can be more difficult to modify or extend the base class implementation correctly. (Our responsibility as the designer of the base class is to provide the appropriate set of base class constructors.)
   ```c++
   #include <iostream>
   #include <string>
   
   class Animal {
   public:
       Animal() = default;
       Animal(const std::string& n) : name(n){}
       std::string name;
   };
   
   class Dog : public Animal {
   public:
       // Good: assign value by base class stor
       Dog(const std::string& n) : Animal(n) {}
   
       // Bad: assign value by derived class stor
       Dog(const std::string& n) { name = n;  }
   };
   
   int main() {
       Dog d("Buddy");
       std::cout << d.name << "\n";
       return 0;
   }
   ```
{% endraw %}