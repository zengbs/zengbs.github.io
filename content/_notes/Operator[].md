---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

1. A subscript operator must be defined as a class member function.
2.  To appear on the left-hand side, its return value must be an lvalue. This is achieved by specifying the return type as a reference:
    ```c++
    inline char&
    String::operator[]( int elem ) const
    {
       return _string[ elem ];
    }
    ```
3. If the return type of the `operator=` is a reference, an object defined by `T obj = arry[3]` can change the value of `arry[3]`, ended up causing unexpected behavior.  True?
    False. `T obj = arry[3]` calls copy ctor, `T obj; obj = arry[3]` calls copy assignment.
{% endraw %}