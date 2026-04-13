---
title: "Class Objects"
date: 2026-04-13T15:32:36+08:00
draft: false
---

---
title: Class Objects
tags: [CPP]

---

1. By default, copying a class object is equivalent to copying all of its data members (shallow copy).
2. By default, a class object is ***passed by value*** when specified as a function argument or as a function return value.
    ```c++
    #include <iostream>
    
    class MyClass {
    public:
        MyClass(int v) : _member(v) {}
        int display() { return _member; }
        int& get() { return _member; }
    private:
        int _member;
    };
    
    void modifyObject( MyClass obj ){
       obj.get() = 3;
    }
    
    MyClass returnByValue(){
       MyClass obj(2);
       return obj;
    }
    
    int main() {
    
        MyClass obj(1);
        modifyObject(obj);
        std::cout << obj.display() << std::endl;
    
        MyClass obj2 = returnByValue();
        std::cout << obj2.display() << std::endl;
    
        return 0;
    }
    ```