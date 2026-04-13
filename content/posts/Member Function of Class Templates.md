---
title: "Member Function of Class Templates"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

---
title: Member Function of Class Templates
tags: [CPP]

---

1. As with nontemplate classes, a member function of a class template can either be defined within the class template definition, in which case the member function is an inline member function, or the member function can be defined outside the class template definition. 
    ```c++
    #include <iostream>
    
    // inline member function defined inside the class
    template <class T>
    struct Queue1 {
       Queue1(T m) : _m(m){}
       T _m;
    };
    
    // inline member function defined outside the class
    template <class T>
    struct Queue2 {
       Queue2(T);
       T _m;
    };
    
    template <class T>
    inline Queue2<T>::
    Queue2(T m) : _m(m){}
    
    int main() {
        Queue1<double> q1(1.2);
        std::cout << q1._m << "\n";
    
        Queue2<int> q2(1);
        std::cout << q2._m << "\n";
        return 0;
    }
    ```
2. A member function of a class template is not instantiated automatically when the class template is itself instantiated. The member function is instantiated only if it is used by the program (a use of a function, recall, invokes the function or takes its address).