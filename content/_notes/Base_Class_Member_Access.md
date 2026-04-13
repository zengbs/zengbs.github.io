---
date: 2026-04-13T15:32:36+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

1. Each base class represents a subobject made up of the nonstatic data members of the base class.
2. The derived class object is made up of its base class subobjects and a derived part consisting of the nonstatic data members of the derived class.
3. Within the derived class, the inherited non-virtual members of the base class subobject can be accessed directly as if they are members of the derived class. (The depth of the inheritance chain does not limit access to these members nor does it add to the cost of that access.)
4. There is one exception to the direct access of a base class member within the derived class — when the name of the base class member is reused within the derived class.
    ```c++
    #include <iostream>
    #include <string>
    
    struct Base {
       int _m;
    };
    
    struct Derived : public Base {
       // hide visibility of Base::_m
       std::string _m;
       void foo();
    };
    
    void Derived::foo(){
       _m = "123";
       //_m = -1; // Error
    }
    
    int main(){
    
       Derived d;
       d.foo();
       std::cout << d._m << "\n";
    
       return 0;
    }
    ```
5. To access a base class member with a name that has been reused within a derived class, we must qualify the base class member with its class scope operator.
1. A common misunderstanding of those new to the language is the expectation that base and derived class member functions make up a set of overloaded functions. 
   ```c++
   #include <iostream>
   #include <string>
   
   struct Base {
      void Foo(int){ }
   };
   
   struct Derived : public Base {
      void Foo(std::string){ }
      void Bar(std::string){
         //Foo(1); // Error
      }
   };
   
   int main(){
      Derived obj;
      obj.Foo("55");
      obj.Foo(1); // Error
      return 0;
   }
   ```
7. What if we really wish to provide an overloaded set of instances of both the derived and base class members?
   Method 1:
   ```c++
   #include <iostream>
   #include <string>
   
   struct Base {
      void Foo(int){
         std::cout << "Called Base::Foo(int)\n";
      }
   };
   
   struct Derived : public Base {
      void Foo(std::string){
         std::cout << "Called Derived::Foo(std::string)\n";
      }
      void Foo(int x){
         Base::Foo(x);
      }
   };
   
   int main(){
      Derived obj;
      obj.Foo(1); // Called Base::Foo(int)
      return 0;
   }
   ```
   Method 2:
   ```c++
   #include <iostream>
   #include <string>
   
   struct Base {
      void Foo(int){
         std::cout << "Called Base::Foo(int)\n";
      }
   };
   
   struct Derived : public Base {
      void Foo(std::string){
         std::cout << "Called Derived::Foo(std::string)\n";
      }
      using Base::Foo;
   };
   
   int main(){
      Derived obj;
      obj.Foo(1);
      return 0;
   }
   ```
   In effect, the using declaration enters each named member of the base class into the scope of the derived class. The base class member is now entered into the set of overloaded instances associated with the name of the member function within the derived class. (The using declaration for a member function cannot specify the parameter list, only the member function name. This means that if the function is overloaded within the base class, all the overloaded instances are added to the scope of the derived class type. We cannot add only one instance of the set of overloaded base class members.)
8. We are saying that a class derived from `Base` may directly access the `_m` data member, while the rest of the program must use the public access function. What this means, however, is that the derived class has access to the protected `_m` data member of its base class subobject. The derived class does not have access to the protected members of an independent base class object. For example:
    ```c++
    #include <iostream>
    #include <string>
    
    struct Base {
       Base () : _m(-2) { }
       int get() { return _m; }
       void set(int m) { _m = m; }
    protected:
       int _m;
    };
    
    struct Derived : public Base {
       void Foo( Base *ptr ){
          //ptr->_m;                        // Error
          std::cout << ptr->get() << "\n";  // 300
          std::cout << _m << "\n";          // -2
       }
       void Bar( Derived *ptr ){
          std::cout << ptr->_m << "\n";     // -2
          std::cout << ptr->get() << "\n";  // -2
          std::cout << _m << "\n";          // -2
       }
    };
    
    int main(){
    
       Base* ptr_b = new Derived;
       ptr_b->set(300);
    
       Derived d1, d2;
       d1.Foo(ptr_b);
    
       d1.Bar(&d2);
    
       return 0;
    }
    ```
    This form of member access constraint does not apply within a class for other objects of its own class (`Derived::Bar(Derived&)`). The derived class may access directly the protected base class members of other objects of its own class, as well as the protected and private members of other objects of its own class.
9. Except for a virtual function declared in the base class and overriden in the derived class, there is no way to access members in the derived clas directly through `Base* ptr`:
    1. If Base and Derived both declare a nonvirtual member function of the same name, the Base instance is always invoked through `Base* ptr`.
    2. Similarly, if Base and Derived both declare a data member of the same name, the Base instance is always accessed through `Base* ptr`.
    3. If Derived introduces a virtual function not present in Base, such as `XX()`, for example, an attempt to invoke it through `Base* ptr` results in a compile-time error.
    4. Similarly, if we try to access a nonvirtual member function or a data member of Derived through `Base* ptr`, a compile-time error results.
    ```c++
    #include <iostream>
    
    struct Base {
       Base() : _m(-1) {}
       void Foo(){
          std::cout << "Calls Base::Foo()\n";
       }
       virtual void Bar(){
          std::cout << "Calls Base::Bar()\n";
       }
       int _m;
    };
    
    struct Derived : public Base {
       Derived() : _m(-2) {}
       void Foo(){
          std::cout << "Calls Derived::Foo()\n";
       }
       void Bar() override {
          std::cout << "Calls Derived::Bar()\n";
       }
       virtual void XX(){
          std::cout << "Calls Derived::XX()\n";
       }
       void YY(){}
       int _m;
    };
    
    int main(){
    
       Base* ptr1 = new Derived;
    
       // Case 1:
       ptr1->Foo(); // Calls Base::Foo()
    
       ptr1->Bar(); // Calls Derived::Bar()
    
       // Case 2:
       std::cout << ptr1->_m << "\n"; // -1
    
       // Case 3:
       //ptr1->XX();  // Error
    
       // Case 4:
       //ptr1->YY();  // Error
    
       Derived* ptr2 = new Derived;;
       ptr2->Foo(); // Calls Derived::Foo()
       ptr2->Bar(); // Calls Derived::Bar()
       ptr2->XX();  // Calls Derived::XX()
    
       return 0;
    }
    ```
10. All derived class objects refer to the same, single, shared static member defined in the base class.
    ```c++
    #include <iostream>
    
    struct Base {
       static int s_m;
    };
    
    struct Derived : public Base {
    };
    
    int Base::s_m = -56;
    
    int main(){
    
       Derived d1, d2;
    
       std::cout << d1.s_m << "\n";
       std::cout << d2.s_m << "\n";
    
       return 0;
    }
    ```
12. If a derived class wishes to access the private members of its base class directly, the base class must declare the derived class explicitly to be a friend. 
13.  Friendship is not inherited. The derived class does not become a friend of a class that granted friendship to one of its base classes. If the derived class requires one or more of the same friendships, each must be granted explicitly by the respective class.
{% endraw %}