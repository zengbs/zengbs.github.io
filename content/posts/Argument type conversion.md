---
title: "Argument type conversion"
date: 2026-04-13T15:32:36+08:00
draft: false
render_with_liquid: false
---

---
title: Argument type conversion
tags: [CPP]

---

# Implicit Conversion Sequence (ICS)
* An implicit conversion sequence is a sequence of conversions used to convert an argument in a function call to the type of the corresponding parameter of the function being called.  ⸺ [over.best.ics.general]/1
* A well-formed implicit conversion sequence is one of the following forms:
  * a standard conversion sequence,
  * a user-defined conversion sequence, or
  * an ellipsis conversion sequence.
⸺ [over.best.ics.general]/3
* Any difference in top-level cv-qualification is subsumed by the initialization itself and does not constitute a conversion. ⸺[over.ics.ref]/2

## Standard Conversion Sequence (SCS)
* Standard conversions are implicit conversions with built-in meaning. 7.3 enumerates the full set of such conversions. A standard conversion sequence is a sequence of standard conversions in the following order:
  * Zero or one conversion from the following set: lvalue-to-rvalue conversion, array-to-pointer conversion, and function-to-pointer conversion.
  * Zero or one conversion from the following set: integral promotions, floating-point promotion, integral conversions, floating-point conversions, floating-integral conversions, pointer conversions, pointer-to-member conversions, and boolean conversions.
  * Zero or one function pointer conversion.
  * Zero or one qualification conversion.
⸺ [conv.general]/1
* Table 16 summarizes the conversions defined in 7.3 and partitions them into four disjoint categories: Lvalue Transformation, Qualification Adjustment, Promotion, and Conversion. ⸺ [over.ics.scs]/1
* A standard conversion sequence either is the Identity conversion by itself (that is, no conversion) or consists of one to three conversions from the other four categories. If there are two or more conversions in the sequence, the conversions are applied in the canonical order: Lvalue Transformation, Promotion or Conversion, Qualification Adjustment. ⸺ [over.ics.scs]/2
* Each conversion in Table 16 also has an associated rank (Exact Match, Promotion, or Conversion). These are used to rank standard conversion sequences. The rank of a conversion sequence is determined by considering the rank of each conversion in the sequence and the rank of any reference binding. If any of those has Conversion rank, the sequence has Conversion rank; otherwise, if any of those has Promotion rank, the sequence has Promotion rank; otherwise, the sequence has Exact Match rank. ⸺ [over.ics.scs]/3
![image](https://hackmd.io/_uploads/ByltpwTeZl.png =70%x)


## User-Defined Conversion Sequence
## Ellipsis Conversion Sequence
An ellipsis conversion sequence occurs when an argument in a function call is matched with the ellipsis parameter specification of the function called. ⸺ [over.ics.ellipsis]/1
# Ranking Implicit Conversion Sequence

* When comparing the basic forms of implicit conversion sequences
  * a standard conversion sequence is a better conversion sequence than a user-defined conversion sequence or an ellipsis conversion sequence, and
  * a user-defined conversion sequence is a better conversion sequence than an ellipsis conversion sequence.
⸺ [over.ics.rank]/2

* The rank of a conversion sequence is the rank of the worst conversion that makes up the sequence.
    > If any of those has Conversion rank, the sequence has Conversion rank; otherwise, if any of those has Promotion rank, the sequence has Promotion rank; otherwise, the sequence has Exact Match rank. ⸺ [over.ics.scs]/3
    > When a parameter of reference type binds directly (9.4.4) to an argument expression, the implicit conversion sequence is the identity conversion, unless the argument expression has a type that is a derived class of the parameter type, in which case the implicit conversion sequence is a derived-to-base conversion. ⸺ [over.ics.ref]/1




## Ranking Standard Conversion Sequence
Standard conversion sequence `S1` is a better conversion sequence than standard conversion sequence `S2` if, when you follow the rules in §13.3.3.2 from top to bottom—at each step asking “is `S1` better than `S2`?”—you find a rule that favors `S1` and stop there; if you exhaust all the rules without a decision, `S1` and `S2` remain indistinguishable: 


0. Removing top-level cv-qualifiers. (added by me)
1. If parameter lists are the same, causing redefinition error. (added by me)
2. `S1` is a proper subsequence of `S2` (comparing the conversion sequences in the canonical form defined by 13.3.3.1.1, excluding any Lvalue Transformation; the identity conversion sequence is considered to be a subsequence of any non-identity conversion sequence) or, if not that, (PH: this step serves as a short circuit)
	```c++
	#include <iostream>
	
	void f(int) { std::cout << "A" << std::endl; }
	void f(short) { std::cout << "B" << std::endl; }
	
	int main() {
	    int a = 1;
	    f(a); // Calls f(int)
	    return 0;
	}
	```
	```c++
	#include <iostream>
	
	void f(int*) { std::cout << "A" << std::endl; }
	void f(const int*) { std::cout << "B" << std::endl; }
	
	int main() {
	    int a = 1;
	    f(&a); // Calls f(int*)
	    return 0;
	}
	```
2.  The rank of `S1` is better than the rank of `S2`, or, if not that,
	```c++
	#include <iostream>
	
	void f(int) { std::cout << "A" << std::endl; }
	void f(unsigned short) { std::cout << "B" << std::endl; }
	
	int main() {
	    short a = 1;
	    f(a);
	    return 0;
	}
	```
3.  `S1` and `S2` differ only in their qualification conversion and yield [similar](https://hackmd.io/3zUNdV0_THKZYofTSF-D-w?view) types `T1` and `T2` (4.4), respectively, and the cv-qualification signature of type `T1` is a proper subset of the cv-qualification signature of type `T2`.
    ```c++
    #include <iostream>
    
    void foo(int*){ std::cout << "A\n"; };
    void foo(const int*){ std::cout << "B\n"; };
    
    int main() {
    
        int value = 1;
    
        foo(&value);
    
        return 0;
    }
    ```
    ```c++
    #include <iostream>
    
    void foo(int * *       volatile * volatile const * const){ std::cout << "A\n"; };
    void foo(int * * const volatile * volatile const * const){ std::cout << "B\n"; };
    
    int main() {
    
        int value = 1;
    
        int *                            r  = &value;
        int * * volatile                 s  = &r;
        int * * volatile *               t  = &s;
        int * * volatile * const * const u = &t;
    
        foo(u); // A, both foo() are overloaded
    
        return 0;
    }
    ```
    ```c++
    #include <iostream>
    
    void foo(int *          * volatile * volatile const * const){ std::cout << "A\n"; };
    void foo(int * volatile * volatile * volatile const * const){ std::cout << "B\n"; };
    
    int main() {
    
        int value = 1;
    
        int *                            r  = &value;
        int * * volatile                 s  = &r;
        int * * volatile *               t  = &s;
        int * * volatile * const * const u = &t;
    
        foo(u); // A, not because of overloading but u cannot be converted to
                // int * volatile * volatile * volatile const * const
    
        return 0;
    }
    ```
    ```c++
    #include <iostream>
    
    void foo(int * *       volatile * volatile const * const){ std::cout << "A\n"; };
    void foo(int * * const volatile *          const * const){ std::cout << "B\n"; };
    
    int main() {
    
        int value = 1;
    
        int *                            r  = &value;
        int * * volatile                 s  = &r;
        int * * volatile *               t  = &s;
        int * * volatile * const * const u = &t;
    
        foo(u); // ambiguous
    
        return 0;
    }
    ```
5. `S1` and `S2` are reference bindings (8.5.3), and the types to which the references refer are the same type except for top-level cv-qualifiers, and the type to which the reference initialized by `S2` refers is more cv-qualified than the type to which the reference initialized by `S1` refers.
	```c++
	#include <iostream>
	
	void f(const int&) { std::cout << "A" << std::endl; }
	void f(volatile int&) { std::cout << "B" << std::endl; }
	
	int main() {
	   int a = 1;
	   f(a); // Error: ambiguous call
	   return 0;
	}
	```
	```c++
	#include <iostream>
	
	void f(const volatile int&) { std::cout << "A" << std::endl; }
	void f(volatile int&) { std::cout << "B" << std::endl; }
	
	int main() {
	   int a = 1;
	   f(a); // Calls f(volatile int&)
	   return 0;
	}
	```

## Ranking User-Defined Conversion Sequence



# Flowchart
![Ranking implicit conversion](https://hackmd.io/_uploads/BJHVX8fvll.jpg =60%x)


# Exact match
## lvalue-to-rvalue conversion
* If the argument is pass-by-value, an lvalue-to-rvalue conversion is performed.
	```c++
	#include <string>
	std::string color( "purple" );
	void print( std::string );
	
	int main() {
	   print( color ); // exact match: lvalue-to-rvalue conversion
	   return 0;
	}
	```
	The argument in the call to `print(color)` is passed by value, an lvalue-to-rvalue conversion takes place to extract a value from color and pass it to `print(string)`.
* If the argument is pass-by-reference, there is no lvalue-to-rvalue conversion applied to an argument.
## array-to-pointer conversion
```c++
int ai[3];
void putValues(int *);
int main() {
   // ...
   putValues(ai); // exact match: array-to-pointer conversion
   return 0;
}
```
## function-to-pointer conversion
```c++
int lexicoCompare( const string &, const string & );
typedef int (*PFI)( const string &, const string & );
void sort( string *, string *, PFI );
string as[10];
int main()
{
   // ...
   sort( as,
   as + sizeof(as)/sizeof(as[0] - 1),
   lexicoCompare // exact match:
   // function-to-pointer conversion
   );
   return 0;
}
```
## qualification conversion
See [Qualification conversions](/3zUNdV0_THKZYofTSF-D-w)

# Promotions
# Conversions
# Reference binding

![Reference binding(4)](https://hackmd.io/_uploads/ByI7UBb-be.jpg)


1. When a parameter of reference type binds directly to an argument expression, the implicit conversion sequence is the identity conversion, unless the argument expression has a type that is a derived class of the parameter type, in which case the implicit conversion sequence is a derived-to-base conversion. ⸺[over.ics.ref]/1
    * Example: parameter of reference type binds directly to an expression:
	  ```c++
	  #include<iostream>
	  
	  void print(int ){};
	  void print(int&){};
	  
	  int main(){
	     int i = 1;
         // print(int) requires lvalue-to-rvalue conversion (exact match)
         // print(int&) is in the identity catagory (exact match)
         // Following the ranking comparison,
         // S1 and S2 remain indistinguishable under all subsequent tiebreaker rules.
	     int& ri = i;
	     print(ri);   // Error: ambiguous
         
         // calls print(int) since print(int) is the only one viable function
	     print(1);
	     return 0;
	  }
	  ```
    * Example: derived-to-base conversion has Conversion rank.
      ```c++
      #include<iostream>
      
      class A { };
      class B : public A { };
      
      void f(A&) {}
      void f(B&) {}
      
      int main() {
         B b;
      
         // calls f(B&), an exact match, rather than f(A&), a conversion
         f(b);
      }
      ```
2. If the parameter binds directly to the result of applying a conversion function to the argument expression, the implicit conversion sequence is a user-defined conversion sequence, with the second standard conversion sequence either an identity conversion or, if the conversion function returns an entity of a type that is a derived class of the parameter type, a derived-to-base conversion. ⸺[over.ics.ref]/1
4. When a parameter of reference type is not bound directly to an argument expression, the conversion sequence is the one required to convert the argument expression to the referenced type according to 12.4.4.2. Conceptually, this conversion sequence corresponds to copy-initializing a temporary of the referenced type with the argument expression. Any difference in top-level cv-qualification is subsumed by the initialization itself and does not constitute a conversion. ⸺[over.ics.ref]/2
   ```c++
   #include<iostream>
   
   void print(int ){};
   void print(const int&){};
   
   int main(){
      short i = 1;
         // print(int) requires lvalue-to-rvalue conversion
         // and integral promotion (Promotion)
         // print(const int&) requires promotion too
         // specifically, compiler first convert the argument `short` to `int`,
         // then copy-initializes a temporary `int` with the result of conversion,
         // and finally binds the reference to the temporary
      print(i);    // Error: ambiguous
      return 0;
   }
   ```
   ```c++
   #include<iostream>
   
   class B {
   public:
      B(unsigned int ui):value(ui){}
   private:
      unsigned int value;
   };
   
   class A {
   public:
      A(int i):value(i){}
   
      // Conversion A => B
      operator B() {
         return B(static_cast<unsigned int>(value));
      }
   
   private:
      int value;
   };
   
   void foo(const B&){ std::cout << "A\n"; }
   
   int main(){
   
      A a(1);
   
      // foo(const B&): user-defined conversion
      // const is required as a temporary object with type B will be created.
      foo(a);
   }
   ```
	```c++
	#include<iostream>
	
	void print(int& a){ std::cout<< a << std::endl; };
	
	int main(){
	   double d = 3;
	   print(d);
	   return 0;
	}
	```
	However, if the reference parameter is `const`, the conversion is allowed.
	```c++
	#include<iostream>
	
	// Step 1: Convert double to a Temporary int (lvalue-to-rvalue conversion)
	// Step 2: Bind const int& to the Temporary int
	// Step 3: Use a in print()
	void print(const int& a){ std::cout<< a << std::endl; };
	
	int main(){
	   double d = 3;
	   print(d);
	   return 0;
	}
	```