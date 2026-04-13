---
date: 2026-04-13T15:32:36+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---


# Aggregate Extensions
* Traditional aggregate initialization (using list initialization):
  ```c++
  struct Data {
     std::string name;
     double value;
  };
  
  // list initalization
  Data x = {"test1", 6.778}; // since C++98
  Data x{"test1", 6.778}; // since C++11
  ```
* Aggregate extension uses the syntax of nested braces, which can be omitted if at least one value is passed:
  ```c++
  struct MoreData : Data {
     bool done;
  };
  
  // list initalization
  MoreData y{{"test1", 6.778}, false}; // since C++17
  MoreData y{"test1", 6.778, false}; // since C++17
  
  // default initialization
  MoreData z; // value/done are unspecified
  
  // value initialization
  MoreData u{}; // value/done have values 0/false
  ```
* Without this feature, we have to define a constructor for aggregate initializaton:
  ```c++
  struct Cpp14Data : Data {
     bool done;
     Cpp14Data (const std::string& s, double d, bool b)
     : {}
  };
  
  Cpp14Data y{"test1",6.778,false};
  ```


## Using Extended Aggregate Initialization
* One typical application of aggregate initialization is the ability to initialize members of a C-style structure
derived by a class to add additional data members or operations. For example:
   ```c++
   struct Data {
      const char* name;
      double value;
   };
   
   struct CppData : Data {
      bool critical;
      void print() const {
         std::cout << '[' << name << ',' << value << "]\n";
      }
   };
   
   CppData y{{"test1", 6.778}, false};
   y.print();
   ```
   Note that you can skip initial values. In that case, the elements are initialized from a default member initializer or they are copy-initialized from `{}`. For example:
   ```c++
   CppData x1{};         // zero-initialize all elements
   CppData x2{{"msg"}};  // same as {{"msg",0.0},false}
   CppData x3{{}, true}; // same as {{nullptr,0.0},true}
   CppData x4;           // values of fundamental types are unspecified
   ```
* You can also derive aggregates from non-aggregate classes. For example:
   ```c++
   struct MyString : std::string {
      void print() const {
         if (empty){
            std::cout << "<undefined>\n";
         }else{
            std::cout << c_str() << '\n';
         }
      }
   };
   
   MyString s{{"test1"}}; // OK
   MyString s{"test1"};   // OK
   ```
* You can even derive aggregates from multiple base classes and/or aggregates:
  ```c++
  template<class T>
  struct D : std::string, std::complex<T>
  {
     std::string data;
  };
  
  D<float> s{{"hello"}, {4.5,6.7}, "world"};         // OK since C++17
  D<float> t{"hello", {4.5, 6.7}, "world"};          // OK since C++17
  std::cout << s.data;                               // outputs: ”world”
  std::cout << static_cast<std::string>(s);          // outputs: ”hello”
  std::cout << static_cast<std::complex<float>>(s);  // outputs: (4.5,6.7)
  ```
## Definition of Aggregates
To summarize, since C++17, an aggregate is defined as
* Either an array
* Or a class type (class, struct, or union) with:
  – No user-declared or explicit constructor
  – No constructor inherited by a using declaration
  – No private or protected non-static data members
  – No virtual functions
  – No virtual, private, or protected base classes

However, there are additional constraints for aggregates to be able to initialize them:
* No private or protected base class members
* No private or protected constructors


## Backward Incompatibilities
```c++
struct Derived;

struct Base {
friend struct Derived;
private:
  Base() {
  }
};

struct Derived : Base {
};

int main()
{
  Derived d1{};    // ERROR since C++17
  Derived d2;      // still OK (but might not initialize)
}
```
### Before C++17
`Derived` was not an aggregate since it is derived from `Base`. Thus, `Derived d1{};` called the implicitly defined default constructor of `Derived`, which by default called the default constructor of the base class `Base`. Although the default constructor of the base class is private, calling it via the default constructor of the derived class was valid because the derived class was defined to be a friend class.
### Since C++17
`Derived` in this example is an aggregate, with no implicit default constructor at all (the constructor is not inherited by a using declaration). Therefore, the initialization is an aggregate initialization, which means that the expression `std::is_aggregate<Derived>::value` yields true. However, you cannot use brace initialization because the base class has a private constructor (see the previous section). Whether the base class is a friend is irrelevant.


```flow
cond0=>condition: brace ini?
cond=>condition: Is it aggregate?
op=>operation: ctor ini
cond2=>condition: private or protected base class members?
private or protected constructors?
op2=>operation: aggregate ini
err=>end: Error
e=>end: End
cond0(yes)->cond
cond0(no)->op
cond(yes)->cond2
cond(no)->op
cond2(yes)->err
cond2(no)->op2
```

# Comarison between Initialization
| Initialization typs        | Syntax form                     | Zero-initializes built-ins               | Calls constructor            | Allows narrowing | Supports aggregates | Typical pitfalls                     |
| -------------------------- | ------------------------------- | ---------------------------------------- | ---------------------------- | ---------------- | ------------------- | ------------------------------------ |
| **Default initialization** | `T x;`                          | ❌ (indeterminate for fundamental types) | ✅ <br>(default constructor)             | N/A              | ❌                  | Uninitialized built-ins              |
| **Value initialization**   | `T x{};`<br>`T x = T();`        | ✅                                       | ✅<br>(default constructor)                           | ❌               | ✅                  | Sometimes confused with default init |
| **Direct initialization**  | `T x(args);`                    | ❌                                       | ✅(constructor)                           | ✅               | ❌                  | Most-vexing parse                    |
| **Copy initialization**<br>Constructor-base only    | `T x = expr;`                   | ❌                                       | ✅ (copy/move/elided) | ✅               | ❌                  | Extra conversions allowed            |
| **List initialization**    | `T x{args};`<br>`T x = {args};` | Depends on args                          | ✅ (constructor)               | ❌               | ✅                  | `std::initializer_list` preference   |


{% endraw %}