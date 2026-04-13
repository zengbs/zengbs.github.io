---
date: 2026-04-13T15:32:36+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---

1. Class names cannot be overloaded.
2. The list with `<` and `>` is referred to as the template parameter list of the class template. It cannot be empty.
3. Each template type parameter must be preceded by the keyword `class` or the keyword `typename`.
4. A template nontype parameter consists of an ordinary parameter declaration. A nontype parameter indicates that the parameter name represents a potential value. This value represents a constant in the class template definition.
    ```c++
    template <sisz_t size = 1024>
    class Buffer;
    ```
5. If a variable with the same name as the template parameter is declared in global scope, that name is hidden.
6. The name of a template parameter cannot be used as the name for a class member declared within the class template definition.
7. The name of a template parameter can be introduced only once within the template parameter list.
8. The name of a template parameter can be reused across class template declarations or definitions.
9. The names of the template parameters do not need to be the same across forward declarations and the definition of the class template.
    ```c++
    template <class T>
    struct Buffer;
    
    template <class U>
    struct Buffer{
    };
    
    int main() {
      Buffer<int> buf;
      return 0;
    }
    ```
10. The parameters of a class template can have default arguments. This is true whether the parameter is a type parameter or a nontype parameter.
11. A default argument for a template parameter is a type or value that is used if no argument is specified when the template is instantiated. The default argument should be a type or value that is suitable for a majority of the class template instantiations.
12. In a template parameter list, the keyword `class` and the keyword `typename` have the same meaning. 
13. As it is the case with default arguments for function parameters, the rightmost uninitialized parameter must be supplied with a default argument before any default argument for a parameter to its left may be supplied. For example:
     ```c++
     #include <iostream>
     #include <string>
     
     template <class T, int size = 1024>
     class Buffer;
     
     template <class T = std::string, int size>
     class Buffer{
     public:
        Buffer(){ std::cout << "B\n";}
     };
     
     int main() {
       Buffer buf;
         return 0;
     }
     ```
 2. Inside the class template definition, the name of the class template can be used as a type specifier whenever a nontemplate class name can be used. I.e., You can write `BufferItem*` instead of `BufferItem<T>*` inside the `BufferItem<T>` class template. Note that this works only inside the class template definition. When `BufferItem` is used as a type specifier in another template definition, the full template parameter list must be specified.
    ```c++
    #include <iostream>
    #include <string>
    
    template <class T>
    struct BufferItem {
       BufferItem(T item) : _item(item){}
       T  _item;
       BufferItem* _next;
    };
    
    template <class T>
    struct Buffer{
       Buffer(BufferItem<T>& ival) : front(&ival){}
       BufferItem<T>* front;
       // BufferItem* front; // Error
    };
    
    int main() {
      BufferItem<int> b(5);
      Buffer<int> buf(b);
        return 0;
    }
    ```
1. Class template definition can refer members of another class even though the class has not been defined yet.
   ```c++
   #include <iostream>
   #include <vector>
   
   template<class C>
   class B;
   
   template<class C>
   class A {
   public:
      A(const B<C>& b) : _x(b.getX()) {}
   private:
      C _x;
   };
   
   template<class C>
   class B {
   public:
      B(C x) : _x(x) {}
      C getX() const { return _x; }
   private:
      C _x;
   };
   
   int main() {
      B<int> b(1);
      A<int> a(b);
      return 0;
   }
   ```
{% endraw %}