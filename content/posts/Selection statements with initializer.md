---
title: "Selection statements with initializer"
date: 2026-04-13T15:32:37+08:00
draft: false
---

---
title: Selection statements with initializer
tags: [CPP]

---

# `if` and `switch` with Initialization

## `if` with initialization
* Any value initialized inside an `if` statement is valid until the end of the *then* and the *else* part. For example,
   
   ```c++
   #include <iostream>
   #include <vector>
   #include <fstream>
   #include <string>
   
   int main() {
      std::vector<std::string> coll{"Hello","World","Dear"};
      if (std::ofstream strm = std::ofstream("output.txt"); coll.empty())
      {
         strm << "no data\n";
      }else{
         for (const auto& e : coll) {
            strm << e << "\n";
         }
      }
   }
   ```
   The destructor for `strm` is called at the end of the whole `if` statement (at the end of the *else* part, `if` any, or at the end of the *then* part, otherwise).
* Multiple declarations with optional initializations are also allowed:
   ```c++
   if (auto x{qqq1()}, auto y{qqq2()}; x != y){
      std::cout << "x and y differs\n";
   }
   ```
* Consider inserting a new element into a map or unordered map.
   ```c++
   #include <iostream>
   #include <string>
   #include <map>
   
   int main() {
      std::map<int,std::string> m;
      if (auto [pos,ok] = m.insert({1,"Hi"}); ok){
         if (ok){
            auto& [key, val] = *pos;
            std::cout << key << ":" << val << "\n";
         }else{
            std::cout << "Failed\n";
         }
      }
   }
   ```
## `switch` with initialization

```
qqq/
├── aaa
│   └── bbb
├── ccc
│   └── bbb
└── xxx
```

```c++
#include <iostream>
#include <filesystem>
#include <string>

int main() {
   namespace fs = std::filesystem;

   std::string name{"qqq"};

   switch( fs::path p{name}; status(p).type() ) {

      case fs::file_type::not_found:
         std::cout << p << " not found\n";
         break;
      case fs::file_type::directory:
         std::cout << p << ": \n";
         for ( const auto& e : std::filesystem::directory_iterator{p} ) {
            std::cout  << "- " << e.path() << "\n";
         }
         break;
      default:
         std::cout << p << " is found but not a directory\n";
         break;
   }
}
```
Result:
```
"qqq":
- "qqq/aaa"
- "qqq/ccc"
- "qqq/xxx"
```