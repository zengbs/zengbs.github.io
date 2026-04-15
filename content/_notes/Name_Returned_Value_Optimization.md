---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

# Example 1
First see [How does a function return local object internally?](/oPiyQizIR5u70ybjT583Dw) for details. 
```c++
#include<iostream>

class Person {
public:

Person(std::string n) : name(n) {}

Person(const Person& rhs)
   : name(rhs.name)
{
   std::cout << "Copy ctor\n";
}

Person(Person&& rhs) noexcept
   : name(rhs.name)
{
   std::cout << "Move ctor\n";
}

Person& operator=( const Person& rhs )
{
   std::cout << "Copy assign\n";
   if ( this != &rhs ) {
      name = rhs.name;
   }
   return *this;
}

Person& operator=( Person&& rhs) noexcept
{
   std::cout << "Move assign\n";
   if ( this != &rhs ) {
      name = rhs.name;
   }
   return *this;
}

private:
   std::string name;
};

Person foo1 (){
   Person obj("YL");
   return std::move(obj);
}

Person foo2 (){
   Person obj("PH");
   return obj;
}

Person foo3 (){
   const Person obj("PH");
   return obj;
}

Person foo4 (){
   Person obj("PH");
   const Person& obj2 = obj;
   return obj2;
}

Person foo5 (){
   Person obj("PH");
   Person& obj2 = obj;
   return obj2;
}

const Person foo6 (){
   const Person obj("PH");
   return obj;
}

int main() {

   Person person("YLPH");

   std::cout << "Calls foo1():\n";
   person = foo1();

   std::cout << "\nCalls foo2():\n";
   person = foo2();

   std::cout << "\nCalls foo3():\n";
   person = foo3();

   std::cout << "\nCalls foo4():\n";
   person = foo4();

   std::cout << "\nCalls foo5():\n";
   person = foo5();

   std::cout << "\nCalls foo6():\n";
   person = foo6();


   std::cout << "\nCalls foo2():\n";
   Person obj2 = foo2();
}
```


|     | Copy elision ON | Copy elision OFF |
|:--- |:---------------:|:----------------:|
<img src="https://hackmd.io/_uploads/S15JrbKhge.png" width="30%" alt="圖片"><br>`Person person("YL");`<br>`person = foo1();` |   Move ctor<br>Move assign      |  Move ctor <br>Move assign           |
| <img src="https://hackmd.io/_uploads/Hkp7HWFhel.png" width="30%" alt="圖片"><br>`Person person("YL");`<br>`person = foo2();`         | (NRVO is applicable)<br>Move assign | Move ctor<br>Move assign |
| <img src="https://hackmd.io/_uploads/HJRVHWFhex.png" width="30%" alt="圖片"><br>```Person person("YL");```<br>```person = foo3();``` | (NRVO is applicable)<br>Move assign | Copy ctor<br>Move assign |
| <img src="https://hackmd.io/_uploads/H1TiSbt2xg.png" width="30%" alt="圖片"><br>```Person person("YL");```<br>```person = foo4();``` | Copy ctor<br>Move assign            | Copy ctor<br>Move assign |
| <img src="https://hackmd.io/_uploads/H17jpPq2gg.png" width="30%" alt="圖片"><br>`Person obj("YL");`<br>`obj = foo5();`               | Copy ctor<br>Move assign | Copy ctor<br>Move assign |
|   <img src="https://hackmd.io/_uploads/BywHRP5heg.png" width="30%" alt="圖片"><br>`Person obj("YL");`<br>`obj = foo6();`|               (NRVO is applicable)<br>Copy assign                      |                        Copy ctor<br>Copy assign  |






1. If the returned object is:
    * const: calls copy ctor
    * reference: calls copy ctor
    * rvalue: calls copy ctor
    * lvalue: calls move ctor
2. If NRVO is applicable:
    * Single named local variable returned directly. I.e., the expression's value category should be lvalue.
    * Function's return type should exactly matches the returned variable’s type, regardless of the cv-mismatch.
    * The returned expression is a automatic (not static) object.
    * The object is returned unmodified (not through a pointer/reference).
3. If the returned type of the function is:
    * const: copy assign
    * otherwise: move assign


# Example 2
```c++
#include <iostream>

struct A {

   A(){ std::cout << "A() "; }
   A(const A& a) { std::cout << "A(const&) ";  }
   A(A&& a) noexcept { std::cout << "A(A&&) "; }
   ~A() { std::cout << "~A() "; }
};


A f1(){ return {}; }
void f2(A a){  }
A f3(A a){ return a; }
A f4(A a){ return {a};}
A f5(A a){ return std::move(a);}

int main(){
   std::cout <<   "Case 1\n";
   {
      f1();
   }
   std::cout <<   "\n\nCase 2\n";
   {
      A a = f1();
   }
   std::cout << "\n\nCase 3\n";
   {
      f2({});
   }
   std::cout << "\n\nCase 4\n";
   {
      f3({});
   }
   std::cout << "\n\nCase 5\n";
   {
      A a = f3({});
   }
   std::cout << "\n\nCase 6\n";
   {
      f4({});
   }
   std::cout << "\n\nCase 7\n";
   {
      A b = f4({});
   }
   std::cout << "\n\nCase 8\n";
   {
      A c = f5({});
   }

   std::cout <<"\n";
}
```
* If the arguments of `A{...}` are glvalues, the only way to create and pass a prvalue to caller is to immediately construct a new temporary object using either copy or move constructor.
* If the arguments of `A{...}` are prvalues, the prvalue `A{...}` does not need to be materialized when used to initialize the function's return value. The construction of `A{...}` may be deferred and performed directly in the caller's storage under guaranteed copy elision.
* Note that `A{a}`, `A{}` and `A{createA()}` are prvalue.


# Without copy elision
## Case 1
```c++
A f1(){ return {}; }
f1();
```
The arg of `{}` is a prvalue, so the materialization performs immediately in the return statement.
1. At `return {}`: use default ctor to construct an object (say, `obj`).
2. At the end of `A f1(){...}`: use destructor to remove `obj`.
## Case 2
```c++
A f1(){ return {}; }
A a = f1();
```
The arg of `{}` is a prvalue, so the materialization performs immediately in the return statement.
1. At `return {}`: use default ctor to construct an object (say, `obj`).
2. At `return {}`: use move ctor to construct `a` from `obj`.
3. At the end of `f1(){}`: use destructor to remove `obj`.
4. At the end of `A a = f1()`: use desstructor to remove `a`.
## Case 3
```c++
void f2(A a){  }
f2({});
```
1. At `f2({})`: use default ctor to construct `a`.
2. At the end of `void f2(A a){}`: use destructor to remove `a`.
## Case 4
```c++
A f3(A a){ return a; }
f3({});
```
1. At `f3({})`: use default ctor to construct `a`;
2. At `return a`: use move ctor to construct the return object.
3. At `return a`: use destructor to remove the return object
4. At `return a`: use destrucor to remove `a`.

## Case 5
```c++
A f3(A a){ return a; }
A a1 = f3({});
```
1. At `A a = f3({})`: use default ctor to construct `a`.
2. At `return a`: use move ctor to construct an object (say `obj`) from `a`.
3. At `return a`: use move ctor to construct `a1` from `obj`.
4. At the end of `f3(A a){...}`: use destructor to remove `obj`.
4. At the end of `f3(A a){...}`: use destructor to remove `a`.
5. At the end of `A a = f3({})`: use destructor to remove `a1`.
## Case 6
```c++
A f4(A a){ return {a}; }
f4({});
```
1. At `A f4(A a){...}`: use default ctor to construct `a`.
2. At `return {a}`: use copy ctor to construct an object (say `obj`) from `{a}`.
4. At the end of `A f4(A a){...}`: use destructor to remove `obj`.
4. At the end of `A f4(A a){...}`: use destructor to remove `a`.
## Case 7
```c++
A f4(A a){ return {a}; }
A b = f4({});
```
1. At `A f4(A a){...}`: use default ctor to construct `a`.
2. At `return {a}`: use copy ctor to construct an object (say `obj`) from `{a}`.
2. At `return {a}`: use move ctor to construct `b` from `obj`.
4. At the end of `A f4(A a){...}`: use destructor to remove `obj`.
4. At the end of `A f4(A a){...}`: use destructor to remove `a`.
4. At the end of `A b = f4({})`: use destructor to remove `b`.
## Case 8
```c++
A f5(A a){ return std::move(a); }
 A c = f5({});
```
1. At `A f4(A a){...}`: use default ctor to construct `a`.
2. At `return std::move(a)`: use move ctor to construct an object (say `obj`) from `std::move(a)`.
2. At `return std::move(a)`: use move ctor to construct `c` from `obj`.
4. At the end of `A f5(A a){...}`: use destructor to remove `obj`.
4. At the end of `A f5(A a){...}`: use destructor to remove `a`.
4. At the end of `A c = f5({})`: use destructor to remove `c`.

# With copy elision
## Case 1
```c++
A f1(){ return {}; }
f1();
```
The arg of `{}` is a prvalue, so the materialization would be defered and performed in the caller's storage. However, there is no an obejct in the caller (`main`) to receive the return object. So the materialization performs immediately in the return statement.
1. At `return {}`: use default ctor to construct an object (say, `obj`).
2. At the end of `A f1(){...}`: use destructor to remove `obj`.

## Case 2
```c++
A f1(){ return {}; }
A a = f1();
```
The arg of `{}` is a prvalue, so the materialization would be defered and performed in the caller's storage. Fortunately, there is an obejct in the caller (`main`) to receive the return object. So the materialization performs at the assignment operator.
1. At `return {}`: use default ctor to construct `a` from `{}`.
2. At the end of `A a = f1()`: use desstructor to remove `a`.


## Case 3
```c++
void f2(A a){  }
f2({});
```
1. At `f2({})`: use default ctor to construct `a`.
2. At the end of `void f2(A a){}`: use destructor to remove `a`.

## Case 4
```c++
A f3(A a){ return a; }
f3({});
```
1. At `f3({})`: use default ctor to construct `a`;
2. At `return a`: use move ctor to construct the return object.
3. At `return a`: use destructor to remove the return object
4. At `return a`: use destrucor to remove `a`.

## Case 5
```c++
A f3(A a){ return a; }
A a1 = f3({});
```
1. At `A a = f3({})`: use default ctor to construct `a`.
2. At `return a`: use move ctor to construct `a1` from `a`.
4. At the end of `f3(A a){...}`: use destructor to remove `a`.
5. At the end of `A a1 = f3({})`: use destructor to remove `a1`.
## Case 6
```c++
A f4(A a){ return {a}; }
f4({});
```
The arg of `{}` is an lrvalue, so the materialization must performe in the return statement. 
1. At `A f4(A a){...}`: use default ctor to construct `a`.
2. At `return {a}`: use copy ctor to construct an object (say `obj`) from `{a}`.
4. At the end of `A f4(A a){...}`: use destructor to remove `obj`.
4. At the end of `A f4(A a){...}`: use destructor to remove `a`.
## Case 7
```c++
A f4(A a){ return {a}; }
A b = f4({});
```
1. At `A f4(A a){...}`: use default ctor to construct `a`.
2. At `return {a}`: use copy ctor to construct `b` from `{a}`.
4. At the end of `A f4(A a){...}`: use destructor to remove `a`.
4. At the end of `A b = f4({})`: use destructor to remove `b`.
## Case 8
```c++
A f5(A a){ return std::move(a); }
 A c = f5({});
```
1. At `A f4(A a){...}`: use default ctor to construct `a`.
2. At `return std::move(a)`: use move ctor to construct an `c` from `std::move(a)`.
4. At the end of `A f5(A a){...}`: use destructor to remove `a`.
4. At the end of `A c = f5({})`: use destructor to remove `c`.
{% endraw %}