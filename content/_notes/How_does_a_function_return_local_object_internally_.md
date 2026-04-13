---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---

```c++
MyClass::MyClass foo() {
   MyClass obj;
   ...
   return obj;
}

void caller() {
   MyClass result = foo();
}
```
* Without NRVO, the compiler converts the above code to something like below:
   ```c++
   void foo(MyClass* __ret) {
   
       // 1) create local with default-construct
       MyClass obj = MyClass();
       
       // ... body using obj ...
   
       // 2) initialize result from local obj
       if (move semantics is available)
           MyClass::MyClass(__ret, move(obj));
       else
           MyClass::MyClass(__ret, obj);
   
       // 3) destroy local
       obj.~MyClass();
   
       // 4) normal return; caller now owns *__ret
       return;
   }
   
   
   // Caller side:
   void caller():
   {
       MyClass result;
       
       foo(&result);
       
       // use result ...
       
       result.~MyClass()
   }
   ```
   
 * With NRVO, the compiler converts the above code to something like below:
   ```c++
   void foo(MyClass* __ret) {
   
       // this step requires that
       // the type of obj must be the same as the type of *__ret
       MyClass& obj = *__ret;
   
       obj = MyClass::MyClass();
   
       // ... use obj normally
   
       return;
   }
   
   // Caller side:
   void caller():
   {
       MyClass result;
       
       foo(&result);
       
       // use result ...
       
       result.~MyClass()
    }
   ```
{% endraw %}