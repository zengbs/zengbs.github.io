---
title: "Tricky Details of Perfect Forwarding"
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: Tricky Details of Perfect Forwarding
tags: [CPP]

---

# Universal References and `const`
A universal reference is the only way we can bind a reference to objects of any value category and still preserve whether or not it is `const`. The only other reference that binds to all objects, `const&`, loses the information about both the constness of the original argument and its value category.


This means that if we want to avoid overloading but want to have different behavior for `const` and non-`const` arguments and support all value categories, we have to use universal references:
```c++
#include <iostream>
#include <string>

void iterate(std::string::iterator beg, std::string::iterator end)
{
   std::cout << "do something for non-const iterator\n";
}

void iterate(std::string::const_iterator beg, std::string::const_iterator end)
{
   std::cout << "do something for const iterator\n";
}

template<class T>
void process(T&& arg)
{
   iterate(arg.begin(), arg.end());
}


int main()
{
   std::string v{"v"};
   const std::string c{"c"};
   
   process(v);
   process(c);
   process(std::string{"t"});
   process(std::move(v));
   process(std::move(c));
}
```

# Universal References in Detail



| Input argument | `T`         | Type of `arg` |
|:--------------:| ----------- |:-------------:|
|     lvalue     | Type&       |     Type&     |
|     xvalue     | Type        |    Type&&     |
|    prvalue     | Type        |    Type&&     |
|  const lvalue  | const Type& |  const Type&  |
|  const xvalue  | const Type  | const Type&&  |


## Constness Dependent Code

```c++
template<class T>
void foo( T&& arg )
{
   if constexpr (std::is_const_v<std::remove_reference_t<T>>) {
      // passed argument is const
   }else{
      // passed argument is not const
   }
}
```

## Value Category Dependent Code

```c++
template<class T>
void foo(T&& arg)
{
   if constexpr(std::is_lvalue_reference_v<T>){
      // passed argument is lvalue
   }else{
      // passed argument is rvalue
   }

}
```

# Universal References of Specific Types
We want to constrain this function to only take strings (both const and non-const without losing this information), we cannot do that easily.


## Since C++20


### When the type must match exactly:
```c++
template<class T>
requires std::same_as<std::remove_cvref_t<T>, std::string>
void processString(T&& arg)
{
   // ...
}
```
* `std::same_as`:
A C++20 concept that checks whether two types are exactly the same.
* `std::remove_cvref_v`:
Removes both const/volatile qualifiers and reference from a type.
### When implicit conversion is allowed:
```c++
template<class T>
requires std::convertible_to<T, std::string>
void processString(T&& arg)
{
   // ...
}
```
* `std::convertible_to`:
Checks whether one type can be implicitly converted to another.
### When even explicit conversions is allowed:
```c++
template<class T>
requires std::constructible_from<std::string, T>
void processString(T&& arg)
{
   // ...
}
```
* `std::constructible_from`:
Checks whether a type can be constructed from a given set of argument types.

## Since C++11
The following code supports all types that are implicitly convertible to `std::string`:

```c++
template<typename T, typename = typename std::enable_if<std::is_convertible<T, std::string>::value>::type>
void processString(T&& args);
```

To restrict to type `std::string`, we need:

```c++
template<typename T, typename = typename std::enable_if<std::is_same<typename std::decay<T>::type,std::string>::value>::type>

void processString(T&& arg);
```

* `std::enable_if`:
Enables or disables template instantiations based on a compile-time boolean condition.
* `std::decay`:
Transforms a type into the form it would have if it were passed by value — that is, after applying the same conversions that occur when you pass an argument to a function by value.


# Universal or Ordinary Rvalue Reference?

## Rvalue References of Members of Generic Types
An rvalue reference to a member type of a template parameter is not a universal reference. For example:
```c++
#include <iostream>
#include <string>
#include <vector>

template<class T>
void foo(T& coll, typename T::value_type&& arg)
{
   coll.push_back(arg);
}

int main() {
   std::vector<std::string> v;
   std::string s{"Hi"};
   const std::string cs{"Hi"};

   foo(v, std::move(s));
   foo(v, std::string{"Hi"});
   foo(v, std::move(cs)); // Error
   foo(v, s); // Error
   foo(v, cs); // Error
}
```
Note that:
* `value_type` is defined in many STL, which represents the type of the elements they hold.
* Inside a template, any name that depends on a template parameter (like `T`) is called a dependent name. When you write something like `T::value_type`, the compiler cannot tell by syntax alone whether `value_type` refers to a type or a static member/function/enum/variable — because it depends on `T`.


## Rvalue References of Parameters in Class Template

An rvalue reference to a template parameter of a class template is not a universal reference. For example:
```c++
template<class T>
class C {
   T&& member; // member is not a univeral reference
   void foo(T&& arg); // arg is not universal reference
};
```


## Rvalue References of Parameters in Full Specializations

An rvalue reference to a parameter of a full specialization of a function template is not a universal reference. For example:

```c++
template<class T>
void foo(T&& arg); // arg is a universal reference


// Specialized template for only rvalue
template<>
void foo(std::string&& arg); // arg is not a universal reference
```

```c++
#include <iostream>
#include <string>

template<class T>
void foo(T&& arg)
{
   std::cout << "A\n";
}

// full specialization for only rvalue
template<>
void foo(std::string&& arg)
{
   std::cout << "B\n";
}

// full specialization for only const rvalue
template<>
void foo(const std::string&& arg)
{
   std::cout << "C\n";
}

template<>
void foo(std::string& arg)
{
   std::cout << "D\n";
}

int main() {

   std::string s;
   const std::string cs;

   foo(s); // D
   foo(cs); // A
   foo(std::move(s)); // B
   foo(std::move(cs)); // C
}
```

Note that you have to declare/define full specializations of member function templates outside the class definition:
```c++
#include <iostream>
#include <string>

template<class T>
class C {
public:
   template<class U>
   void foo(U&& arg) {
      std::cout << "A\n";
   }
   T member;
};

// explicit instantiation
template class C<int>;

// specialize function template in a class template (for only rvalue)
template<>
template<>
void C<int>::foo( std::string&& arg ) {
   std::cout << "B\n";
}

// specialize function template in a class template (for only lvalue)
template<>
template<>
void C<int>::foo( const std::string& arg ) {
   std::cout << "C\n";
}

int main() {

   C<int> c;
   std::string s;
   const std::string cs;
   
   c.foo(s); // A
   c.foo(cs); // C
   c.foo(std::move(s)); // B
   c.foo(std::move(cs)); // A

}
```

# How the Standard Specifies Perfect Forwarding


C++ standard `[temp.deduct.call]` specifies:
> If the parameter type is an rvalue reference to a cv-unqualified template parameter and the argument is an lvalue, the type “lvalue reference to T” is used in place of T for type deduction.

That means that: If (1) the type of the parameter `arg` is declared with `&&` and not declared with `const` or `volatile`, and (2) lvalue is passed, then `T` is deduced as `T&` instead. For example:

```c++
template<class T>
void foo(T&& arg) {
   // ...
}

std::string s;
const std::string cs;

foo(s);            // T is deduced as std::string&
foo(cs);           // T is deduced as const std::string&
foo(std::move(s)); // T is deduced as std::string&&
```

Also, `[dcl.ref]` indicates that
* `Type& &` becomes `Type&`
* `Type& &&` becomes `Type&`
* `Type&& &` becomes `Type&`
* `Type&& &&` becomes `Type&&`

That means:

```c++
template<class T>
void foo(T&& arg) {
   // ...
}

std::string s;
const std::string cs;

foo(s);            // arg has the type std::string&
foo(cs);           // arg has the type const std::string&
foo(std::move(s)); // arg has the type std::string&&
```

Now, consider
* `std::move()` defined by `static_cast<std::remove_reference_t<T>&&>(t)`. It removes any references and converts to the corresponding rvalue type.
* `std::forward()` only adds rvalue referenceness to the passed type parameter: `static_cast<T&&>(t)`. Here the reference collapsing rules apply again:
    * If `T` is deduced as an lvalue reference, `T&&` is still an lvalue reference. This implies that `arg` has no move semantics.
    * If `T` is deduced as an rvalue reference, `T&&` is still an rvalue reference. This effectively means that the value category of `arg` has changed from lvalue to xvalue.

Note that string literals are lvalues so that we deduce `T` and `arg` for them as follows:
```c++
// lvalue passed, so T and arg have type const char(&)[3]
foo("hi");

// xvalue passed, so T is deduced as const char[3]
// arg has type const char(&&)[3]
foo(std::move("hi")); 
 ```
Remember also that references to functions are always lvalues, Therefore, `T` is always deduced as an lvalue reference if we pass a reference to a function to a universal reference:
```c++
void func(int) {}

// lvalue passed to f(), so T and arg have type void(&)(int)
f(func);

// lvalue passed to f(), so T and arg have type void(&)(int)
f(std::move(func));
```


## Explicit Specification of Types for Universal References
In an explicit specification, the universal reference no longer acts as a universal reference.

```c++
#include <iostream>
#include <string>

template<class T>
void foo(T&& arg) { }

int main() {

   std::string s;
   const std::string cs;

   // arg type is std::string&&
   // foo<std::string>(s); // Error

   // arg type is std::string&
   foo<std::string&>(s); // Ok

   // arg type is std::string&&
   // foo<std::string&&>(s); // Error


   // arg type is std::string&&
   foo<std::string>(std::move(s)); // Ok

   // arg type is std::string&&
   foo<std::string&&>(std::string{}); // Ok

   // arg type is const std::string&
   foo<const std::string&>(s); // Ok
   foo<const std::string&>(cs); // Ok
   foo<const std::string&>(std::move(s)); // Ok
   foo<const std::string&>(std::string{}); // Ok
}
```

## Conflicting Template Parameter Deduction with Universal References
```c++
#include <iostream>
#include <string>
#include <vector>

template<class T>
void insert(std::vector<T>& vec, T&& elem) { 
   vec.push_back(std::forward<T>(elem));
}

int main() {
   std::string s;
   std::vector<std::string> coll;
   insert(coll, s); // Error
}
```
The problem is that both parameters can be used to deduce parameter `T` but the deduced types are not the same:
* Using the parameter `coll`, `T` it is deduced as `std::string`.
* However, according to the special rule for universal references, parameter `arg` forces to deduce `T` as `std::string&`.
Therefore, the compiler raises an ambiguity error.

The feasible fixes are:
1. Using the type trait `std::remove_reference_t<>`:
   ```c++
   #include <iostream>
   #include <string>
   #include <vector>
   
   
   template<class T>
   void insert(std::vector<std::remove_reference_t<T>>& vec, T&& elem) {
      vec.push_back(std::forward<T>(elem));
   }
   
   int main() {
      std::string s;
      std::vector<std::string> coll;
      insert(coll, s);
   }
   ```
2. We can also use two template parameters:
   ```c++
   #include <iostream>
   #include <string>
   #include <vector>
   
   template<class T1, class T2>
   void insert(std::vector<T1>& vec, T2&& elem) {
      vec.push_back(std::forward<T2>(elem));
   }
   
   int main() {
      std::string s;
      std::vector<std::string> coll;
      insert(coll, s); // Error
   }
   ```
   
   
## Pure Rvalue References of Generic Types
With the special rule for deducing template parameters of universal references (deducing the type as an lvalue reference when lvalues are passed), we can constrain generic  reference parameters to only bind to rvalues (C++20):

```c++
#include <iostream>
#include <string>

void foo(std::string&& s) { }

template<class T>
requires (!std::is_lvalue_reference_v<T>)
void callFoo(T&& arg) {
   foo(std::forward<T>(arg));
}

int main() {
   std::string s;
   //callFoo(s); // Error
   callFoo(std::string{});
}
```
{% endraw %}