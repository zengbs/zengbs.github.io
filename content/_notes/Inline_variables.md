---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

# Inline Variables
## Using Inline Variables
* A non-const and non-inline static data member is not allowed to have an in-class initializer. See [Static Class Members](/SP9q1kt9TxONvAYUqG381A).
* Since C++17, we can initialize a non-const static member with `inline`:
   ```c++
   strtuc MyType {
      inline static std::string msg{"OK"};
   };
   ```
* Note that you still have to ensure that types are complete before you can initialize them. For example, if a struct or class has a static member of its own type, the member can only be defined inline after the type declaration:
   ```c++
   struct MyType {
      int value;
      MyType(int i) : value{i} { }
      static MyType max;           // OK
      inline static MyType min{0}; // Error
   };
   inline MyType MyType::max{0};
   ```
## `constexpr` Now Implies `inline` For Static Members
* For static data members, constexpr implies inline now, such that since C++17.
* This code violated the one definition rule (ODR). When built with an optimizing compiler, it might have worked as expected or might have given a link error due to the missing definition. When built without any optimizations, it will almost certainly be rejected due to the missing definition of `D::n`.
   ```c++
   #include<iostream>
   
   struct D {
      static constexpr int n{5};
   };
   
   // It needs an actual object with storage to bind the reference to D::n
   // Program needs its address / identity / memory location. (ODR-use)
   int twice1(const int& i) {
      return i;
   }
   
   int twice2(const int i) {
      return i;
   }
   
   int main() {
      std::cout << D::n << "\n";         // OK, before and after C++17
      std::cout << twice1(D::n) << "\n"; // Error, before C++17 without optimization
      std::cout << twice2(D::n) << "\n"; // OK, before and after C++17
   }
   ```
## Inline Variables and `thread_local`
By using `thread_local` you can also make an inline variable unique for each thread:
 
 ```c++
 #include<iostream>
#include<thread>

struct MyData {
   inline static std::string gName{"global"};           // unique per program
   inline static thread_local std::string tName{"tls"}; // unique per thread
   std::string lName{"local"};                          // unique per object

   void print(const std::string& msg) const {
      std::cout << msg << '\n';
      std::cout << "gName: " << gName << '\n';
      std::cout << "tName: " << tName << '\n';
      std::cout << "lName: " << lName << '\n';
   }
};

inline thread_local MyData myThreadData; // unique per thread

void foo()
{
   myThreadData.print("foo()begin:");
   myThreadData.gName = "thread2 name";
   myThreadData.tName = "thread2 name";
   myThreadData.lName = "thread2 name";
   myThreadData.print("foo() end:");
}

int main() {

   myThreadData.print("main() begin:");
   // main() begin:
   // gName = global
   // tName = tls
   // lName = local

   myThreadData.gName = "thread1 name";
   myThreadData.tName = "thread1 name";
   myThreadData.lName = "thread1 name";

   myThreadData.print("main() later:");
   // main() later:
   // gName = thread1 name
   // tName = thread1 name
   // lName = thread1 name

   std::thread t(foo);
   // foo() begin:
   // gName = thread1 name
   // tName = tls
   // lName = local

   // foo() end:
   // gName = thread2 name
   // tName = thread2 name
   // lName = thread2 name

   t.join();

   myThreadData.print("main() end:");
   // main() end:
   // gName = thread2 name
   // tName = thread1 name
   // lName = thread1 name
}
 ```
{% endraw %}