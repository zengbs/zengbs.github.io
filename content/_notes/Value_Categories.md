---
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---


**Types and "value categories" are different things. Don't mix them up!**

# `l-value` (locator value)
* An expression that is just the name of a variable, function, or data member (except a plain value member of an rvalue)
* An expression that is just a string literal (e.g., `"hello"`)
   ```c++
   T a = 3; // a is l-value with type T
   T& ra = a; // ra is l-value with type T&
   T&& rr = 3; // rr is l-value with type T&&
   std::string s = "Hello"; // "Hello" is l-value
   ```
* The return value of a function if it is declared to return an lvalue reference (return type `Type&`)
   ```c++
   int& foo(int &i){
      return i;
   }
   int arg = 0;
   foo(arg) = 3;
   ```
  For string literal, the compiler internally creates an array of type `const char[N]`, where `N` is the length of the string plus 1 for the null terminator (`'\0'`).
* Any reference to a function, even when marked with `std::move()`:
   ```c++
   void foo(int);
   
   // r is an lvalue
   void (&r)(int) = foo;  // bind a reference to the function
   r();                   // calls foo
   
   // rr is an lvalue
   void (&&rr)(int) = foo;  // bind an rvalue reference to the function
   rr();                    // calls foo
   
   // ar is lvalue of type void(&)(int)
   auto& ar = std::move(f);
   ```
* The result of the built-in unary `*` operator (i.e., what dereferencing a raw pointer yields)
   ```c++
   int i = 1;
   int* pi = &i;
   
   *pi = 2;
   ```
   
# `pr-value` (pure rvalue)
* A pr-value has no a corresponding object in memory but can be bound to r-value reference.
   ```c++
   int a = 3; // 3 is pr-value
   ```
* The return type of a function if it is declared to return by value:
   ```c++
   class Foo {
   ...
   };
   
   void Bar(Foo);
   
   Bar(Foo{}); // Foo {} is pr-value
   ```
* The result of the built-in unary & operator is a prvalue:
   ```c++
   int i = 1;
   int* ri = &i;
   ```
   `&x` gives you a temporary pointer value — the address of `x`.
* A lambda expression.
   
# `x-value` (expiring value)
* The result of marking an object (not reference to function) with `std::move()`:
   ```c++
   std::string A = "Hello";
   std::string&& B = std::move(A);
   ```
* A cast to an rvalue reference of an object type (not a function type)
   ```c++
   std::string A = "Hello";
   std::string&& B = static_cast<std::string&&>(A);
   ```
* The returned value of a function if it is declared to return an rvalue reference (return type `Type&&`)
   ```c++
   std::string&& foo() {
      std::string i = "aaapppppp";
      return i;
   }
   ```
* A non-static value member of an rvalue (see below)
   ```c++
   std::move(obj).member // rvalue
   ```

# Materialization (prvalue-to-xvalue conversion)

* Materialization exists both before and after C++17.
The change is:
    * Before C++17: prvalues always implied a temporary object, i.e., materialize prvalue into a temporary object immediately.
    * After C++17: prvalues are only materialized when necessary
* For example, prior to C++17, we cannot compile the code below:
   ```c++=
   #include <iostream>
   
   class C {
   public:
      C() = default;
      C(const C&) = delete;
      C(C&&) = delete;
   };
   
   C createC() { return C{}; }
   void takeC(C val) {}
   
   int main(){
      C c = createC();  // Ok since C++17 (error prior to C++17)
      takeC(createC()); // Ok since C++17 (error prior to C++17)
   }
   ```
   ![image](https://hackmd.io/_uploads/ByOasyP8Wl.png =60%x)
   However, all C++ versions can compile this code provided that copy and move constructors are enabled:
   ```c++=
   #include <iostream>
   
   class C {
   public:
      C()  { std::cout<< "DEFAULT CTOR\n"; };
      C(const C&) { std::cout<< "COPY CTOR\n"; }
      C(C&&) { std::cout<< "MOVE CTOR\n"; }
      C& operator=(const C&) { std::cout << "COPY ASSIGN\n"; return *this; }
      C& operator=(C&&) { std::cout << "MOVE ASSIGN\n"; return *this; }
   };
   
   C createC() {
      return C{};
   } // In C++17, no temporary object is created at this point
   
   void takeC(C val) {}
   
   int main(){
   
      std::cout << "1st step:\n";
      C c = createC();
   
      std::cout << "\n2nd step:\n";
      createC();
   
      std::cout << "\n3rd step:\n";
      takeC(createC());
   
   }
   ```
   * `g++ main.cc -std=c++11 -fno-elide-constructors  && ./a.out` gives:
      ```
      1st step:
      DEFAULT CTOR
      MOVE CTOR
      MOVE CTOR
      
      2nd step:
      DEFAULT CTOR
      MOVE CTOR
      
      3rd step:
      DEFAULT CTOR
      MOVE CTOR
      MOVE CTOR
      ```
      So conceptually, `creatC()` is effectively like the snippet below:
      ```c++
      C creatC() {
         C temp;                  // default ctor
         C ret = std::move(temp); // move ctor
         return ret;
      }
      ```
   * Both `g++ main.cc -std=c++11  && ./a.out` and `g++ main.cc -std=c++17  && ./a.out` give:
      ```
      1st step:
      DEFAULT CTOR
      
      2nd step:
      DEFAULT CTOR
      
      3rd step:
      DEFAULT CTOR
      ```
* More details inside `createC()`:
   ```c++
   C creatC() { return C{}; }
   foo(const C& c);
   
   C c = createC();
   foo(createC());
   ```
   * `creatC()`:
       * Before C\++17:
          1. Created and initialized (materialize) a temporary object (xvalue candidate) with prvalue. (used default ctor)
          2. Converted the temporary to xvalue. (Step 1 and Step 2 are considered as prvalue-to-xvalue conversion)
          3. Construct a new object from the xvalue. (used move ctor)
       * After C\++17:
           1. Return the prvalue(`C{}`) to the caller directly.
   * `C c = createC()`:
       * Before C\++17:
          1. Construct an lvalue (`c`) with the return object with move ctor.
       * After C\++17:
          1. Construct an lvalue (`c`) with prvalue.
   * `takeC(createC())`:
       * Before C\++17:
          1. Construct a temporary object (`const C& c`) from the return object with move ctor.
       * After C\++17:
          1. Construct a temporary object (`const C& c`) with prvalue (materialize arises here).




See [C++ on Friday: A prvalue is not a temporary](https://blog.knatten.org/2025/10/31/a-prvalue-is-not-a-temporary/) for more details.

# Special Rules for Value Categories

## Value Category of Functions
* C++ standard states that all expressions that are references to functions are lvalues:
   ```c++
   void f(int) {}
   class A {};
   
   int main(){
      void (*fptr)(int) = f;
      void (&fr)(int) = f;
      void (&&frr)(int) = f;
    
      A a;
   
      // cannot bind non-const lvalue reference of type ‘A&’ to an rvalue of type 'A'
      auto& am = std::move(a);
   
      // Okay
      const auto& am = std::move(a);
      
      // Okay
      // -->because a function marked with std::move() is still an lvalue.
      auto& ar = std::move(f);
   }
   ```
* In contrast to types of objects, we can bind a non-const lvalue reference to a function marked with `std::move()` because a function marked with `std::move()` is still an lvalue.


## Value Category of Data Members
| Member kind                          | Accessed from lvalue object | Accessed from rvalue object |
| ------------------------------------ | --------------------------- | --------------------------- |
| **non-static, non-reference member** | **lvalue**                  | **xvalue**                  |
| **static or reference member**       | **lvalue**                  | **lvalue**                  |

* This rule reflects that reference or static members are not really part of an object.
* `std::move()` for non-static, non-reference member:
   ```c++
   std::vector<std::string> coll;
   std::pair<std::string, std::string&&> sp;
   
   coll.push_back(std::move(sp.first)); // move
   coll.push_back(std::move(sp.second)); // move
   coll.push_back(std::move(sp).first); // move
   coll.push_back(std::move(sp).second); // move
   ```
* `std::move()` for static and reference member
   ```c++
   struct S {
      static std::string statString;
      std::string& refString;
   }
   
   S obj;
   
   coll.push_back(std::move(obj.statString)); // move
   coll.push_back(std::move(obj.refString)); // move
   coll.push_back(std::move(obj).statString); // copy
   coll.push_back(std::move(obj).refString); // copy
   ```

In generic code, you might not know whether members are static or references. Therefore, using the approach to mark the object with `std::move()` is less dangerous.


# Imapact of Value Categories When Binding References

## Overload Resolution with Rvalue References



![image](https://hackmd.io/_uploads/SkiUpWR0el.png =80%x)



|              | lvalue reference | const lvalue reference | rvalue reference | const rvalue reference |
| ------------ | ---------------- | ---------------------- | ---------------- | ---------------------- |
| lvalue       | 1                |   2                     |     n/a             |  n/a                      |
| const lvalue |       n/a           |     1                   |       n/a           |              n/a          |
| prvalue      |      n/a            |    3                    |    1              |   2                     |
| xvalue       |   n/a               |    3                    |        1          |   2                     |
|  const xvalue            |    n/a              |      2                  |     n/a             |     1                   |




* A non-const lvalue reference takes only non-const lvalues.
* An rvalue reference takes only non-const rvalues.
* A const lvalue reference can take everything and serves as the fallback mechanism in case other overloads are not provided.
* If we pass an rvalue (temporary object or object marked with `std::move()`) to a function and there is no specific implementation for move semantics (declared by taking an rvalue reference), the usual copy semantics is used inside `f()`, taking the argument by `const&`.
## Overloading by Reference and Value
* There is no specific priority between call-by-value and call-by-reference. If you have a function declared to take an argument by value (which can take any argument of any value category), any matching declaration taking the argument by reference creates an ambiguity.
* Therefore, you should usually only take an argument either by value or by reference (with as many reference overloads as you think are useful) but never both.
# When Lvalues become Rvalues
We can only bind rvalue reference to rvalue. For example:
```c++
void rvFun(std::string&&);
std::string s{...};
rvFun(s); // Error
rvFun(std::move(s)); // Okay
```
However, note that sometimes, binding rvalue reference to lvalue seemingly works. For example:
```c++
rvFun("Hello"); // Okay. Why?
rvFun(std::string{"Hello"})
```
There is a hidden operation involved, because the type of the argument (array of five constant characters) does not match the type of the parameter. We have an implicit type conversion, performed by the string constructor, which creates a temporary object that does not have a name.


# When Rvalues become Lvalues
```c++
void rvFun(std::string&& str);
std::string s{...};

rvFun(s); // Error
rvFun(std::move(s)); // Okay
rvFun(std::string{"Hello"});
```
when we use the parameter `str` inside the function, we are dealing with an object that has a name. This means that we use `str` as an lvalue. We can do only what we are allowed to do with an lvalue:
```c++
void rvFun(std::string&& str) {
   rvFun(str); // Error
}
```
We have to mark `str` with `std::move()` inside the function again:
```c++
void rvFun(std::string&& str) {
   rvFun(std::move(str)); // Okay
}
```
# Checking Value Categories with `decltype`

## Using `decltype` to Check the Type of Names (Entities)


* If the variable is declared as `T` entity, then `decltype(entity)` yields `T`.
* If the variable is declared as `T&` entity, then `decltype(entity)` yields `T&`.
* If the variable is declared as `T&&` entity, then `decltype(entity)` yields `T&&`.

For example:
If we declare `T entity;` then
|  | lvalue | prvalue |  xvalue   |
| -------- | ------ | ------- | --- |
|  `std::is_same<decltype(entity),T>`    | true  |   true  |   false  |
|  `std::is_same<decltype(entity),T&>`    |false  |  false   |  false   |
|  `std::is_same<decltype(entity),T&&>`    | false |  false   |  true   |


|                                                     | lvalue | prvalue | xvalue |
| --------------------------------------------------- | ------ | ------- | ------ |
| `std::is_reference<decltype(entity)>::value`        | false   | false   | true   |
| `std::is_lvalue_reference<decltype(entity)>::value` | false   | false   | false  |
| `std::is_rvalue_reference<decltype(entity)>::value` | false  | false   | true   |


Note that `decltype(entity)` cannot be used to check expresion's value category. For example:
```c++
std::string s = "Hi";
std::string& rs = s;
```
`decltype(s)` and `decltype(rs)` yield `std::string` and `std::string&`, respectively; however, both `s` and `rs` are lvalue. This is why we need `decltype((expr))` to distinguish value category further.

## Using `decltype` to Check the Value Category of an Expression

* If the expression is lvalue, then `decltype((expr))` yields `T&`;
* If the expression is prvalue, then `decltype((expr))` yields `T`. 
* If the expression is xvalue, then `decltype((expr))` yields `T&&`;


|  | lvalue | prvalue |  xvalue   |
| -------- | ------ | ------- | --- |
|  `std::is_same<decltype((expr)),T>`    | false  | true    |   false  |
|  `std::is_same<decltype((expr)),T&>`    | true |  false   |  false   |
|  `std::is_same<decltype((expr)),T&&>`    |  false | false    |  true   |





|                                                     | lvalue | prvalue | xvalue |
| --------------------------------------------------- | ------ | ------- | ------ |
| `std::is_reference<decltype((expr))>::value`        | true   | false   | true   |
| `std::is_lvalue_reference<decltype((expr))>::value` | true   | false   | false  |
| `std::is_rvalue_reference<decltype((expr))>::value` | false  | false   | true   |

`decltype((expr))` is not meant to describe the type of the value itself — it’s a mechanism for mapping an expression’s value category into a corresponding reference-qualified type.

The type it yields is useful only insofar as it encodes the value category.

## Summary
| You want to know...                            | Use...                                      | Result                         |
| ---------------------------------------------- | ------------------------------------------- | ------------------------------ |
| Entity’s declared type                         | `decltype(name)` (no parentheses)           | e.g. `int&`                    |
| Expression’s mapped type (with value category) | `decltype((expr))`                          | e.g. `int&`, `int&&`, or `int` |
| Expression type (drop references)         | `std::remove_reference_t<decltype((expr))>` | e.g. `int`                     |
| Value category (lvalue/xvalue/prvalue)         | See how `decltype((expr))` behaves          | maps to `&` / `&&` / none      |


# Example

```c++
int global = 100;

int& getRef() {
    return global;   // returns a reference → an lvalue
}

int main() {
    getRef() = 5;   //  OK! Modifies 'global'
}
```



![image](https://hackmd.io/_uploads/S16LQ0Qcxe.png)

```c++=
#include <iostream>

struct T {
    T(int t) : _t(t) { std::cout << "T constructed\n"; }
    T(const T& rhs) { _t = rhs._t; std::cout << "T copied\n"; }
    ~T() { std::cout << "T destroyed\n"; }
    void show() { std::cout << "t = " << _t << "\n"; }
    int _t;
};

struct M {
    M(int m): _m(m) { std::cout << "M constructed\n"; }
    M(const M& rhs) { _m = rhs._m; std::cout << "M copied\n"; }
    M(M&&) { std::cout << "M moved\n"; }
    ~M() { std::cout << "M destroyed\n"; }
    void show() { std::cout << "m = " << _m << "\n"; }
    int _m;
};

template<class U>
U prvalue(int u) {
    return U(u);
}

template<class U>
U& lvalue(int u) {
    U* ptr = new U(u);
    std::cout << "ptr = " << ptr << "\n";
    return *ptr;
}

template<class U>
U&& xvalue(int u) {
    U* ptr = new U(u);
    std::cout << "ptr = " << ptr << "\n";
    return std::move(*ptr);
}

int main() {

    // Test movable object

    std::cout << "################ returns prvalue ###############\n";
    std::cout << "=== M ===\n";
    {
        M obj = prvalue<M>(1);
        obj._m = 2;
        obj.show();
        std::cout << "Inside block\n";
    }
    std::cout << "\n=== const M& binding ===\n";
    {
        const M& obj = prvalue<M>(1);
        std::cout << "Inside block\n";
    }

    std::cout << "\n=== M&& binding ===\n";
    {
        M&& obj = prvalue<M>(1);
        std::cout << "Inside block\n";
    }

    std::cout << "\n=== const M&& binding ===\n";
    {
        const M&& obj = prvalue<M>(1);
        std::cout << "Inside block\n";
    }


    std::cout << "\n################ returns lvalue ###############\n";
    std::cout << "=== M ===\n";
    {
        M obj = lvalue<M>(1);
        std::cout << "obj = " << &obj << "\n";
        std::cout << "Inside block \n";
    }
    std::cout << "\n=== M& binding ===\n";
    {
        M& obj = lvalue<M>(1);
        std::cout << "obj = " << &obj << "\n";
        delete &obj;
        std::cout << "Inside block\n";
    }
    std::cout << "\n=== const M& binding ===\n";
    {
        const M& obj = lvalue<M>(1);
        std::cout << "obj = " << &obj << "\n";
        delete &obj;
        std::cout << "Inside block\n";
    }

    std::cout << "\n################ returns xvalue ###############\n";
    std::cout << "=== M ===\n";
    {
        M obj = xvalue<M>(1);
        std::cout << "obj = " << &obj << "\n";
        std::cout << "Inside block\n";
    }
    std::cout << "\n=== const M& binding ===\n";
    {
        const M& obj = xvalue<M>(1);
        std::cout << "obj = " << &obj << "\n";
        delete &obj;
        std::cout << "Inside block\n";
    }
    std::cout << "\n=== M&& binding ===\n";
    {
        M&& obj = xvalue<M>(1);
        std::cout << "obj = " << &obj << "\n";
        delete &obj;
        std::cout << "Inside block\n";
    }
    std::cout << "\n=== const M&& binding ===\n";
    {
        const M&& obj = xvalue<M>(1);
        std::cout << "obj = " << &obj << "\n";
        delete &obj;
        std::cout << "Inside block\n";
    }

    // Test non-movable object

    std::cout << "################ returns prvalue ###############\n";
    std::cout << "=== T ===\n";
    {
        T obj = prvalue<T>(1);
        std::cout << "Inside block\n";
    }
    std::cout << "\n=== const T& binding ===\n";
    {
        const T& obj = prvalue<T>(1);
        std::cout << "Inside block\n";
    }

    std::cout << "\n=== T&& binding ===\n";
    {
        T&& obj = prvalue<T>(1);
        std::cout << "Inside block\n";
    }

    std::cout << "\n=== const T&& binding ===\n";
    {
        const T&& obj = prvalue<T>(1);
        std::cout << "Inside block\n";
    }


    std::cout << "\n################ returns lvalue ###############\n";
    std::cout << "=== T ===\n";
    {
        T obj = lvalue<T>(1);
        std::cout << "obj = " << &obj << "\n";
        std::cout << "Inside block \n";
    }
    std::cout << "\n=== T& binding ===\n";
    {
        T& obj = lvalue<T>(1);
        std::cout << "obj = " << &obj << "\n";
        delete &obj;
        std::cout << "Inside block\n";
    }
    std::cout << "\n=== const T& binding ===\n";
    {
        const T& obj = lvalue<T>(1);
        std::cout << "obj = " << &obj << "\n";
        delete &obj;
        std::cout << "Inside block\n";
    }

    std::cout << "\n################ returns xvalue ###############\n";
    std::cout << "=== T ===\n";
    {
        T obj = xvalue<T>(1);
        std::cout << "obj = " << &obj << "\n";
        std::cout << "Inside block\n";
    }
    std::cout << "\n=== const T& binding ===\n";
    {
        const T& obj = xvalue<T>(1);
        std::cout << "obj = " << &obj << "\n";
        delete &obj;
        std::cout << "Inside block\n";
    }
    std::cout << "\n=== T&& binding ===\n";
    {
        T&& obj = xvalue<T>(1);
        std::cout << "obj = " << &obj << "\n";
        delete &obj;
        std::cout << "Inside block\n";
    }
    std::cout << "\n=== const T&& binding ===\n";
    {
        const T&& obj = xvalue<T>(1);
        std::cout << "obj = " << &obj << "\n";
        delete &obj;
        std::cout << "Inside block\n";
    }

    return 0;
}
```
{% endraw %}