---
title: "std__deque"
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: 'std::deque'
tags: [CPP]

---

# Implementation
double-ended queue

# Capacity

# Modifiers
| Operation      | Time                                                                                                                  |
| -------------- |:--------------------------------------------------------------------------------------------------------------------- |
| `clear`        | O(n)                                                                                                                  |
| `insert`       | insert an element: O(1)+O(min(\|`end`-`pos`\|,\|`begin`-`pos`\|))<br>insert a range: O(\|`range`\|)+O(min(\|`end`-`pos`\|,\|`begin`-`pos`\|)) |
| `insert_range` |   O(\|`range`\|)+O(min(\|`end`-`pos`\|,\|`begin`-`pos`\|))                                                                                   |
| `emplace`      | O(min(\|`end`-`pos`\|,\|`begin`-`pos`\|))                                                                                                    |
| `erase`        | O(`erased length`)+O(\|`end`-`pos`\|)                                                                                 |
| `push_back`    | O(1)                                                                                                                  |
| `emblace_back` | O(1)                                                                                                                  |
| `append_range` | If reallocation happen: O(m)<br>Otherwise: O(\|`range`\|)                                                             |
| `pop_back`     | O(1)                                                                                                                  |
| `resize`       | If reallocation happen: O(m)<br>Otherwise: O(`erased/inserted length`)                                                |
| `swap`         | O(1)                                                                                                                  |

* n = length of original vector.
* m = length of modified vector
* end = the index of the last element of the orignal vector
* pos = the position where new element inserted/erased.



![deque](https://hackmd.io/_uploads/BJg0_M03T.png)

{% endraw %}