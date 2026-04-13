---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

1. The initialization of one class object by another object of its class, such as `Account oldAcct( "Anna Livia Plurabelle" );` and `Account newAcct( oldAcct );` is referred to as default memberwise initialization. *Default* because it occurs automatically whether or not we supply an explicit constructor. *Memberwise* because the unit of initialization is the individual nonstatic data member rather than a bitwise copy of the entire class object.
2. For example, given a class:
   ```c++
   class Foo() {
   public:
   ...
   private:
      char* m_name;
      int m_index;
   };
   ```
   If there is no the declaration of copy constructor in the class, compiler will implicitly generate a default copy constrctor to perform memberwise initialization as follow:
   ```c++
   inline Foo::
   Foo( const Foo& rhs ){
      m_name = rhs.m_name;
      m_index = rhs.m_index;
   }
   ```
3. The initialization of a class object with another object of its class occurs in following program situations:
    * The explicit initialization of one class object with another; for example:
      ```c++
      Account newAcct( oldAcct );
      ```
    * The passing of a class object as an argument to a function; for example:
      ```c++
      extern bool cash_on_hand( Account acct );
      if ( cash_on_hand( oldAcct ))
      // ...
      ```
    * The passing of a class object as the return value of a function; for example:
      ```c++
      extern Account
      consolidate_accts( const vector< Account >& )
      {
         Account final_acct;
         // do the finances ...
         return final_acct;
      }
      ```
    * The definition of a nonempty sequence container type; for example:
      ```c++
      // five string copy constructors invoked
      vector< string > svec( 5 );
      ```
      (In this example, one temporary is created using the string default constructor and then this temporary is copied in turn into the five elements of the vector using the string copy constructor.)
    * The insertion of a class object into a container type; for example:
      ```c++
      svec.push_back( string( "pooh" ));
      ```
4. If a class contains a raw pointer and relies on the default copy constructor, copying the object results in a shallow copy—both objects share the same memory address. When the original object is destroyed, its destructor frees the memory, leaving the copied object's pointer dangling. Accessing this invalid pointer causes undefined behavior, making bugs hard to detect and debug. There are three ways to resolve or prevent this:
    * Using deep copy.
    * Declare the copy ctor as private.
    * Do not provide the definition of copy ctor, only provide its definition, disallowing compiler generates default copy ctor.


# Member Class Object Initialization
1. When a member class object is recognized, the same process is applied recursively. Does the class provide an explicit copy constructor? If it does, that instance is invoked to initialize the member class object. Otherwise, default memberwise initialization is applied to the member class object. If all the members of that class are built-in or compound data types, each is initialized in turn, thus completing the initialization of the member class object. Otherwise, if one or more of those members are themselves member class objects, the process is applied recursively until each built-in and compound data member is handled.
2. If a string member is included in a class like this:
   ```c++
   class Account {
      std::string _name;
      int _index;
   };
   ```
   How to write a copy stor? You may write something like:
   ```c++
   class Account {
      Account( const Account& rhs ){
          _name = rhs._name;
          _index = rhs._index;
      }
      std::string _name;
      int _index;
   };
   ```
   However, there are two steps involved in the copy ctor: 1) Initialize `_name` by the default ctor of `std::string`. 2) Assign `rhs._name` to `_name`. The second step is redundant, a better solution is as follows:
   ```c++
   class Account {
      Account( const Account& rhs ) : _name(rhs._name) {
          _index = rhs._index;
      }
      std::string _name;
      int _index;
   };
   ```
{% endraw %}