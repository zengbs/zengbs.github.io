---
title: "Mandatory Copy Elision or Passing Unmaterialized Objects"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: Mandatory Copy Elision or Passing Unmaterialized Objects
tags: [CPP]

---



# Materialization 
Materialization is the step by which prvalue is used to create a temporary object in memory. Temporary objects have existed since C++98, but the timing of prvalue materialization was redefined in C\++17. Since C\++17, prvalues do not "immediately" materialize temporary objects; materialization occurs only when a temporary object is required. In other words, C\++17 defers the materialization of a prvalue "as long as possible". [cf. class. temporary] This change guarantees copy elision.
 
For example:
```c++
class C{};
C create() { return C{}; }
void foo(C c){}
 
int main(){
 foo(create());
}
```
## Behavior before C++17 without copy elision:
1. Create and initialize (materialize occurs here) a temporary object with prvalue C{}. (used default ctor)
2. Construct another return object from the temporary. (used move ctor)
3. The temporary object returned by create() is then moved into function parameter c.
 
 
## Behavior since C++17:
1. Construct an object as the function parameter of foo() with the prvalue C{}(materialize happens here), and then pass the object into the caller.

## Comparison
By comparing these two behaviors, we can see that the advantage of deferring the materialization of prvalues is that no copy or move constructor needs to be invoked; threrfore, copy elision is guaranteed.


Please see below for more details:
[How does a function return local object internally?](/oPiyQizIR5u70ybjT583Dw)
[Name Returned Value Optimization](/7PW3XTjqSA-TYgnsRdQkwQ)
[Avoid Unnecessary `std::move()`](https://hackmd.io/tD4j7zd4SqaDuwXmKk74Jg#Avoid-Unnecessary-stdmove)
{% endraw %}