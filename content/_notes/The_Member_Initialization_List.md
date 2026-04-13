---
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---

1. The member initialization list follows the signature of the constructor and is set off by a colon. The member name is specified, followed by the initial values enclosed within parentheses.
   ```c++
   class Image {
   public:
      Image(const std::string& name, int index) : _name(name), _index(index) {}
   private:
      int _index;
      std::string _name;
   };
   ```
2. What is the difference between Step 2 and Step 3?
   ```c++
   #include <iostream>
   
   class A {
   public:
   
     // default ctor
     A()  { _ia = 1; std::cout << "Called default ctor\n";}
   
     // copy ctor
     A(const A& other) : _ia(other._ia) { std::cout << "Called copy ctor\n"; }
   
     // copy assignment
     A& operator=(const A& other) {
        std::cout << "Called copy assignment\n";
        if (this != &other) {
           _ia = other._ia;
        }
        return *this;
     }
   
     // move ctor
     A(A&& other) noexcept : _ia(std::move(other._ia)) { std::cout << "Called move ctor\n"; }
   
     // move assignment
     A& operator=(A&& other) noexcept {
        std::cout << "Called move assignment\n";
        if ( this != &other ){
           _ia = std::move(other._ia);
        }
        return *this;
     }
   
     int _ia;
   };
   
   class B {
   public:
      B(A& a) : _a(a) { }
      A _a;
   };
   
   class C {
   public:
      C(A& a) { _a = a; }
      A _a;
   };
   
   int main(){
      std::cout << "Step1\n";
      A a;
      std::cout << "\nStep2\n";
      B b(a);
      std::cout << "\nStep3\n";
      C c(a);
   }
   ```
   ```
   Step1
   Called default ctor
   
   Step2
   Called copy ctor
   
   Step3
   Called default ctor
   Called copy assignment
   ```
5. The step 2, **Direct construction**, does one operation: the single copy constructor you intended.
4. The step 3, **Default-then-assign**, does two operations: a default construction (occurs at member declaration) plus an assignment ctor.
5. All class members are initialized before we get to the constructor body. After all members have been initialized, we finally enter the constructor body.
6. For class objects, the distinction between initialization and assignment is significant. A member class object should always be initialized in the member initialization list rather than assigned to within the body of the constructor.
7. For non-class data member, the initialization or assignment of a nonclass data member, with two exceptions, is equivalent both in its result and in its performance.
8. Each member may be named only once in the member initialization list. The order of initialization is determined not by the order of names in the initialization list but by the class declaration order of the members.
9. Our recommendation is always to place the initialization of one member with another (if you really feel that it is necessary) within the body of the constructor, as follows:
   ```c+
   class X {
      int i;
      int j;
      public:
      // oops! do you see the problem?
         X( int val ) : j( val ), i( j )
      {}
      // ...
   };
   ```
   ```c++
   // preferred idiom
   X::X( int val ) : i( val ) { j = i; }
   ```
{% endraw %}