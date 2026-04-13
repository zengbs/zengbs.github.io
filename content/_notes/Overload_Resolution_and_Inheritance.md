---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---

# Candidate Functions
* With inheritance, if the argument is of (1) class type, (2) a reference to class type, or (3) a pointer to class type, and (4) the class has base classes, the functions declared within the namespaces where the base classes are defined, and with the same name as the function called, are also added to the set of candidate functions.

   ```c++
   #include <iostream>
   
   namespace NS {
      class ZooAnimal { };
      void display(const ZooAnimal&);
   }
   
   void NS::display( const ZooAnimal& rz ){
      std::cout << "NS::display( const ZooAnimal& )\n";
   }
   
   class Bear : public NS::ZooAnimal { };
   
   int main(){
   
      Bear bear;
      display(bear);
   
      return 0;
   }
   ```
* With inheritance, if the argument type is a class with base classes, the friend functions with the same name as the function that is called and declared within the base class definitions are also added to the set of candidate functions.
   ```c++
   #include <iostream>
   
   namespace NS {
      class ZooAnimal {
         friend void display(const ZooAnimal&);
      };
      void display(const ZooAnimal&);
   }
   
   void NS::display( const NS::ZooAnimal& rz ){
      std::cout << "NS::display( const ZooAnimal& )\n";
   }
   
   class Bear : public NS::ZooAnimal { };
   
   int main(){
   
      Bear bear;
      display(bear);
   
      return 0;
   }
   ```
* Hence, if an ordinary function call has an argument that is either an object of class type, a pointer to a class type, or a reference to a class type, the candidate functions are the union of
    1. The functions visible at the point of the call.
    2. The functions declared within the namespace where the class type is defined or within the namespaces where the class' base classes are defined.
    3. The functions that are friends of the class or friends of the class' base classes.

# Viable Functions and User-Defined Conversion Sequences
* A viable function is a function for which there exists type conversions to convert each function call argument to the type of a corresponding, viable function parameter.
* A user-defined conversion is either a conversion function or a nonexplicit constructor taking one argument.
* User-defined conversion functions are inherited like any other class member functions.
   ```c++
   #include <iostream>
   #include <bits/stdc++.h>
   
   class ZooAnimal {
   public:
      ZooAnimal ( const std::string& name ) : _name(name) {}
      operator const char*(){
         std::cout << "Calls conversion operator\n";
         char* c_name = new char[ _name.length()+1 ];
         std::strcpy( c_name, _name.c_str() );
         return c_name;
      }
      std::string _name;
   };
   
   
   void display( const char* name ){
      std::cout << name << "\n";
      delete [] name;
   }
   
   class Bear : public ZooAnimal {
   public:
      Bear( const std::string& name ) : ZooAnimal( name ) {}
   };
   
   int main(){
      Bear bear("my bear");
      display(bear);
      return 0;
   }
   ```
* Constructors are not inherited. So we cannot use the constructor of base class as conversion.
* With inheritance, user-defined conversion functions are inherited, thus a greater set of viable functions is considered during the second step of function overload resolution.

# Best Viable Function
* Inheritance also impacts the third step of the function overload resolution, that of selecting the best viable function.
* When ranking the conversions applied to function arguments, these conversions (upcasting) have the rank of a standard conversion.
    1. Converting an argument of a derived class type to a parameter of any of its base class types
    2. Converting a pointer to a derived class type to a pointer to any of its base class types
    3. Initializing a reference to a base class type with an lvalue of a derived class type
     ```c++
     #include <iostream>
     
     class ZooAnimal { };
     
     void display1( const ZooAnimal za ){
        std::cout << "Converting an argument of a derived class type to a parameter of any of its base class types()\n";
     }
     void display2( const ZooAnimal* za ){
        std::cout << "Converting a pointer to a derived class type to a pointer to any of its base class types\n";
     }
     void display3( const ZooAnimal& za ){
        std::cout << "Initializing a reference to a base class type with an lvalue of a derived class type\n";
     }
     
     class Bear : public ZooAnimal { };
     
     int main(){
        Bear bear;
        Bear* ptr = &bear;
     
        display1(bear);
        display2(ptr);
        display3(bear);
        return 0;
     }
     ```
* Similar to function overloading, a standard conversion sequence is better than a user-defined conversion sequence when ranking type conversions to select the best viable function.
   ```c++
   #include <iostream>
   #include <bits/stdc++.h>
   
   class ZooAnimal {
   public:
      ZooAnimal ( const std::string& name ) : _name(name) {}
      operator const char*(){
         std::cout << "Calls conversion operator\n";
         char* c_name = new char[ _name.length()+1 ];
         std::strcpy( c_name, _name.c_str() );
         return c_name;
      }
      std::string _name;
   };
   
   void display( const char* name ){
      std::cout << "Calls user-defined function\n";
      delete [] name;
   }
   
   void display( const ZooAnimal& za ){
      std::cout << "Calls display with standard conversion\n";
   }
   
   class Bear : public ZooAnimal {
   public:
      Bear( const std::string& name ) : ZooAnimal( name ) {}
   };
   
   int main(){
      Bear bear("my bear");
      display(bear);
      return 0;
   }
   ```
 * When ranking different standard conversions from a derived class type to different base class types, a conversion to a base class that is less removed from the derived class type is considered a better standard conversion than a conversion to a base class that is further removed from the derived class type.
   ```c++
   #include <iostream>
   #include <bits/stdc++.h>
   
   class ZooAnimal { };
   
   class Bear : public ZooAnimal { };
   
   void display( const Bear& ){
      std::cout << "Calls display( const Bear& )\n";
   }
   
   void display( const ZooAnimal& ){
      std::cout << "Calls display( const ZooAnimal& )\n";
   }
   
   int main(){
      Bear bear;
      display(bear);
      return 0;
   }
   ```
* When ranking different standard conversions from a pointer to a derived class type to pointers to different base class types, the conversion to the base class that is less removed from the derived class type is considered a better standard conversion.
   ```c++
   #include <iostream>
   
   class ZooAnimal { };
   
   class Bear : public ZooAnimal { };
   
   void display( const Bear* ){
      std::cout << "Calls display( const Bear* )\n";
   }
   
   void display( const ZooAnimal* ){
      std::cout << "Calls display( const ZooAnimal* )\n";
   }
   
   int main(){
      Bear bear;
      display(&bear);
      return 0;
   }
   ```
* A standard conversion to a pointer to a base class type is better than a conversion to `void*`
   ```c++
   #include <iostream>
   
   class ZooAnimal { };
   
   class Bear : public ZooAnimal { };
   
   void display( Bear* ){
      std::cout << "Calls display( Bear* )\n";
   }
   
   void display( void* ){
      std::cout << "Calls display( void* )\n";
   }
   
   int main(){
      Bear bear;
      display(&bear);
      return 0;
   }
   ```
* Multiple inheritance may cause two standard conversions from a derived class type to different base class types to be equally good if both base classes are equally removed from the derived class type.
   ```c++
   #include <iostream>
   
   class ZooAnimal { };
   
   class Endangered : virtual public ZooAnimal {};
   
   class Bear : virtual public ZooAnimal { };
   
   class Panda : public Bear, public Endangered {};
   
   void display( const Bear& ){
      std::cout << "Calls display( Bear& )\n";
   }
   
   void display( const Endangered& ){
      std::cout << "Calls display( Endangered& )\n";
   }
   
   int main(){
   
      Panda p;
   
      // Error: ambiguous
      display(p);
      
      // Ok
      display(static_cast<Bear>(p));
      
      return 0;
   }
   ```
* Since the slicing issue, (1) the initialization of a derived class object with an object of base class type, (2) the initialization of a reference of a derived class type with an object of base class type, or (3) the conversion of a pointer to a base class type to a pointer to a derived class type is never applied as an implicit conversion.
   ```c++
   #include <iostream>
   
   class ZooAnimal { };
   
   class Bear : public ZooAnimal { };
   
   
   void display( const Bear& ){
      std::cout << "Calls display( Bear& )\n";
   }
   
   int main(){
   
      ZooAnimal za;
   
      display( za );
   
      return 0;
   }
   ```
{% endraw %}