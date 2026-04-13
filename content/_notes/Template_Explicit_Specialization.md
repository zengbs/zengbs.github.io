---
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

# Example
```c++
#include<iostream>

template<typename T>
void foo(T){ std::cout << "Generic template" << std::endl; }

template<>
void foo<int>(int){ std::cout << "Specialized template" << std::endl; }

int main(){
   foo(1); // Specialized template
   return 0;
}
```
# Rules
1. The function parameter list cannot be omitted from the specialization declaration.
2. The explicit specification of the template arguments can be omitted from the explicit specialization declaration if the template arguments can be deduced from the function parameters.
3. Omitting the `template<>` portion of an explicit specialization declaration is not always an error.
4. A function template explicit specialization can be declared even if the function template that it specializes is declared but not defined.
5. The declaration of a function template explicit specialization must be seen before it is used in a source file.
	```c++
	#include<iostream>
	
	template<typename T> void foo(T);
	
	//template<> void foo<int>; // Error: missing parameter list (rule 1)
	
	// OK: explicit spcialization can be declared even if the generc template is not defined (rule 4)
	// OK: template argument deduced from parameter types (rule 2)
	// OK: The declaration of a function template explicit specialization must be seen
	//     before it is used in the source file. (rule 5)
	template<> void foo(int); 
	
	//void foo(int); // OK: declare an ordinary function but need to define (rule 3)
	
	int main(){
	   foo(1);
	   return 0;
	}
	
	template<typename T>
	void foo(T){ std::cout << "Generic template" << std::endl; }
	
	template<>
	void foo<int>(int){ std::cout << "Specialized template" << std::endl; }
	```
7. The explicit specialized template must be declared in every translation unit in which such a use occurs; otherwise no diagnostic required.
    > [ISO 14882-1998 14.7.3.6] If a template, a member template or the member of a class template is explicitly specialized then that specialization shall be declared before the first use of that specialization that would cause an implicit instantiation to take place, in every translation unit in which such a use occurs; no diagnostic is required.

    In the example below, there is no the declaration of specialized template in`File1.cc`, so the example results undefined behavior without any error and warning.
	```c++
    // max.h
	template <class Type>
	void max( Type t ) {
	   std::cout << "Generic template" << std::endl;
	}
	```
	```c++
    // File.cc
	#include <iostream>
	#include "max.h"
	
	void another();
	
	int main() {
	    // Calls specialized template
	    max( "hello");
	    another();
	    return 0;
	}
	```
	```c++
    // File2.cc
	include <iostream>
	#include <cstring>
	# include "max.h"
	
	typedef const char *PCC;
	template<> void max< PCC >( PCC s ) {
	   std::cout<<"Specialized template"<<std::endl;
	}
	
	void another() {
	   // Calls specialized template
	   max( "hi");
	}
	```
{% endraw %}