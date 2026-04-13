---
title: "Classes as Namespace Members"
date: 2026-04-13T15:32:36+08:00
draft: false
---

---
title: Classes as Namespace Members
tags: [CPP]

---

1. The name of a class defined in a user-declared namespace is only visible in the scope of that namespace and not in the global scope or in other namespaces. This means that the class name does not collide with other names declared in other namespaces.
   ```c++
   namespace ns1 {
      class Node {
      };
   }
   
   namespace ns2 {
      class Node {
      };
   }
   
   ns1::Node obj;
   
   int main() {
      return 0;
   }
   ```
2. The definition of class member can be placed either in the namespce containing the outermost class definition or in one of its enclosing namespace.
   ```c++
   // *.h
   namespace ns {
      class Outer {
      public:
      private:
         class Inner {
            void foo();
            int bar(int);
         };
      };
   }
   
   // *.cc
   namespace ns {
      int Outer::Inner::bar(int val){ return val; }
   }
   void ns::Outer::Inner::foo(){}
   
   int main() {
      return 0;
   }
   ```
3. A small trick to remember the order in which the scopes are examined when looking up a name that appears in a member definition located outside its class definition. The names by which the member name is qualified indicate the order in which the scopes are searched. The qualifiers  `ns::EnclosingClass::NestedClass::` indicate the reverse order in which the class scopes and namespace scopes are to be searched.
   ```c++
   ns::EnclosingClass::NestedClass::foo()
   ```
4. See [Unqualified Name Lookup](/cmvzTXvfTJOizt_Y9XQgUw) for details.