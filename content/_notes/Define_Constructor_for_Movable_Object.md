---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

# The Best Way to Define Constructor

Assuming the capacity of the member to be constructed is zero.

# Short answer

### For movable object
```c++
// For lvalue/rvalue
Person(std::string n) : name{std::move(n)} {}
```
### For non-movable object
```c++
// For lvalue
Person(const std::string& n) : name{n} {}
// For rvalue
Person(std::string&& n) : name{std::move(n)} {}
```
or
```c++
// For lvalue/rvalue
Person(const std::string& n) : name{n} {}
```
# Lvalue Argument
## Pass-by-value
GCC: https://quick-bench.com/q/TAj4y76nTywf73Dit6hok_dCBA0
<img src="https://hackmd.io/_uploads/H1_C82X2ex.png" width="60%">

Clang: https://quick-bench.com/q/9cXSSD5AZ7VC0cwdYBK-fq4pKUM
<img src="https://hackmd.io/_uploads/rkRJv2Q3gg.png" width="60%">


```c++
class Person {
public:
   Person(std::string n) : name{std::move(n)} {}
   //Person(const std::string& n) : name{n} {}
   //Person(std::string&& n) : name{std::move(n)} {}
private:
   std::string name;
};

static void TakeValue_lvalue(benchmark::State& state) {
  // Code inside this loop is measured repeatedly
  std::string name = "Constantdw wwdw dqwdfqwyypfn;qwlnm5465";
  for (auto _ : state) {
    Person person(name);
    benchmark::DoNotOptimize(person);
  }
}
BENCHMARK(TakeValue_lvalue);
```

## Pass-by-reference
GCC: https://quick-bench.com/q/Di-71lEKR30kBict_AMGOOGLRWU
<img src="https://hackmd.io/_uploads/SkyP8h73gg.png" width="60%">

Clang: https://quick-bench.com/q/W7RzNVMf0ga4mxq9IS0r6LYd1GU
<img src="https://hackmd.io/_uploads/rykM83X3ex.png" width="60%">
```c++
class Person {
public:
   //Person(std::string n) : name{std::move(n)} {}
   Person(const std::string& n) : name{n} {}
   //Person(std::string&& n) : name{std::move(n)} {}
private:
   std::string name;
};

static void TakeValue_lvalue(benchmark::State& state) {
  // Code inside this loop is measured repeatedly
  std::string name = "Constantdw wwdw dqwdfqwyypfn;qwlnm5465";
  for (auto _ : state) {
    Person person(name);
    benchmark::DoNotOptimize(person);
  }
}
BENCHMARK(TakeValue_lvalue);
```

# Rvalue Argument
## Pass-by-value

```c++
class Person {
public:
   Person(std::string n) : name{std::move(n)} {}
   //Person(const std::string& n) : name{n} {}
   //Person(std::string&& n) : name{std::move(n)} {}
private:
   std::string name;
};

static void rvalue(benchmark::State& state) {
  // Code inside this loop is measured repeatedly
  std::string name = "Constantdw wwdw dqwdfqwyypfn;qwlnm5465";
  for (auto _ : state) {
    Person person(std::move(name));
    benchmark::DoNotOptimize(person);
  }
}
BENCHMARK(rvalue);
```
GCC: https://quick-bench.com/q/GjLYdlyRLPiwGEgmVulHDtbzReQ
<img src="https://hackmd.io/_uploads/HkEd_nmhle.png" width="60%">
Clang: https://quick-bench.com/q/Mlt4tRPB6wuqsd6svDZaUFxvblg
<img src="https://hackmd.io/_uploads/SJsQd2mhgl.png" width="60%">
## Pass-by-reference

```c++
class Person {
public:
   //Person(std::string n) : name{std::move(n)} {}
   Person(const std::string& n) : name{n} {}
   //Person(std::string&& n) : name{std::move(n)} {}
private:
   std::string name;
};

static void rvalue(benchmark::State& state) {
  // Code inside this loop is measured repeatedly
  std::string name = "Constantdw wwdw dqwdfqwyypfn;qwlnm5465";
  for (auto _ : state) {
    Person person(std::move(name));
    benchmark::DoNotOptimize(person);
  }
}
BENCHMARK(rvalue);
```
GCC: https://quick-bench.com/q/H_33D9MRmpfUJdy8_zaCbP504-Q
<img src="https://hackmd.io/_uploads/rJG6dh7heg.png" width="60%">
Clang: https://quick-bench.com/q/LNzBy3uBlVRC22PBVLW8xafCT1o
<img src="https://hackmd.io/_uploads/BkmmK2m2lg.png" width="60%">
## Pass-by-rvalue-reference

```c++
class Person {
public:
   //Person(std::string n) : name{std::move(n)} {}
   //Person(const std::string& n) : name{n} {}
   Person(std::string&& n) : name{std::move(n)} {}
private:
   std::string name;
};

static void rvalue(benchmark::State& state) {
  // Code inside this loop is measured repeatedly
  std::string name = "Constantdw wwdw dqwdfqwyypfn;qwlnm5465";
  for (auto _ : state) {
    Person person(std::move(name));
    benchmark::DoNotOptimize(person);
  }
}
BENCHMARK(rvalue);
```
GCC: https://quick-bench.com/q/MjO6qPy4y2Q_MDF1rn3CfVUMExk
<img src="https://hackmd.io/_uploads/Hyee92mhgl.png" width="60%">
Clang: https://quick-bench.com/q/ewH4cWNZOf6_r24Qea2w8BNvzHs
<img src="https://hackmd.io/_uploads/ry5YY3mnll.png" width="60%">


# Summary
|                                          | lvalue argument                            | rvalue argument                |
|:----------------------------------------:| -------------------------------------------------- | -------------------------------------------- |
|      ` Person(std::string n) : name{std::move(n)} {}`       |1. Copy construct `n` from lvalue arg<br>2. Move construct  | 1. Move construct `n` from rvalue arg<br>2. Move construct |
| ` Person(const std::string& n) : name{n} {}` | 1. Bind `n` to lvalue arg<br>2. Copy construct | 1.Bind `n` to rvalue arg<br>2. Copy construct  | 
|    `Person(std::string&& n) : name{std::move(n)} {}`    | N/A                                                | 1. Bind `n` to rvalue arg<br>2. Move construct |
{% endraw %}