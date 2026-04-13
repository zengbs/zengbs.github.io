---
title: "The Try Block"
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: The Try Block
tags: [CPP]

---

* We will take the code below as an example throughout this section:
   ```c++
   #include <iostream>
   #include "iStack.h"
   
   int main() {
      iStack stack( 32 );
      stack.display();
      for ( int ix = 1; ix < 51; ++ix )
      {
         if ( ix % 3 == 0 )
            stack.push( ix );
         if ( ix % 4 == 0 )
            stack.display();
         if ( ix % 10 == 0) {
            int dummy;
            stack.pop( dummy );
            stack.display();
         }
      }
      return 0;
   }
   ```
* A try block must enclose the statements that can throw exceptions.
* Following the try block is a list of handlers called catch clauses. The try block groups a set of statements and associates with these statements a set of handlers to handle the exceptions that the statements can throw.
* Bad version: Its organization, however, intermixes the handling of the exceptions with the normal processing of the program and thus is not ideal. After all, exceptions are program anomalies that occur only in exceptional cases.
   ```c++
   for ( int ix = 1; ix < 51; ++ix ) {
      try { // try block for pushOnFull exceptions
         if ( ix % 3 == 0 )
            stack.push( ix );
         }
         catch ( pushOnFull ) { ... }
         
         if ( ix % 4 == 0 )
            stack.display();
            
         try { // try block for popOnEmpty exceptions
            if ( ix % 10 == 0 ) {
               int dummy;
               stack.pop( dummy );
               stack.display();
            }
         }
   }
   catch ( popOnEmpty ) { ... }
   ```
* Good version: We want to separate the code that handles the program anomalies from the code that implements the normal manipulation of the stack.
   ```c++
   try {
      for ( int ix = 1; ix < 51; ++ix )
      {
         if ( ix % 3 == 0 )
            stack.push( ix );
         if ( ix % 4 == 0 )
            stack.display();
         if ( ix % 10 == 0 ) {
            int dummy;
            stack.pop( dummy );
            stack.display();
         }
      }
   }
   catch ( pushOnFull ) { ... }
   catch ( popOnEmpty ) { ... }
   ```
* The program control flow in our example is one of the following:
   1. If no exception occurs, the code within the try block is executed and the handlers associated with the try block are ignored. The function `main()` returns 0.
   2. If the `push()` member function called within the first if statement of the for loop throws an exception, the second and third if statements of the for loop are ignored, the for loop and the try block are exited, and the handler for exceptions of type `pushOnFull` is executed.
   3. If the `pop()` member function called within the third if statement of the for loop throws an exception, the call to `display()` is ignored, the for loop and the try block are exited, and the handler for exceptions of type `popOnEmpty` is executed.
* When an exception is thrown, the statements following the statement that throws the exception are skipped. Program execution resumes in the catch clause handling the exception. If no catch clause capable of handling the exception exists, program execution resumes in the function terminate() defined in C++ standard library.
* A try block can contain any C++ statement — expressions as well as declarations. A try block introduces a local scope, and variables declared within a try block cannot be referred to outside the try block, including within the catch clauses. For example:
  ```c++
  int main() {
     try {
           iStack stack( 32 ); // ok: declaration in try block
           stack.display();
           for ( int ix = 1; ix < 51; ++ix )
           {
              // same as before
           }
        }
        catch ( pushOnFull ) {
        // cannot refer to stack here
        }
        catch ( popOnEmpty ) {
           // cannot refer to stack here
        }
     
     // cannot refer to stack here
     return 0;
  }
  ```
* It is possible to declare a function so that the entire body of the function is contained within the try block. In such a case, instead of placing the try block within the function definition we can enclose the function body within a function try block. This organization supports the cleanest separation between the code that supports the normal processing of the program and the code that supports the handling of the exceptions. For example:
   ```c++
   int main() {
   
      try {
         iStack stack( 32 );
         stack.display();
         for ( int ix = 1; ix < 51; ++ix )
         {
            // same as before
         }
         return 0;
      }
      
      catch ( pushOnFull ) {
         // cannot refer to stack here
      }
      catch ( popOnEmpty ) {
         // cannot refer to stack here
      }
      
   }
   ```
{% endraw %}