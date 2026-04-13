---
title: "Lambda capture `this` by value"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

---
title: Lambda capture `this` by value
tags: [CPP]

---

* When using lambdas in non-static member functions, you have no implicit access to the object the member function is called for. That is, inside the lambda, you cannot use members of the object without capturing `this` in some form (whether you qualify the members with `this->` does not matter):
  ```c++
  class C {
  private:
     std::string name;
  public:
     void foo(){
        auto l1 = [] { std::cout << name << '\n'; }; // Error
        auto l2 = [] { std::cout << this->name << '\n';  }; // Error
     }
  };
  ```
* In C\++11 and C\++14, you have to pass this either by value or by reference:
  ```c++
  class C {
  private:
     std::string name;
  public:
     void foo(){
     
        // Captures: the this pointer explicitly.
        auto l1 = [this] { std::cout << name << '\n'; }; // OK
        
        // Captures: everything used inside the lambda by value.
        // [=] implicitly captures this by value
        auto l2 = [=] { std::cout << name << '\n';  }; // OK
        
        // Captures: everything used inside the lambda by reference.
        auto l3 = [&] { std::cout << name << '\n';  }; // OK
     }
  };
  ```
* However, the problem here is that even copying `this` captures the underlying object by reference (as only the pointer was copied). This can become a problem if the lifetime of the lambda exceeds the lifetime of the object upon which the member function is invoked.
* Since C++17, you can explicitly ask to capture a copy of the current object by capturing `*this`:
  ```c++
  class C {
  private:
     std::string name;
  public:
     void foo(){
        // captures a copy of an entire object
        auto l1 = [*this] { std::cout << name << '\n'; };
     }
  };
  ```
* A complete example:
   ```c++
   #include <iostream>
   #include <string>
   #include <thread>
   
   class Data {
     private:
       std::string name;
     public:
       Data(const std::string& s) : name(s) {
       }
       auto startThreadWithCopyOfThis() const {
           // start and return new thread using this after 3 seconds:
           using namespace std::literals;
           std::thread t([*this] {
                                  std::this_thread::sleep_for(3s);
                                  std::cout << name << '\n';
                              });
           return t;
       }
   };
   
   int main()
   {
       std::thread t;
       {
         Data d{"c1"};
         
         // create a worker thread at here:
         t = d.startThreadWithCopyOfThis();
         
       } // d is no longer valid
       
       // main thread wait at here:
       t.join();
   }
   ```