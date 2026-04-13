---
title: "Memberwise Initialization and Assignment"
date: 2026-04-13T15:32:37+08:00
draft: false
---

---
title: Memberwise Initialization and Assignment
tags: [CPP]

---

# Memberwise Initialization (copy constructor)
```c++
class Query {
public:
// ...
protected:
   int _paren;
   std::set<short>* _solution;
   std::vector<location> _loc;
};

class NameQuery : public Query {
public:
   NameQuery( std::string& name ) : _name(name){}
private:
   std::string _name;
};
```

```c++
NameQuery folk( "folk" );
```

the initialization of `music` with `folk` `NameQuery`
```c++
music = folk;
```
causes the following steps to occur:
1. The compiler checks to see if the `NameQuery` class defines an explicit instance of a copy constructor. It does not. Therefore, the compiler prepares to apply default memberwise initialization.
2. The compiler next checks to see if the `NameQuery` class contains any base class subobjects. Yes, it contains a `Query` base class subobject.
3. The compiler checks to see if the `Query` base class defines an explicit instance of a copy constructor. It does not. Therefore, the compiler prepares to apply default memberwise initialization.
4. The compiler checks to see if the `Query` class contains any base class subobjects. No, it does not.
5. The compiler examines each nonstatic member of the `Query` class in order of declaration. If the member is a nonclass object, such as `_paren` and `_solution`, it initializes the `music` object member with the value of `folk`'s member. If the member is a class object, such as `_loc` , it applies step 1 recursively. Yes, the `vector` class defines an explicit instance of a copy constructor. The copy constructor is invoked to initialize `music._loc` with `folk._loc`.
6. The compiler next examines each nonstatic member of the `NameQuery` class in order of declaration. The string member class object is recognized as providing an explicit copy constructor. It is invoked to initialize `music._name` with `folk._name`.

Note that the default copy constructor always performs memberwise copy initialization unless explicitly overridden.

![圖片](https://hackmd.io/_uploads/HJhufQ_Xel.png)

# Case 1: A member pointer is declared in Base class
The default initialization of `music` with `folk` is now complete. It is well behaved except for the default copy of `_solution` that, if permitted, is likely to cause our program to fail. (Since the data referenced by `_solution` may be released by `folk`) We override the default handling by providing an explicit `Query` class copy constructor.

One solution is to copy the entire `std::set _solution`. However, because our implementation of the solution set is to have it calculated on demand, there is really no imperative to copy it now. The purpose of our copy constructor is to prevent its default copy. It's sufficient to initialize `_solution` to 0:

```c++
#include <iostream>
#include <set>
#include <vector>
#include <string>

class Query {
public:
   Query(int p, std::set<short>* s, const std::vector<int>& v):
   _p(p), _v(v), _s(s) {}

   Query( const Query& rhs )
   : _p(rhs._p), _s(0), _v(rhs._v) {
      std::cout << "Query's copy ctor\n";
   }
protected:
   int _p;
   std::set<short>* _s;
   std::vector<int> _v;
};


class NameQuery : public Query {
public:
   NameQuery( int p, std::set<short>* s, const std::vector<int>& v, const std::string& name )
   : _name(name), Query(p, s, v) {}
private:
   std::string _name;
};

int main() {
    std::set<short> s{1, 5, 3};
    NameQuery music(1, &s, std::vector<int>(10,0), "YLPH");
    NameQuery running = music; // Output: Query's copy ctor
    return 0;
}
```


By doing so, the program will call explicit copy constructor of Base class and default copy constructor of Derived class in turn.

# Case 2: A member pointer is declared in Derived class

The `NotQuery` derived class contains a `Query` base class subobject and a `Query*` data member, `_op`, addressing its operand allocated on the free store. The `NotQuery` destructor applies the `delete` expression to the operand. The `NotQuery` class cannot safely allow default memberwise initialization of its `_op` member, and so must provide an explicit copy constructor. Its implementation makes use of the virtual `clone() `function defined in the previous section.
```c++
#include <iostream>
#include <set>
#include <vector>
#include <string>

class Query {
public:
   Query(int p, std::set<short>* s, const std::vector<int>& v)
   : _p(p), _v(v), _s(s) {}

   Query( const Query& rhs )
   : _p(rhs._p), _s(0), _v(rhs._v) {
      std::cout << "Query's copy ctor\n";
   }
   Query* clone(){
      return new Query(*this);
   }
protected:
   int _p;
   std::set<short>* _s;
   std::vector<int> _v;
};


class NotQuery : public Query {
public:
   NotQuery(int p, std::set<short>* s, const std::vector<int>& v, Query* op)
   : Query(p, s, v), _op(op->clone()){}
   // rhs is of type const NotQuery&,
   // how can we use it to call Query(rhs)?
   // -- because NotQuery is a derived class of Query,
   // so a const NotQuery& can be implicitly converted to
   // a const Query& — this is a standard rule of polymorphism:
   NotQuery( const NotQuery& rhs ) : Query(rhs) {
      _op = rhs._op->clone();
   }
private:
   Query* _op;
};


int main() {

    std::set<short> s{1, 5, 3};
    std::vector<int> v(10,0);

    std::cout << "Step 1:\n";
    Query q(1, &s, v);

    std::cout << "Step 2:\n";
    NotQuery music(1, &s, v, &q);

    std::cout << "Step 3:\n";
    NotQuery running = music;

    // Output:
    // Step 1:
    // Step 2:
    // Query's copy ctor
    // Step 3:
    // Query's copy ctor
    // Query's copy ctor
    return 0;
}
```

# Memberwise Assignment (copy assignment)
Memberwise assignment is similar to memberwise initialization. If an explicit copy assignment operator is present, it is invoked to assign one class object with another. Otherwise, default memberwise assignment is applied.

If a base class is present, the base class subobject is memberwise assigned first. If the base class provides an explicit copy assignment operator, it is invoked. Otherwise, default memberwise assignment is applied recursively to the base classes and members of the base class subobject.

Each nonstatic data member is examined in turn in the order of declaration. If it is a nonclass type, the right-hand instance is copied to the left. If it is a class type and the class defines an explicit copy assignment operator, the operator is invoked. Otherwise, default memberwise assignment is applied recursively to the base classes and members of the member class object.
```c++
#include <iostream>
#include <set>
#include <vector>
#include <string>

class Query {
public:
   Query(int p, std::set<short>* s, const std::vector<int>& v)
   : _p(p), _v(v), _s(s) {}

   Query* clone(){
      return new Query(*this);
   }

   // copy assignment
   Query& operator=(const Query& rhs) {
      if ( this != &rhs ){
         _p = rhs._p;
         _v = rhs._v;
         if (_s != nullptr) delete _s;
         _s = nullptr;
      }
      return *this;
   }
protected:
   int _p;
   std::set<short>* _s;
   std::vector<int> _v;
};


class NameQuery : public Query {
public:
   NameQuery(int p, std::set<short>* s, const std::vector<int>& v, const std::string& name)
   : Query(p, s, v), _name(name){}
private:
   std::string _name;
};

class NotQuery : public Query {
public:
   NotQuery(int p, std::set<short>* s, const std::vector<int>& v, Query* op)
   : Query(p, s, v), _op(op->clone()){}

   // copy assignment
   NotQuery& operator=( const NotQuery& rhs ){
      if ( this != &rhs ){
         this->Query::operator=(rhs);
         // Or the line below:
         (*static_cast<Query*>(this)) = rhs;
         
         _op = rhs._op->clone();
      }
      return *this;
   }
private:
   Query* _op;
};



int main() {

    std::vector<int> v(10,0);

    std::set<short>* s = new std::set<short>();
    s->insert(1);
    s->insert(2);
    s->insert(3);

    NameQuery car(-1, s, v, "YLPH");
    NameQuery driver(0, s, v, "PHYL");
    driver = car;


    s = new std::set<short>();
    s->insert(1);
    s->insert(2);
    s->insert(3);
    Query q(1, s, v);

    NotQuery music(1, s, v, &q);
    NotQuery running(2, s, v, &q);
    running = music;

    return 0;
}
```