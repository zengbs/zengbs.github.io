---
title: "Class Definition"
date: 2026-04-13T15:32:36+08:00
draft: false
---

---
title: Class Definition
tags: [CPP]

---

1. If two classes have members with the same name, the program is not in error and the members refer to different objects.
2. It is not necessary to declare the two members of type short separately.
3. A data member cannot be initialized explicitly in the class body. (Since C++11, we can initialize data members in the class body)
4. Class data members are initialized using the class constructor.
5. The member functions of a class are declared inside the class body. The definition of a member function can also be placed inside the class body.
6. Member functions are declared within the scope of their class. This means that the name of a member function is not visible outside the scope of its class.
7. Member functions have full access privileges to both the public and private members of the class whereas, in general, ordinary functions have access only to the public members of the class. Of course, the member functions of one class, in general, have no access privileges to the members of another class.
8. A public member is accessible from anywhere within a program.
9. A private member can be accessed only by the member functions and friends of its class.
   ```c++
   #include <iostream>
   
   class Screen {
      friend std::istream& operator>>( std::istream&,       Screen& );
      friend std::ostream& operator<<( std::ostream&, const Screen& );
   public:
      Screen(int width, int height)
         : _width(width), _height(height) {}
   private:
      int _width;
      int _height;
   };
   
   std::ostream& operator<<( std::ostream& os, const Screen& s )
   {
      os << "height = " << s._height << "\n";
      os << "width  = " << s._width  << "\n";
      return os;
   }
   
   
   std::istream& operator>>( std::istream& is, Screen& s )
   {
      std::cout << "Enter height and width: ";
      is >> s._height >> s._width;
      return is;
   }
   
   int main() {
   
      Screen s(1,2);
      std::cout << s;
      std::cin >> s;
      std::cout << s;
   
      return 0;
   }
   ```
11. A protected member behaves as a public member to a derived class, and behaves as a private member to the rest of the program.
12. Each section remains in effect until either another section label or the closing right brace of the class body is seen. If no access specifier is specified, by default the section immediately following the opening left brace of the class body is private.
13. Since friends are not members of the class granting friendship, they are not affected by the public, private, or protected section in which they are declared within the class body.
14. A friend may be a namespace function, a member function of another previously defined class, or an entire class.
15. Once the class is defined, all the class members are known. The size of the class is then known as well.
16. One cannot define objects of a class type if the class is not defined, because the size of the class type is not known and the compiler does not know how much storage to reserve for an object of that class type.
17. Because a class is not considered defined until its class body is complete, a class cannot have data members of its own type.
18. A class can then have data members that are pointers and references to its own class type.
    ```c++
    class LinkScreen {
       Screen window;
       LinkScreen *next; // ok
       LinkScreen *prev; // ok
    };
    ```