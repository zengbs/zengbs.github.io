---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---





# Copy Constructor
The copy constructor is automatically generated when all of the following apply:
 * No move constructor is user-declared.
 * No move assignment operator is user-declared.
    



# Move Constructor
The move constructor is automatically generated when all of the following apply:
 * No copy constructor is user-declared
 * No copy assignment operator is user-declared
 * No move assignment operator is user-declared
 * No destructor is user-declared

### Quiz
What it the output?
```c++
#include <iostream>
#include <type_traits>

class GeoObj {
public:
    GeoObj& operator=(const GeoObj&) { return *this; };
};

int main() {
    std::cout << std::boolalpha;
    std::cout << std::is_move_constructible<GeoObj>::value << "\n";
}
```
You may think "false" because of no move constructor based on the standard; however the answer is "true". Because types without a move constructor, but with a copy constructor that accepts const T& arguments, satisfy std::is_move_constructible. See [here](https://en.cppreference.com/w/cpp/types/is_move_constructible.html) for more details.

# Copy Assignment
The copy assignment operator is automatically generated when all of the following apply:7
 * No move constructor is user-declared
 * No move assignment operator is user-declared


# Move Assignment
The move assignment operator is automatically generated when all of the following apply:
* No copy constructor is user-declared
* No move constructor is user-declared
* No copy assignment operator is user-declared
* No destructor is user-declared

# Destructor
Destructors are nothing special with move semantics except that their declaration disables the automatic generation of move operations.

# Default Constructor
The default constructor (the “not-so-special” special member function) is still automatically generated if no other constructor is declared. That is, the declaration of a move constructor disables the generation of a default constructor.


# Class Hierarchies
In C++11, if any base class or member of a class cannot be copied or moved (because its special member function is `= delete`, `private`, or otherwise inaccessible), then the compiler automatically defines the corresponding implicitly-declared special member of the derived class as deleted.

# Cases Study
## Declaring constructors supresses the implicit declaration of default constructor

## Declaring copying suppresses the implicit declaration of moving.
When declaring a copying special member function (or the destructor), we have the automatic generation of the moving special member functions disabled.

Because the fallback mechanism works, copying and moving a Person compiles but the move is performed as a copy:

```c++
class Person {
public:
   // copy constructor/assignment declared:
   Person(const Person&) = default;
   Person& operator=(const Person&) = default;
   // NO move constructor/assignment declared
};

std::vector<Person> coll;
Person p{"Tina", "Fox"};

coll.push_back(p);             // OK, copies p
coll.push_back(std::move(p));  // OK, copies p
```

## Declaring moving deleted Copying
If you have user-declared move semantics, you have disabled copy semantics. The copying special member functions are deleted.

In other words, if the move constructor or the move assignment operator is explicitly declared (implemented, generated with `=default`, or disabled with `=delete`), you have disabled to call the copy constructor and the copy assignment operator by declaring them with `=delete`.

Assume the following declaration of a class Person:
```c++
class Person {
public:
// NO copy constructor declared
// move constructor/assignment declared:
Person(Person&&) = default;
Person& operator=(Person&&) = default;
};
```
In this case, we have a move-only type. A `Person` can be moved but not copied:
```c++
std::vector<Person> coll;
Person p{"Tina", "Fox"};
coll.push_back(p);                      // ERROR: copying disabled
coll.push_back(std::move(p));           // OK, moves p                               
coll.push_back(Person{"Ben", "Cook"});  // OK, moves temporary person into coll
```
The consequence: the attempt to copy an object will no longer compile.


### Disabling Both Copying and Moving
Deleting the copying special member functions is enough. (Never `=delete` the special move member functions).

![hinnant_table](https://hackmd.io/_uploads/rJS1ELiaxl.png)

* “Not declared” means: the function doesn’t exist.
* “Deleted” means: it exists, but you cannot call it.
{% endraw %}