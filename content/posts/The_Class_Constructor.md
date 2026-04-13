---
title: "The Class Constructor"
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: The Class Constructor
tags: [CPP]

---

1. The constructor is identified by providing it with the same name as the class.
2. There is no constraint on the number of constructors we may declare for a class, provided the parameter list of each constructor is unique.
3. Our preferred solution is the use of the default argument because it reduces the number of constructors associated with the class.
4. C++ requires that the constructor be applied to the defined class object prior to the first use of that object.
5. There are three generally equivalent forms for pecifying the arguments to a constructor:
    ```c++
    // generally equivalent forms
    Account acct1( "Anna Press" );
    Account acct2 = Account( "Anna Press" );
    Account acct3 = "Anna Press";
    ```
6. The `acct3` form can only be used when specifying a single argument. For two or more arguments, only the `acct1` and `acct2` forms can be used. In general, we recommend using the `acct1` form.
7. If a class does not declare any constructors, the compiler generates a default constructor for you.
8. If a class declares at least one constructor, and none of them is a default constructor, then:
    * You must explicitly call one of the declared constructors when you create an object.
    * You cannot create an object without passing arguments.
9. You can have a default constructor along with multiple user-defined constructors in the same class.
   ```c++
   #include <iostream>
   
   class Person {
   public:
       Person() {
           std::cout << "Default constructor called\n";
       }
   
       Person(std::string name) {
           std::cout << "Constructor with name: " << name << "\n";
       }
   
       Person(std::string name, int age) {
           std::cout << "Constructor with name and age: " << name << ", " << age << "\n";
       }
   };
   
   int main() {
       Person p1;                      // Calls default constructor
       Person p2("Alice");             // Calls constructor with name
       Person p3("Bob", 30);           // Calls constructor with name and age
       return 0;
   }
   ```
10. The member initialization list can only be specified within the constructor definition, not its declaration.
11. Member initialization list provides the following features:
    * Direct initialization avoiding default-construction followed by assignment.
    * Especially important for objects like std::string, std::vector, or custom classes.
11. Constructors and destructors cannot be declared as const and volatile. Please see [here](https://hackmd.io/clYUO5MmSJKBP3bNsVnRVw?view#const-and-volatile-member-functions) for details.
12. Since a class can have multiple constructors, unintended implicit class conversions might cause diffcult-to-trace errors. The `explicit` modifier informs the compiler not to provide implicit conversion.
    ```c++
    #include <iostream>
    
    class Foo {
    public:
       explicit Foo() : a(-2), b(5.6) {  };
       explicit Foo(int ia, double ib) : a(ia), b(ib){};
       int a;
       double b;
    };
    
    int main() {
        Foo foo1;
        Foo foo2(1, 2.3);
        Foo foo3{1, 2.3};
        Foo foo4 = Foo();
        //Foo foo = {1, 1.1};  // error
        //Foo foo = {1, 1.1};  // error
        //Foo foo = {1, -5.2}; // error
        std::cout << foo1.a << ", " << foo1.b << std::endl;  // -2, 5.6
        std::cout << foo2.a << ", " << foo2.b << std::endl;  //  1, 2.3
        std::cout << foo3.a << ", " << foo3.b << std::endl;  //  1, 2.3
        std::cout << foo4.a << ", " << foo4.b << std::endl;  // -2, 5.6
        return 0;
    }
    ```
13. A constructor that is declared without the function specifier `explicit` is called a converting constructor. 

# The Default Constructor

1. A default constructor is a constructor that **is able to** be invoked ***without*** user-specified arguments. This does not mean that it cannot accept arguments. It means only that a default value is associated with each parameter of the constructor.
   ```c++
   // each is a default constructor
   Account::Account() { ... }
   iStack::iStack( int size = 1 ) { ... }
   Complex::Complex(double re=0.2,double im=8.0) { ... }
   
   // each is not default constructor
   iStack::iStack( int size ) { ... }
   Account::Account( std::string& ) { ... }
   ```
2. When we create an object from a class, one of the following occurs:
   * The default constructor is defined. It is applied to an object.
   * The default constructor is defined, but it is nonpublic. The definition of acct is flagged at compile-time as an error: `main()` has no access privilege.
   * No default constructor is defined, but one or more constructors requiring arguments is defined. The definition of the oject is flagged at compile-time as an error: too few constructor arguments.
   * No default constructor is defined, nor any other constructor. The definition is legal. The object is uninitialized and no constructor is invoked.


# Constraining Object Creation

1. To prevent the copying of one class object with another object of its class.
   ```c++
   // until C++11
   class NoCopy {
   private:
       NoCopy(const NoCopy&);            // prevent copy
       NoCopy& operator=(const NoCopy&); // prevent assignment
   public:
       NoCopy() = default;
   };
   ```
      ```c++
      // since C++11
   class NoCopy {
   public:
       NoCopy(const NoCopy&) = delete;            // prevent copy
       NoCopy& operator=(const NoCopy&) = delete; // prevent assignment
       NoCopy() = default;
   };
   ```
   :::info
   | Scenario                        |           Why copying is bad            |
   | ------------------------------- |:---------------------------------------:|
   | Unique resources (file, socket) |      Double-free, dangling handles      |
   | Singleton pattern               |         Enforce single instance         |
   | Abstract base/interface         |        No meaningful way to copy        |
   | Mutex/Thread-safe class         |         Copying mutex is unsafe         |
   | Expensive-to-copy objects       | Avoid performance hit, use move instead |
   :::
2. To indicate that a constructor is intended to be invoked only when the class serves as a base class within an inheritance hierarchy and not as an object to be manipulated directly within the application.
# The Copy Constructor
1. The initialization of one class object with another object of its class is referred to as default memberwise initialization.
2. Conceptually, the copying of one class object with another is accomplished by copying each of the class nonstatic data members in turn.
   ```c++
   #include <iostream>
   
   struct Foo {
      Foo(int ival, double dval) : x(ival), y(dval) {};
   
      // cpmpiler-generated copy constructor
      //Foo(const Foo &rhs ) = default;
   
      // User-provided copy constructor
      Foo( const Foo &rhs )
      {
         std::cout << "Called copy constructor\n";
         x = rhs.x;
         y = rhs.y;
      }
   
      int x;
      double y;
   };
   
   int main() {
       Foo foo(1, -6e2);
       Foo bar1 = Foo(foo); // Called copy ctor and copy assignment
       
       // Direct initialization
       Foo bar2(foo); // Called copy ctor
       
       // Copy initialization
       Foo bar3 = foo; // Called copy ctor
       
       return 0;
   }
   ```

# Initializations in C++
## Aggregate Structure
* An array, or
* A class/struct/union that all of the following hold:
	* No user‑provided (or inherited) constructors
	* No private or protected non‑static data members
	* No base classes
	* No virtual functions


# Default initialization
```c++
#include <iostream>

struct Aggregate {
   int x; double y;
};

struct Foo {
   Foo(int ival, double dval) : x(ival), y(dval) {};
   int x; double y;
};

struct Bar {
   Bar() : x(0), y(2.0) {}; // user-provided ctor
   Bar(int ival, double dval) : x(ival), y(dval*1.6) {};
   int x; double y;
};

int main() {

   // 1. Built-in type
   float z;
   static float s_z;
   std::cout << z << ", " <<  s_z << std::endl; // Uninitialized, 0.0

   // 2. auto
   // auto i; Error: declaration of 'auto i' has no initializer

   // 3. Aggregation
   Aggregate agg;
   static Aggregate s_agg;

   std::cout << agg.x   << ", " << agg.y   << std::endl; // Uninitialized
   std::cout << s_agg.x << ", " << s_agg.y << std::endl; // 0, 0.0

   // 4. Type without user-provided default ctor
   //Foo foo; // Error:  no matching function for call to 'Foo::Foo()'

   // 5. Type with user-provided default ctor
   Bar bar;
   std::cout << bar.x   << ", " << bar.y   << std::endl; // 0, 2.0

   return 0;
}
```

## Copy Initialization
```c++
#include <iostream>

struct Aggregate {
   int x;
};

struct Foo {
   Foo(int ival) : x(2*ival) {};
   int x;
};

struct Bar {
   Bar() : x(0) {}; // user-provided ctor
   Bar(int ival) : x(2*ival) {};
   int x;
};

int main() {

   // 1. Built-in type
   float z = 1.1;
   std::cout << z << std::endl;

   // 2. auto
   auto y = 2.5f;
   std::cout << y << std::endl;

   // 3. Aggregation
   // Aggregate agg = 2; Error: conversion from 'int' to non-scalar type 'Aggregate' requested

   // 4. Type without user-provided default ctor
   Foo foo = 2;
   std::cout << foo.x << std::endl; // 4

   // 5. Type with user-provided default ctor
   Bar bar = 3;
   std::cout << bar.x << std::endl; // 6

   return 0;
}
```

## Direct Initialization
```c++
#include <iostream>

struct Aggregate {
   int x; double y;
};

struct Foo {
   Foo(int ival, double dval) : x(ival), y(dval) {};
   int x; double y;
};

struct Bar {
   Bar() : x(0), y(1.2) {}; // user-provided ctor
   Bar(int ival, double dval) : x(ival), y(dval) {};
   int x; double y;
};

int main() {

   // 1. Built-in type
   float z (1.1);
   std::cout << z << std::endl; // 1.1

   // 2. auto
   //auto y (2.5f);
   //std::cout << y << std::endl;

   // 3. Aggregation
   // error: no matching function for call to 'Aggregate::Aggregate(int, double)'
   // --> can compile since C++20
   // Aggregate agg (2, 3.2); // error: no matching function for call to 'Aggregate::Aggregate(int, double)'
   // std::cout << agg.x << agg.y << endsl;

   // 4. Type without user-provided default ctor
   Foo foo (2, 1.5);
   std::cout << foo.x << ", " << foo.y << std::endl; // 2, 1.5

   // 5. Type with user-provided default ctor
   Bar bar (3, -5.2);
   std::cout << bar.x << ", " << bar.y <<  std::endl; // 3, -5.2

   return 0;
}
```


## Direct List Initialization (recommended way in modern C++)
```c++
#include <iostream>

struct Aggregate {
   int x; double y;
};

struct Foo {
   Foo(int ival, double dval) : x(ival), y(dval) {};
   int x; double y;
};

struct Bar {
   Bar() : x(0), y(1.2) {}; // user-provided ctor
   Bar(int ival, double dval) : x(ival), y(dval) {};
   int x; double y;
};

int main() {

   // 1. Built-in type
   float z {1.1};
   // float zz {1.1, 5.6}; Error
   std::cout << z << std::endl; // 1.1

   // 2. auto
   auto y {2.5f};
   // auto y {2.5f, -2.36f}; Error
   std::cout << y << std::endl; // 2.5

   // 3. Aggregation
   Aggregate agg {2, 3.2}; // Aggregation initialization
   std::cout << agg.x << ", " << agg.y << std::endl; // 2, 3.2

   // 4. Type without user-provided default ctor
   //    --> Calls the matching ctor
   Foo foo {2, -6.2};
   std::cout << foo.x << ", " << foo.y << std::endl; // 2, -6.2

   // 5. Type with user-provided default ctor
   //    --> Calls the matching ctor
   Bar bar {-6, 2.8};
   std::cout << bar.x << ", " << bar.y <<  std::endl; // -6, 2.8

   return 0;
}
```

## Copy List Initialization
```c++
#include <iostream>

struct Aggregate {
   int x; double y;
};

struct Foo {
   Foo(int ival, double dval) : x(ival), y(dval) {};
   int x; double y;
};

struct Bar {
   Bar() : x(0), y(1.2) {}; // user-provided ctor
   Bar(int ival, double dval) : x(ival), y(dval) {};
   int x; double y;
};

int main() {

   // 1. Built-in type
   float z = {1.1};
   // float zz {1.1, 5.6}; Error
   std::cout << z << std::endl; // 1.1

   // 2. auto
   auto y  = {2.5f};                // std::initializer_list
   auto yy = {2.5f, 12.1f, -5.3f};  // std::initializer_list
   for (float f : yy)
   {
      std::cout << f << std::endl;
   }

   // 3. Aggregation
   Aggregate agg = {2, 3.2};  // Aggregation initialization
   std::cout << agg.x << ", " << agg.y << std::endl; // 2, 3.2

   // 4. Type without user-provided default ctor
   //    --> Calls the matching ctor
   Foo foo = {2, -6.2};
   std::cout << foo.x << ", " << foo.y << std::endl; // 2, -6.2

   // 5. Type with user-provided default ctor
   //    --> Calls the matching ctor
   Bar bar = {-6, 2.8};
   std::cout << bar.x << ", " << bar.y <<  std::endl; // -6, 2.8

   return 0;
}
```

## Value Initialization
```c++
#include <iostream>

struct Aggregate {
   int x; double y;
};

struct Foo {
   Foo(int ival, double dval) : x(ival), y(dval) {};
   int x; double y;
};

struct Bar {
   Bar() : x(-6), y(1.2) {}; // user-provided ctor
   Bar(int ival, double dval) : x(ival), y(dval) {};
   int x; double y;
};

int main() {

   // 1. Built-in type
   float z1 = float();
   float z2 = {};
   float z3 {};
   std::cout << z1 << ", " << z2 << ", " << z3 << std::endl; // 0, 0, 0

   // 2. auto
   // auto y ();

   // 3. Aggregation
   //  error: request for member 'x' in 'agg1', which is of non-class type 'Aggregate()'
   // Aggregate agg1 ();
   Aggregate agg1 {};   // Aggregation initialization
   Aggregate agg2 = {}; // Aggregation initialization
   std::cout << agg1.x << ", " << agg1.y << std::endl; // 0, 0
   std::cout << agg2.x << ", " << agg2.y << std::endl; // 0, 0

   // 4. Type without user-provided default ctor

   // warning: empty parentheses interpreted as a function declaration
   // Foo foo1 ();

   // error: no matching function for call to 'Foo::Foo(<brace-enclosed initializer list>)'
   // Foo foo1 {};

   // error: could not convert '<brace-enclosed initializer list>()' from '<brace-enclosed initializer list>'
   // Foo foo2 = {};


   // 5. Type with user-provided default ctor
   // Bar bar1 ();   // error: request for member 'x' in 'bar1', which is of non-class type 'Bar()'
   Bar bar1 {};
   Bar bar2 = {};
   std::cout << bar1.x << ", " << bar1.y <<  std::endl; // -6, 2.8
   std::cout << bar2.x << ", " << bar2.y <<  std::endl; // -6, 2.8

   return 0;
}
```
{% endraw %}