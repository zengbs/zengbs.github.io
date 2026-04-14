---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

1. When one class object is assigned to another object of its class, such as `newAcct = oldAcct;` the following steps take place:
   1. The class is examined to determine whether an explicit copy assignment operator is provided.
   2. If it is, its access level is checked to determine whether or not it may be invoked within this portion of the program.
   3. If it is not accessible, a compile-time error message is generated; otherwise, it is invoked to carry out the assignment.
   4. If an explicit instance is not provided, default memberwise assignment is carried out.
   5. Under default memberwise assignment, each data member of a built-in or compound type is assigned the value of its corresponding member.
   6. Each member class object has steps 1 through 6 applied to it recursively until all data members of the built-in and compound types are assigned.
```c++
#include <iostream>
#include <string>

class Foo {
public:
   Foo ( std::string s, int index ) : _name(s), _index(index){};

   Foo(const Foo& rhs):_name(rhs._name){
      _index = rhs._index;
   }

   // Copy assignment
   Foo& operator=(const Foo& rhs){

      // Guard against self-assignment
      if ( &rhs != this ){
         _name.clear();

         // invokes string::oprator=(const string&)
         _name = rhs._name;
         _index = rhs._index;
      }
      return *this;
   }

   std::string _name;
   int _index;
};

int main(){
   Foo f1("qwddf", 54);
   Foo f2 = f1;
   std::cout << f2._name << ", " << f2._index << "\n";
}
```
2. To prevent memberwise copy altogether, we do the same as we did to prevent memberwise initialization: declare the operator private and do not provide an actual definition of the operator.
3. In general, the copy constructor and copy assignment operator should be thought of as a unit. If we require one, we more than likely require the other. If we prohibit one, we should likely prohibit the other.
{% endraw %}