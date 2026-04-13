---
title: "std__vector"
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

---
title: 'std::vector'
tags: [CPP]

---


# Implementation

Dynamic 1D array


# Element Access
| Operation   | Time | Comment |
|:----------- | ---- |:------- |
| `at`          | O(1) | Returns a reference to the element at specified location pos, with bounds checking.         |
| `operator []` | O(1) | Returns a reference to the element at specified location pos.<br>No bounds checking is performed.         |
| `front`       | O(1) |    Returns a reference to the first element in the container.      |
| `back`        | O(1) |   Returns a reference to the last element in the container.       |
| `data`        | O(1) |   Returns pointer to the underlying array serving as element storage. The pointer is such that range `[data(), data() + size())` is always a valid range.      |


# Modifiers
| Operation      | Time                                                                                            |Usage     |          Version          |
| -------------- |:----------------------------------------------------------------------------------------------- | --- |:-------------------------:|
| `clear`        | O(n)                                                                                            | `v.clear()`    |                           |
| `insert`       | insert an element: O(1)+O(\|`end`-`pos`\|)<br>insert a range: O(\|`range`\|)+O(\|`end`-`pos`\|) |  `v.insert(itr pos, T value)`<br>`v.insert(itr pos, int count, T value)`<br>`insert(itr pos, itr list_begin, itr list_end)`<br>`insert(itr pos, list)`   |                           |
| `insert_range` | O(\|`range`\|)+O(\|`end`-`pos`\|)                                                               |     | Since C++23<br>(Uncommon) |
| `emplace`      | O(\|`end`-`pos`\|)                                                                              | `v.emplace(itr pos, constructor parameters)`    |        Since C++11        |
| `erase`        | O(`erased length`)+O(\|`end`-`pos`\|)                                                           |  `v.erase(itr pos)`<br>`v.erase(itr first,itr last)`   |                           |
| `push_back`    | O(1)                                                                                            |  `v.push_back(value)`   |                           |
| `emblace_back` | O(1)                                                                                            |   `v.emplace_back(constructor parameters)`  |        Since C++11        |
| `append_range` | If reallocation happen: O(m)<br>Otherwise: O(\|`range`\|)                                       | `v.append_range(range)`    |  Since C++23<br>Uncommon  |
| `pop_back`     | O(1)                                                                                            |  `v.pop_back()`   |                           |
| `resize`       | If reallocation happen: O(m)<br>Otherwise: O(`erased/inserted length`)                          | `v.resize(new_length)`<br>`v.resize(new_length,initial_value)`    |                           |
| `swap`         | O(1)                                                                                            |   `v1.swap(v2)`  |                           |

* n = length of original vector.
* m = length of modified vector
* end = the index of the last element of the orignal vector
* pos = the position where new element inserted/erased.
# Loop
```c++=
// Range-based loop (since C++11)
for (auto& element : v){
   element = ...
}

// Using traditional loop
for (int i=0;i<v.size();i++){
   v[i] = ...
}

// Using iterator
for (auto it = vec.begin(); it != vec.end(); ++it) {
   // Double each element
   *it = ...
}

```

# Declarations
```c++=
// [1,2,3,4]
std::vector<int> v{1,2,3,4};

// [0,0,0,0]
std::vector<int> v(4);

// [1,1,1,1]
std::vector<int> v(4,1);

vector<int> v1 = {10, 20, 30};
// v2 = [10, 20, 30]
vector<int> v2(v1);
// v3 = [10, 20, 30]
vector<int> v3 = v1;

vector<int> v1 = {10, 20, 30, 40, 50};
// v2 = [30,40,50]
vector<int> v2(v1.begin() + 2, v1.end());

vector<int> v1 = std::move(v2);
```


# Reference
![vector](https://hackmd.io/_uploads/Sk9CDzAn6.png)
[C++11 使用 emplace 取代 push_back 和 insert](https://viml.nchc.org.tw/cpp11-emplace/)