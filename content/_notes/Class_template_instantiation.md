---
title: "Class template instantiation"
date: 2026-04-13T15:32:36+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: Class template instantiation
tags: [CPP]

---

![Template(3)](https://hackmd.io/_uploads/r1AbX47bgg.jpg =60%x)

1. This generation, `Queue<int> qi`, of a class from the generic class template definition is called template instantiation.
2. There is no special relationship between the instantiations of a class template for different types. Rather, each instantiation of a class template constitutes an independent class type.
3. Unlike template arguments for function template instantiations, the template arguments for class template instantiations are never deduced from the context in which a class template instantiation is used.
   ```c++
   Queue qs; // Error: which template argument type?
   ```
5. An instantiation of the class template Queue can be used by the general program wherever a nontemplate class type can be used.
   ```c++
   // the return type and two parameters are instantiations of Queue
   extern Queue< complex<double> >
   foo( Queue< complex<double> > &, Queue< complex<double> > & );
   
   // pointer to member function of an instantiation of Queue
   bool (Queue<double>::*pmf)() = 0;
   
   // explicit cast of 0 to a pointer to an instantiation of Queue
   Queue<char*> *pqc = static_cast< Queue<char*>* > ( 0 );
   ```
6. A template declaration or definition can refer to a class template or to an instantiation of a class template. However, outside the context of a template definition, only class template instantiations can be used.
   ```c++
   template<class T>
   class Queue {}; 
   
   template<class T>
   void bar( Queue<T>&, Queue<double>& ){}
   void foo( Queue<int>& ){}
   
   int main() {
       Queue<int> qi;
       Queue<double> qd;
       bar<int>(qi, qd);
       foo(qi);
       return 0;
   }
   ```
7. A class template is instantiated only when the name of an instantiation is used in a context that requires a class definition to exist. Not all uses of a class require the class definition to be known. For example, it is not necessary to know the definition of a class before pointers and references to a class can be declared.
    ```c++
    class Matrix;
    Matrix* pm;            // ok
    void inverse(Matrix&); // ok
    ```
1. The definition of the class `Queue<int>` becomes known to the compiler at the point (`Queue<int> qi;`), called the point of instantiation of the class `Queue<int>`. Similarly, if a pointer or reference refers to a class template instantiation, only when examining the object to which such a pointer or reference refers is the class template instantiated.
   ```c++
   void foo( Queue<int> &qi )
   {
      // instantiatioan point of Queue<double>
      Queue<double> qd;
      Queue<int> *pqi = &qi;
      
      // instantiatioan point of Queue<int>
      pqi->add( 255 );
   }
   ```
1. In the following case, the type `QueueItem<int>` is only instantiated when these members are dereferenced in the member functions of class `Queue<int>`.
   ```c++
   template <class Type>
   class Queue {
      public:
      // ...
      private:
      QueueItem<Type> *front;
      QueueItem<Type> *back;
   };
   ```
1. Depending on the types with which a class template is instantiated, some design considerations must be taken into account when defining a class template. For example,
   ```c++
   template <class Type>
   class QueueItem {
   public:
      QueueItem( Type ); // bad design choice
   };
   ```
   ```c++
   template <class Type>
   class QueueItem {
      // potentially inefficient
      QueueItem( const Type &t ) {
         item = t; next = 0;
      }
   };
   ```
   ```c++
   template <class Type>
   class QueueItem {
      // item initialized in constructor member initialization list
      QueueItem( const Type &t ): item(t) { next = 0; }
   };
   ```
   See [Consider pass by value for copyable parameters that are cheap to move and always copied.](/ibiB09WVTpa9A4KQrGcCAg) for details.

# Template Arguments for Nontype Parameters
1. The template argument shall be a constant expression.
    * const exp: the address of any object, either const or non-const, of name scope
    * const exp: sizeof expression
      ```c++
      template <int size> Buf{ ... };
      template <int *ptr> class BufPtr { ... };
      int size_val = 1024;
      const int c_size_val = 1024;
      Buf< 1024 > buf0; // ok
      Buf< c_size_val > buf1; // ok
      Buf< sizeof(size_val) > buf2; // ok: sizeof(int)
      BufPtr< &size_val > bp0; // ok
      ```
    * non-const exp: the value of non-const object
      ```c++
      template <int *ptr> class BufPtr { ... };
      // error: template argument cannot be evaluated at compile-time
      BufPtr< new int[24] > bp;
      ```
      ```c++
      template <int size> Buf{ ... };
      int size_val = 1024;
      Buf< size_val > buf3;
      ```
2. Some conversions are allowed between the type of a template argument and the type of a nontype template parameter. The set of conversions allowed is a subset of the conversions allowed on function arguments:
    * Lvalue transformations, including lvalue-to-rvalue conversion, array-to-pointer conversion, and function-to-pointer conversion:
       ```c++
       template <int *ptr> class BufPtr { ... };
       int array[10];
       BufPtr< array > bpObj; // array-to-pointer conversion
       ```
    * Qualification conversions:
       ```c++
       template <const int *ptr> class Ptr { ... };
       int iObj;
       Ptr< &iObj > pObj; // conversion from int* to const int*
     * Promotions:
       ```c++
       template <int hi, int wid> class Screen { ... };
       const short shi = 40;
       const short swi = 132;
       Screen< shi, swi > bpObj2; // promotion from short to int
       ```
    * Integral conversions:
        ```c++
        template <lunsigned int size> Buf{ ... };
        Buf<l 1024 > bObj; // conversion from int to unsigned int
        ```
3. The following conversion that converts the value 0 of integer type to a value of pointer type is not allowed:
   ```c++
   template <int *ptr>
   class BufPtr { ... };
   // error: 0 is of type int
   // implicit conversion to the null pointer value using
   // an implicit pointer conversion is not applied
   BufPtr< 0 > nil;
   ```
{% endraw %}