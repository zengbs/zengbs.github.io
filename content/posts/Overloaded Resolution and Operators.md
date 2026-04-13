---
title: "Overloaded Resolution and Operators"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: Overloaded Resolution and Operators
tags: [CPP]

---

1. How does the compiler decide, on encountering an operator such as the addition operator in the following initialization:
   ```c++
   SomeClass sc;
   int iobj = sc + 3;
   ```
2. Overload resolution for overloaded operators follows the usual three-step process:
   * Select the candidate functions.
   * Select the viable functions.
   * Select the best match function.
3. Function overload resolution is never applied if an operator only has operands of built-in types. For such operands, a built-in operator is guaranteed to be used,  even though the operands could be converted to the class type through a constructor or user-defined conversion.
    ```c++
    #include <iostream>
    
    struct SmallInt {
    
       SmallInt(int val) : _val(val) { std::cout << "Called ctor\n"; }
    
       SmallInt operator+( int a ){ std::cout << "Called SmallInt::operator+\n"; return _val+a; }
    
       void showVal(){ std::cout << "val = " << _val << "\n"; }
    
       int _val;
    };
    
    SmallInt operator+ ( const SmallInt& s1, const SmallInt& s2){
    
       std::cout << "Called SmallInt::operator+\n";
    
       return s1._val+s2._val;
    }
    
    int main() {
    
        SmallInt s(1);
        s = 1 + 2; // Calls built-int operator+(int,int)
        s.showVal();
    
        return 0;
    }
    ```

# Candidate Operator Functions

1. Five sets of candidate operator functions are built for the use of an operator using the operator syntax with an operand of class type. 
    * **[Global OP]** The set of operators visible at the point of the call.
      ```c++
      #include <iostream>
  
      class SmallInt {
      public:
         SmallInt(int val) : _val(val) {
            std::cout << "Called ctor\n";
         }
         int _val;
      };
      
      // Global OP
      SmallInt operator+ ( const SmallInt& s1, const SmallInt& s2 ){
         std::cout << "Called ::operator+()\n";
         return s1._val + s2._val;
      }
      
      int main() {
      
          NS::SmallInt s(1);
          NS::SmallInt t  = s + 2;
      
          return 0;
      }
      ```
    * **[Non-member OP]** The set of operators declared within the namespace where the type of an operand is defined.
       ```c++
       #include <iostream>
       
       namespace NS {
          class SmallInt {
             public:
                SmallInt(int val) : _val(val) {
                   std::cout << "Called ctor\n";
                }
                int _val;
          };
       
          // Non-member OP
          SmallInt operator+( SmallInt& s1, double dval ){
             return s1._val+static_cast<int>(dval);
          }
       }
       
       int main() {
       
           NS::SmallInt s(1);
           NS::SmallInt t  = s + 2;
       
           return 0;
       }
       ```
    * **[Friend OP]** For operands of class type, if the class definition declares friend operator functions with the same name as the operator used, the friend operator functions are added to the set of candidate operator functions.
    * **[Member OP]** The set of member operators declared in the class of the left-hand operand.
       ```c++
       #include <iostream>
       
       namespace NS {
       
          class SmallInt {
             // Friend OP
             friend SmallInt operator+( const SmallInt&, double );
             public:
                SmallInt(int val) : _val(val) {
                   std::cout << "Called ctor\n";
                }
                // Member OP
                SmallInt operator+(int);
             private:
                int _val;
          };
       
          SmallInt operator+( const SmallInt& s, double dval ){
             std::cout << "Called ctor A\n";
             return s._val + dval;
          }
       
          // the type of the implied object parameter is SmallInt&
          SmallInt SmallInt::operator+(int ival){
             std::cout << "Called ctor B\n";
             return this->_val + ival;
          }
       }
       
       int main() {
       
           NS::SmallInt s(1);
           NS::SmallInt t  = s + 2.0;
       
           return 0;
       }
       ```
    * The set of built-in operators. For example,
      ```c++
      int operator+(int, int)
      double operator+(double, double)
      T* operator+(T*, I)
      T* operator+(I, T*)
      ```
       The third and fourth declarations represent the built-in operator for pointer types, which is used to add values of integral type to pointer values.
2. The set of candidate operator functions is the union of the five sets of candidate functions listed previously. 
# Viable Functions
1. A set of viable operator functions is selected from the set of candidate operator functions by selecting only the operator functions that can be called with the operands specified when the operator is used.
2.  Since arguments and parameters are associated by position within their respective lists, the convention is that the implicit object parameter, if present, is always the first parameter and the implied object argument, if present, is always the first argument.
3. For non-static member functions, the type of the implicit object parameter is “reference to cv `X`” where `X` is the class of which the function is a member and cv is the cv-qualification on the member function declaration. 
    ```c++
    #include <iostream>
    
    namespace NS {
    
       class SmallInt {
          // Friend OP
          friend SmallInt operator+( const SmallInt&, double );
          public:
             SmallInt(int val) : _val(val) {
                std::cout << "Called ctor\n";
             }
             // Member OP
             SmallInt operator+(int);
          private:
             int _val;
       };
    
       SmallInt operator+( const SmallInt& s, double dval ){
          std::cout << "Called ctor A\n";
          return s._val + dval;
       }
    
       // the type of the implied object parameter is SmallInt&
       SmallInt SmallInt::operator+(int ival){
          std::cout << "Called ctor B\n";
          return this->_val + ival;
       }
    }
    
    int main() {
    
        NS::SmallInt s(1);
        NS::SmallInt t  = s + 2.0;
    
        return 0;
    }
    ```
    Since the type of the implied object parameter is `SmallInt&`, the member and non-member operator functions can be considered as:
    ```c++
    SmallInt operator+(SmallInt&, int );
    SmallInt operator+(const SmallInt&, double );
    ```
    For the first argument, the member operator is a better match. For the second argument, non-member function is a better match. Since neither function is strictly better than the other in all arguments, the compiler reports an ambiguity error.

# Ambiguity
1. Providing both conversion functions that perform implicit conversions to built-in types and overloaded operators for the same class type may lead to ambiguities between the overloaded operators and the built-in operators.
2. User-defined conversions are applied implicitly by the compiler. This may cause built-in opeators to become viable functions for the use of an operator with operands of class types. Conversion functions and nonexplicit constructors should therefore be used judiciously.



{% endraw %}