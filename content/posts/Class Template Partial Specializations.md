---
title: "Class Template Partial Specializations"
date: 2026-04-13T15:32:36+08:00
draft: false
render_with_liquid: false
---

---
title: Class Template Partial Specializations
tags: [CPP]

---

1. If a class template has more than one template parameter, one might want to specialize the class template for a particular template argument or a set of template arguments without specializing the template for every template parameter.
2. The template parameter list for the partial specialization only lists the parameters for which the template arguments are still unknown.
3. When class template partial specializations are declared, the compiler chooses the template definition that is the most specialized for the instantiation. When no partial specialization can be used, the generic template definition is used.
4. The definition of a partial specialization is completely disjointed from the definition of the generic template. The partial specialization may have a completely different set of members from the generic class template.
5. A class template partial specialization must have its own definitions for its member functions, static data members, and nested types. The generic definitions for the members of a class template are never used to instantiate the members of the class template partial specialization.
    ```c++
    #include<iostream>
    
    template<class T, class U>
    class Box {
    public:
       Box(T h, U w) : _h(h), _w(w){}
       void showBox(){
          std::cout << "Called completely specialization\n";
       }
    private:
       T _h;
       U _w;
    };
    
    template<class T>
    class Box<T, int> {
    public:
       Box(T h, int w) : _h(h), _w(w){}
    
       void showBox(){
          std::cout << "Called partial specialization\n";
       }
    
    private:
       T _h;
       int _w;
    };
    
    
    int main(){
    
       Box box1(13, 55);
       Box box2(13, 20.1);
    
       box1.showBox();
       box2.showBox();
    
       return 0;
    }
    ```