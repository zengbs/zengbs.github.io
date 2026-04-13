---
title: "Class Template Specializations"
date: 2026-04-13T15:32:36+08:00
draft: false
render_with_liquid: false
---

---
title: Class Template Specializations
tags: [CPP]

---



1. Even though the class type `MyClass<LongDouble>` is instantiated from the generic class template definition, each object of type `MyClass<LongDouble>` uses the specializations for the member functions `min()` and `max()` — these member functions are not instantiated from the generic member function definitions for the class template `MyClass`.
    ```c++
    #include <iostream>
    
    class LongDouble {
    public:
       LongDouble( double dv ) : _dv(dv) { }
       double get() { return _dv; }
       operator double(){return _dv;}
    private:
       double _dv;
    };
    
    template<class T>
    class MyClass {
    public:
       MyClass(T m, T n): _m(m), _n(n) { }
       T sum( ) { return _m + _n; }
       T get_m() { return _m; }
       T get_n() { return _n; }
    private:
       T _m;
       T _n;
    };
    
    // Explicit specialization definition
    template<> LongDouble MyClass<LongDouble>::sum()
    {
       std::cout << "Called specialized member function:\n";
       return get_m() + get_n();
    }
    
    int main(){
    
       LongDouble ld1(5.6);
       LongDouble ld2(-9.9);
       MyClass<LongDouble> objl(ld1, ld2);
       std::cout << objl.sum() << "\n";
    
       return 0;
    }
    ```
2. Because the explicit specialization definitions for the member functions `sum()` is function definitions and not template definitions, (and because these definitions are not declared inline), they cannot be placed in a header file.
3. Fortunately, it is possible just to declare a function template explicit specialization without defining it.
   ```c++
   template<> LongDouble MyClass<LongDouble>::sum();
   ```
4. In some cases the entire class template definition may be inappropriate for use with a particular type. In this case the programmer can provide a definition to specialize the entire class template.
   ```c++
   #include <iostream>
   
   
   class LongDouble {
   public:
      LongDouble( double dv ) : _dv(dv) { }
      double get() { return _dv; }
      operator double(){return _dv;}
   private:
      double _dv;
   };
   
   template<class T>
   class MyClass {
   public:
      MyClass(T m, T n): _m(m), _n(n) { }
      T sum( ) { return _m + _n; }
      T get_m() { return _m; }
      T get_n() { return _n; }
   private:
      T _m;
      T _n;
   };
   
   // Explicit specialization for a class type
   template<> class MyClass<LongDouble> {
   public:
      MyClass ( LongDouble ld1, LongDouble ld2 ) : _m(ld1), _n(ld2) {
         std::cout << "Called specialized constructor:\n";
      }
      LongDouble sum(){
         std::cout << "Called specialized member function:\n";
         return get_m() + get_n();
      }
      LongDouble get_m() {
         std::cout << "Called specialized get_m():\n";
         return _m;
      }
      LongDouble get_n() {
         std::cout << "Called specialized get_n():\n";
         return _n;
      }
   private:
      LongDouble _m;
      LongDouble _n;
   };
   
   
   int main(){
   
      MyClass<float> objf(4.6f, -5.0f);
   
      LongDouble ld1(5.6);
      LongDouble ld2(-9.9);
   
      MyClass<LongDouble> objl(ld1, ld2);
   
      std::cout << objl.sum() << "\n";
   
      return 0;
   }
   ```
5. An explicit specialization for a class template can be defined only after the general class template has been declared.
6. The generic member definitions of the class template are never used to create the definitions for the members of an explicit specialization. This is because the class template specialization may have a completely different set of class members from the generic template.
7. If we decide to provide an explicit specialization definition for the class type `MyClass<longDouble>`, not only must we provide the definitions for the member functions `sum()`, but we must also provide the definitions for all of the other member functions as well.
8. A class template cannot be instantiated from the generic template definition in some files and be specialized in other files for the same set of template arguments. 