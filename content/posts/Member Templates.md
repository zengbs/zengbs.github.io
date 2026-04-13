---
title: "Member Templates"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

---
title: Member Templates
tags: [CPP]

---

1. A function or class template can be a member of an ordinary class or a member of a class template.
    ```c++
    #include <iostream>
    
    template <class T>
    class Queue {
    
    public:
       // Ctor
       Queue(T e): _e(e) {}
    
       // function member template
       template <class V>
       void foo( V value ){
          std::cout << "In foo(): passed value = " << value << "\n";
       }
    
       // class member template
       // --> The declaration of a member template
       //     has template parameters of its own.
       template <class U>
       class QueueItem {
       public:
          QueueItem(T m, U n) : _m(m), _n(n) {}
          T show_m(){ return _m; }
          U show_n(){ return _n; }
       private:
          // The definition of a member template
          // can also use the template parameters
          // of the enclosing class template.
          T _m;
          U _n;
       };
    
    private:
       T _e;
    };
    
    
    int main(){

        Queue<int> q(10);
     
        q.foo<double>(-9.3); // In foo(): passed value = -9.3
        Queue<int>::QueueItem<double> qitem(1, 1.2);
        std::cout << qitem.show_m() << ", " << qitem.show_n() << "\n"; // 1, 1.2
     
        // Type conversions are allowed.
        q.foo<long>(-9.3); // In foo(): passed value = -9
     
        return 0; 
    }
    ```
3. The declaration of a member template has template parameters of its own.
4. The definition of a member template can also use the template parameters of the enclosing class template.
5. Declaring a member template within the class template `Queue` means that an instantiation of `Queue` contains a potentially infinite number of nested classes `QueueItem` and a potentially infinite number of member functions `foo()`.
6. A member template is only instantiated when it is itself used in a program.
7. Type conversions are allowed.
8. Any member function can be defined as a member template. A constructor, for example, can be defined as a member template.
   ```c++
   #include <iostream>
   
   template <class T>
   class Queue {
   
   public:
      // regular ctor
      Queue( T e ) : _e(e) { std::cout << "A\n"; }
   
      // template ctor
      template <class U>
      Queue(const Queue<U>& other): _e( static_cast<T>(other.show()) ) { std::cout << "B\n"; }
   
      T show() const { return _e; }
   
   private:
   
      T _e;
   };
   
   
   int main(){
   
      Queue<double> qd(1.63); // A
      Queue<int> qi(qd); // B
   
      std::cout << qi.show() << "\n"; // 1
   
      return 0;
   }
   ```
10. Like nontemplate members, a member template can be defined outside its enclosing class or class template definition. The definition of a member template defined outside the class template definition must be preceded by the class template parameter list, followed by the member's own template parameter list.
    ```c++
    #include <iostream>
    
    template <class T>
    class Queue {
    public:
       // function member template
       template <class U>
       void foo(U);
    };
    
    // The template parameters do not
    // have to have the same name as
    // those specified within the class template definition.
    template<class T> template<class W>
    void Queue<T>::foo( W u ){
      std::cout << u << "\n";
    }
    
    int main(){
    
       Queue<int> qi;
    
       qi.foo<double>(1.6);
    
       return 0;
    }
    ```
12. The template parameters do not have to have the same name as those specified within the class template definition.