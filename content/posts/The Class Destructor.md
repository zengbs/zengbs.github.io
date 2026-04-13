---
title: "The Class Destructor"
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

---
title: The Class Destructor
tags: [CPP]

---

# Class Destructor
1. A destructor is a special user-defined member function that is invoked automatically whenever an object of its class goes out of scope or whenever the delete expression is applied to a pointer to a class object.
2. The destructor is given the name of the class prefixed with a tilde (~).
3. It can neither return a value nor can it take any parameters. Because it cannot specify any parameters, it cannot be overloaded. 
4. Although we can define multiple class constructors, we can provide only a single destructor to be applied to all objects of our class.
   ```c++
   #include <iostream>
   
   class Foo {
   public:
      Foo(int ival, double dval) : x(ival), y(dval) {};
      ~Foo();
   private:
      int x;
      double y;
   };
   
   inline
   Foo::~Foo()
   {
      x = 0;
      y = 0.0;
   }
   
   int main() {
       return 0;
   }
   ```
5. If the data members of a class are contained by value, no destructor is necessary.
6. Neither the declaration of the reference to a class object nor that of the pointer to class object results in a constructor being invoked.
7. Unlike constructors, however, there is no associated source code statement to indicate the invocation of a destructor on a class object. Rather, the compiler simply inserts the invocation subsequent to the last use of the object but before termination of the associated scope.
8. The language guards internally against applying operator delete to a pointer addressing no object, and so we do not need to write code to guard against that:
   ```c++
   // unnecessary -- carried out implicitly by compiler
   if ( ptr != 0 ) delete ptr;
   ```
# Explicit Destructor Invocation
Explicit destructor invocation often in conjunction with replacement new. For example:

## Use case 1: allocate memory pool for a single object
```c++
#include <iostream>
#include <new>

class Image {
public:
   Image(const std::string& name) : _name (name)
   {
      std::cout << "Called constructor" << std::endl;
   }
   ~Image(){
      _name.clear();
      std::cout << "Called destructor" << std::endl;
   }
private:
   std::string _name;

};

int main() {
    // allocate a heap buffer of size sizeof(Image) bytes.
    std::cout << "Step1:" << std::endl;
    char *arena = new char [sizeof(Image)];

    // construct Image in pre-allocated memory
    std::cout << "Step2:" << std::endl;
    Image *ptr = new (arena)  Image("Qhsil"); // Called constructor
    
    // manually destroy
    std::cout << "Step3:" << std::endl;
    ptr->~Image(); // Called destructor

    // construct Image in pre-allocated memory
    std::cout << "Step4:" << std::endl;
    ptr = new (arena)  Image("Dqqkd"); // Called constructor

    // manually destroy
    std::cout << "Step5:" << std::endl;
    ptr->~Image(); // Called destructor

    // free allocated memory
    std::cout << "Step6:" << std::endl;
    delete[] arena;

    std::cout << "Finished." << std::endl;
    return 0;
}
```
## Use case 2: allocate memory pool for an array of objects
```c++
#include <iostream>
#include <new>
#include <string>

class Image {
public:
   Image(const std::string& name, int index) : _name(name), _index(index) {}
   ~Image() {
       _name.clear();
       _index = -1;
   }
private:
   std::string _name;
   int _index;
};

int main() {
    int numImgs = 10;
    char* arena = new char[sizeof(Image) * numImgs];
    Image* images[numImgs];

    // 1st group of images
    for (int i = 0; i < numImgs; ++i) {
        char* ptr = arena + i * sizeof(Image);
        images[i] = new (ptr) Image("Qhsil", i);
    }

    for (int i = 0; i < numImgs; ++i) {
        images[i]->~Image();
    }

    // 2nd group of images
    for (int i = 0; i < numImgs; ++i) {
        char* ptr = arena + i * sizeof(Image);
        images[i] = new (ptr) Image("Dqqkd", i);
    }

    for (int i = 0; i < numImgs; ++i) {
        images[i]->~Image();
    }
    delete[] arena;

    return 0;
}
```
However, using `std::vector` is safer and more flexible.

# Potential of Program Code Bloat
1. An inline destructor can be an unsuspected source of program code bloat because it is inserted at each exit point within a function for each active local class object.
2. For example, the destructor must be expanded inline prior to each return statement:
   ```c++
   Account acct( "Tina Lee" );
   int swt;
   // ...
   switch( swt ) {
   case 0:
   return;
   case 1:
   // do something
   return;
   case 2:
   // do something else
   return;
   // and so on
   }
   ```
   the solution is either to declare the destructor to be non-inline or to rewrite the program code as follows:
   ```c++
   // rewritten to provide a single return point
   switch( swt ) {
   case 0:
   break;
   case 1:
   // do something
   break;
   case 2:
   // do something else
   break;
   // and so on
   }
   // single return point
   return;
   ```