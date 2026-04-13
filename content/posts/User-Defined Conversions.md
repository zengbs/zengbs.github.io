---
title: "User-Defined Conversions"
date: 2026-04-13T15:32:38+08:00
draft: false
---

---
title: User-Defined Conversions
tags: [CPP]

---

# Motivation
We reuse our class `SmallInt` holding the same range of values as an 8-bit `unsigned char`— that is, 0 to 255.

If we want to be able to add and subtract `SmallInt` objects both with other `SmallInt` objects and with objects of built-in arithmetic type, we must support for these operations by providing six `SmallInt` operator functions:

```c++
class SmallInt {
   friend operator+( const SmallInt &, int );
   friend operator-( const SmallInt &, int );
   friend operator-( int, const SmallInt & );
   friend operator+( int, const SmallInt & );
public:
   SmallInt( int ival ) : value( ival ) { }
   operator+( const SmallInt & );
   operator-( const SmallInt & );
   // ...
private:
   int value;
};
```
However, it's a daunting idea! An better alternative is to provide user-defined conversion:
```c++
#include <iostream>

class SmallInt {
public:
   SmallInt(int ival) : value(ival) {}
   operator int(){ return value; }
   void showValue()
   {
      std::cout << "value = "<< value << "\n";
   }
private:
   int value;
};

int main(){
   SmallInt s(1);
   s.showValue();

   // 1. Convert s to int by conversion operator
   // 2. Perform + operator of int
   // 3. Convert s+1 to SmallInt by constructor
   s = s + 1;

   s.showValue();
   return 0;
}
```

What if two classes have different number of members?
```c++
#include <iostream>

template<class C>
class ClassA {
public:
   // A ctor with two parameters is required!
   ClassA(C m, C n) : _m(m), _n(n){}
   C get_m(){ return _m; }
   C get_n(){ return _n; }
private:
   C _m;
   C _n;
};

template<class C>
class ClassB {
public:
   ClassB(C m) : _m(m){}

   template <class D>
   
   // Can be optimized by rvalue ref?
   operator ClassA<D>(){
      return { static_cast<D>(_m), static_cast<D>(_m+_m) };
   }
   C get(){ return _m; }
private:
   C _m;
};

int main(){

   ClassB<double> b(1.6);
   ClassA<int> a = b;

   std::cout << a.get_m() << "\n"; // 1
   std::cout << a.get_n() << "\n"; // 3

   return 0;
}
```

# Conversion Operator
1. A conversion operator defines a user-defined conversion to convert a class object into some other type.
2. A conversion function is declared in the class body by specifying the keyword operator followed by the type that is the target type of the conversion.
3. The name that follows the keyword `operator` in the declaration of a conversion function does not have to be a built-in type name.
4. In a conversion operator, do not return a private pointer to keep encapsulation. For example:
   ```c++
   #include <iostream>
   
   class Unsafe {
   private:
       int secret = 42;
   
   public:
       // Dangerous: returns private data pointer
       operator int*() { return &secret; }
       
       // Safe
       operator int() { return secret; }
   };
   
   int main() {
       Unsafe u;
       int* p = u;   // Calls operator int*()
       *p = 99;      // Modifies private data!
       std::cout << *p << "\n";  // 99
   }
   ```
5. If the target of the conversion (in this case type double) does not match the type of the conversion function (in this case type int) exactly, a conversion function can still be invoked if the target type can be reached through a standard conversion sequence.
6. Only standard conversion sequences are allowed following the user-defined conversion. If, to reach the target type, a second user-defined conversion must be applied, ***no conversion*** is applied implicitly by the compiler.


# A Constructor as a Conversion Function
1. The collection of constructors for a class taking a **single** parameter, such as `SmallInt`'s constructor `SmallInt(int)`, defines a set of implicit conversions from values of the constructors' parameter types to values of type `SmallInt`. `SmallInt(int)` , for example, converts values of type `int` into `SmallInt` values.
2. Multiple-parameter constructors are not served as conversion constructors.
3. If necessary, a standard conversion sequence is applied to an argument before a constructor is called to perform a user-defined conversion.
4. The compiler implicitly uses a constructor with a single parameter to convert values of the parameter type to values of the constructor's class type. This may not always be what we want. To prevent the use of a constructor for implicit type conversions, we can declare the constructor `explicit`.
    ```c++
    #include <iostream>
    
    class SmallInt {
    public:
       SmallInt(int ival) : value(ival) { std::cout << "Calls SmallInt ctor\n"; }
       operator int(){ std::cout << "SmallInt ==> int\n"; return value; }
       void showValue()
       {
          std::cout << "value = "<< value << "\n";
       }
    private:
       int value;
    };
    
    
    class Token {
    public:
       Token(std::string n, int val) : name(n), value(val){}
       operator SmallInt(){ std::cout << "Token ==> SmallInt\n"; return value; }
       operator int(){ std::cout << "Token ==> int\n"; return value; }
       operator std::string(){ std::cout << "Token ==> std::string\n"; return name; }
       void showToken()
       {
          std::cout << "name = " << name << ", value = "<< value << "\n";
       }
    private:
       int value;
       std::string name;
    };
    
    void Token2Double( double dval) {}
    void Token2Int( int ival) {}
    void Token2SmallInt( SmallInt s ){}
    
    int main(){
    
       Token t1("weff", 45);
       
       // Token ==> int
       // int ==> double (standard conversion)
       Token2Double(t1);  // fails if operator int() is absent
    
       // Token ==> SmallInt
       // Calls SmallInt ctor
       Token2SmallInt(t1);
    
       // Token ==> int
       Token2Int(t1); // fails if operator int() is absent
       
       // double ==> int (standard conversion)
       // Using explicit ctor can avoid the above implicit conversion
       // Calls SmallInt ctor
       Token2SmallInt(2.1);
    
       // Calls SmallInt ctor
       SmallInt s(2);
    
       // SmallInt ==> int
       // Calls SmallInt ctor
       s = s + 1;
    
       // value = 3
       s.showValue();
    
       return 0;
    }
    ```