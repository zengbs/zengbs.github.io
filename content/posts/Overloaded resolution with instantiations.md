---
title: "Overloaded resolution with instantiations"
date: 2026-04-13T15:32:37+08:00
draft: false
---

---
title: Overloaded resolution with instantiations
tags: [CPP]

---

How function overload resolution proceeds when function template instantiations, function template specializations, and ordinary functions of the same name are involved:
1. Build the set of candidate functions.
    Function templates with the same name as the function called are considered. If template argument deduction succeeds with the function call arguments, a function template is instantiated, or if a template specialization exists for the template argument deduced, the template specialization is a candidate function.
2. Build the set of viable functions.
From the set of candidate functions, keep only the functions that can be called with the function call arguments.
3. Rank the type conversions.
    a. If only one function is selected, call this function.
    b. If the call is ambiguous, remove the function template instantiations from the set of viable functions.
4. Perform overload resolution considering only the ordinary functions in the set of viable functions.
    a. If only one function is selected, call this function.
    b. Otherwise, the call is ambiguous.
    
    
# Example
1. The template type deduction succeeds, and exactly match the type of template arguments.
	```c++
	#include <iostream>
	
	template <class T>
	void foo(T, int){
	   std::cout << "Version 1" << std::endl;
	}
	
	void foo(double, double){
	   std::cout << "Version 2" << std::endl;
	};
	
	int main(){
	
	   // Calls "Version 1"
	   foo(2.0, 1);
	
	   return 0;
	}
	```
2. A function template instantiation is entered in the set of candidate functions only if template argument deduction succeeds.
	```c++
	#include <iostream>
	
	template <class T>
	void foo(T*, int){
	   std::cout << "Version 1" << std::endl;
	}
	
	void foo(double, double){
	   std::cout << "Version 2" << std::endl;
	};
	
	int main(){
	
	   // Calls "Version 2"
	   // Since we fail to decuce T in "Version 1"
	   foo(2.0, 1);
	
	   return 0;
	}
	```
3. What if template argument deduction succeeds but the template is explicitly specialized for the template arguments deduced?
	```c++
	#include <iostream>
	
	template <class T>
	void foo(T, int){
	   std::cout << "Version 1" << std::endl;
	}
	
	template<>
	void foo<double>(double, int){
	   std::cout << "Version 2" << std::endl;
	}
	
	void foo(double, double){
	   std::cout << "Version 3" << std::endl;
	};
	
	int main(){
	
	   // Calls "Version 2"
	   // Priority of specializd template is higher than generic template
	   foo(2.0, 1);
	
	   return 0;
	}
	```
 4. Template explicit specializations are not automatically entered in the set of candidate functions. Only if template argument deduction succeeds is a template explicit specialization considered for a function call.
	 ```c++
	 #include <iostream>
	
	template <class T>
	void foo(T, T){
	   std::cout << "Version 1" << std::endl;
	}
	
	template<>
	void foo<double>(double, double){
	   std::cout << "Version 2" << std::endl;
	}
	
	void foo(double, double){
	   std::cout << "Version 3" << std::endl;
	};
	
	int main(){
	
	   // Calls "Version 3"
	   foo(2.0, 1);
	
	   return 0;
	}
	```
 5. A function call could match equally well this ordinary function and a function instantiated from the function template.
	 ```c++
	 #include <iostream>
	
	template <class T>
	void foo(T){
	   std::cout << "Version 1" << std::endl;
	}
	
	void foo(double){
	   std::cout << "Version 2" << std::endl;
	};
	
	int main(){
	
	   // Calls "Version 2"
	   foo(2.0);
	
	   return 0;
	}
	```
 6. Once function overload resolution resolves a call to an ordinary function, there is no going back later if the program does not contain a definition of this function.
	```c++
	#include <iostream>
	
	template <class T>
	void foo(T){
	   std::cout << "Version 1" << std::endl;
	}
	
	void foo(double);
	
	int main(){
	
	   // Error: undefined reference
	   foo(2.0);
	
	   return 0;
	}
	```
  7. Suppose that we want to define a function template specialization `foo<int>(int,int)` and we want this function to be invoked when `foo()` is called with arguments of any integer type, whether or not the arguments have the same type.
		```c++
		#include <iostream>
		
		template <class T>
		void foo(T, int){
		   std::cout << "Version 1" << std::endl;
		}
		
		void foo(int a, int b){
		   foo<int>(a, b);
		}
		
		int main(){
		
		   short s = 1;
		
		   // Calls "Version 1"
           // Note that there are no candidate functions for this call
		   foo(2, s);
		
		   return 0;
		}
		```