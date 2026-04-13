---
title: "Class Scope"
date: 2026-04-13T15:32:36+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: Class Scope
tags: [CPP]

---

1. Members declared later in the class body cannot be used by the declarations of members declared earlier.
   ```c++
   #include <iostream>
   
   class MyClass {
      char& operator[]( index_type );
      typedef int index_type; // Error
   };
   
   int main(){
      MyClass obj;
      return 0;
   }
   ```
2. The resolution of names used in the definition of an inline member function takes place in two steps. First, the function declaration (that is, the function return type and the parameter list) is processed at the location where it appears in the class definition, then the function body is processed in the completed scope of the class.
   ```c++
   #include <iostream>
   
   class MyClass {
   public:
      typedef int index_type;
      char& operator[]( index_type elem ){ return _string[elem]; }
   private:
      char* _string;
   };
   
   int main(){
      MyClass obj;
      return 0;
   }
   ```
 3. If the definition of a class member appears outside the class body, the program text that follows the name of the member being defined is considered in class scope until the end of the member definition.
     ```c++
     #include <iostream>
     
     class MyClass {
     public:
        typedef int index_type;
        char& operator[]( index_type);
     private:
        char* _string;
     };
     
     char& MyClass::operator[]( index_type elem ){ return _string[elem]; }
     
     int main(){
        MyClass obj;
        return 0;
     }
     ```
4. In the definition of a class member that appears outside the class body, the program text before the member name being defined is not in the scope of the class.
   ```c++
   #include <iostream>
   
   class Account {
   typedef double Money; //type definition can also be private
   private:
      static Money _interestRate;
      static Money initInterest(Money);
   };
   
   // The return type Money must be qualified by qualifier
   Account::Money Account::initInterest(Money m){
      _interestRate = m;
      return _interestRate;
   }
  
   // everything following the name of the static member 
   // _interestRate until the semicolon ending
   // the static member definition is
   // in the scope of class Account.
   Account::Money Account::_interestRate = initInterest(1.2);
   
   int main(){
      Account obj;
      return 0;
   }
   ```
   ```c++
   #include <iostream>
   
   class Account {
   public:
      typedef double Money;
      Money _interestRate;
      Money initInterest(Money);
   };
   
   Account::Money Account::initInterest(Money m){
      _interestRate = m;
      return _interestRate;
   }
   
   int main(){
      Account obj;
      std::cout << obj.initInterest(1.2) << std::endl;
      return 0;
   }
   ```
   
   # Name Resolution in Class Scope
   - [Unqualified Name Lookup](/cmvzTXvfTJOizt_Y9XQgUw)
{% endraw %}