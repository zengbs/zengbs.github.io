---
title: "Namespaces and Class Templates"
date: 2026-04-13T15:32:37+08:00
draft: false
---

---
title: Namespaces and Class Templates
tags: [CPP]

---

1. As with any other global scope definitions, a class template definition can be placed in a namespace.
2. The class template name `MyClass` must be qualified by the namespace name `ns` when it is used outside of the namespace, or be introduced through a using declaration. 
    ```c++
    #include <iostream>
    
    namespace ns {
    
       template<class T1, class T2>
       class MyClass {
       public:
          MyClass(T1 m1, T2 m2) : _m1(m1), _m2(m2) {}
          void show(){
             std::cout << "m1 = "<< _m1 << ", m2 = " << _m2 << std::endl;
          };
       private:
          T1 _m1;
          T2 _m2;
       };
    
    }
    
    int main(){
    
       ns::MyClass<int, float> obj(2, -2.64f);
       obj.show();
    
       return 0;
    }
    ```
3. When this pointer is used to refer to the member function `show()`, it refers to the member function `show()` of this template instantiation.
   ```c++
   #include <iostream>
   
   namespace ns {
      template<class T1, class T2>
      class MyClass {
      public:
         MyClass(T1 m1, T2 m2) : _m1(m1), _m2(m2) {}
         void show(){
            std::cout << "m1 = "<< _m1 << ", m2 = " << _m2 << std::endl;
         };
      private:
         T1 _m1;
         T2 _m2;
      };
   }
   
   int main(){
   
      ns::MyClass<int, float>* p_obj = new ns::MyClass<int,float>(2, -2.64f);
      p_obj->show();
      delete p_obj;
   
      return 0;
   }
   ```
4. A specialization declaration for a class template or for a member of a class template must be declared in the namespace where the generic template is defined.
    ```c++
    #include <iostream>
    
    namespace ns {
       template<class T1, class T2>
       class MyClass {
       public:
          MyClass(T1 m1, T2 m2) : _m1(m1), _m2(m2) {}
          void show(){
             std::cout << "Called ns::MyClass<int,float>::show()\n";
             std::cout << "m1 = "<< _m1 << ", m2 = " << _m2 << std::endl;
          };
       private:
          T1 _m1;
          T2 _m2;
       };
    
       // partial specialization declaration for ns::MyClass<float, T>
       template<class T> class MyClass<float, T>;
    
       // specialization declaration for ns::MyClass<float, char>
       template<> class MyClass<float, char>;
    
       // specialization declaration for ns::MyClass<double,double>::show()
       template<> void MyClass<double, double>::show();
    
    }
    
    // partial specialization definition for ns::MyClass<float, T>
    template<class T>
    class ns::MyClass<float, T> {
       public:
          MyClass(float m1, T m2) : _m1(m1), _m2(m2) {}
          void show(){
             std::cout << "Called ns::MyClass<float,T>::show()\n";
             std::cout << "m1 = "<< _m1 << ", m2 = " << _m2 << std::endl;
          };
       private:
          float _m1;
          T   _m2;
    };
    
    // specialization definition for ns::MyClass<float, char>
    template<>
    class ns::MyClass<float, int> {
       public:
          MyClass(float m1, int m2) : _m1(m1), _m2(m2) {}
          void show(){
             std::cout << "Called ns::MyClass<float,int>::show()\n";
             std::cout << "m1 = "<< _m1 << ", m2 = " << _m2 << std::endl;
          };
       private:
          float _m1;
          int   _m2;
    };
    
    
    // specialization definition for ns::MyClass<double,double>::show()
    template<>
    void ns::MyClass<double, double>::show(){
       std::cout << "Called ns::MyClass<double,double> show()\n";
       std::cout << "m1 = "<< _m1 << ", m2 = " << _m2 << std::endl;
    }
    
    int main(){
    
       ns::MyClass<int, float>* p_obj1 = new ns::MyClass<int,float>(2, -2.64f);
       p_obj1->show();
       delete p_obj1;
    
       ns::MyClass<float, int>* p_obj2 = new ns::MyClass<float,int>(26.502f, -2);
       p_obj2->show();
       delete p_obj2;
    
       ns::MyClass<double,double>* p_obj3 = new ns::MyClass<double, double>(2.6e-3, -2.51);
       p_obj3->show();
       delete p_obj3;
    
       ns::MyClass<float, double>* p_obj4 = new ns::MyClass<float,double>(26.502f, -2.55);
       p_obj4->show();
       delete p_obj4;
    
       return 0;
    }
    ```