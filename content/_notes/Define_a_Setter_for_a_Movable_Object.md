---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

# The Best Way to Define a Setter

Assuming the capacity of existing member has been pre-allocated and sufficient for the passed object.



# Short answer
### For movable object
```c++
// For lvalue argument:
void setter(const std::string & m) { _member = m; }
// For rvalue argument:
void setter(std::string&& m) { _member = std::move(m); }
```
### For non-movable object
```c++
// For lvalue/rvalue argument:
void setter(const std::string & m) { _member = m; }
```

There are several common approaches to writing setters in modern C++. Today, we will benchmark three major patterns and analyze their performance.






# Lvalue Argument

GCC: https://quick-bench.com/q/PbEMn4tk0uYIZWC9_ZJ3Oi9R0V8
<img src="https://hackmd.io/_uploads/B1NrmoXnll.png" width="60%">

Clang: https://quick-bench.com/q/6cCqUiQ56fL0eyT2Vu49doSc1bA
<img src="https://hackmd.io/_uploads/HyL0Shmnxl.png" width="60%">


```c++
class Person {
public:
   Person() : name("Constantdw wwdw dqwdfqwyypfn;qwlnm5465"){}
   void setName1(std::string n) {
      name = std::move(n);
   }
   void setName2(const std::string& n) {
      name = n;
   }
private:
   std::string name;
};

static void setName1_lvalue(benchmark::State& state) {
  // Code inside this loop is measured repeatedly
  Person person;
  std::string name = "Constantdw wwdw dqwdfqwyypfn";
  for (auto _ : state) {
    person.setName1(name);
  }
}
BENCHMARK(setName1_lvalue);

static void setName2_lvalue(benchmark::State& state) {
  // Code inside this loop is measured repeatedly
  Person person;
  std::string name = "Constantdw wwdw dqwdfqwyypfn";
  for (auto _ : state) {
    person.setName2(name);
  }
}
BENCHMARK(setName2_lvalue);
```

# Rvalue Argument

GCC: https://quick-bench.com/q/mUFg5UXJj28ZTqtE2v7eGr30T70
<img src="https://hackmd.io/_uploads/rk3YZiQ2xg.png" width="60%">

Clang: https://quick-bench.com/q/a1pANo1yjRH3K_mjUq7AfttJx7E
<img src="https://hackmd.io/_uploads/BJynWj72xl.png" width="60%">


```c++
class Person {
public:
   Person() : name("Constantdw wwdw dqwdfqwyypfn;qwlnm5465"){}
   void setName1(std::string n) {
      name = std::move(n);
   }
   void setName2(const std::string& n) {
      name = n;
   }
   void setName3(std::string&& n) {
      name = std::move(n);
   }
private:
   std::string name;
};



static void setName1_rvalue(benchmark::State& state) {
  // Code inside this loop is measured repeatedly
  Person person;
  std::string name = "Constantdw wwdw dqwdfqwyypfn";
  for (auto _ : state) {
    person.setName1(std::move(name));
  }
}
BENCHMARK(setName1_rvalue);



static void setName2_rvalue(benchmark::State& state) {
  // Code inside this loop is measured repeatedly
  Person person;
  std::string name = "Constantdw wwdw dqwdfqwyypfn";
  for (auto _ : state) {
    person.setName2(std::move(name));
  }
}
BENCHMARK(setName2_rvalue);


static void setName3_rvalue(benchmark::State& state) {
  // Code inside this loop is measured repeatedly
  Person person;
  std::string name = "Constantdw wwdw dqwdfqwyypfn";
  for (auto _ : state) {
    person.setName3(std::move(name));
  }
}
BENCHMARK(setName3_rvalue);
```

# Conclusion
For the remaining cases, I summarize them in the table for easier comparison.


|                                          | lvalue argument                            | rvalue argument                |
|:----------------------------------------:| -------------------------------------------------- | -------------------------------------------- |
|      Take by value and assign       |Copy construct, then move assign  | Move construct, then move assign |
| Take by const lvalue ref and assign | Copy assign | Copy assign  | 
|    Take by rvalue ref and assign    | N/A                                                | Move assign |

$\dagger$ Assuming the capacity of existing member is greater than or equal to the passed object. Ie., no allocation occurs in copy/move assignment


{% endraw %}