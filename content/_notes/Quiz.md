---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

# Reference
https://github.com/Mooophy/Cpp-Primer/tree/master
### 1. Determine the type of each of the following literals.
```c++
(a) 'a', L'a', "a", L"a"
(b) 10, 10u, 10L, 10uL, 012, 0xC
(c) 3.14, 3.14f, 3.14L
(d) 10, 10u, 10., 10e-2
// (a): character literal, wide character literal, string literal, string wide character literal.
// (b): decimal, unsigned decimal, long decimal, unsigned long decimal, octal, hexadecimal.
// (c): double, float, long double.
// (d): decimal, unsigned decimal, double, double.
```

### 2. What is the result?
```c++
unsigned int a = 10;
int b = 20;
cout << a-b << endl;

//Ans: 4294967286
```
### 3. What is the result?
```c++
int a = 010, b = 01;
std::cout << a - b << std::endl;

//Ans: 7
```

### 4. What are the initial values?
```c++
std::string global_str;
int global_int;
int main()
{
    int local_int;
    std::string local_str;
}
```

### 5. Explain whether each of the following is a declaration or a definition:
```c++
(a) extern int ix = 1024;
(b) int iy;
(c) extern int iz;
//(a): definition. (b): definition. (c): declaration.
```
### 6. Which of the following definitions, if any, are invalid? Why?
```c++
    (a) int ival = 1.01;
    (b) int &rval1 = 1.01;
    (c) int &rval2 = ival;
    (d) int &rval3;
// (a): valid.
// (b): invalid. initializer must be an object.
// (c): valid.
// (d): invalid. a reference must be initialized.
```
### 7. Is it legal?
```c++
int a = 0;
int *p = a;
```
### 8. Why is the initialization of p legal but that of lp illegal?
```c++
int i = 42;
void *p = &i;
long *lp = &i;
```
Inherited from C, void* is a special pointer that may point to any type, hence the second line is legal. For type safety, C++ forbids implicit conversions like long *lp = &i;, thus such code is illegal.
### 9. Determine the types and values of each of the following variables.
```c++
    (a) int* ip, i, &r = i;
    (b) int i, *ip = 0;
    (c) int* ip, ip2;
```
(a): ip is a pointer to int, i is an int, r is a reference to int i.
(b): ip is a valid, null pointer, and i is an int.
\(c\): ip is a pointer to int, and ip2 is an int.
### 10. Which of the following initializations are legal?
```c++
const int& r = 0;
int& r = 0;
```
### 11.  Identify any that are illegal.
```c++
int i, *const cp;       // illegal, cp must initialize.
int *p1, *const p2;     // illegal, p2 must initialize.
const int ic, &r = ic;  // illegal, ic must initialize.
const int *const p3;    // illegal, p3 must initialize.
const int *p;           // legal. a pointer to const int.
```
### 12. Uing the variables in the previous exercise, which of the following assignments are legal? 
```c++
i = ic;     // legal.
p1 = p3;    // illegal. p3 is a const pointer to const int.
p1 = &ic;   // illegal. ic is a const int.
p3 = &ic;   // illegal. p3 is a const pointer.
p2 = p1;    // illegal. p2 is a const pointer.
ic = *p3;   // illegal. ic is a const int.
```

### 13. Check if illegal
```c++
const int v2 = 0; int v1 = v2;
int *p1 = &v1, &r1 = v1;
const int *p2 = &v2, *const p3 = &i, &r2 = v2;

r1 = v2; // legal, top-level const in v2 is ignored.
p1 = p2; // illegal, p2 has a low-level const but p1 doesn't.
p2 = p1; // legal, we can convert int* to const int*.
p1 = p3; // illegal, p3 has a low-level const but p1 doesn't.
p2 = p3; // legal, p2 has the same low-level const qualification as p3.
```
### 14. Check if illegal
```c++
int i = 0, &r = i;
auto a = r;
const int ci = i, &cr = ci;
auto b = ci;
auto c = cr;
auto d = &i;
auto &g = ci;

a=42; // set 42 to int a.
b=42; // set 42 to int b.
c=42; // set 42 to int c.
d=42; // ERROR, d is an int *. correct: *d = 42;
e=42; // ERROR, e is an const int *. correct: e = &c;
g=42; // ERROR, g is a const int& that is bound to ci.
```
### 15. Check types
```c++
int a = 3, b = 4;
decltype(a) c = a;
decltype((b)) d = a;
++c;
++d;
// c is an int, d is a reference of a. all their value are 4.
```
```c++
int a = 3, b = 4;
decltype(a) c = a;
decltype(a = b) d = a;
// c is an int, d is a reference of int. the value: a=3, b=4, c=3, d=3
```

### 16. What are promotion/conversion performed?
```c++
int ia = 3, ib = 2;
double dc = ia / ib;
double dd = static_cast<double>(ia) / ib;
double de = ia / static_cast<double>(ib);
// dc: integer division (truncate result toward zero), and convert the result to double
// dd: promote ib to double first, then perform floating-point division
// de: promote ia to double first, then perform floating-point division
```

### 17. What is the result?
```c++
unsigned ua = 10, ub = 23;
cout << ua - ub << endl;
```

### 18. What's the result?
```c++
#include <iostream>
#include <string>
#include <string_view>
#include <typeinfo>


class Base
{
   public:
      virtual void Set(int mem){
         m_mem = mem;
      };

   private:
      int m_mem;

};

class Derived : public Base
{
   public:
      void Set(int mem){
         m_a = 2*mem;
      };
   private:
      int m_a;
};

int main(){

   Base* b = new Derived();

   std::cout << typeid(b).name() << std::endl;
   std::cout << typeid(*b).name() << std::endl;

   delete b;

   return 0;
}
```

```c++
class Base {};                 
class Derived : public Base {};                                                                                                          
                               
int main(){                    
                               
   Base* b = new Derived();       
                               
   std::cout << typeid(b).name() << std::endl;
   std::cout << typeid(*b).name() << std::endl;
                               
   delete b;                   
                               
   return 0;                   
}
```

# Does `dynamic_cast` success?

`vtable` only stores the information between the base and derived classes in the inheritance hierarchy. `dynamic_cast` can only upcast/downcast to the class stored in the `vtable`.

```c++
#include <iostream>
#include <typeinfo>

using namespace std;

class A {
public:
	virtual ~A() {}
};

class B : public A {
public:
	virtual ~B() {}
};

class C : public B {
public:
	virtual ~C() {}
};

class D : public B, public A {
public:
	virtual ~D() {}
};


int main(int argc, char const *argv[])
{

   B* pb1 = new C;   
   A* pa1 = dynamic_cast<A*>(pb1); // upcasting, succeed
   if (pa1) cout << "succedd" << endl;
   else cout << "fail" << endl;
   
   A *pa2 = new C;
   B *pb2 = dynamic_cast< B* >(pa2); // downcasting, succeed
   if (pb2) cout << "succeed!" << endl;
   else cout << "fail!" << endl;
   
   B* pb3 = new B;
   C *pc3 = dynamic_cast< C* >(pb3); // downcasting, fail
   if (pc3) cout << "succeed!" << endl;
   else cout << "fail!" << endl;
   
   B* pb4 = new B;
   A *pc4 = dynamic_cast< A* >(pb4); // upcasting, succeed
   if (pc4) cout << "succeed!" << endl;
   else cout << "fail!" << endl;
   
   B* pb5 = new C;
   C *pc5 = dynamic_cast< C* >(pb5); // downcasting, succeed
   if (pc5) cout << "succeed!" << endl;
   else cout << "fail!" << endl;
   
   
   A* pa6 = new B;
   C *pc6 = dynamic_cast< C* >(pa6); // downcasting, fail
   if (pc6) cout << "succeed!" << endl;
   else cout << "fail!" << endl;

   /*
   D inherits from both B and A. However, B itself already inherits from A.
   This creates a situation where D contains two separate A subobjects:
   One A subobject inherited through B.
   Another A subobject inherited directly.
   This is known as multiple inheritance with a diamond-shaped hierarchy,
   and it leads to ambiguity when you try to convert a D* to an A*.
   Why A* pa6 = new D; Fails
   
   When you write A* pa6 = new D;,
   the compiler cannot determine which A subobject you are referring to:
   Is it the A subobject inherited through B?
   Or is it the A subobject inherited directly?
   
   This ambiguity results in a compilation error.
   */
   A* pa6 = new D; // fail, A is an ambiguous base of D
   B* pb6 = dynamic_cast< B* >(pa6);
   
   return 0;
}
```

![Ambiguity Inheritance](https://hackmd.io/_uploads/ByHNsRgu1l.png =30%x)

{% endraw %}