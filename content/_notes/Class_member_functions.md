---
title: "Class member functions"
date: 2026-04-13T15:32:36+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: Class member functions
tags: [CPP]

---

1. Class member functions implement the set of operations that can be performed on a class object. 
2. Although each class object has its own copy of the class data members, there exists only one copy of each class member function.


# Inline versus non-inline member functions
1. If the definition of a member function is within a class body, the function is ***implicitly*** inline.
 	```c++
	class Screen {
	public:
	   void home() { _cursor = 0; }
	   char get() { return _screen[_cursor]; }
	};
	```
2. A member function can be inline in a class if one of the following points satisfiy:
   * A member function that is declared inline in the class declaration.
   * A member function that is defined with the inline keyword outside the class body.
   * A member function that is both declared inline in the class and defined inline outside.
   ```c++
   class Demo {
   public:
       void nonInline();
       inline void inlineViaDecl();
       void inlineViaDef();
       inline void inlineBoth();
   };
   
   void Demo::nonInline() {
       std::cout << "nonInline() called" << std::endl;
   }
   
   void Demo::inlineViaDecl() {
       std::cout << "inlineViaDecl() called" << std::endl;
   }
   
   inline void Demo::inlineViaDef() {
       std::cout << "inlineViaDef() called" << std::endl;
   }
   
   inline void Demo::inlineBoth() {
       std::cout << "inlineBoth() called" << std::endl;
   }
   ```
3. Since inline functions must be defined in every text file in which they are called, an inline member function that is not defined within the class body must be placed in the header file in which the class definition appears.

# Access to class members
1. The member function definition can refer to any of the class members, whether the member is private or public, without violating the class access restrictions.
2. The member function can access the members of its class without using the dot and arrow member access operators.
# Private versus public member functions
1. A class member function can be declared within the public, protected, or private section of the class body. 
2. The set of public member functions defines the interface of the class. 
3. The functions presented are public member functions. They can be invoked from anywhere within the program. Private member functions, however, can only be invoked by other member functions (and friends) of the class. They cannot be invoked directly by the program. Private member functions provide support to other member functions in implementing the class abstraction.
# Special member function
1. An initialization member function is called a constructor. It is invoked implicitly each time a class object is defined or allocated by a new expression. A constructor is declared by giving it its class name.
# `const` and `volatile` member functions
1. In object-oriented programming, we don’t usually modify the data members of an object directly from outside the class. Instead, we define and use member functions (a.k.a. methods) — these functions are the interface through which the object is safely and predictably modified or queried.
3. Only member functions declared as const can be invoked for a class object that is const.
4. A const member function defined outside the class body must specify the const keyword in both its declaration and its definition. 
   ```c++
   class Screen {
   public:
      bool isEqual( char ch ) const;
   private:
      string::size_type _cursor;
      string  _screen;
   };
   
   bool Screen::isEqual( char ch ) const
   {
      return ch == _screen[_cursor];
   }
   ```
4. Declaring a member function const guarantees that the member function does not modify the class data members, but if the class contains pointers, the objects to which the pointers refer may be modified within a const member function.
5. A const member function can be overloaded with a non- const member function that has the same parameter list.
    ```c++
    #include <iostream>
    
    class Screen {
    public:
       void get(int x, int y) {
          std::cout << "Called non-const member" << std::endl;
       };
       void get(int x, int y) const {
          std::cout << "Called const member" << std::endl;
       };
    };
    
    int main() {
       const Screen cs;
       cs.get(0,0); // calls const member
    
       Screen s;
       s.get(0,0);  // calls non-const member
    }
    ```
6. Even though a constructor or destructor is never a const member function, they can be called for const class objects. 
7. The const-ness of a class object is established when the constructor ends its execution and the class object has been initialized. The const-ness disappears once the destructor is invoked. A const class object is therefore considered const from the time its construction completes to the time its destruction starts.
8. Similar to const class objects, only volatile member functions, constructors, and the destructor can be invoked for a volatile class object.
9. Summary: non-const object can call either non-const or const member functionl; const object can only call const member function.
   |                           | Non-const object | Const object |
   |:-------------------------:|:----------------:|:------------:|
   | Non-const member function |        O         |      X       |
   |   Const member function   |        O         |      O       |

# Mutable data members
To allow a class data member to be modified even though it is the data member of a const object, we can declare the data member as mutable. A mutable data member is a member that is never const, even when it is the data member of a const object. A mutable member can always be updated, even in a const member function. To declare a member as a mutable data member, the keyword mutable must precede the declaration of the data member in the class member list.
{% endraw %}