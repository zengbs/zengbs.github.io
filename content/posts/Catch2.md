---
title: "Catch2"
date: 2026-04-13T15:32:36+08:00
draft: false
---

---
title: Catch2
tags: [CPP]

---

# Example
```c++=
// main.cpp
#include <catch2/catch_test_macros.hpp>
#include <catch2/benchmark/catch_benchmark.hpp>

TEST_CASE("Benchmark Convolution", "[benchmark]") {


    BENCHMARK("Benchmark function") {
        return function(arg1, arg2, arg3);
    };

    REQUIRE( isCorrect(arg1, arg2) );

}
```

# Reference
https://github.com/catchorg/Catch2