---
title: "Overloaded function declarations"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: Overloaded function declarations
tags: [CPP]

---

# Declarations
## Legal redeclaration
1. If both the return type and the parameter list of the two function declarations match exactly, the second declaration is treated as a redeclaration of the first.
    ```c++
    void print( const string &str );
    void print( const string & );    // redeclaration (legal)
    ```
2. Top-level cv-qualifiers are ignored when comparing parameter types.
	```c++
	void f( int );
	void f( const int ); // redeclaration (legal)
	```
1. If the parameter lists of the two functions differ only in their default arguments, the second declaration is treated as a redeclaration of the first.
	```c++
	int max( int *ia, int sz );
	int max( int *, int sz = 10 ); // legal
	```
## Erroneous redeclaration
1. If the parameter lists of the two functions differ only in that one uses a typedef and the other uses the type to which the typedef corresponds, the second declaration is treated as an erroneous redeclaration.
	```c++
	typedef double DOLLAR;
	extern DOLLAR calc( DOLLAR );
	extern int calc( double );    // error
	```
3. If the parameter lists of the two functions match exactly but the return types differ, the second declaration is treated as an erroneous redeclaration of the first and is flagged at compile-time as an error.
	```c++
	unsigned int max( int i1, int i2 );
	int max( int , int );                 // error: only return type is different
	```
## Overloaded function declarations

1. If the parameter lists of the two functions differ in either the number or type of their parameters, the two functions are considered to be overloaded.
	```c++
	void print( const string & );
	void print( vector<int> & ); // overloaded
	```


7. Low-level cv-qualifiers are considered part of the parameter type.
	```c++
	void f( int* );
	void f( const int* ); // overloaded
	```
	```c++
	void f( int& );
	void f( const int& ); // overloaded
	```
# Overloading and scope
The candidate functions are the union of the overloaded functions that 1) has the same name as the function called and 2) visible at the point of the call — including the functions introduced by using declarations and using directives — and 3) the member functions declared in the namespaces associated with the types of the arguments.

1. If the type of a function argument is declared within a namespace, the namespace member functions that have the same name as the function called are added to the set of candidate functions. I.e., [argument-dependent lookup (ADL)](https://en.wikipedia.org/wiki/Argument-dependent_name_lookup).
	```c++
	namespace NS {
	class C { /* ... */ };
	    void takeC( C& );
	}
	
	// the type of cobj is class C declared in namespace NS
	NS::C cobj;
	
	int main() {
	
	    // no takeC() visible at here
	    
	    takeC( cobj ); // ok: calls NS::takeC( C& )
	                   // because the argument is of type NS::C
	                   // the function takeC() declared in
	                   // namespace NS is considered
	return 0;
	}
	```
2. A locally declared function hides rather than overloads all functions declared at global scope.
	```c++
	#include<iostream>
	#include<string>
	
	void print( const std::string & );
	void print( double );
	
	void foo()
	{
	   extern void print( int );
	   // Candidate functions at here: print(int)
	   // local declaration hides both instances of global print()
	   print(1); // Call print(int)
	   print("abc"); // Error: print(const std::string&) is hidden in this scope
	   print(1.4); // Call print(int)
	}
	
	void print(const std::string&) { std::cout << "string" << std::endl; };
	void print(double) { std::cout << "double" << std::endl; };
	void print(int) { std::cout << "int" << std::endl; };
	
	int main(){
	   foo();
	   return 0;
	}
	```
    ```c++
    char* format( int );
    void g() {
        char* format( double );
        char* format( char* );
        
        // Candidate functions at here
        // format(double)
        // format(char*)
    }
    ```
2. A set of overloaded functions can also be declared within a class. TBD
3. A set of overloaded functions can also be declared within a namespace.
	```c++
	#include <string>
	
	namespace IBM {
	    extern void print( const string );
	    extern void print( double );
        // Candidates:
        // print(double)
        // print(const string)
	}
	namespace Disney {
	    extern void print( int );
        // Candidates:
        // print(int)
	}
	```
4.  using declaration vs. using directive
     ```c++
	 namespace libs_R_us {
		int max( int, int );
		double max( double, double );
	 }
	 char max( char, char );
	 void func()
	 {
		// Only the global function max( char, char ) is visible at here
	 }
    ```
    * A using declaration in local scope hides the global declaration
	    ```c++
		 namespace libs_R_us {
			int max( int, int );
			double max( double, double );
		 }
		 char max( char, char );
	     using libs_R_us::max;
		 void func()
		 {
	            // Candadiate at here:
	            // libs_R_us::max(int,int)
	            // libs_R_us::max(double,double)
	            // ::max(char,char)
		 }
	    ```
	    ```c++
		 namespace libs_R_us {
			int max( int, int );
			double max( double, double );
		 }
		 char max( char, char );
		 void func()
		 {
	            using libs_R_us::max;
	            // Candadiate at here:
	            // libs_R_us::max(int,int)
	            // libs_R_us::max(double,double)
	            // ::max( char, char ) is hidden
		 }
	    ```
    * A using directive is unaffected whether the using directive appears in local scope or in global scope since the declarations in the namespace `libs_R_us` has been lifted up the lowest common ancestor of the current namespace and the target namespace. I.e., global namespace. See [here](https://quuxplusone.github.io/blog/2020/12/21/using-directive/)
	    ```c++
		 namespace libs_R_us {
			int max( int, int );
			double max( double, double );
		 }
		 char max( char, char );
	     using namespace libs_R_us;
		 void func()
		 {
	            // Candadiate at here:
	            // libs_R_us::max(int,int)
	            // libs_R_us::max(double,double)
	            // ::max(char,char)
		 }
	    ```
	    ```c++
		 namespace libs_R_us {
			int max( int, int );
			double max( double, double );
		 }
		 char max( char, char );
		 void func()
		 {
	            using namespace libs_R_us;
	            // Candadiate at here:
	            // libs_R_us::max(int,int)
	            // libs_R_us::max(double,double)
	            // ::max( char, char )
		 }
	    ```

5. If the `using` declaration introduces a function in a scope that already has a function of the same name with the same parameter list, then the `using` declaration is in error.
	```c++
	namespace libs_R_us {
	    void print( int );
	    void print( double );
	}
	void print( int );
	using libs_R_us::print; // error: redeclaration of print(int)
	void fooBar( int ival )
	{
        // Cadidates: nothing
	}
	```
7. Multiple `using` directives are present. The member functions from different namespaces that have the same name are added to the same overload set.
	```c++
	namespace IBM {
	    int print(int);
	}
	namespace Disney {
	    double print(double);
	}
	// using directives:
	// form an overload set of functions from different namespaces
	using namespace IBM;
	using namespace Disney;
	long double print(long double);
	
	int main() {
        // Candidate functions:
        // IBM::print(int)
        // Disney::print(double)
        // long double print(long double)
	}
    ```

{% endraw %}