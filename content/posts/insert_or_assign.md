---
title: "insert_or_assign"
date: 2026-04-13T15:32:37+08:00
draft: false
---

---
title: insert_or_assign
tags: [CPP]

---


This function attempts to insert a given key-value pair into the container. If the key already exists, the function assigns the new value to the existing key, effectively updating it. If the key does not exist, a new element with the key and value is inserted.

# Usage
```c++=
#include <iostream>
#include <unordered_map>

int main() {
    std::unordered_map<int, std::string> myMap;

    // Insert a new key-value pair
    myMap.insert_or_assign(1, "one");

    // Key 1 exists, so assign a new value to it
    myMap.insert_or_assign(1, "ONE");

    // Insert a new key-value pair
    myMap.insert_or_assign(2, "two");

    for (const auto& pair : myMap) {
        std::cout << pair.first << ": " << pair.second << std::endl;
    }

    return 0;
}
```
