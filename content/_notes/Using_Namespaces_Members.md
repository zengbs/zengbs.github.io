---
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---

# Namespace Aliases
* A namespace alias can be used to associate a shorter synonym with a namespace name.
   ```c++
   namespace IBM = International_Business_Machine;
   ```
* A namespace alias can also refer to a nested namespace.

   ```c++
   namespace IBM = Companies::International_Business_Machine;
   ```
* A namespace can have many synonyms, or aliases.
   ```c++
   namespace X = long_namespace;
   namespace Y = long_namespace;
   ```
* It is an error if the original namespace name is not a name known to be a namespace name.


# Using Declarations
* `using namespace_name::member_name`
* using declaration is to make the name of a namespace member visible so that the member can be referred to in a program using the unqualified form of its name.
* A using declaration introduces a name in the scope in which the using declaration appears.
* As with any other declaration, a name introduced by a using declaration has these characteristics:
    * It must be unique in its scope.
    * It hides the same name introduced by a declaration in an enclosing scope.
    * It is hidden by a declaration of the same name in a nested scope. For example:
   ```c++=
   #include <iostream>
   
   
   namespace blip {
       int bi = 16, bj = 15, bk = 23;
   }
   
   int bj = 0;
   
   void manip() {
       using blip::bi;  // bi in manip() refers to blip::bi
       ++bi;            // sets blip::bi to 17
   
       using blip::bj;  // hides global bj
       ++bj;            // sets blip::bj to 16
   
       int bk;          // local variable bk declared here
   
       using blip::bk;  // Error: redeclaration of bk in manip()
   }
   
   int wrongInit = bk;  // Error: bk is not visible in global scope
   
   
   
   int main() {
       manip();
       return 0;
   }
   ```




# Using Directives
* `using namespace_name`
* It is an error if the name does not refer to a previously defined namespace name.
* A using directive allows us to make all the names from a specific namespace visible in their short form.
* A using directive does not declare local aliases for the namespace member names. Rather, it has the effect of lifting the namespace members into the least common ancestor scope of the current scope and the target namespace's own scope.
   ```c++=
   #include <iostream>
   
   namespace A {
      namespace C {
         namespace F {
            void foo(int) {
               std::cout << "Calls foo(int)\n";
            }
         }
      }
   
      namespace B {
         namespace E {
            void foo(short) {
               std::cout << "Calls foo(short)\n";
            }
         }
         namespace D {
            using namespace A::B::E;
            using namespace A::C::F;
            void test (){
               unsigned short ui = 1;
               foo(ui);
            }
         }
      }
   }
   
   int main() {
       A::B::D::test(); // Calls foo(short)
       return 0;
   }
   ``` 
* The using directive in `manip()` applies only within the block of the function `manip()`.
* Ambiguity errors caused by using directives are detected when a name is used and not when the using directive is encountered. For example, the member `bj` appears to `manip()` as if it were declared outside the namespace blip, in global scope, at the location where the namespace definition is located. However, there is already a variable named `bj` in global scope. The use of the name `bj` within the function `manip()` is therefore ambiguous: the name refers both to the global variable and to the member of namespace blip. The using directive is not an error, however. Only when `bj` is used within `manip()` is the ambiguity error detected. If `bj` was never used within `manip()`, no error would be issued.
* The use of qualified names is not affected by using directives.
* Because the namespace members appear as if they were declared outside the namespace, at the location where the namespace definition is located, the members appear to the function `manip()` as if they were declared in global scope. This means that local declarations within `manip()` may hide some of the namespace member names. The local variable bk hides the namespace member `blip::bk`. Referring to `bk` within `manip()` is not ambiguous; it refers to the local variable `bk`.
   ```c++=
   namespace blip {
       int bi = 16, bj = 15, bk = 23;
   }
   
   int bj = 0;
   
   void manip() {
       using namespace blip;  // using directive
   
       ++bi;           // OK: sets blip::bi to 17
       ++bj;           // ERROR if used: ambiguous - could refer to global or blip::bj
   
       ++::bj;         // Explicit: sets global bj to 2
       ++blip::bj;     // OK: sets blip::bj to 16
   
       int bk = 97;    // Local variable bk declared, hides blip::bk
       ++bk;           // OK: sets local bk to 98
   }
   
   int main(){
      manip();
   }
   ```
{% endraw %}