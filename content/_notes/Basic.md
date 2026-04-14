---
date: 2026-04-13T15:32:36+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

###### tags: `CPP`
# Basic

1. Scope operator `::`
The compiler should look in the scope of the left-hand operand for the name of the right-hand operand.
2. `using` declaration
A using declaration lets us use a name from a namespace without qualifying the name with a `namespace_name::` prefix.
Note: headers should not include using declarations.

## `string`
![](https://i.imgur.com/8mhT1ks.png)
![](https://i.imgur.com/Gjp1jBa.png)

```c++
#include <string>         // Include string (std namespace)
string s1, s2="hello";    // Create strings
s1.size(), s2.size();     // Number of characters: 0, 5
s1 += s2 + ' ' + "world"; // Concatenation
s1 == "hello world"       // Comparison, also <, >, !=, etc.
s1[0];                    // 'h'
s1.substr(m, n);          // Substring of size n starting at s1[m]
s1.c_str();               // Convert to const char*
s1 = to_string(12.05);    // Converts number to string
getline(cin, s);          // Read line ending in '\n'
```
## `vector`
![](https://i.imgur.com/3eI6y84.png)
![](https://i.imgur.com/CvgZzP3.png)
```c++
#include <vector>         // Include vector (std namespace)
vector<int> a(10);        // a[0]..a[9] are int (default size is 0)
vector<int> b{1,2,3};        // Create vector with values 1,2,3
a.size();                 // Number of elements (10)
a.push_back(3);           // Increase size to 11, a[10]=3
a.back()=4;               // a[10]=4;
a.pop_back();             // Decrease size by 1
a.front();                // a[0];
a[20]=1;                  // Crash: not bounds checked
a.at(20)=1;               // Like a[20] but throws out_of_range()
for (int& p : a)
  p=0;                    // C++11: Set all elements of a to 0
for (vector<int>::iterator p=a.begin(); p!=a.end(); ++p)
  *p=0;                   // C++03: Set all elements of a to 0
vector<int> b(a.begin(), a.end());  // b is copy of a
vector<T> c(n, x);        // c[0]..c[n-1] init to x
T d[10]; vector<T> e(d, d+10);      // e is initialized from d
```
Note: The body of a range `for` must not change the size of the sequence over which it is iterating.
* Two vectors are equal if they have the same number of elements and if the corresponding elements all have the same value.
*  If the vectors have differing sizes, but the elements that are in common are equal, then the vector with fewer elements is less than the one with more elements.
*  If the elements have differing values, then the relationship between the vectors is determined by the relationship between the first elements that differ.
{% endraw %}