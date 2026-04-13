---
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

# Rules
1. Template argument deduction is done by comparing **each** function template parameter type with the type of the corresponding argument of the call.
3. The function parameter type and function argument type do not have to match exactly. The following type conversions can be applied to the function argument to convert it to the type of the corresponding function parameter:
    * If a function argument is **not** a reference type:
        * Lvalue transformations
            * lvalue-to-rvalue conversion
            * array-to-pointer conversion
            * function-to-pointer conversion
          ```c++
          #include <iostream>
          // 1. Lvalue-to-rvalue conversion
          template <typename T>
          void printValue(T x) {
              std::cout << "Lvalue-to-rvalue conversion: " << x << std::endl;
          }
          
          // 2. Array-to-pointer conversion
          template <typename T>
          void printArray(T arr) {
              std::cout << "Array-to-pointer conversion: First element = " << arr[0] << std::endl;
          }
          
          // 3. Function-to-pointer conversion
          template <typename T>
          void callFunction(T func) {
              func();  // Calls the function
          }
          
          // Example function to be passed
          void sampleFunction() {
              std::cout << "Function-to-pointer conversion" << std::endl;
          }
          
          int main() {
              // **1. Lvalue-to-rvalue conversion**
              int a = 42;
              printValue(a);  // Lvalue 'a' is converted to rvalue
          
              // **2. Array-to-pointer conversion**
              int arr[] = {10, 20, 30};
              printArray(arr); // Array 'arr' decays to pointer
          
              // **3. Function-to-pointer conversion**
              callFunction(sampleFunction); // Function name decays into a pointer
          
              return 0;
          }
          ```
        * Qualification conversions
          * The top level cv-qualifiers of arguments/parameters are ignored if `P` is not a reference type.
          * `A` can be another pointer or pointer to member type that can be converted to the deduced `A` via a qualification conversion.
            ```c++=
            #include <iostream>
            
            template <typename Type>
            Type min3( Type* const array, const int size) {
                Type min_value = array[0];
                for (int i = 1; i < size; ++i) {
                    if (array[i] < min_value) {
                        min_value = array[i];
                    }
                }
                return min_value;
            }
            
            int main() {
                int numbers[] = {42, 23, 56, 1, 78, 34, 89, 12, 5, 90};
                int* ptr1 = numbers;
                const int* ptr2 = numbers;
                int* const ptr3 = numbers;
                const int* const ptr4 = numbers;
            
                std::cout << min3(ptr1, 10) << std::endl;
            
                // error: Type = const int, resulting in min_value is read-only
                std::cout << min3(ptr2, 10) << std::endl;
            
                std::cout << min3(ptr3, 10) << std::endl;
            
                // error: Type = const int, resulting in min_value is read-only
                std::cout << min3(ptr4, 10) << std::endl;
            
                return 0;
            }
            ```
    * Derived class to base class type conversion, given that the function parameter has the form `T<args>`, `T<args>&`, or `T<args>*`, where the parameter list args contains at least one of the template parameters.
       ```c++
       #include <iostream>
       #include <typeinfo>
       
       template <typename T>
       struct Base {
           T value;
       };
       
       template <typename T>
       struct Derived : Base<T> { /* ... */ };
       
       template <typename T>
       void show(Base<T>& obj) {
           std::cout << "Template argument deduction succeeded! T = "
                     << typeid(T).name() << ", value = " << obj.value << "\n";
       }
       
       int main() {
           Derived<int> d;
           d.value = 42;
       
           show(d);
       
           return 0;
       }
       ```
4. If the same template parameter is found in more than one function parameter, the template argument deduced from each corresponding function argument must be the same type.
    ```c++=
    #include <iostream>
    
    template<typename T>
    void foo(T, T){ std::cout << "foo was called" << std::endl; }
    
    int main(){
       double d = 1.0;
       foo(1, d); // error: no matching function for call to ‘foo(int, double&)’
       foo(1.0, d); // foo was called
       return 0;
    }
    ```

# Example
1. Only the parameters that actually depend on the template parameters participate in template argument deduction.
	```c++
	#include <iostream>
	
	template<typename T>
	void foo(T, int){ std::cout << "foo was called" << std::endl; }
	
	int main(){
	   double d = 1.0;
	   foo(1, d); // foo was called
	   return 0;
	}   
	```
4.  template argument deduction/substitution failed:  couldn’t deduce template parameter `U`.
	```c++
	#include <iostream>
	
	template<typename T, typename U>
	void foo(T){ }
	
	int main(){
	   foo(2);
	   return 0;
	}
	```
 3.  Summary (14.8.2.1 Deducing template arguments from a function call [temp.deduct.call]):
     * If P is not a reference type:
         * The top level cv-qualifiers of A’s type are ignored for type deduction.
         *  The top level cv-qualifiers of P’s type are ignored for type deduction.
     *  If P is a reference type:
         *  The deduced A (i.e., the type referred to by the reference) can be more cv-qualified than A.
         *  The top level cv-qualifiers of P’s type are ignored for type deduction.
         *  The type referred to by P is used for type deduction.
     * A can be another pointer or pointer to member type that can be converted to the deduced A via a qualification conversion.
     ```c++
     #include <iostream>
     #include <type_traits>
     
     template <typename T>
     void func1(T param) {
         std::cout << std::is_const<T>::value << std::is_reference<T>::value << '\n';
     }
     
     template <typename T>
     void func2(const T param) {
         std::cout << std::is_const<T>::value << std::is_reference<T>::value << '\n';
     }
     
     template <typename T>
     void func3(T& param) {
         std::cout << std::is_const<T>::value << std::is_reference<T>::value << '\n';
     }
     
     template <typename T>
     void func4(const T& param) {
         std::cout << std::is_const<T>::value << std::is_reference<T>::value << '\n';
     }
     
     int main() {
         int i = 42;
         int& ri = i;
         const int ci = 100;
         const int& cri = ci;
     
         func1(i);    // 00
         func1(ci);   // 00
         func1(ri);   // 00
         func1(cri);  // 00
     
         func2(i);    // 00
         func2(ci);   // 00
         func2(ri);   // 00
         func2(cri);  // 00
     
         func3(i);    // 00
         func3(ci);   // 10
         func3(ri);   // 00
         func3(cri);  // 10
     
         func4(i);    // 00
         func4(ci);   // 00
         func4(ri);   // 00
         func4(cri);  // 00
     }
     ```
{% endraw %}