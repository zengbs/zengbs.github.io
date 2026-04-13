---
title: "Local Classes"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

---
title: Local Classes
tags: [CPP]

---

1. A class can also be defined inside a function body. Such a class is called a local class.
2. A local class is only visible in the local scope in which it is defined.
3. Unlike a nested class, there is no syntax to refer to the member of a local class outside the local scope in which the class is defined. 
4. Because there is no syntax to define the members of a local class in a namespace scope, a local class is not permitted to declare static data members.
5. A class nested within a local class can be defined outside its class definition. However, the definition must appear in the local scope that contains the definition of the enclosing local class. The name of the nested class in the local scope definition must be qualified by the name of the enclosing class. The declaration of the nested class in the enclosing class cannot be omitted.
   ```c++
   int main() {
      class Outer {
         class Inner;
      };
      class Outer::Inner {
         int foo;
      };
      return 0;
   }
   ```