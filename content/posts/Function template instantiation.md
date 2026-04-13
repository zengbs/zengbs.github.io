---
title: "Function template instantiation"
date: 2026-04-13T15:32:37+08:00
draft: false
---

---
title: Function template instantiation
tags: [CPP]

---

1. A function template is instantiated either (1) when it is invoked or (2) when its address is taken.
	```c++=
	#include <iostream>
	
	template <typename T>
	void foo(T t){ std::cout << t << std::endl; };
	
	int main(){
	   foo(1);
	   void (*pf)(int) = &foo;
	   pf(2);
	   return 0;
	}
	```
2. When the address of a function template instantiation is taken, the context must be such that it allows a unique type or value to be determined for a template argument.
	```c++
	#include <iostream>
	
	template <typename Type, int size>
	Type min(Type (&r_array)[size]) {
	    Type m = r_array[0];
	    for (int i = 1; i < size; ++i) {
	        if (r_array[i] < m)
	            m = r_array[i];
	    }
	    return m;
	}
	
	typedef double (&rad)[3];
	
	void func(int (*f)(int (&)[4])) {
	    int arr[4] = {9, 3, 5, -1};
	    std::cout << "Minimum int: " << f(arr) << std::endl;
	}
	
	void func(double (*f)(rad)) {
	    double arr[3] = {9.1, 3.2, 19.0};
	    std::cout << "Minimum double: " << f(arr) << std::endl;
	}
	
	int main() {
	    // Error: ambiguous call
	    func(&min);
	
	    // This call selects the instantiation: double min(double (&)[3]).
	    func(static_cast<double(*)(rad)>(&min));
	
	    // This call selects the instantiation: int min(int (&)[4]).
	    func(static_cast<int(*)(int (&)[4])>(&min));
	
	    return 0;
	}
	```