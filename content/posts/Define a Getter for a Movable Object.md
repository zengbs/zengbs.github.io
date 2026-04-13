---
title: "Define a Getter for a Movable Object"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

---
title: Define a Getter for a Movable Object
tags: [CPP]

---

# Motivation
In convention, the definition of getter may be shown as follows:
```c++
class Person
{
public:
    // note that non-const object can call this getName()
    const std::string& getName() const {
        return __name; 
    }
private:
   std::string __name;
};
```
However, the behavior of this convention will be undefined when the getter is called on an rvalue. For example,
```c++
for (char c : returnPersonByValue().getName()) {
    ...
}
```
Internally, the compiler might change the above code to that below:
```c++
auto&& range = returnPersonByValue().getName();
// OOPS: returned temporory object is destroyed here
for (auto pos = range.begin(); pos != range.end(); ++pos) {
   char c = *pos;
   ...
}
```
The `auto&&` ensures that if expression is an rvalue (a temporary object), it is moved into `range`, and if it's an lvalue (a named object), it's bound by reference.

In this case, `returnPersonByValue()` returns an rvalue, and `getName()` returns an lvalue that binds to a member of a temperory object that is about to destroyed. So in this convention, the behavior of getter is undefined when it is called on an rvalue.

# The Best Approach

```c++
// it is called on lvalue object
const std::string& get() const& { return name } 

// it is called on rvalue object
std::string get() && { return std::move(name); }
```

# Advantage
```c++
Person p;
std::vector<Person> coll;

// calls push_back(const Person&)
// --> copy
coll.push_back(p.getName());

// calls push_back(Person&&)
// --> move
coll.push_back(std::move(p).getName());
```