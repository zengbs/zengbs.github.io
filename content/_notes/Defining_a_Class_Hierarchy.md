---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

1. An abstract class can be thought of as an incomplete class that is more or less finished with each subsequent class derivation.
2. The abstract base class defines the set of data and function members that are common to all the types derived fromn the base class.
3. A derived class inherits the data members and the member functions of its base class and can use them directly as if they were members of the derived class.
4. ***polymorphism*** and ***dynamic binding*** not only allow for the addition, revision, or removal of types without requiring changes to user programs, but frees the provider of a new type from having to recode behavior or actions common to all types in the hierarchy itself.
5. Although the polymorphic manipulation of an object requires that the object be accessed either through a pointer or a reference, the manipulation of a pointer or a reference in C++ does not in itself necessarily result in polymorphism.
6. The C++ language supports polymorphism in the following ways:
    * Through the implicit conversion of a derived class pointer, a reference to a pointer, or a reference of its public base type:
        ```c++
        Query *pquery = new NameQuery( "Glass" );
        ```
    * Through the virtual function mechanism:
        ```c++
        pquery->eval();
        ```
    * Through the dynamic_cast and typeid operators (these are discussed in detail in Section 19.1):
       ```c++    
       if ( NameQuery *pnq =
       dynamic_cast< NameQuery* >( pquery )) ...
       ```
7.  The syntactic outline of defining our `Query` class hierarchy picture below is:
    ```c++
    class Query { ... };
    class AndQuery : public Query { ... };
    class OrQuery : public Query { ... };
    class NotQuery : public Query { ... };
    class NameQuery : public Query { ... };
    ```
    ![image](https://hackmd.io/_uploads/SJz7_1Nfee.png)
8. The class specified in the derivation list must be defined prior to being specified as a base class. The following forward declaration of Query, for example, is not sufficient for it to serve as a base class:
   ```c++
   // This case reports a error
   class Query;
   class NameQuery : public Query {
      ...
   };
   ```
9. The forward declaration of a derived class does not include its derivation list, but simply the class name — the same as if it were a nonderived class. For example, the following forward declaration of NameQuery results in a compile-time error:
   ```c++
   // error: a forward declaration must not include
   // the derivation list of the derived class
   class NameQuery : public Query;
   ```
   The correct forward declaration is as follows:
   ```c++
   class Query;
   class NameQuery;
   ```
{% endraw %}