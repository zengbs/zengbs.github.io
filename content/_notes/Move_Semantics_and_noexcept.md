---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

# Move Constructors without `noexcept`
```c++
#include <string>
#include <iostream>

class Person {
  private:
    std::string name;
  public:
    Person(const char* n)
     : name{n} {
    }

    std::string getName() const {
      return name;
    }

    // print out when we copy or move:
    Person(const Person& p)
     : name{p.name} {
        std::cout << "COPY " << name << '\n';
    }
    Person(Person&& p)
     : name{std::move(p.name)} {
        std::cout << "MOVE " << name << '\n';
    }
    //...
};

int main()
{
   std::vector<Person> coll{ "Wolfgang Amadeus Mozart",
                             "Johann Sebastian Bach",
                             "Ludwig van Beethoven" };
                             
   std::cout << "capacity: " << coll.capacity() << '\n';
   
   coll.push_back("Pjotr Iljitsch Tschaikowski");
}
```

The output of the program is as follows:
```
COPY Wolfgang Amadeus Mozart
COPY Johann Sebastian Bach
COPY Ludwig van Beethoven
capacity: 3
MOVE Pjotr Iljitsch Tschaikowski
COPY Wolfgang Amadeus Mozart
COPY Johann Sebastian Bach
COPY Ludwig van Beethoven
```
The following diagrams demonstrate how does `push_back()` work internally:
* Step 1:
<img src="https://hackmd.io/_uploads/S1SHoWLCgl.png" width="50%">
* Step 2:
<img src="https://hackmd.io/_uploads/SylzLj-IAex.png" width="50%">
* Step 3:
<img src="https://hackmd.io/_uploads/S1SwoWLAgg.png" width="50%">

The reason that vector reallocation does not use move semantics is the strong exception handling guarantee we give for `push_back()`: When an exception is thrown in the middle of the reallocation of the vector the C++ standard library guarantees to roll back the vector to its previous state. Please see [STL container with noexcept](/9vytxRpLQGWMiwLdUs0ntA) for more details.


# Move Constructors with `noexcept`

When we guarantee that the move constructor never throw:
```c++
Person(Person&& p) noexcept
     : name{std::move(p.name)} {
        std::cout << "MOVE " << name << '\n';
    }
```
The output will be:
```
COPY Wolfgang Amadeus Mozart
COPY Johann Sebastian Bach
COPY Ludwig van Beethoven
capacity: 3
MOVE Pjotr Iljitsch Tschaikowski
MOVE Wolfgang Amadeus Mozart
MOVE Johann Sebastian Bach
MOVE Ludwig van Beethoven
```
* Step 1:
<img src="https://hackmd.io/_uploads/Hke9bG8Rgg.png" width="50%">
* Step 2:
<img src="https://hackmd.io/_uploads/Hyi5WfI0el.png" width="50%">
* Step 3:
<img src="https://hackmd.io/_uploads/S16ibGLAll.png" width="50%">

Please see [emplace_back vs. push_back](/GRwsNRl_QiS4GoyYEC-TCA) for more details.

# Details of `noexcept` Declarations
* See [noexcept specifier](/h3xGM3n7QIiRzjUibx7_0Q).
* The move constructor usually does not output anything; therefore, in general when members do not throw, we can give the guarantee not to throw for the move constructor as a whole.
* If you implement a move constructor, you should declare whether and when it guarantees not to throw.
* If you do not have to implement the move constructor, you do not have to specify anything at all.


## `noexcept` for Copying and Moving Special Member Functions
* `noexcept` condition is generated for generated special member functions.
* `noexcept` condition is not generated for user-implement special member functions.
* Before C\+\+20, if the generated and specified `noexcept` conditions contradict, the defined function was deleted. Since C++20, the specified `noexcept` condition takes precedence over the generated one.
   ```c++
   class C
   {
      public:
       // guarantees not to throw (OK since C++20)
      C(const C&) noexcept = default;
      
      // specifies that it might throw (OK since C++20)
      C(C&&) noexcept(false) = default;
   };
   ```
   
## `noexcept` for Destructors
By rule, destructors always guarantee not to throw by default. This applies to both generated and implemented destructors.
For example:
```c++
class B
{
private:
   std::string s;
public:
   ~B() {
       // automatically always declared as ~B() noexcept
   }
};
```
With `noexcept(false)`, you can declare them without this guarantee, but that usually never makes any sense because several guarantees of the C++ standard library are based on the fact that destructors never throw.

# `noexcept` Declarations in Class Hierarchies
* Following the rules of the C++ standard, we should declare it not to throw when all base classes and all member types do not throw on a move construction. The general pattern would be as follows:
   ```c++
   class Ancestor {
   ...
   };
   
   class Descendant : public Ancestor {
      MemType member;
      Descendant(Descendant&&)
      noexcept(std::is_nothrow_move_constructible_v<Ancestor> &&
               std::is_nothrow_move_constructible_v<MemType>);
   };
   ```
* The move assignment operator might use the same pattern but note that the move assignment operator should be [deleted](https://hackmd.io/OIrF4_RqSC-_urbcqGdHDQ#Avoid-Defining-Assignment-Opeators-in-an-Abstract-Base-Class) in polymorphic types anyway, which means that there is usually no need to implement them in derived classes.
* Note that the type trait `std::is_nothrow_move_constructible<>` always yields false because it also checks whether you can create an object of this type with the move constructor, which is not possible for abstract types.
* The solution is to implement a non-abstract wrapper:
  ```c++
  #include <iostream>
  #include <vector>
  #include <type_traits>
  
  template<typename Base>
  struct Wrapper : Base {
     using Base::Base;
     // implement all possibly wrapped pure virtual functions:
     // --> Make Wrapper is not an abstract class
     void print() const {}
  };
  
  template<typename T>
  static constexpr inline bool is_nothrow_movable_v
  = std::is_nothrow_move_constructible_v<Wrapper<T>>;
  
  
  class Base {
  private:
     std::string id;
  public:
     Base() = default;
     // pure virtual function (forces abstract base class)
     virtual void print() const = 0;
     virtual ~Base() = default;
  
  protected:
     // protected copy and move semantics (also forces abstract base class):
     Base(const Base&) = default;
     Base(Base&&) = default;
     // disable assignment operator (due to the problem of slicing):
     Base& operator= (Base&&) = delete;
     Base& operator= (const Base&) = delete;
  };
  
  class Drv : public Base {
  public:
     void print() const override {
        std::cout << "Drv::print()\n";
     }
  
     Drv() = default;
     Drv(const Drv& rhs)
     {
        if (this == &rhs) return;
        std::cout << "COPY\n";
     }
  
     Drv(Drv&& rhs) noexcept(is_nothrow_movable_v<Base>)
     //Drv(Drv&& rhs) noexcept(std::is_nothrow_move_constructible_v<Base>)
     {
        if (this == &rhs) return;
        std::cout << "MOVE\n";
  
     }
  
  };
  
  int main()
  {
     std::cout << std::boolalpha;
     std::cout << "std::is_nothrow_move_constructible_v<Base>: "
     << std::is_nothrow_move_constructible_v<Base> << '\n';
  
     std::cout << "is_nothrow_movable_v<Base>                : "
     << is_nothrow_movable_v<Base> << '\n';
  
     std::vector<Drv> v;
     v.reserve(2);
  
     v.push_back(Drv{});
     v.push_back(Drv{});
     v.push_back(Drv{});
  }
  ```
  * Using `is_no_throw_movable_v` in `Drv`'s move constructor yields:
    ```
    MOVE
    MOVE
    MOVE
    MOVE
    MOVE
    ```
  * Using `std::is_nothrow_move_constructible_v` in `Drv`'s move constructor yields:
     ```
     MOVE
     MOVE
     MOVE
     COPY
     COPY
     ```
{% endraw %}