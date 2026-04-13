---
title: "How to benefit from move semantics"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: How to benefit from move semantics
tags: [CPP]

---

# Avoid Objects with Names
```c++
// Bad
MyType x{42, "hello"};
foo(x);

// Good
foo({42,"hellow"});
```

# When You Cannot Avoid Using Names
```c++
std::string str{"hello"};
std::vector<std::string> coll;

coll.push_back(str);
coll.push_back(std::move(str));
```

```c++
std::string line;
while(std::getline(myStream, line)) {
   coll.push_back(std::move(line));
}
```

# Avoid Unnecessary `std::move()`

* If the returned expression is not an lvalue, the NRVO may be inhibited:
   ```c++
   std::string foo(){
      std::string name;
      ...
      // BAD:
      return std::move(name);
   }
   ```
   See [Name Returned Value Optimization](/7PW3XTjqSA-TYgnsRdQkwQ) for more details.
* Thus, if you return a local object, do not use `std::move()` whereby either NRVO or move semantics will perform:
  ```c++
  std::string foo(){
     std::string name;
     ...
     return name;
  }
  ```


{% endraw %}