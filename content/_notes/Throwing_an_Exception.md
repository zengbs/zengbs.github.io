---
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---

* We will take the code below as an example throughout this section:
   ```c++
   #include <vector>
   
   class iStack {
   public:
      iStack( int capacity )
      : _stack( capacity ), _top( 0 ) { }
      bool pop( int &top_value );
      bool push( int value );
      bool full();
      bool empty();
      void display();
      int size();
   private:
      int _top;
      vector< int > _stack;
   };
   ```
* Exceptions are most often implemented
using classes.
   ```c++
   // stackExcp.h:
   // stackExcp.h
   class popOnEmpty { /* ... */ };
   class pushOnFull { /* ... */ };
   ```
* An exception is an object, and `pop()` must throw an object of class type. The expression in the throw expression cannot simply be a type. To create an object of class type, we need to call the class constructor.
* We are now ready to provide the new implementations of `iStack`'s `pop()` and `push()` member functions:
   ```c++
   #include "stackExcp.h"
   
   void iStack::pop( int &top_value )
   {
      if ( empty() )
      throw popOnEmpty();
      top_value = _stack[ --_top ];
      cout « "iStack::pop(): " « top_value « endl;
   }
   
   void iStack::push( int value )
   {
      cout « "iStack::push( " « value « " )\n";
      if ( full() )
      throw pushOnFull();
      _stack[ _top++ ] = value;
   }
   ```
   Because exceptions are now used to indicate the failure of the `pop()` and `push()` operations, the return values from these functions are now unnecessary.
* Although exceptions are most often objects of class type, a throw expression can throw an object of any type. 
{% endraw %}