---
title: "Static Data Members of Class Templates"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

---
title: Static Data Members of Class Templates
tags: [CPP]

---

1. A class template can declare static data members. Each instantiation of the class template has its own set of static data members. 
2. The template definition of a static data member must appear outside the class template definition.
3.  The static data member definitions are added to a header file. These definitions must be included in the files in which instantiations of the static data members are used. 
4. A static data member is instantiated from the template definition only if it is used in a program. 
5. The template definition for the static data member does not cause any memory to be allocated. Memory is only allocated for particular instantiations of the static data member.
    ```c++
    #include <iostream>
    
    template <class T>
    class MyClass{
    public:
       MyClass(int m) : _m(m){}
    
       // do not allocate memory for static member at this line
       static int counter;
    private:
       T _m;
    };
    
    // allocate memory for static member at this line when MyClass is instantiated
    template<class T>
    int MyClass<T>::counter = 2;
    
    int main(){
    
       // No additional memory allocated for static member
       MyClass<int> obj(1);
       MyClass<float> objf(1);
    
       std::cout << MyClass<int>::counter << "\n";
       std::cout << MyClass<float>::counter << "\n";
    
       MyClass<float>::counter = 3;
    
       std::cout << MyClass<int>::counter << "\n";
       std::cout << MyClass<float>::counter << "\n";
    
       return 0;
    }
    ```