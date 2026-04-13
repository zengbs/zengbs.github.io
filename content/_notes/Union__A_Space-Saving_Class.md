---
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

1. A union can have a member of a class type that defines either a constructor, destructor, or copy assignment operator. 
1. Unions can have static data members in C++11 and later, because static members are not stored inside the union's memory.
2. Reference members in union are not allowed. Because a reference must be initialized when declared, and unions can’t guarantee how or when that memory will be initialized.
3. In C++11 and later, you can have class-type members with non-trivial constructors/destructors, but you must explicitly construct/destruct them using placement new or similar techniques — they are not automatically managed.
```c++
#include <iostream>
#include <string>

class Screen {
public:
    Screen();
    ~Screen();
};

union MyUnion {
    Screen s;
    std::string str;  // non-trivial member
    static int i;

    // Constructor
    // --> Placement new
    MyUnion() {
        new (&str) std::string("hello");
    }

    // Deconstructor
    // --> Explicit destructor
    ~MyUnion() {
        // Use the actual class name instead of the typedef.
        str.~basic_string<char, std::char_traits<char>, std::allocator<char>>();
    }
};

int MyUnion::i = 3;

int main() {
    MyUnion u;
    u.str = "123";
    std::cout << u.str << std::endl;
    std::cout << MyUnion::i << std::endl;
    return 0;
}
```

# Anonymous union

1. An anonymous union cannot have private or protected members, nor can it define member functions. 
2. An anonymous union defined in global scope must be declared as static.


```c++
class A {
public:
   union X{
       int i;
       void foo(){  }
   };
};


class B {
public:
   union {
       int j;
       // void bar(){ }; // Error: anonymous union cannot have member function;
       private:
       // int x; // Error: anonymous union cannot have private members
       protected:
       // int y; // Error: anonymous union cannot have protected members
   } q;

};

class C {
public:
   union {
       int k;
   };
};

// An anonymous union defined in global scope must be declared as static
static union {
  int x;
};

int main() {

    A::X u;
    u.i = 42;  // Access member 'i' directly as part of object 'a'

    B b;
    b.q.j = 1;

    C c;
    c.k = 3;

    return 0;
}
```
{% endraw %}