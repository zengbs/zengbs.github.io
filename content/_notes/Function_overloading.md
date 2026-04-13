---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

###### tags: `CPP`

# Function overloading
By function overloading, we can have multiple definitions for the same function name in the same scope.
  ```cpp=
    float absolute(float var){
        if (var < 0.0)   var = -var;
        return var;
    }
    
    int absolute(int var) {
         if (var < 0)    var = -var;
        return var;
    }
    
    int main() {
        cout <<  absolute(-5) << endl;
        cout <<  absolute(5.5f) << endl;
        return 0;
    }
  ```
  
  
* [Function call operator](https://hackmd.io/eXvnjQjXQEiLpYW17YcKEA?both#Function-call-operator)
```cpp=
#include <iostream>
using namespace std;
       
class Distance {
   public: 
      void operator()(int a, int b) {
         printf("Two parameters\n");
      }
      void operator()(int a, int b, int c) {
         printf("Three parameters\n");
      } 
};  
       
int main() {
       
   Distance myClass;
       
   myClass(11, 10);
   myClass(11, 10, 3); 
       
   return 0;
}
```
Output:
```
Two parameters
Three parameters
```
{% endraw %}