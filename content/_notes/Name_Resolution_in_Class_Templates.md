---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

1. See [Name resolution in template definitions](/-cfPBQQtRiuZ4EvzEx5JiA)
2. The two steps of name resolution in the definitions of class templates or in the definition of members of class templates are therefore the following:
    * The names that do not depend on a template parameter are resolved when the template is defined.
    * The names that depend on a template parameter are resolved when the template is instantiated.
     ```c++
     #include<iostream>
     #include<vector>
     
     
     class LongDouble {
     public:
        LongDouble (double dv) : _dv(dv){}
        double get() const { return _dv; }
     private:
        double _dv;
     };
     
     
     template <class T>
     class Queue {
     public:
        Queue() {
           list.clear();
        }
        void pop();
        void push(T val);
     private:
        std::vector<T> list;
     };
     
     
     template <class T>
     void Queue<T>::push(T val){
        list.push_back(val);
     }
     
     
     template <class T>
     void Queue<T>::pop(){
        if (list.empty()){
           std::cout << "Queue is empty\n";
        }else{
           std::cout << "value poped out: " << list.back() << "\n";
           list.pop_back();
        }
     }
     
     
     std::ostream& operator<<(std::ostream& os, const LongDouble& obj) {
         os << obj.get();
         return os;
     }
     
     int main(){
     
        LongDouble ld(56.56);
        Queue<LongDouble> list;
     
        list.push(ld);
        list.pop();
        list.pop();
     
        return 0;
     }
     ```
     In the expression
     ```
     std::cout << "value poped out: " << list.back() << "\n";
     ```
     `list.back()` is of type `T`, and its actual type is unknown until the member function `pop()` is instantiated. The `operator<<()` chosen depends on the actual type of `list.back()`, that is, on the type with which the template parameter `T` is replaced. It is therefore impossible to know which `operator<<()` is called until `pop()` is instantiated.
3. **[Need to be clarified]** Knowing where a template's point of instantiation is located is important because it determines which declarations are considered for the names that depend on a template parameter.
    * A class template point of instantiation is always in namespace scope and it always immdiately ***precedes*** the declaration or definition that refers to the class template instantiation.
    * The point of instantiation of a member function or a static data member of a class template always immediately ***follows*** the declaration or definition that refers to the instantiation of the member of the class template.
{% endraw %}