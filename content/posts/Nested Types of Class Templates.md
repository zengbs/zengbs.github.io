---
title: "Nested Types of Class Templates"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

---
title: Nested Types of Class Templates
tags: [CPP]

---

1. An alternative implementation strategy is to nest the definition of the class template `QueueItem` within the private section of the class template `Queue`. With `QueueItem` being a nested private type, it becomes inaccessible to the general program.
2. Nested classes of class templates are autmatically class templates, and the template parameter of the enclosing class template can be used within the nested class template.
3. Each instantiation of `Queue` generates its own `QueueItem` class with the appropriate template argument for `Type` . The mapping between an instantiation for the `QueueItem` class template and an instantiation of the enclosing `Queue` class template is one to one.
4. A nested class of a class template is not instantiated automatically when the enclosing class template is instantiated. The nested class is only instantiated if it is itself used in a context that requires a complete class type. 
5. `QueueItem<int>` is still only instantiated when the members `front` and `back` are dereferenced in the member functions of class `Queue<int>`.
    ```c++
    #include <iostream>
    
    template <class T>
    class Queue {
    public:
       Queue(T e):_e(e), item(e){}
    
       class QueueItem {
       friend class Queue;
       public:
       QueueItem(T n):_n(n){}
       T show(){ return _n; }
       private:
          T _n;
       };
    
       QueueItem item;
       T show(){ return item.show(); }
    
    private:
       T _e;
    };
    
    int main(){
    
       Queue<int> ei(2);
    
       std::cout << ei.show() << "\n";
    
       return 0;
    }
    ```
6. A public nested type of a non-template class can be used outside its class definition. However, for a public nested type (or an enumerator of a nested enumeration) of a class template, only an instantiation of the nested type can be referenced by the general program. In this case the name of the nested type must be prefixed with the name of the class template instantiation.
   ```c++
   #include <iostream>
   
   template <class T>
   class Queue {
   public:
      Queue(T e):_e(e), item(e){}
   
      class QueueItem {
      friend class Queue;
      public:
      QueueItem(T n):_n(n){}
      T show(){ return _n; }
      private:
         T _n;
      };
   
      QueueItem item;
      T show(){ return item.show(); }
   
   private:
      T _e;
   };
   
   int main(){
   
      Queue<int>::QueueItem qitem(3);
      std::cout << qitem.show() << "\n";
   
      return 0;
   }
   ```