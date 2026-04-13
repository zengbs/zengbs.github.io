---
title: "Template compilation model"
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

---
title: Template compilation model
tags: [CPP]

---

# Inclusion Model (implicit instantiations)
```c++
// my_template.h
#include <iostream>

// Template function defined in the header file
template <typename T>
void printValue(const T& value) {
    std::cout << "Value: " << value << std::endl;
}
```
```c++
#include "my_template.h"

void foo() {
    printValue(42);
    printValue(3.632);
    printValue("=====");
}
```

```c++
// main.cpp
#include "my_template.h"
void foo();

int main() {
    printValue(42);
    printValue(3.14);
    printValue("Hello, World!");
    foo();
    return 0;
}
```
![image](https://hackmd.io/_uploads/HJo_ZDa-xx.png)

Drawbacks:
1. The body of a function template describes implementation details that our users may want to ignore or that we may want to hide from our users. 
2. If the definitions of our function templates are large, the level of detail present in the header file may be overwhelming.
3. Compiling the same function template definitions across multiple files can unnecessarily add to the compile-time of our programs.

# Exclusion Model (explicit instantiations)
1. The definition for the function template must be provided in the file in which the explicit instantiation declaration appears.
2. An explicit instantiation declaration for a given function template instantiation must appear only once in a program.
```c++
// my_template.h
#include <iostream>

// Generic template declaration
template <typename T>
void printValue(const T& value);

// Explicit specialize template declaration
template <>
void printValue(const char& value);
```

```c++
// my_template.cpp
#include "my_template.h"

// Generic template function definition
template <typename T>
void printValue(const T& value) {
    std::cout << "Value: " << value << std::endl;
}

// Specialized template function definition
template <>
void printValue(const char& value) {
    std::cout << "Value: " << value << std::endl;
}

// The explicit instantiation must be preceded by the template definition
template void printValue<int>(const int&);
template void printValue<double>(const double&);
```

```c++
// main.cpp
#include "my_template.h"

int main() {
    printValue('a');
    printValue(42);
    printValue(3.14);
    return 0;
}
```
In g++, use the flag `-fno-implicit-templates` to supress the implicit instantiation.

Upside:
1. The compiler instantiate template exactly once.
2. Reduces code bloat.
3. Improves compile time.


Downside:
1. No inline expansion.
2. Extensibility is lost: only predefined types allowed.
3. Modularity suffers: adding a new type requires touching the .cpp file.

![image](https://hackmd.io/_uploads/Byv7zwT-el.png)


# Exclusion Model (extern template) C++11
An `extern` keyword which makes the compiler not compile a template function. You should use this if and only if you know it is used in the same binary somewhere else.

```c++
// main.cpp
#include "my_template.h"

// Ask compiler not to instantiate for types double, int, and char
// since compiler has done (or will do) in my_template.cpp
extern template void printValue<double>(const double&);
extern template void printValue<int>(const int&);
extern template void printValue<char>(const char&);

void another();

int main() {
    another();
    printValue('b'); // compiler instantiate
    printValue(4);
    printValue(3.14);
    return 0;
}
```
```c++
// my_template.h
#include <iostream>


// Generic template function definition
template <typename T>
void printValue(const T& value) {
    std::cout << "Value: " << value << std::endl;
}
```
```c++
// my_template.cpp
#include "my_template.h"

// Specialized template function definition
template <>
void printValue(const char& value) {
    std::cout << "Value: " << value << std::endl;
}

void another(){
   printValue('a');
   printValue(1);
   printValue(1.2);
}
```

![image](https://hackmd.io/_uploads/rJzQ7wTWgl.png)



T: Symbol is defined in this object file (.text section – code).
W: Weak symbol — definition that can be overridden by a strong one.
U: Undefined symbol — used but not defined in this object file.
t: Local (non-global) symbol in .text.


[Explicit instantiations vs. extern instantiations](https://daniele77.github.io/general/2019/05/03/explicit-instantiation-reusability-modularity.html)
[using extern template (C++11) to avoid instantiation](https://stackoverflow.com/questions/8130602/using-extern-template-c11-to-avoid-instantiation)




|         Model          | Extensible | Object file size | inlineable | Compilation speed |
|:----------------------:| ---------- | ---------------- | ---------- |:-----------------:|
|       Inclusion        |     Yes       | Largest          | Yes        |      slowest      |
| Explicit instantiation | No         |        Smallest          |        No    |       Fastest            |
|    Extern template     |            |               Small   |       Yes*     |            Fast       |
|     C++20 Modules      |            |                  |            |                   |

* Yes*: inlineable for Extern Template: Inlining works for types not declared with extern template.
* Extensibility means:
"Can the code be extended to handle new types or use cases not foreseen originally?"