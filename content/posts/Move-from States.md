---
title: "Move-from States"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

---
title: Move-from States
tags: [CPP]

---

# Required and Guaranteed States of Moved-From Objects
## Required States of Moved-From Objects
* We hve to ba able to **destroy** moved-from objects.
* We hve to ba able to **assign a new value** to moved-from objects.
* We hve to ba able to **copy/move/assign moved-from objects to other objects**.
## Guaranteed States of Moved-From Objects
* All moved-from objects are "valid but unspecified state".
* If (1) the object’s **invariants** are met, and (2) **all** operations on the object behave as specified for its type then the object is in specified state.
* For example:
    *  If an object `x` of type `std::vector<std::string>` is in a valid but unspecified state, `x.empty()` can be called unconditionally, and `x.front()` can be called only if `x.empty()` returns `false`.
    *  ```c++
       x.push_back(std::move(s));
       
       std::cout << s << '\n'; // OK
       std::cout << s.size() << '\n'; // OK
       std::cout << s[0] << '\n'; // ERROR
       std::cout << s.front() << '\n'; // ERROR
       s = "new value"; // OK
       ```
## Class Invariant
* Invariants are the guarantees that apply to all of the objects that can be created.
* Methods of the class should preserve the invariant.
* Class invariants are established during construction and constantly maintained between calls to public methods. Code within functions may break invariants as long as the invariants are restored before a public function ends.
* Defining class invariants can help programmers and testers to catch more bugs during software testing.
* Class invariants are inherited, that is, "the invariants of all the parents of a class apply to the class itself."
* Take `std::vector` as an example:
  | Invariant                                                  | Meaning                                            |
  | ---------------------------------------------------------- | -------------------------------------------------- |
  | `0 <= size() <= capacity()`                                | Logical and memory consistency.                    |
  | `data() != nullptr` or `size() == 0`                       | If non-empty, `data()` must point to valid memory. |
  | `elements are contiguous`                                  | Equivalent to an array of `T`.                     |
  | `begin() + size() == end()`                                | Iterator arithmetic consistency.                   |
  | `capacity()` never decreases unless you explicitly shrink. | `capacity()` only grows or resets.                 |
  | `data()` points to same block until reallocation.          | Stable storage invariant.                          |


# Destructible and Assignable

## Assignable and Destructible Moved-From Objects
In most of the classes, the generated special move member functions bring moved-from objects into a state where the assignment operator and destructor work just fine. However, provided each moved-from member is assignable and destructible, both an assignment and the destruction of the moved-from object as a whole should work well:
* The assignment will overwrite the unspecified state of the member by assigning the state from the corresponding source member.
* The destructor will destroy the member (that has the unspecified state). For example:
   ```c++
   class Customer {
   void foo() {
      std::string customer = "Rocky";
      name = std::move(customer);
      // both _name and _value are valid but unspecified
   } // destructor of Customer is expected to destory _name and _value too
   
   std::string name;
   std::vector<int> value;
   };
   ```


## Non-Destructible Moved-From Objects
Example:
```c++

#include <array>
#include <thread>

class Tasks {
private:
  std::array<std::thread,10> threads;  // array of threads for up to 10 tasks
  int numThreads{0};                   // current number of threads/tasks
public:
  Tasks() = default;

  // pass a new thread:
  template <typename T>
  void start(T op) {
    threads[numThreads] = std::thread{std::move(op)};
    ++numThreads;
  }
  //...

  // OOPS: enable default move semantics:
  Tasks(Tasks&&) = default;
  Tasks& operator=(Tasks&&) = default; 

  // at the end wait for all started threads:
  ~Tasks() {
    // numThreads and the number of active threads
    // in threads[] is inconsistent
    for (int i = 0; i < numThreads; ++i) {
      threads[i].join();
    }
  }
}; 
```

```c++
int main()
{
  try {
    Tasks ts;
    ts.start([]{
               std::this_thread::sleep_for(std::chrono::seconds{2});
               std::cout << "\nt1 done" << std::endl;
             });
    ts.start([]{
               std::cout << "\nt2 done" << std::endl;
             });

    // OOPS: move tasks:
    Tasks other{std::move(ts)};
  }
  catch (const std::exception& e) {
    std::cerr << "EXCEPTION: " << e.what() << std::endl;
  }
}
```
The move operations of containers move the elements, so that after the `std::move()`, ts no longer contains any thread objects that represent a running thread. Therefore, `numThreads` is just copied, which means that we create an inconsistent/invalid state. The destructor will finally loop over the first two elements calling `join()`, which throws an exception (which is a fatal error in a destructor).

# Dealing with Borken Invariant
* Unfortunately, moved-from objects can break the “valid but unspecified state” guarantee a lot easier than breaking the requirement to be destructible. We can accidentally bring objects into a state where we break their invariants.
* In principle, if the invariants of a class are broken by a (generated) move operation, you have the following options:
    * Fix the move operations to bring the moved-from objects into a state that does not break the invariants.
    * Disable move semantics.
    * Relax the invariants that define all possible moved-from states also as valid. In particular, this might mean that member functions and functions that use the objects have to be implemented differently to deal with the new possible states.
    * Document and provide a member function to check for the state of “broken invariants” so that users of the type do not use an object of this type after it has been marked with `std::move()` (or only use a limited set of operations). 

## Breaking Invariant Due to Moved Member
```c++
class Card {
public:
   Card(const std::string& v) : _value(v)
   {
      assertValidCard(_value);
   }
   std::string getValue() const {
      return _value;
   }
private:
   std::string  _value;
};
```
In this class, one of the expected invariat is that `_value` should always follow a specific pattern. For example, `_value = "queen-of-hearts"`. However, the `_value` in the moved_from object does not adhere to this pattern.

The options for fixing this class are as follow:
* Disable move semantics.
* Disable copying and moving at all.
* Fix the broken special move member functions.
    * However, what would be a valid fix (is always assigning a “default value” such as "ace-of-clubs" OK)? And how do you ensure that objects with the default value perform well without allocating memory?
* Internally allow the new state but disallow calling `getValue()` or other member functions.
* Extend the invariant by introducing a new state that a `Card` might have no value.
   ```c++
   void print(const Card& c) {
      std::string val{ c.getValue() };
      auto pos = val.find("-of-");
      
      // find position of substring
      If (pos != std::string::npos) {
         // check whether it exists
         std::cout << val.substr(0, pos) << ' ' << val.substr(pos+4) << '\n';
      } else {
         std::cout << "no value\n";
      }
   }
   ```
   
   
## Beaking Invariants Due to Moved Consistent Value Members
Two member values are expected to be consistent. For example:
```c++
class IntString {}
private:
   int val;
   std::string sval;
public:
   IntString(int i=0) : val{i}, sval{std::to_string(i)}
   { }
   
   oid dump() {
      std::cout << val << "/" << sval << "\n";
   }
;
```

## Beaking Invariants Due to Moved Point-Like Members

```c++
class SharedInt {
private:
   std::shared_ptr<int> sp;
public:
   explicit SharedInt(int val)
   : sp{std::make_shared<int>(val)} {}

   // Error: assumes there is always an int value
   std::string asString() const {
      return std::to_string(*sp);
   }
};
```

Resolutions:
* Fixing Broken Member Functions
* Disabling Move Semantics
* Implementing Move Semantics
   ```c++
   class SharedInt {
   private:
      std::shared_ptr<int> sp;
      
      // define moved-from value
      inline static std::shared_ptr<int> movedFromValue{std::make_shared<int>(0)};
   public:
      explicit SharedInt(int val)
      : sp{std::make_shared<int>(val)} {}
   
      // Error: assumes there is always an int value
      std::string asString() const {
         return std::to_string(*sp);
      }
      
      // Move semantics
      SharedInt(SharedInt&& rhs)
      : sp{std::move(rhs.sp)}{
         rhs.sp = movedFromValue;
      }
      
      SharedInt& operator=(SharedInt&& rhs) {
         if (this != &rhs) {
            sp = std::move(rhs.sp);
            rhs.sp = moveFromValue;
         }
         return *this
      }
   };
   ```