---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---

# Operators `new` and `delete`
1. A class member operator `new()` must have a return type of `void*` and take a first parameter of type `size_t`.
   ```c++
   class Screen {
   public:
      void *operator new( size_t );
   };
   ```
2. When a `new` expression creates an object of class type, the compiler looks to see if the class has a member operator `new()`. If it has, this operator is selected to allocate the memory for the class object; otherwise, the global operator `new()` is called.
3. The programmer can selectively invoke the global operator `new()` through the use of the global scope resolution operator. For example:
   ```c++
   Screen *ps = ::operator new Screen
   ```
   invokes the global operator `new()` even if class `Screen` defines operator `new()` as a member.
4. The class member operator `delete()` must have a `void` return type and a first parameter of type `void*`.
   ```c++
   class Screen {
   public:
      void operator delete(void*);
   };
   ```
5. When the operand of a `delete` expression is a pointer to an object of class type, the compiler looks to see if the class has a member operator `delete()`. If it has, this operator is selected to deallocate the memory for the class object; otherwise, the global operator `delete()` is called.
6. The programmer can selectively invoke the global operator `delete()` by using the global scope resolution operator. For example: `::operator delete ps;` invokes the operator `delete()` defined in global scope even if class `Screen` defines operator `delete()` as a member.
7.  In general, the operator `delete()` used should match the operator `new()` that is used to allocate the storage. For example, if `ps` refers to storage that was allocated with a `new` expression invoking the global operator `new()`, then the `delete` expression should also invoke the global operator `delete()`.
8.  The operator `delete()` defined for a class type and called by a `delete` expression may have two parameters instead of one. The first parameter must still be of type `void*`. The second parameter must be of the predefined type `size_t`.
    ```c++
    class Screen {
    public:
       // replaces:
       void operator delete( void *, size_t );
    };
    ```
    If present, the additional parameter is initialized automatically by the compiler with the size in bytes of the object addressed by the first parameter. 
10. The keyword `static` is optional for these functions: whether used or not, the allocation function is a static member function. Why? operator `new`/`delete` are called before/after any object is created. So there's no this pointer — because there's no object yet!
10. An allocation using operator `new()` (no matter default `new` or not), such as `Screen *ptr = new Screen( 10, 20 );` is equivalent to the following two-statement sequence:
    ```c++
    // Pseudo C++ code
    ptr = Screen::operator new( sizeof( Screen ) );
    Screen::Screen( ptr, 10, 20 );
    ```
# Array operators `new[]` and `delete[]`
1. Operator `new[]` is a built-in or user-defined function used to allocate a block of memory large enough to hold an array of objects. For example:
    ```c++
    Screen* ps = new Screen[5];
    ```
2. A class member operator `new[]()` must have a return type of void* and take a first parameter of type `size_t`.
    ```c++
    class Screen {
       void* operator new[]( size_t );
    };
    ```
3. When a `new` expression creates an array of objects of class type, the compiler looks to see if the class has a member operator `new[]()`. If it does, this operator is selected to allocate the memory for the array; otherwise, the global operator `new[]()` is called.
4. The operator's `size_t` parameter is initialized automatically with a value that represents the size of the storage required to store an array of ten Screen objects in ***bytes***.
5. Even though class Screen has a member operator `new[]()`, the programmer can invoke the global operator `new[]()` to create an array of Screen objects through the use of the global scope resolution operator. 
6. The member operator `delete[]()` must have a `void` return type and a first parameter of type `void*`.
    ```c++
    class Screen {
       void operator delete[]( void* );
    };
    ```
7. To delete an array of classes, the delete expression must use the array syntax: 
    ```c++
    delete[] ps;
    ```
8. When the operand of such a `delete` expression is a pointer to class type, the compiler looks to see if the class has a member operator `delete[]()`. If it does, this operator is selected to deallocate the memory for the array; otherwise, the global operator `delete[]()` is called.
9. The operator's `void*` parameter is initialized automatically with a value that represents the beginning of the storage in which the array is stored.
10. Even though class Screen has a member operator `delete[]()`, the programmer can invoke the global operator `delete[]() ` selectively by using the global scope resolution operator. For example, `::operator delete[] ps;` invokes the operator `delete[]()` defined in global scope.
11. A `new` expression that creates an array first calls the class operator `new[]()` to allocate the storage and then calls the ***default*** constructor to initialize iteratively every element of the array.
12. If the class has a constructor, but no default constructor, the `new` expression is an error.
13. No syntax exists to specify initializers for the array elements or to specify arguments for a class constructor in a `new` expression for arrays.
14. A delete expression that deletes an array first calls the class destructor to destroy iteratively every element of the array, and then calls the class operator `delete[]() `to deallocate the storage. 
15. The operator `delete[]()` for a class may also have two parameters instead of one, the second parameter being of the predefined type `size_t`. For example:
    ```c++
    class Screen {
    public:
       void operator delete[]( void*, size_t );
    };
    ```
    If present, the additional parameter is initialized automatically by the compiler with the size in bytes of the storage required to store the array.
# Placement Operators `new()` and `delete()`
1.  The first parameter of any class operator `new()` must always be a parameter of type `size_t`. The additional parameters are initialized with the placement arguments specified in a `new` expression.
    ```c++
    class Screen {
       void *operator new( size_t, Screen* );
    };
    ```
    ```c++
    Screen* start = new Screen;
    Screen* ps = new(start) Screen;
    ```
2. It is also possible to overload the class member operator `delete()`. However, such an operator is never invoked from a `delete` expression. An overloaded operator `delete()` is only called implicitly by the implementation if the constructor called by a `new` expression (yes, this is not a typo, we really mean a new expression) ***throws an exception***.
3. The actions of the following `new` expression
    ```c++
    Screen *ps = new ( start ) Screen;
    ```
    are as follows:
    a. It calls the class operator `new(size_t, Screen*)`.
    b. It then calls the default constructor for class `Screen` to initialize the object.
    c. It then initializes `ps` with the address of the `Screen` object.
4. If the class designer provides an overloaded operator `delete()` with parameters with types that match the parameter types of operator `new()`, the implementation automatically calls this operator `delete()` to deallocate the storage. For example,
    ```c++
    Screen *ps = new (start) Screen;
    ```
    If the default constructor for class `Screen` exits by throwing an exception, the implementation looks for an operator `delete()` in the scope of class `Screen`. For an operator `delete()` to be considered, it must have parameters with types that match those of the operator `new()` called. The implementation looks in class `Screen` for an operator `delete()` of the following form:
    ```c++
    void operator delete( void*, Screen* );
    ```
5. The class designer can then decide whether to provide an operator `delete()` that matches a specific operator `new()`, depending on whether the operator `new()` allocates storage or whether it reuses storage already allocated. If it allocates storage, then a placement operator `delete()` should be provided to deallocate the memory in case the constructor throws an exception when called from a new expression. If the placement operator `new()` does not allocate storage, then there is no need to provide a matching operator `delete()` to deallocate the memory.



# Example
```c++
#include <iostream>
#include <string>
#include <cstdlib>


class Screen {
public:
   Screen(int x, int y) : m_x(x), m_y(y){}
   Screen() : m_x(-1), m_y(-1){}
   // Single object
   void* operator new( size_t );

   // If delete(void*) and delete(void*,size_t) are present,
   // compiler calls delete(void*)
   void  operator delete( void* );
   void  operator delete( void*, size_t );

   // Array objects
   void* operator new[]( size_t );
   void  operator delete[]( void* );
   void  operator delete[]( void*, size_t );

   // Placement operators
   void* operator new( size_t, void* );
   void  operator delete( void*, void* );

   void* operator new[]( size_t, void* );
   void  operator delete[]( void*, void* );

   void showPosition();
private:
   int m_x;
   int m_y;
};


void* Screen::operator new( size_t size )
{
   std::cout<< "Overloading new operator with size: " << size << " bytes\n";
   //void* ptr = ::operator new(size);
   void* ptr = malloc(size);
   return ptr;
}

void Screen::operator delete( void* ptr )
{
   std::cout<< "Overloading delete operator with unknown size\n";
   free(ptr);
}

void Screen::operator delete( void* ptr, size_t size )
{
   std::cout<< "Overloading delete operator with size: " << size << " bytes\n";
   free(ptr);
}

void* Screen::operator new[]( size_t size )
{
   std::cout<< "Overloading new[] operator with size: " << size << " bytes\n";
   void* ptr = malloc(size);
   return ptr;
}

void Screen::operator delete[]( void* ptr )
{
   std::cout<< "Overloading delete[] operator with unknown size\n";
   free(ptr);
}

void Screen::operator delete[]( void* ptr, size_t size )
{
   std::cout<< "Overloading delete[] operator with size: " << size << " bytes\n";
   free(ptr);
}

void* Screen::operator new( size_t size, void* ptr)
{
   std::cout << "Placement new overloaded: using custom memory\n";
   return ptr;
}

void Screen::operator delete( void*, void* ptr)
{
   std::cout << "Placement new overloaded: using custom memory\n";
   free(ptr);
}

void* Screen::operator new[]( size_t size, void* ptr)
{
   std::cout << "Placement new overloaded: using custom memory\n";
   return ptr;
}

void Screen::operator delete[]( void*, void* ptr)
{
   std::cout << "Placement new overloaded: using custom memory\n";
   free(ptr);
}

void Screen::showPosition()
{
   std::cout << "m_x=" << this->m_x << ", m_y=" << this->m_y << "\n";
}

int main(){

   // Allocate single object
   Screen *s = new Screen(1, 3);
   s->showPosition();
   delete s;

   // Allocate object array
   Screen *as = new Screen[10];
   for (int i=0;i<10;i++){
      as[i].showPosition();
   }
   delete[] as;

   // Place single object
   char* start1 = new char [sizeof(Screen)];
   Screen* ps = new(start1) Screen;
   ps->showPosition();
   delete[] start1;

   // Place object array
   char* start2 = new char [sizeof(Screen)*10];
   Screen* psa = new(start2) Screen[10];
   for (int i=0;i<10;i++){
      psa[i].showPosition();
   }
   delete[] start2;

   return 0;
}
```
{% endraw %}