---
title: "[[nodiscard]], [[maybe_unused]], [[fallthrough]] attributes"
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: '[[nodiscard]], [[maybe_unused]], [[fallthrough]] attributes'
tags: [CPP]

---

# Attribute `[[nodiscard]]`
* The new attribute `[[nodiscard]]` can be used to encourage warnings by the compiler if a return value of a function is not used.
## Use cases:

### Memory leaks
Functions that allocate resources that have to be released by another function call should be marked with `[[nodiscard]]`. A typical example would be a function to allocate memory, such as `malloc()` or the member function `allocate()` of allocators.

### Unexpected or non-intuitive behavior
A good example of a function changing its behavior non-intuitively when not using the return value is `std::async()` (introduced with C\++11). `std::async()` starts a functionality asynchronously in the background and returns a handle that can be used to wait for the end of the started functionality (and get access to any return value or exception). However, when the return value is not used the call becomes a synchronous call because the destructor of the unused return value is called immediately waiting for the end of the started functionality. Therefore, not using the return value silently contradicts the whole purpose of calling `std::async()`. Compilers can warn about this when `std::async()` is marked with `[[nodiscard]]`.
### Unnecessary overhead
Another example is the member function `empty()`, which checks whether an object (container/string) has no elements. Programmers pretty often call this function to “empty” the container (remove all elements): `cont.empty();`.

This incorrect application of `empty()` can often be detected because it does not use the return value. Therefore, marking the member function accordingly:
```c++
class MyContainer {
public:
   [[nodiscard]] bool empty() const noexcept;
};
```
helps to detect such an logical error. If for whatever reason you do not want to use a return value marked with `[[nodiscard]]` you can cast the return value to void:
```
(void)coll.empty(); // disable [[nodiscard]] 
warning
```


## Notes
* Note that attributes in function declarations are not inherited if the functions are overwritten:
   ```c++
   struct B {
      [[nodiscard]] int* foo();
   };
   
   
   struct D : B {
      int* foo();
   };
   
   
   B b;
   b.foo(); // warning
   (void)b.foo(); // no warning
   
   D d;
   d.foo(); // no warning
   ```
   Therefore, you have mark the derived member function with `[[nodiscard]]` again (unless there is a reason that not using the return value makes sense in the derived class).
* You can place an attribute that applies to a function in front of all declaration specifiers or after the function name:
   ```c++
   class C{
      [[nodiscard]] friend bool operator==(const C&, const C&); // OK
      friend bool operator!=[[nodiscard]](const C&, const C&); // OK
      friend [[nodiscard]] bool foo(const C&, const C&); // Error
      friend bool [[nodiscard]] bar[[nodiscard]](const C&, const C&); // Error
   };
   ```
# Attribute `[[maybe_unused]]`
* The new attribute `[[maybe_unused]]` can be used to avoid warnings by the compiler for not using a name or entity.
* The attribute may be applied to the declaration of a class, a type definition with `typedef` or `using`, a variable, a non-static data member, a function, an enumeration type, or an enumerator (enumeration value).
* One application is to name a parameter without (necessarily) using it:
   ```c++
   void foo(int val, [[maybe_unused]] std::string msg)
   {
   #ifdef DEBUG
      log(msg);
   #endif
   }
   ```
* Another example would be to have a member without using it:
   ```c++
   class MyStruct {
      char c;
      int i;
      [[maybe_unused]] char makeLargerSize[100];
   };
   ```
* You cannot counter `[[nodiscard]]` with `[[maybe_unused]]` directly:
  ```c++
  [[nodiscard]] void* foo();
  int main()
  {
     foo();
     [[maybe_unused]] foo();
     [[maybe_unused]] auto x = foo();
  }
  ```
# Attribute `[[fallthrough]]`
The new attribute `[[fallthrough]]` can be used to avoid warnings by the compiler for not having a `break` statement after a sequence of one or more case labels inside a switch statement.
For example:
```c++
void commentPlace(int place)
{
   switch (place) {
   case 1:
      std::cout << "very ";
      [[fallthrough]];
   case 2:
      std::cout << "well\n";
      break;
   default:
      std::cout << "OK\n";
      break;
   }
}
```
Here, passing the place 1 will print:
`very well`, using a statement of case 1 and case 2.
Note that the attribute has to be used in an empty statement. It must therefore end with a semicolon. Using the attribute as the last statement in a switch statement is not allowed.
{% endraw %}