---
title: "Friend Declarations in Class Templates"
date: 2026-04-13T15:32:37+08:00
draft: false
---

---
title: Friend Declarations in Class Templates
tags: [CPP]

---

There are three kinds of friend declarations that may appear within a class template:
1. A nontemplate friend class or friend function.
   ```c++
   class Foo {
   public:
      void bar();
   };
   
   template <class T>
   class QueueItem {
      friend class foobar;
      friend void foo();
      
      // It grants Foo::bar() access to the private/protected members of
      // the specific instantiation of the class QueueItem<T>.
      friend void Foo::bar();
      // ...
   };
   ```
   The class `foobar` and the function `foo()` do not have to be declared or defined in global scope before the class template `QueueItem` declares them as friends. However, the class `Foo` must be defined before the class `QueueItem` can declare one of its members as a friend. 
3. A ***bound*** friend class template, function template, or member function template. A one-to-one mapping is defined between the instantiation of the class template `QueueItem` and its friends, also template instantiations.
   ```c++
   #include <iostream>
   
   template <typename T> class Helper;
   template <typename T> class MyClass;
   template <typename T> void foo(MyClass<T>&);
   
   template <class T>
   class Helper2 {
   public:
      void reveal2( MyClass<T>& obj ){
         std::cout << obj._m << "\n";
      }
   };
   
   
   template<class T>
   class MyClass {
   
   // function template 
   friend void foo<T>( MyClass<T>& );
   
   // class template
   friend class Helper<T>;
   
   // member function template
   friend void Helper2<T>::reveal2( MyClass<T>& );
   
   public:
      MyClass(T m) : _m(m){}
   private:
      T _m;
   };
   
   template<class T>
   class Helper {
   public:
      void reveal( MyClass<T>& obj ){
         std::cout << obj._m << "\n";
      }
   };
   
   template<class T>
   void foo( MyClass<T>& obj ){
      std::cout << obj._m << "\n";
   }
   
   
   int main(){
   
      MyClass<int> cl(1);
      foo(cl);
   
      Helper<int> hi;
      hi.reveal(cl);
   
      Helper2<int> hi2;
      hi2.reveal2(cl);
   
      return 0;
   }
   ```
5. An ***unbound*** friend class template or function template. In the following example, a one-to-many mapping is defined between the instantiation of the class template `QueueItem` and the friend.
    ```c++
    #include <iostream>
    
    template <typename T> class Helper;
    template <typename T> class MyClass;
    template <typename T> void foo(MyClass<T>&);
    
    template <class T>
    class Helper2 {
    public:
       void reveal2( MyClass<T>& obj ){
          std::cout << obj._m << "\n";
       }
    };
    
    
    template<class T>
    class MyClass {
    
    // function template
    template <class U>
    friend void foo( MyClass<U>& );
    
    // class template
    template <class U>
    friend class Helper;
    
    // member function template
    template <class U>
    friend void Helper2<U>::reveal2( MyClass<U>& );
    
    public:
       MyClass(T m) : _m(m){}
    private:
       T _m;
    };
    
    template<class T>
    class Helper {
    public:
       void reveal( MyClass<T>& obj ){
          std::cout << obj._m << "\n";
       }
    };
    
    template<class T>
    void foo( MyClass<T>& obj ){
       std::cout << obj._m << "\n";
    }
    
    
    int main(){
    
       MyClass<int> cli(1);
       MyClass<double> cld(1.2);
    
       foo(cli);
       foo(cld);
    
       Helper<double> hi;
       hi.reveal(cld);
    
       Helper2<int> hi2;
       hi2.reveal2(cli);
    
       return 0;
    }
    ```

# Example: Queue and QueueItem Friend Declarations