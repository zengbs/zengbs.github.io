---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

* `begin()` returns the iterator denoting the first element.
* `end()` returns the iterator denoting the one past the last element.
* `cbegin()` and `cend()` return `container<T>::const_iterator`.
* There is no operator of adding two iterators.
* `std::container<T>::difference_type` represents the distance, signed type, between two iterators:
	```c++
	std::vector<int>::difference_type distance = std::distance(it1, it2);
	std::vector<int>::iterator it3 = it1 + distance;
	```

# Empty container
If the container is empty, the iterators returned by `begin()` and `end()` are equal.
```c++
while(!s.empty())
{
...
}
```
equals to
```c++
while(s.begin() != s.end()){

}
```
# Moving iterator
```c++
for (auto it=s.begin(); it != s.end(); ++it)
```

# Iterator type
```c++
vector<int>::iterator it;
string::iterator it2
vector<int>::const_iterator it;
string::const_iterator it2
```

```
begin(), end()
cbegin(), cend()
```

# Standard Container Iterator Operations
```c++
*it
it->member
++it
--it
it1 == it2
it1 != it2
```
{% endraw %}