---
title: "Operator Overloading"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: Operator Overloading
tags: [CPP]

---

1. Member operator must take exactly one parameter.
2. Non-member operator must take exactly two parameters.
3. Only operators lists as follows can be overloaded: 
`+` `-` `*` `/` `%` `^` `&` `|` `~` `!` `=` `<` `>` `+=` `-=` `*=` `/=` `%=` `^=` `&=` `|=` `<<` `>>` `>>=` `<<=` `==` `!=` `<=` `>=` `<=>`(since C++20) `&&` `||` `++` `--` , `->*` `->` `()` `[]`
4. The predefined meaning of an operator for the built-in types may not be changed. For example, the built-in integer addition operation cannot be replaced with an operation that checks for overflow.
   ```c++
   // error: cannot redefine built-in operator for ints
   int operator+( int, int );
   ```
5. Nor may additional operators be defined for the built-in data types. For example, an operator+ taking two operands of array types cannot be added to the set of built-in operations.
6. The predefined precedence of the operators cannot be overridden. Regardless of the class type and of the operator implementation, `x == y + z;` always performs `operator+` before `operator==`.
7. As with the predefined operators, when using an overloaded operator, precedence can be overridden with the use of parentheses.
8. Default arguments for overloaded operators are illegal, except for `operator()`.
   ```c++
   #include <iostream>
   
   Struct Foo {
       //Foo operator+(const Foo& other = Foo(0)) const;
       void operator()(int x = 0, int y = 0) const {
           std::cout << "x = " << x << ", y = " << y << '\n';
       }
   };
   
   Int main() {
       Foo foo;
       foo();         // x=0, y=0
       foo(5);        // x=5, y=0
       foo(5, 6);     // x=5, y=6
   }
   ```
9. The predefined arity of the operator must be preserved. The unary logical NOT operator, for example, cannot be defined as a binary operator for two objects of class String. The following implementation is illegal and results in a compile-time error:
   ```c++
   // illegal: ! is a unary operator
   bool operator!( const String &s1, const String &s2 )
   {
      return( strcmp( s1.c_str(), s2.c_str() ) != 0 );
   }
   ```
10. For built-in types, four predefined operators (`+`, `-`, `*`, and `&`) serve as both unary and binary operators. Either or both arities of these operators can be overloaded.
11. When overloading operators for a class, if you define `operator+`, you must also explicitly define `operator+=` if you want compound assignment to work.
C++ does not automatically create `+=` from `+`, unlike built-in types.
The meaning of `+=` should match the natural expectation based on `+`.


|             Situation             | Member operator | Non-member operator |
|:---------------------------------:|:---------------:|:-------------------:|
|       LHS is a class object       |    Required     |     Won't work      |
|     Need symmetric operation      |  Often awkward  |       Better        |
| Special operators (=, [], (), ->) |    Required     |      Forbidden      |


|        Operator         | Member function parameters | Non-member function parameters |
|:-----------------------:|:--------------------------:|:------------------------------:|
|      Unary (`-a`)       |             0              |               1                |
|     Binary (`a+b`)      |             1              |               2                |
|     Assignment `=`      |             1              |               Forbidden               |
|     Subscript `[]`      |             1              |               Forbidden               |
|   Function call `()`    |          (custom)          |               Forbidden               |
|   Member access `->`    |             0              |               Forbidden               |
| Postfix increment `a++` |      1 (dummy `int`)       |    2 (object + dummy `int`)    |


```c++
#include <iostream>

struct Foo {

   Foo ( ) : _data(0) {};
   Foo (int ia) : _data(ia) {};

   void operator+=(int ia){
      this->_data += ia;
      std::cout << "Foo::operator +=\n";
   }

   Foo operator+(int ia ){
      Foo foo;
      foo._data = this->_data + ia;
      std::cout << "Foo::operator +\n";
      return foo;
   }

   bool operator==( Foo f ){
      return this->_data == f._data;
   }

   const int showData() { return _data; }

   int _data;
};


Foo operator+( int ia, Foo& foo ){
   Foo result;
   result._data = foo._data + ia;
   std::cout << "::operator +=\n";
   return result;
}

int main(){
   Foo foo;
   foo += 5;
   foo = foo + 10;
   foo = 10 + foo;

   std::cout << foo.showData() << "\n";

   if ( foo == Foo {25} ){
      std::cout << "Same!\n";
   }
   return 0;
}
```
{% endraw %}