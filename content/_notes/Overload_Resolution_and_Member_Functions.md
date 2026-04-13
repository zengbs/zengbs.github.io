---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

Member functions can also be overloaded. Overload resolution for member functions is very similar to overload resolution for nonmember functions. The processe composed of the same three steps:
1. Select the candidate functions.
2. Select the viable functions.
3. Select the best match function.

There are some minor differences in how candidate functions and viable functions are selected for calls to member functions. We will examine these differences in this section.

# Declarationsof Overloaded Member Functions
1. Class member functions can be overloaded.
2. If two member function declarations with the same name differ only in their return type, the second declaration is treated as an erroneous declaration and is flagged as a compile-time error.
3. Unlike namespace functions, member functions must be declared only once in the class member list. If both the return type and the parameter list of two member function declarations with the same name match exactly, the second declaration is flagged by the compiler as an invalid member function redeclaration.
4. All the functions in a set of overloaded functions are declared within the same scope. Therefore, member functions never overload functions declared in namespace scope.
5. A set of overloaded member functions may contain both static and nonstatic member functions.
# Candidate Functions
1. The set of candidate functions for the three calls below is composed of functions found when looking up declarations for `mf()` in the scope of class `myClass`.
   ```c++
   myClass mc;
   myClass* pmc;
   
   mc.mf( arg );
   pmc->mf( arg );
   myClass::mf( arg );
   ```
2. If no member function named `mf()` exists in `myClass`, the set of candidate functions is empty. (Actually, functions in base classes may then be considered.)


# Viable Functions
1. A viable member function is a function from the set of candidate member functions that can be called with the argument list specified on the call.
2. If the best viable function selected is a nonstatic member function, and the call cannot actually take place because no object is specified for the call (as is the case here), the call is flagged as an error by the  compiler.
    ```c++
    #include <iostream>
    
    struct myClass {
       static void mf(int){ std::cout << "A\n"; };
       void mf(char){ std::cout << "B\n"; };
    
    };
    
    int main() {
        char c = 1;
        myClass::mf(c);
        return 0;
    }
    ```
4. Because non-const nonstatic member function `mf(double)` cannot be called, it is excluded from the set of viable functions. The only viable function for the call is the const member function `mf(int)` , which is selected as the best viable function for the call.
   ```c++
   #include <iostream>
   
   struct myClass {
      static void mf(int*){ std::cout << "A\n"; };
      void mf(double){ std::cout << "B\n"; };
      void mf(int) const{ std::cout << "C\n"; };
   
   };
   
   int main() {
       const myClass mc;
       mc.mf(1.2); // C
       return 0;
   }
   ```
6. Static member functions are generic to all objects of a particular class type. Static member functions can only access the class static members directly. The nonstatic members of the const object mc, for example, cannot be accessed by the static member function `mf(int)`. For this reason it is always valid to call a static member function for a const object using the dot or arrow operator.
   ```c++
   #include <iostream>
   
   class Student {
   public:
       Student(int id) : m_id(id) {}
       static void foo() { std::cout << "Called static function\n"; }
   private:
       int m_id;
   };
   
   int main() {
       Student s(1);
       s.foo();
       return 0;
   }
   ```
{% endraw %}