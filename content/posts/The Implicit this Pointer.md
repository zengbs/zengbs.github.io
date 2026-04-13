---
title: "The Implicit this Pointer"
date: 2026-04-13T15:32:38+08:00
draft: false
---

---
title: The Implicit this Pointer
tags: [CPP]

---


* The `this` pointer addresses the class object for which the member function is called.
* Its type in a non-`const` member function is a pointer to the class type, a pointer to a `const` class type in a `const` member function, and a pointer to a `volatile` class type in a `volatile` member function.
* There are two transformations that must be applied to support the this pointer:
  1. Translate the definition of the class member function.
     ```c++
     inline void move( Screen* this, int r, int c )
     {
        this->_cursor = ...;
     }
     ```
  2. Translate each invocation of the class member function to add an additional argument — the address of the object for which the member function is invoked. 
     ```c++
     myScreen.move( 2, 2 )
     //is translated into
     move( &myScreen, 2, 2 )
     ```
# When to use the `this` pointer

## Case 1: Disambiguation
```c++
class MyClass {
    int value;
public:
    void setValue(int value) {
        this->value = value;  // "this->value" is the member; "value" is the parameter.
    }
};
```
## Case 2: Method chaining
```c++
class MyClass {
    int x, y;
public:
    MyClass& setX(int x) {
        this->x = x;
        return *this;  // Enables chaining.
    }
    MyClass& setY(int y) {
        this->y = y;
        return *this;  // Enables chaining.
    }
};

// Usage:
MyClass obj;
obj.setX(10).setY(20);
```
## Case 3: Self-assignment check
```c++
class MyClass {
    int data;
public:
    MyClass& operator=(const MyClass& other) {
        if (this == &other)  // Check for self-assignment.
            return *this;
        // Copy data...
        data = other.data;
        return *this;
    }
};
```
## Case 4: Passing the current object
Sometimes you need to pass the current object’s address to other functions or methods. You can do this directly using this.
## Case 5: Lambda capturing
In C++11 and later, when using lambdas inside member functions, you might capture this to access members of the current object:
```c++
class MyClass {
    int value;
public:
    void doSomething() {
        auto lambda = [this]() { 
            // Use this->value inside the lambda.
            return this->value;
        };
        int result = lambda();
    }
};
```