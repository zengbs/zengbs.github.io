---
title: "Catching an Exception"
date: 2026-04-13T15:32:36+08:00
draft: false
---

---
title: Catching an Exception
tags: [CPP]

---

![Throwing Exception](https://hackmd.io/_uploads/S1VY70lHlg.jpg =60%x)

* A C++ exception handler is a catch clause. When an exception is thrown from statements within a try block, the list of catch clauses that follows the try block is searched to find a catch clause that can handle the exception.
* A catch clause consists of three parts: the keyword `catch`, the declaration of a single type or single object within parentheses (referred to as an exception declaration), and a set of statements within a compound statement.
* A handler is selected to handle an exception if the type of its exception declaration matches the type of the exception thrown. 
* After a catch clause has completed its work, the execution of the program continues at the statement that follows the last catch clause in the list. 

```c++
#include <vector>
#include <iostream>

template<class T> class pushOnFull;
template<class T> class popOnEmpty;

template<class T>
class Stack {
public:
   Stack(int len) : _len(len) {}
   void push( const T& e );
   void pop();
   int len() { return _len; }
private:
   std::vector<T> vec;
   int _len;
};


template<class T>
void Stack<T>::push( const T& e ){
   if ( vec.size() >= _len ){
      throw pushOnFull<T>(e);
   }
   vec.emplace_back(e);
}

template<class T>
void Stack<T>::pop(){
   if ( vec.size() == 0 ){
      throw popOnEmpty<T>();
   }
   vec.pop_back();
}

template<class T>
class pushOnFull {
public:
   pushOnFull(T value) : _val(value){}
   int value() { return _val; }
private:
   T _val;
};


template<class T>
class popOnEmpty {
public:
   popOnEmpty() = default;
};

int main()
{
   try {

      Stack<float>* s = new Stack<float>(2);

      s->push(3.0f);
      s->push(2.0f);
      s->push(1.0f);

      return 0;
   }
   catch ( popOnEmpty<float>& e){
      std::cerr << "Pop on empty stack!\n";
   }
   catch ( pushOnFull<float>& e ){
      std::cerr << "Push " << e.value() << " on full stack!\n";
   }
   catch (...) {

   }

   std::cerr << "Finished the program\n";
}
```

# Exception Objects
* When should the exception declaration in a catch clause declare an object? An object should be declared when it is necessary to obtain the value or manipulate the exception object created by the throw expression. If we design our exception classes to store information in the exception object when the exception is thrown and if the exception declaration of the catch clause declares an object, the statements within the catch clause can use this object to refer to the information stored by the throw expression.
* Without copy elision, an temporary object is always created at the throw point even though the throw expression is a constructor call.
   ```c++
   #include <iostream>
   
   struct ErrorCode {
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
   
   void mathFunc(int i) {
       if (i == 0) {
           throw ErrorCode(42);   // calls ctor for temporary object
                                  // calls copy ctor for exception object
       }                          // calls destructor for the temporary object
   }
   
   int main() {
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
   ```
   # g++ main.cc (with copy elision, mandatory from C++11)
   ErrorCode: constructor called. this: 0x565312d1ef30
   Caught error with code = 42
   ErrorCode: destructor called. this: 0x565312d1ef30
   ```
* No matter whether copy elision exists, an exception object is always created at the throw point even though the throw expression is not a constructor call and even though it doesn't appear to be creating an exception object.
   ```c++
   #include <iostream>
   
   struct ErrorCode {
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
   
   void mathFunc(int i) {
       if (i == 0) {
           ErrorCode err(42);  // calls ctor for object A
           throw err;          // calls copy ctor for object B
       }                       // calss destructor for object A
   }
   
   int main() {
       try {
           mathFunc(0);
       } catch (ErrorCode& e) {
           std::cout << "Caught error with code = " << e.code << "\n";
       } // calls destructor for object B
   }
   ```
   So calling constructor at throw point is more efficient.
* The exception declaration of a catch clause behaves very much like a parameter declaration. When a catch clause is entered, if the exception declaration declares an object, this object is initialized with a copy of the exception object (similar to pass-by-value).
   ```c++
   #include <iostream>
   
   struct ErrorCode {
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
   
   void mathFunc(int i) {
       if (i == 0) {
           ErrorCode err(42);  // calls ctor for object A
           throw err;          // calls copy ctor for object B
       }                       // calss destructor for objects A
   }
   
   int main() {
       try {
           mathFunc(0);
       } catch (ErrorCode e) { // calls copy ctor for object C
           std::cout << "Caught error with code = " << e.code << "\n";
       } // calls destructor for objects C and B in turn
   }
   ```
* As is the case for function parameters, the exception declaration of a catch clause can be changed to a reference declaration. The catch clause then directly refers to the exception object created by the throw expression instead of creating a local copy.
* For the same reasons that parameters of class type should be declared as references to prevent unnecessary copying of large class objects, it is also preferable if exception declarations for exceptions of class type are declared as references.
* With an exception declaration of reference type, the catch clause is able to modify the exception object. However, any variable specified by the throw expression remains unaffected. 
   ```c++
   #include <iostream>
   
   struct ErrorCode {
       ErrorCode(int c) : code(c) {
           std::cout << "ErrorCode: constructor called. this: " << this << "\n";
       }
       ErrorCode(const ErrorCode& other) : code(other.code) {
           std::cout << "ErrorCode: copy constructor called. this: " << this << "\n";
       }
       ~ErrorCode() {
           std::cout << "ErrorCode: destructor called. this: " << this << "\n";
       }
       int code;
   };
   
   ErrorCode g_e(2);  // calls ctor for g_e
   
   void mathFunc(int i) {
       if (i == 0) {
           throw g_e;     // calls copy ctor for copied g_e
       }
   }
   
   int main() {
   
       try {
           mathFunc(0);
       } catch (ErrorCode &e) {
           std::cout << "code = " << e.code << "\n"; // 2
           e.code = 3;
           std::cout << "code = " << e.code << "\n"; // 3
       } // calls destructor for copied g_e
   
       std::cout << "code = " << g_e.code << "\n"; // 2
   
   } // calls destructor for g_e
   ```
* The assignment modifies in exception handler affectes only the exception object created by the throw expression.


# Stack Unwinding
* The search for a catch clause to handle a thrown exception proceeds as follows: if the throw expression is located within a try block, the catch clauses associated with this try block are examined to see whether one of these clauses can handle the exception. If a catch clause is found, the exception is handled. If no catch clause is found, the search continues in the calling function. If the call to the function exiting with the thrown exception is located within a try block, the catch clauses associated with this try block are examined to see whether one can handle the exception. If a catch clause is found, the exception is handled. If no catch clause is found, the search continues in the calling function. This process continues up the chain of nested function calls until a catch clause for the exception is found. As soon as a catch clause that can handle the exception is encountered, the catch clause is entered and the execution of the program continues within this handler.
* The process by which compound statements and function definitions exit because of a thrown exception in the search for a catch clause to handle the exception is called stack unwinding.
*  As the stack is unwound, the lifetime of local objects declared in the compound statements and in function definitions that are exited ends. C++ guarantees that, as the stack is unwound, the destructors for local class objects are called even though their lifetime ends because of a thrown exception.
   ```c++
   #include <iostream>
   
   
   class Tracker {
   public:
   
      Tracker( const std::string& name ) : _name(name)
      { std::cout << "calls ctor " << _name << "\n"; }
      
      ~Tracker() { std::cout << "calls destructor " << _name << "\n"; }
   
   private:
      std::string _name;
   
   };
   
   void level3(){
      Tracker t3("in level 3");
      throw std::runtime_error("Exception thrown in level3");
   }
   
   void level2(){
      Tracker t2("in level 2");
      level3();
   }
   
   void level1(){
      Tracker t1("in level 1");
      level2();
   }
   
   int main(){
       try {
           level1();
       } catch (const std::exception& e) {
           std::cout << "Caught exception: " << e.what() << std::endl;
       }
   }
   ```
* What if the program does not provide a catch clause for the exception that is thrown? An exception cannot remain unhandled.
*  If no handler is found, the program calls the `terminate()` function defined in the C++ standard library. The default behavior of `terminate()` is to call `abort()`, indicating the abnormal exit from the program. 
* The compiler cannot inform users when no handler exists for an exception. This is why the `terminate()` function exists: it is a run-time mechanism to tell users when no handler matches the exception thrown.


# Rethrow
* It is possible that a single catch clause cannot completely handle an exception. After some corrective actions, a catch clause may decide that the exception must be handled by a function further up the list of function calls. A catch clause can pass the exception to another catch clause further up the list of function calls by rethrowing the exception.
* The exception that is rethrown is the original exception object.
   ```c++
   #include <iostream>
   #include <stdexcept>  // for std::runtime_error
   
   struct ErrorCode {
       ErrorCode(int c) : code(c) {
           std::cout << "ErrorCode: constructor called. this: " << this << "\n";
       }
       ErrorCode(const ErrorCode& other) : code(other.code) {
           std::cout << "ErrorCode: copy constructor called. this: " << this << "\n";
       }
       ~ErrorCode() {
           std::cout << "ErrorCode: destructor called. this: " << this << "\n";
       }
       int code;
   };
   
   
   void inner () {
      std::cout << "Calls inner()\n";
      throw ErrorCode(0); // ctor for object A
   }
   
   void outer () {
      try {
         std::cout << "Calls outer()\n";
         inner();
      } catch ( const ErrorCode& e ) {
         std::cout << "Intermediate hadler: code = " << e.code << "\n";
   
         //  Doing partial handling, then rethrowing...
   
         throw;
      }
   }
   
   
   int main(){
      try {
         outer();
      } catch ( const ErrorCode& e ) {
         std::cout << "Final handler: code = " << e.code << "\n";
      }
   }
   ```
   ```
   Calls outer()
   Calls inner()
   ErrorCode: constructor called. this: 0x5569787fd340
   Intermediate hadler: code = 0
   Final handler: code = 0
   ErrorCode: destructor called. this: 0x5569787fd340
   ```
* Another good reason to declare the exception declaration of the catch clause as a reference is to ensure that modifications applied to the exception object within the catch clause are reflected in the exception object that is rethrown. 

# The Catch-All Handler
* A function may want to perform some action before it exits with a thrown exception even though it cannot handle the exception that is thrown.
* The release of the resource res is bypassed if an exception is thrown. To guarantee that the resource is released, rather than provide a specific catch clause for every possible exception and because we can't know all the exceptions that might be thrown, we can use a catch-all catch clause.
* A `catch(...)` is used in combination with a rethrow expression.
   ```c++
   #include <iostream>
   #include <stdexcept>
   
   class Resource {
   public:
       Resource()  { std::cout << "Resource acquired.\n"; }
       ~Resource() { std::cout << "Resource released.\n"; }
   };
   
   void riskyFunction() {
       Resource* res = new Resource();
   
       try {
           std::cout << "riskyFunction(): Doing something risky...\n";
           throw std::runtime_error("Boom! Something went wrong.");
       } catch (...) {
           std::cout << "riskyFunction(): Exception caught. Cleaning up before rethrow.\n";
           delete res;  // Manual cleanup (if not using RAII)
           throw;       // Rethrow current exception
       }
   }
   
   int main() {
       try {
           riskyFunction();
       } catch (const std::exception& e) {
           std::cout << "main(): Exception handled: " << e.what() << "\n";
       }
   
       return 0;
   }
   ```
* Catch clauses are examined in turn, in the order in which they appear following the try block. Once a match is found, subsequent catch clauses are not examined. This implies that if a `catch (...)` is used in combination with other catch clauses, it must always be placed last in a list of exception handlers; otherwise, a compiler error is issued.