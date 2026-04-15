---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

<img src="https://hackmd.io/_uploads/SJ-lQ4QWex.jpg" width="30%" alt="Template(3)">


# Syntax rules
1. If an object, function, or type having the same name as the template parameter is declared in global scope, the global scope name is hidden.
	```c++
	#include <iostream>
	
	typedef double Type;
	int a = 2;
	
	template <typename Type>
	void foo(Type a)
	{
	   std::cout << "Type of a is " << typeid(a).name() << std::endl;
	   std::cout << "a = " << a << std::endl;
	}
	
	int main(){
	    // Type of a is i
	    // a = 1
	   foo(1);
	   return 0;
	}
	```
3. An object or type declared within the function template definition cannot have the same name as that of a template paramete.
	```c++
	#include <iostream>
	
	template <typename Type>
	void foo(Type a)
	{
	   typedef double Type; // error:  declaration of ‘int a’ shadows a parameter
	   int a = 2; // error:  declaration of ‘int a’ shadows a parameter
	   std::cout << "Type of a is " << typeid(a).name() << std::endl;
	   std::cout << "a = " << a << std::endl;
	}
	
	int main(){
	   foo(1);
	   return 0;
	}
	```
5. If a function template has more than one template type parameter, each template type parameter must be preceded by the keyword `class` or the keyword `typename`.
	```c++
	#include <iostream>
	
	template <typename T, U> // error: ‘U’ has not been declared
	void foo(T a, U b) { }
	
	int main(){
	   foo(1, 1.0f);
	   return 0;
	}
	```
7. In a function template parameter list, the keywords `typename` and `class` have the same meaning and can be used interchangeably.
	```c++
	#include <iostream>
	
	template <typename T, class U>
    void foo(T a, U b) { }
	
	int main(){
	   foo(1, 1.0f);
	   return 0;
	}
	```
9. It is impossible for the compiler to identify which expressions are types in a template definition. Always put `typename` before a dependent name (the name depends on `T`, like `T::value_type`):
	```c++
	#include <iostream>
	
	// A type with a nested type 'name'.
	struct MyType
	{
	    typedef int name;  // 'name' is a type
	    int value;
	
	    MyType(int v = 0) : value(v) {}
	};
	
	// Define an operator- for MyType so we can do array[0] - value.
	MyType operator-(const MyType& lhs, int rhs)
	{
	    return MyType(lhs.value - rhs);
	}
	
	template <class Parm, class U>
	Parm minusFunc(Parm* array, U value)
	{
	    // Without 'typename', this line causes a compiler error in a template,
	    // because the compiler cannot be certain 'Parm::name' is a type.
	    typename Parm::name* p = 0;  // explicitly state 'Parm::name' is a type
	    (void)p;                     // just to use 'p' so we don't get an unused variable warning
	
	    // Perform some operation to demonstrate the function works.
	    return array[0] - value;
	}
	
	int main()
	{
	    MyType arr[1] = { MyType(42) };
	    MyType result = minusFunc(arr, 2);
	    std::cout << "Result = " << result.value << std::endl; // Expect 40
	    return 0;
	}
	```
 7. A function template can be declared `inline` or `extern` in the same way as a nontemplate function. The specifier is placed following the template parameter list.
	```c++
	#include <iostream>
	
	template <class T> inline
	void foo(T) { }
	
	int main(){
	   foo(1);
	   return 0;
	}
	```
{% endraw %}