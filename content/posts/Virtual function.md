---
title: "Virtual function"
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

---
title: Virtual function
tags: [CPP]

---

###### tags: `CPP`

# Virtual function
A virtual function is used in the base class in order to ensure that the function is overridden. This especially applies to cases where a pointer of base class points to an object of a derived class.

![](https://i.imgur.com/qxQCu4y.png)


```cpp
#include<iostream>


using namespace std;

class Base {
   public:
    virtual void virtualPrint_override0() {
        cout << "Base Function" << endl;
    }
    virtual void virtualPrint_override1() {
        cout << "Base Function" << endl;
    }
    virtual void virtualPrint_override2() {
        cout << "Base Function" << endl;
    }
    virtual void virtualPrint() {
        cout << "Base Function" << endl;
    }
    void nonvirtualPrint() {
        cout << "Base Function" << endl;
    }
};

// the "Derived" class is derived from the "Base" class
class Derived : public Base {
   public:
    void virtualPrint_override0(char) override {
        cout << "Derived Function" << endl;
    }
    void virtualPrint_override1(char) {
        cout << "Derived Function" << endl;
    }
    void virtualPrint_override2() override {
        cout << "Derived Function" << endl;
    }
    void virtualPrint()  {
        cout << "Derived Function" << endl;
    }
    void nonvirtualPrint() {
        cout << "Derived Function" << endl;
    }
};


int main() {

    Derived derived;
    Base* base = &derived;

    base->virtualPrint_override0(); 
    base->virtualPrint_override1(); 
    base->virtualPrint_override2();
    base->virtualPrint();          
    base->nonvirtualPrint();        

    return 0;
}
```

* The first call to `virtualPrint_override0` results in a compiling error because the Derived class has overridden the `virtualPrint_override0` function with a different function signature than the one in the Base class. This means that the compiler will not be able to find a matching function in the Base class to call, and will generate an error.

* The second call to `virtualPrint_override1` is successful, because the Derived class has overridden the `virtualPrint_override1` function with a different function signature, but the Base class still contains a matching function. The Base class's `virtualPrint_override1` function is called, which prints "Base Function".

* The third call to `virtualPrint_override2` is successful, because the Derived class has overridden the `virtualPrint_override2` function with the same function signature as the one in the Base class. The Derived class's `virtualPrint_override2` function is called, which prints "Derived Function".

* The fourth call to `virtualPrint` is successful, because the Derived class has overridden the `virtualPrint` function with the same function signature as the one in the Base class. The Derived class's `virtualPrint` function is called, which prints "Derived Function".

* The fifth call to `nonvirtualPrint` is successful, because the Derived class has overridden the `nonvirtualPrint` function with the same function signature as the one in the Base class. However, since the `nonvirtualPrint` function is not virtual, the Base class's `nonvirtualPrint` function is called, which prints "Base Function".



## Pure virtual function
The virtual function without implementation is pure virtual function. Sometimes implementation of all function cannot be provided in a base class because we don’t know the implementation until deriving a new class from base class.

   ```cpp
    class Base {
       public:
        virtual void print() = 0;                                                                            
    };
     
    class Derived : public Base {
       public:
        void print() {
            cout << "Derived Function" << endl;
        }   
    };
     
    int main() {
     
        Derived derived;
     
        Base *basePtr1 = &derived;
     
        basePtr1->print();    // Derived Function
     
        derived.print();      // Derived Function
     
        return 0;
    }
```

In this case, `Base` is an abstract class, we cannot create an instance of an abstract class.