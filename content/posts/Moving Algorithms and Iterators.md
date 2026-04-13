---
title: "Moving Algorithms and Iterators"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

---
title: Moving Algorithms and Iterators
tags: [CPP]

---



# Moving Algorithms
* `std::move()`, which moves elements to another range or backwards in the same range. You specify the beginning of the destination range and the elements are moved from the beginning to the end of the source range.
* `std::move_backward()`, which moves elements to another range or forward in the same range. You specify the end of the destination range and the elements are moved from the end to the beginning of the source range.
* As usual for overwriting algorithms, the destination container must already have enough elements that are overwritten (otherwise you have undefined behavior).
* The number of elements does not change (neither in the source nor in the destination range).
* However, the elements of the source range get a moved-from state. Thus, we do not know the values of the strings in the source range after this call (unless we have specified behavior for moved-from objects such as for move-only types).
![2025-12-04_12-06](https://hackmd.io/_uploads/BJaxtYAW-g.jpg =50%x)


```c++
# include<iostream>
# include<vector>
# include<string>

template<class T>
void print(const std::string& name, const T& coll)
{
   std::cout << name << " (" << coll.size() << " elems): ";
   for (const auto& elem : coll) {
      std::cout << " '" << elem << "'";
   }
   std::cout << "\n";
}

int main() {

   std::vector<std::string> v1={"love","is","all","you","need"};
   std::vector<std::string> v2;
   std::vector<std::string> v3;

   v2.resize(v1.size());
   v3.resize(v1.size()+3);

   std::move(v1.begin(),v1.end(),v2.begin());
   std::move_backward(v2.begin(),v2.begin()+3,v3.end());

   print("v1",v1);
   print("v2",v2);
   print("v3",v3);
}
```
Result:
```
v1 (5 elems):  '' '' '' '' ''
v2 (5 elems):  '' '' '' 'you' 'need'
v3 (8 elems):  '' '' '' '' '' 'love' 'is' 'all'
```

# Removing Algorithms
* By design, C++ algorithms use iterators to deal with the elements of containers and ranges. However, like pointers operating on arrays, iterators can only read and write values; they cannot insert or remove elements.
Therefore, “removing” algorithms do not really remove elements; they only move the values of all elements that are not removed to the front of the processed range and return the new end.
* For example, given you have a sequence of the following integer values:
1 2 3 4 5 4 3 2 1
calling the algorithm `std::remove()` with the value 2 to remove all elements with the value 2 modifies the sequence as follows:
1 3 4 5 4 3 1 2 1
* The removing algorithms leave elements where the value was moved-away in a moved-from state.
* The following algorithms can create move-from states:
   * `std::remove()` and `std::remove_if()`
   * `std::unique()`

# Move Iterators
* By using move iterators (also introduced with C++11), you can use move semantics even in other algorithms and in general wherever input ranges are taken (e.g., in constructors).
* A move iterator is an iterator adaptor that turns copying into moving. Normally, when you use an iterator in algorithms like `std::copy`, the algorithm will copy elements:
   ```c++
   std::copy(src.begin(), src.end(), dst.begin());
   ```
   ```c++
   std::copy(
      std::make_move_iterator(src.begin()),
      std::make_move_iterator(src.end()),
      std::back_inserter(dst)
   );
   ```
* Example with `std::for_each`:
   ```c++
   #include <iostream>
   #include <string>
   #include <vector>
   #include <algorithm>
   
   template<typename T>
   void print(const std::string& name, const T& coll)
   {
     std::cout << name << " (" << coll.size() << " elems): ";
     for (const auto& elem : coll) {
       std::cout << " \"" << elem << "\"";
     }
     std::cout << "\n";
   }
   
   void process(std::string s)  // gets moved value from rvalues
   {
     std::cout << "- process(" << s << ")\n";
     //...
   }                
   
   int main()
   {
     std::vector<std::string> coll{"don't", "vote", "for", "liars"};
     print("coll", coll);
     
     // move away only the elements processed:
     std::for_each(std::make_move_iterator(coll.begin()),
                   std::make_move_iterator(coll.end()),
                   [] (auto&& elem) {
                     if (elem.size() != 4) {
                       process(std::move(elem));
                     }
                   });
   
     print("coll", coll);
   } 
   ```
  
 # Move Iterators in Constructors and Member Functions

```c++
std::list<std::string> src{"don't", "vote", "for", "liars"};

// move all elements from the list to the vector:
std::vector<std::string> vec{
   std::make_move_iterator(src.begin()),
   std::make_move_iterator(src.end())
};
```

By the way, what's difference between them?
```c++
std::vector<int> v1={1,2,3};
std::vector<int> v2 = std::move(v1);
```
```c++
std::vector<int> v1={1,2,3};
std::vector v3{
   std::make_move_iterator(v1.begin()),
   std::make_move_iterator(v1.end())
};
```
The first move an entire object to another with time complexity O(1). However, in the second, each element was moved individually to another with time complexity O(N).