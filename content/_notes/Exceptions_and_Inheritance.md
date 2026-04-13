---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---

# Exceptions Defined as Class Hierarchies
* In real-life C++ programs, the class types representing exceptions are most often organized into groups or hierarchies. For example, we can define a base class, called `Excp`, from which both of the exception classes are derived. This base class encapsulates the data members and member functions common to both derived classes:
   ```c++
   class Excp {
   public:
   // print error message
   static void print( string msg ) {
   cerr « msg « endl;
   }
   };
   
   class Excp { ... };
   class stackExcp : public Excp { ... };
   class popOnEmpty : public stackExcp { ... };
   class pushOnFull : public stackExcp { ... };
   class mathExcp : public Excp { ... };
   class zeroOp : public mathExcp { ... };
   class divideByZero : public mathExcp { ... };
   ```
# Throwing an Exception of Class Type
* Let's take the code below as an example:
   ```c++
   #include <iostream>
   
   Struct ErrorCode {
       int code;
       ErrorCode(int c) : code(c) {
           std::cout << "ErrorCode: constructor called. this: " << this << "\n";
       }
       ErrorCode(const ErrorCode& other) : code(other.code) {
           std::cout << "ErrorCode: copy constructor called. this: " << this << "\n";
       }
       ~ErrorCode() {
           std::cout << "ErrorCode: destructor called. this: " << this << "\n";
       }
   };
   
   Void mathFunc(int i) {
       if (i == 0) {
           throw ErrorCode(42);   // calls ctor for temporary object
                                  // calls copy ctor for exception object
       }                          // calls destructor for the temporary object
   }
   
   Int main() {
       try {
           mathFunc(0);
       } catch (ErrorCode& e) {
           std::cout << "Caught error with code = " << e.code << "\n";
       } // calls destructor for the exception object
   }
   ```
   ```
   # g++ main.cc -std=c++98
   # g++ main.cc -fno-elide-constructors -std=c++11 (without copy elision):
   ErrorCode: constructor called. this: 0x7ffe289f4704
   ErrorCode: copy constructor called. this: 0x5558d90d8f30
   ErrorCode: destructor called. this: 0x7ffe289f4704
   Caught error with code = 42
   ErrorCode: destructor called. this: 0x5558d90d8f30
   ```
   Without copy elision, the following steps take place:
   1. The throw expression creates a temporary object of class type `ErrorCode` by calling the class constructor.
   2. An exception object of type `ErrorCode` is created to be passed to the exception handler. The exception object is a copy of the temporary object created by the throw expression in step 1. It is created by calling the class `ErrorCode`'s copy constructor.
   3. The temporary object created by the throw expression in step 1 is destroyed before the search fora handler starts.

    With copy elision, no temporary object is created.
   ```
   # g++ main.cc (with copy elision, mandatory from C++11)
   ErrorCode: constructor called. this: 0x565312d1ef30
   Caught error with code = 42
   ErrorCode: destructor called. this: 0x565312d1ef30
   ```
 *  Why the throw expression creates a temporary object, and destroy it at the end of the throw expression? The exception, however, must last until a handler is found, which may be many functions further up the chain of function calls. It is therefore necessary to copy the temporary object into a storage location, called the exception object, that is guaranteed to last until the exception has been handled.
 *  If the exception object is created by copying the value of the throw expression, the exception thrown always has the exact type of the expression specified on the throw expression. For example,
    ```c++
     #include <iostream>
    
    struct Excep { };
    
    struct DerivedExcep : public Excep { };
    
    void mathFunc() {
       DerivedExcep e;
       Excep *ptr = &e;
       throw *ptr;
    }
    
    int main() {
        try {
            mathFunc();
        } catch (DerivedExcep& e) {
            std::cout << "Caught error with type: DerivedExcep\n";
        } catch ( Excep& e ) {
            std::cout << "Caught error with type: Excep \n";
        }
    }
    ```
* The throw expression is in error if:
  1. The class `ErrorCode` does not have a constructor that accepts an argument of type int or if this constructor is not accessible. (e.g., it's private or is deleted)
  2. The class `ErrorCode` has either a copy constructor or a destructor that is not accessible.
  3. The class `ErrorCode` is an abstract base class, because a program cannot create an object of an abstract class type.

   For example, if we disable copy constructor, the code can succesfully compile with copy elision enabled, but fails to compile when copy elision is disabled.
    ```c++
    #include <iostream>
    
    struct ErrorCode {
        int code;
        ErrorCode(int c) : code(c) {
            std::cout << "ErrorCode: constructor called. this: " << this << "\n";
        }
        ErrorCode( const ErrorCode& other ) = delete;
        ~ErrorCode() {
            std::cout << "ErrorCode: destructor called. this: " << this << "\n";
        }
    };
    
    void mathFunc(int i) {
        if (i == 0) {
            throw ErrorCode(42);
        }
    }
    
    int main() {
        try {
            mathFunc(0);
        } catch (ErrorCode& e) {
            std::cout << "Caught error with code = " << e.code << "\n";
        }
    }
    ```
    The code above can succesfully compile with copy elision enabled, but fails to compile when copy elision is disabled.

# Handling an Exception of Class Type
* When exceptions are organized into class hierarchies, an exception of class type may be caught by a catch clause for a public base class of that class type.
   ```c++
   #include <iostream>
   
   class ExceptBase { };
   class ErrorCode : public ExceptBase { };
   
   void Foo (int i) {
      if ( i == 2 ){
         throw ErrorCode();
      }
   }
   
   int main() {
   
      try {
         Foo(2);
      } catch ( ExceptBase& e ) {
         std::cout << "Caught ExceptBase\n";
      } catch ( ErrorCode& e ) {
         std::cout << "Caught ErrorCode\n";
      }
   
      return 0;
   }
   ```
    The catch clause that is selected is the first match; that is, the first catch clause encountered that can handle the exception. This is why, in a list of catch clauses, the most specialized catch clause must appear first. Once a catch clause has been found for an exception, no further catch clause is examined. Hence, the appropriate order for the catch clauses is the following:
   ```c++
   try {
      Foo(2);
   } catch ( ErrorCode& e ) {
      std::cout << "Caught ErrorCode\n";
   } catch ( ExceptBase& e ) {
      std::cout << "Caught ExceptBase\n";
   }
   ```
* The class type rethrown by `throw` is the original type that was thrown initially.
   ```c++
   #include <iostream>
   
   class ExceptBase { };
   class ErrorCode : public ExceptBase { };
   
   void Foo (int i) {
      if ( i == 2 ){
         throw ErrorCode();
      }
   }
   
   void Bar () {
      try {
         Foo(2);
      } catch ( ExceptBase& e ) {
         std::cout << "Caught ExceptBase\n";
         throw; // rethrow an exception of class type 'ErrorCode'
      }
   }
   
   int main() {
      try {
         Bar();
      } catch ( ErrorCode& e ) {
         std::cout << "Caught ErrorCode\n";
      }
      return 0;
   }
   ```
* If the catch clause rethrows the exception, passing the exception object to a catch clause higher up in the chain of function calls, the exception object cannot be destroyed before the last catch clause handling the exception has been reached. For this reason, the exception object is not destroyed until the final catch clause for this exception exits.
   ```c++
   #include <iostream>
   
   class ErrorCode {
   public:
      ErrorCode() { std::cout << "Calls ctor of ErrorCode: " << this << "\n"; }
      ~ErrorCode() { std::cout << "Calls destructor of ErrorCode: " << this << "\n"; }
      ErrorCode ( const ErrorCode& other ) { std::cout << "Calls copy ctor of ErrorCode: " << this << "\n"; }
   };
   
   
   void Foo (int i) {
      std::cout << "Calls Foo()\n";
      if ( i == 2 ){
         std::cout << "Throwing ...\n";
         throw ErrorCode(); // Calls ctor of ErrorCode: 0x564d38ae6340
      }
   }
   
   void Bar () {
      try {
         Foo(2);
      } catch ( ErrorCode e ) {  // Calls copy ctor of ErrorCode: 0x7ffde50ae6a7
         std::cout << "Caught ErrorCode\n";
         throw; // rethrow an exception of class type 'ErrorCode'
                // Calls destructor of ErrorCode: 0x7ffde50ae6a7
      }
   }
   
   int main() {
      try {
         std::cout << "Calls Bar()\n";
         Bar();
      } catch ( ErrorCode e ) { // Calls copy ctor of ErrorCode: 0x7ffde50ae6d7
         std::cout << "Caught ErrorCode\n";
      } // Calls destructor of ErrorCode: 0x7ffde50ae6d7
        // Calls destructor of ErrorCode: 0x564d38ae6340
      return 0;
   }
   ```
   The exception object with address `0x564d38ae6340` does not destroyed until at the end of the first catch clause that matchs the exception object.
# Exceptions Objects and Virtual Functions
* If the exception object thrown is of derived class type and it is handled by a catch clause for a base class type, the catch clause cannot generally use the features of the derived class type. We can redesign our exception class hierarchy to define virtual functions that can be used in the catch clause for the base class `Excp` to invoke the more specialized member functions in the derived class types.
   ```c++
   #include <iostream>
   
   class ExceptBase {
   public:
      virtual void print() {
         std::cout << "print ExceptBase\n";
      }
   
   };
   
   class ErrorCode : public ExceptBase {
   public:
      void print() {
         std::cout << "print ErrorCode\n";
      }
   };
   
   void Foo (int i) {
      if ( i == 2 ){
         throw ErrorCode();
      }
   }
   
   int main() {
      try {
         Foo(2);
      } catch ( ExceptBase& e ) {
         e.print(); // print ErrorCode
      }
      return 0;
   }
   ```
   Therefore, another good reason to declare the exception declaration of the catch clause as a reference is to ensure that the virtual functions associated with the type of the exception object are properly invoked.


# Stack Unwinding and Destructor Calls
* When an exception is thrown, the search for a catch clause that can handle the exception takes place, starting within the function throwing the exception and proceeding up through the chain of nested function calls, until a catch clause for the exception is found. This process of searching for a catch clause up through the chain of function calls is called ***stack unwinding***.
* During stack unwinding, as the functions in the chain of function calls exit during the search for a catch clause, the actions each function performs are ended abruptly. This may not be so good if a function acquires a resource (for example, if it opens a file or allocates some memory on the free store) and this resource is never released.
   ```c++
   #include <iostream>
   #include <exception>
   
   class PTR {
   public:
      PTR() { ptr = new int[10]; }
      int* ptr;
   };
   
   void mathFunc(int x) {
       if (x == 0)
           throw std::runtime_error("divide by zero");
   }
   
   void manip(int parm) {
       std::cout << "In manip()\n";
       PTR obj;
       mathFunc(parm);
       // the program does not execute the lines from here:
       // --> leading to memory leakage
       delete[] obj.ptr;
       std::cout << "Leaving manip()\n";
   }
   
   int main() {
       try {
           manip(0); // This will throw!
       } catch (const std::exception& e) {
           std::cout << "Caught in main: " << e.what() << std::endl;
       }
       return 0;
   }
   
   // Output:
   // In manip()
   // Caught in main: divide by zero
   ```
* To resolve this issue, we have to use destructor to release resources allocated by constructor. Since C++ exception handling process respect the programming techique known as "resource acquisition is initialization; resource release is destruction". In other words: 
* If the block that exits has some local object that is of class type, the destructor for this object is called ***automatically*** by the stack unwinding process before the compound statement or function exits. For example:
   ```c++
   #include <iostream>
   #include <exception>
   
   
   class PTR {
   public:
      PTR() { ptr = new int[10]; }
      ~PTR() { delete[] ptr; }
      int* ptr;
   };
   
   void mathFunc(int x) {
       if (x == 0)
           throw std::runtime_error("divide by zero");
   }
   
   void manip(int parm) {
       std::cout << "In manip()\n";
       PTR obj;
       mathFunc(parm);
   
       // the program does not execute the lines from here,
       // but will call ~PTR(), preventing memory leakage
       std::cout << "Leaving manip()\n";
   }
   
   int main() {
       try {
           manip(0); // This will throw!
       } catch (const std::exception& e) {
           std::cout << "Caught in main: " << e.what() << std::endl;
       }
       return 0;
   }
   
   // Output:
   // In manip()
   // Caught in main: divide by zero
   ```

# Constructors and Function try Blocks
* How should we implement the constructor if we want to handle exceptions thrown by member initializer list?
   ```c++
   #include <iostream>
   #include <exception>
   
   int mathFunc(int x) {
       if (x == 0)
           throw std::runtime_error("divide by zero");
       return x;
   }
   
   class PTR {
   public:
      PTR(int x) : _x( mathFunc(x) ) {   }
   private:
      int _x;
   };
   
   int main() {
       PTR obj(0);
       return 0;
   }
   
   // Output:
   // terminate called after throwing an instance of 'std::runtime_error'
   //   what():  divide by zero
   // Aborted (core dumped)
   ```
* The solution is:
   ```c++
   #include <iostream>
   #include <exception>
   
   int mathFunc(int x) {
       if (x == 0)
           throw std::runtime_error("divide by zero");
       return x;
   }
   
   class PTR {
   public:
      PTR(int x)
      try  : _x( mathFunc(x) )
      {
   
      } catch (std::runtime_error& e){
         std::cout << "Caught divide by zero\n";
      }
   private:
      int _x;
   };
   
   int main() {
       PTR obj(0);
       return 0;
   }
   
   // Output:
   // Caught divide by zero
   // terminate called after throwing an instance of 'std::runtime_error'
   //   what():  divide by zero
   // Aborted (core dumped)
   ```
{% endraw %}