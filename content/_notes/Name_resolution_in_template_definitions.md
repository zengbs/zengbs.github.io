---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

# Lookup rules
* Non-dependent names are looked up and bound at the point of template definition. This binding holds even if at the point of template instantiation there is a better match.
* The lookup of a dependent name used in a template is postponed until the template arguments are known, at which time:
    1. Non-ADL lookup finds whatever declarations are visible from the template definition context.
    2. ADL (argument-dependent) lookup may add additional declarations from the associated namespaces (excluding global namespace) of the function-call arguments.
    3. The final overload set is the union of the candidates from both lookups. No matter where the declaration is defined before or after the template definition.
    4. Overload resolution picks the best match from that combined set (in other words, adding a new function declaration after template definition does not make it visible, except via ADL).
# Example 1
Non-dependent name is looked up and bound at the point of template definition.
```c++
#include <iostream>
 
void g(double) { std::cout << "g(double)\n"; }
 
template<class T>
struct S
{
    void f() const
    {
        g(1); // “g” is a non-dependent name, bound now
    }
};
 
void g(int) { std::cout << "g(int)\n"; }
 
int main()
{
    g(1);  // calls g(int)
 
    S<int> s;
    s.f(); // calls g(double)
}
```
# Example 2
The two examples below show that the set of candidate functions is the union of the candidates from non-ADL and ADL lookups:
```c++
#include <iostream>

namespace Foo2 {
    struct MyType2 {};
    void h(MyType2) {
        std::cout << "Called Foo::h(MyType2)\n";
    }
}

template <class T>
void g(T a) {
    h(a);
}

namespace Foo {
    struct MyType {};
    void h(MyType) {
        std::cout << "Called Foo::h(MyType)\n";
    }
}

int main() {
    g(Foo2::MyType2()); // Called Foo::h(MyType2)
    return 0;
} 
```
```c++
#include <iostream>

namespace Foo {
    struct MyType {};
    void h(MyType) {
        std::cout << "Called Foo::h(MyType)\n";
    }
}

template <class T>
void g(T a) {
    h(a);
}

namespace Foo2 {
    struct MyType2 {};
    void h(MyType2) {
        std::cout << "Called Foo::h(MyType2)\n";
    }
}

int main() {
    g(Foo2::MyType2()); //Called Foo::h(MyType2)
    return 0;
}
```
# Example 3
```c++
#include<iostream>

void h(double);

template<class T> void g(T a) {
  h(a);
}

void h(double) { std::cout << "Called h(double)" << std::endl; }
void h(int) { std::cout << "Called h(int)" << std::endl; }

int main(){
   g(234); // Called h(double)
   return 0;
}
```
1. When `g<T>` is defined, the compiler does an unqualified lookup of `h`. At that point, it only sees the forward declaration `void h(double);`.
2. Later, when you call `g(234)`, ADL (argument-dependent lookup) tries to find more overloads in the namespace of `int`, but `int` is a fundamental type with no associated namespace—so no new overloads are found.
3. Thus, the only candidate is `h(double)`, which is called, printing `"Called h(double)"`. The `h(int)` overload is ignored because it wasn’t visible at `g`'s definition time and ADL doesn’t bring it in.
{% endraw %}