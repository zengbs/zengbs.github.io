---
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---

# Implementation
Static 1D array


# Element Access


| Operation | Time |                      Comment                       |
|:---------:|:----:|:--------------------------------------------------:|
|   `at`    | O(1) |   access specified element with bounds checking    |
|   `[]`    | O(1) |              access specified element              |
|  `front`  | O(1) |              access the first element              |
|  `back`   | O(1) |              access the last element               |
|  `data`   | O(1) | direct access to the underlying contiguous storage |




# Declarations
```c++=
std::array<int, 5> myArray;

std::array<int, 5> myArray = {1, 2, 3, 4, 5};

// Creates an array with all elements initialized to 7
std::array<int, 5> myArray2 = std::array<int, 5>::filled(7);

std::array<int, 5> myArray3 = myArray;

std::array<int, 5> myArray4{1, 2, 3, 4, 5};

std::vector<int> vec = {1, 2, 3, 4, 5};
std::array<int, 5> myArray5(vec.begin(), vec.end());
```


# Loops

```c++=
std::array<int, 5> myArray = {1, 2, 3, 4, 5};

for (int element : myArray) {
    // Access each element using 'element'
}

for (auto it = myArray.begin(); it != myArray.end(); ++it) {
    // Access each element using '(*it)'
}

for (auto it = myArray.cbegin(); it != myArray.cend(); ++it) {
    // Access each element using '(*it)'
}

for (size_t i = 0; i < myArray.size(); ++i) {
    // Access each element using 'myArray[i]'
}

for (int& element : myArray) {
    // Modify elements using 'element' directly
}

std::for_each(myArray.begin(), myArray.end(), [](int& element) {
    // Access each element using 'element'
});

for (int& element : myArray | std::views::filter([](int x) { return x > 2; })) {
    // Access each filtered element using 'element'
}
```
{% endraw %}