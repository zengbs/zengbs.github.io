---
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

###### tags: `CPP`

# Template

Templates are not actually compiled until they are instantiated, or specialized, with a specific type.

## Implicit instantiation
* Must call template function in the same file as the declaration is located.
```cpp
#include <iostream>

template <typename T>
T max(T a, T b) {
  return (a > b) ? a : b;
}

int main(){
   int x = max(3, 4);  // Implicit instantiation of max<int>
   double y = max(3.14, 2.72);  // Implicit instantiation of max<double>
}
```

## Explicit instantiation

* `template.cpp`:
```cpp
template <typename T>
T max(T a, T b) {
  return (a > b) ? a : b;
}

template int max<int>(int, int);
template double max<double>(double, double);
```

* `main.cpp`:
```cpp=
#include<iostream>

template <typename T>
T max(T a, T b);

int main(){
 int x = max(3, 4);           // Implicit instantiation of max<int>
 double y = max(3.14, 2.72);  // Implicit instantiation of max<double>

 printf("%d, %e\n", x, y);
}
```

# Reduced Redundant Code Generation
## Implicit Instantiation:
   The compiler generates template instantiations on demand for **every type used in the program**. If the same template is used across multiple files, **the compiler generates the instantiation for each file**, potentially leading to redundant instantiation.
## Explicit Instantiation:
   The template is instantiated once for a specific type in a designated translation unit, and the linker uses this pre-generated instantiation across the program. This avoids redundant code generation during compilation. So we prefer explicit instantiation to implicit instantiation when several files call the same template.

# Questions
1. Should I instantiate template derived class again if it's base class already instantiated?
    * No, you do not need to instantiate a template-derived class again if its base class is already instantiated, provided that the derived class doesn't introduce additional template parameters.
2. Should I instantiate a template member function within a template class again if the template class already instantiated?
    * You do not need to explicitly instantiate template member functions within a template class if the class is already instantiated. The compiler automatically instantiates them when they are used.
    * If a template member function has its own template parameters, it is treated as a separate template and instantiated independently as needed.

# Template Member Function within a Template Class


### `MyClass.h`
```c++
#include <iostream>

// Template class definition
template <typename T>
class MyClass {
public:
    // Non-template member function
    void func1(T val);

    // Template member function
    template <typename U>
    void func2(T val1, U val2);
};
```

### `MyClass.cpp`
```c++
#include "MyClass.h"

// Define the non-template member function
template <typename T>
void MyClass<T>::func1(T val) {
    std::cout << "MyClass::func1 called for type T:" << val  << std::endl;
}

// Define the template member function
template <typename T>
template <typename U>
void MyClass<T>::func2(T val1, U val2) {
    std::cout << "MyClass::func2 called with value: " << val1 << " and " << val2 << std::endl;
}

template class MyClass<int>;
template void MyClass<int>::func2<float>(int, float);
```


### `main.cpp`
```c++
#include "MyClass.h"

int main() {
    MyClass<int> obj;
    obj.func1(1);
    obj.func2<float>(42, -2.5f);
    return 0;
}
```
# Inheritance with Template Class

## `Base.h`
```c++
// Template Base Class
template <typename T>
class Base {
protected:
    T value;

public:
    Base(T val); // Constructor declaration
    void printValue() const; // Member function declaration
};
```
## `Base.cpp`
```c++
template <typename T>
Base<T>::Base(T val) : value(val) {}

// Define the member function
template <typename T>
void Base<T>::printValue() const {
    std::cout << "Base value: " << value << std::endl;
}

// Explicit instantiation for T = int
template class Base<int>;
```

## `Derived.h`
```c++
#include "Base.h"

// Template Derived Class
template <typename T, typename U>
class Derived : public Base<T> {
private:
    U extraValue;

public:
    Derived(T val, U extra); // Constructor declaration
    void printExtraValue() const; // Member function declaration
    void printBothValues() const; // Member function declaration
};
```

## `Derived.cpp`
```c++
#include "Derived.h"

// Define the constructor
template <typename T, typename U>
Derived<T, U>::Derived(T val, U extra) : Base<T>(val), extraValue(extra) {}

// Define the member function to print the extra value
template <typename T, typename U>
void Derived<T, U>::printExtraValue() const {
    std::cout << "Derived extra value: " << extraValue << std::endl;
}

// Define the member function to print both values
template <typename T, typename U>
void Derived<T, U>::printBothValues() const {
    this->printValue(); // Call Base class member function
    std::cout << "Derived extra value: " << extraValue << std::endl;
}

// Explicit instantiation for T = int and U = double
template class Derived<int, double>;
```

## `main.cpp`
```c++
#include "Derived.h"

int main() {
    // Create an instance of the explicitly instantiated derived template class
    Derived<int, double> obj(10, 3.14);

    // Call functions from both Base and Derived
    obj.printValue();       // From Base class
    obj.printExtraValue();  // From Derived class
    obj.printBothValues();  // Combines Base and Derived outputs

    return 0;
}
```
# Instantiation of Virtual Function in Class Template
In a class template, non-virtual functions are only instantiated if they’re used – but virtual functions are instantiated every time when a class instances are created. 
# Common Compiling Error

```cpp=
#include <iostream>
  
template <typename T>
T sum(int a, int b)
{ 
   return a+b;
} 
  
template long  sum<long >(int a, int b); 
template int   sum<int  >(int a, int b); 
template short sum<short>(int a, int b); 
  
  
int main()
{ 
   long ans = sum(2,4);
   
   std::cout << ans << std::endl;
  
   return 0;
}
```

```
test.cpp: In function ‘int main()’:
test.cpp:16:22: error: no matching function for call to ‘sum(int, int)’
   16 |    long ans = sum(2,4);
      |                      ^
test.cpp:4:3: note: candidate: ‘template<class T> T sum(int, int)’
    4 | T sum(int a, int b)
      |   ^~~
test.cpp:4:3: note:   template argument deduction/substitution failed:
test.cpp:16:22: note:   couldn’t deduce template parameter ‘T’
   16 |    long ans = sum(2,4);
      |                      ^
```

This error occurs because C++ compiler is unable to select the type T based on the target function. To address this issue, we can call the function with an explicit type, e.g. calling `long ans = sum<long>(2,4)`.
{% endraw %}