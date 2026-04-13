---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---


Examples of move-only types in the C++ standard library are:
* IOStreams
* Threads
* Unique pointers

# Declaring and Using Move-Only Types
## Declaring Move-Only Types

```c++
class MoveOnly {
public:
   MoveOnly(MoveOnly&&) noexcept;
   MoveOnly& operator=(MoveOnly) noexcept;
   
   // delete copy ctor and assignment
   MoveOnly(const MoveOnly&) = delete;
   MoveOnly& operator=(const MoveOnly&) = delete;

};
```
By rule, it would be enough to declare the moving special member function. However, explicitly marking the copying special member function with `=delete` makes the intention more clear.


## Using Move-Only Types

With a declaration like the one above, you can create and move but not copy objects. For example:
```c++
std::vector<MoveOnly> coll;

coll.push_back(MoveOnly{}); // OK

MoveOnly mo;
coll.push_back(mo); // ERROR
coll.push_back(std::move(mo)); // OK
```


To move the value of a move-only element out of the container, simply use std::move() for a reference to the element. For example:
```c++
// move assign first element (still there with moved-from state)
mo = std::move(coll[0]);
```
However, remember that after this call, the element is still in the container with a moved-from state.

Moving out all elements is also possible in loops:
```c++
for (auto& elem : coll) {            // note: non-const reference
   coll2.push_back(std::move(elem)); // move element to coll2
}
```
Again: the elements are still in the container with their moved-from state.

For move-only types, a couple of operations that are usually valid are not possible:
* You cannot use `std::initializer_lists` because they are usually passed by value, which requires copying of the elements:
  ```c++
  std::vector<MoveOnly> coll{ MoveOnly{}, ... }; // ERROR
  ```
* You can only iterate by reference over all move-only elements of a container:
   ```c++
   std::vector<MoveOnly> coll;
   
   // const lvalue reference binds to lvalue
   for (const auto& : coll) { // OK
      ...
   }
   
   // Lvalue reference binds to lvalue
   for (auto& : coll) { // OK.
      ...
   }
   
   // Can't copy move-only type
   for (auto : coll) { // Error
      ...
   }
   ```

## Passing Move-Only Objects as Arguments
Option 1:
```c++
void sink(MoveOnly arg);

sink(MoveOnly{}); // OK

MoveOnly mo;
sink(mo); // Error
sink(std::move(mo)); // OK, moves mo to arg
```
Option 2:
```c++
void sink(MoveOnly&& arg);

sink(MoveOnly{}); // OK

MoveOnly mo;
sink(mo); // Error
sink(std::move(mo)); // OK, might move mo to something inside sink()
```

If it is important for you to give up ownership (because you want to ensure that the file is closed, the thread has stopped, or the associated resource was released), ensure this directly after the call with a corresponding statement. For example:
```c++
MoveOnly mo;
foo(std::move(mo));  // might move ownership
// ensure mo’s resource is longer acquired/owned/open/running:
mo.close();   // or mo.reset() or mo.release() or so
```
Move-only objects usually have such a functions but the names differ (e.g., in the C++ standard library, it is called `close()` for streams, `join()` for threads, or `reset()` for unique pointers). These functions usually bring the objects into a default constructed state.

## Returning Move-Only Objects by Value

If you return a local object that way, move semantics is automatically used:
```c++
MoveOnly source()
{
   MoveOnly mo;
   ...
   return mo;  // moves mo to the caller
}
MoveOnly m{source()}; // takes ownership of the associated value/resource
 ```

## Moved-From States of Move-Only Objects

Typically, the check is positive—you ask whether the object still has its resource, not whether it was moved from. Examples include:

* `if (s.is_open())` — for a file stream `s`, indicating whether a file is still open.
* `if (up)` — for a `std::unique_ptr up`, which converts to true if it still owns a pointer.
* `if (t.joinable())` — for a `std::thread t`, meaning it still represents an active thread of execution.
* `if (f.valid())` — for a `std::future f`, indicating whether it still refers to a shared state.
{% endraw %}