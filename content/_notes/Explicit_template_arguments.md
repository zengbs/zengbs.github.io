---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

1. When the template arguments are explicitly specified, there is no need to deduce the template arguments. 
	```c++
	#include<iostream>
	#include<typeinfo>
	
	template<typename T>
	void foo(T a, T b){
	   std::cout << typeid(a).name() << std::endl;
	   std::cout << typeid(b).name() << std::endl;
	}
	
	int main(){
	   // foo(unsigned int, unsigned int) instantiated
	   foo<unsigned int>(2U, 123);
	   return 0;
	}
	```
2. In the explicit specification we need only list the template arguments that cannot be implicitly deduced, with the constraint that, as with default arguments, we can omit only trailing arguments.
	```c++
	#include<iostream>
	#include<typeinfo>
	
	template<typename T1, typename T2, typename T3>
	void foo(T1 a, T2 b, T3 c){
	   std::cout << typeid(a).name() << std::endl;
	   std::cout << typeid(b).name() << std::endl;
	   std::cout << typeid(c).name() << std::endl;
	}
	
	int main(){
	   // instantiate foo(double,short,float)
	   foo<double, short>(2.0d, 123, 1.f);
	
	   // instantiate foo(int,int,float)
	   foo<int>(2.0d, 123, 1.f);
	
	   // instantiate foo(double,int,float)
	   foo<double>(2.0d, 123, 1.f);
	
	   
	   void (*pf)(double, int, short) = &foo<double>; 
	
	   // instantiate foo(double,int,short)
	   pf(2,4,5);
	
	   return 0;
	}
	```
{% endraw %}