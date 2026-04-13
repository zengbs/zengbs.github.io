---
title: "Time complexities of modifiers"
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: Time complexities of modifiers
tags: [CPP]

---



| Container/Modifier    | clear | insert | insert_range | insert_or_assign | emplace | emplace_hint | try_emplace | erase | push_front | prepend_range | emplace_front | pop_front | push_back | append_range | emplace_back | pop_back | swap | merge | extract |
|-----------------------|-------|--------|--------------|------------------|---------|--------------|-------------|-------|------------|---------------|---------------|-----------|-----------|--------------|--------------|----------|------|-------|---------|
| **string**            | O(n)  | N/A    | O(n)         | N/A              | N/A     | N/A          | N/A         | O(n)  | N/A        | N/A           | N/A           | N/A       | O(n)      | O(n)         | O(n)         | O(1)     | O(1) | N/A   | N/A     |
| **array**             | N/A   | N/A    | N/A          | N/A              | N/A     | N/A          | N/A         | N/A   | N/A        | N/A           | N/A           | N/A       | N/A       | N/A          | N/A          | N/A      | O(n) | N/A   | N/A     |
| **vector**            | O(n)  | O(n)   | O(n)         | N/A              | O(n)    | N/A          | N/A         | O(n)  | N/A        | N/A           | N/A           | N/A       | O(1)*     | O(n)         | O(1)*        | O(1)     | O(1) | N/A   | N/A     |
| **deque**             | O(n)  | O(n)   | O(n)         | N/A              | O(n)    | N/A          | N/A         | O(n)  | O(1)       | O(n)          | O(1)          | O(1)      | O(1)      | O(n)         | O(1)         | O(1)     | O(1) | N/A   | N/A     |
| **forward_list**      | O(n)  | O(1)   | O(n)         | N/A              | O(1)    | N/A          | N/A         | O(1)  | O(1)       | O(n)          | O(1)          | O(1)      | N/A       | N/A          | N/A          | N/A      | O(1) | N/A   | N/A     |
| **list**              | O(n)  | O(1)   | O(n)         | N/A              | O(1)    | N/A          | N/A         | O(1)  | O(1)       | O(n)          | O(1)          | O(1)      | O(1)      | O(n)         | O(1)         | O(1)     | O(1) | O(1)  | N/A     |
| **set**               | O(n)  | O(log n) | O(n)       | N/A              | O(log n)| O(log n)     | N/A         | O(log n) | N/A      | N/A           | N/A           | N/A       | N/A       | N/A          | N/A          | N/A      | O(1) | O(n)  | O(log n)|
| **multiset**          | O(n)  | O(log n) | O(n)       | N/A              | O(log n)| O(log n)     | N/A         | O(log n) | N/A      | N/A           | N/A           | N/A       | N/A       | N/A          | N/A          | N/A      | O(1) | O(n)  | O(log n)|
| **unordered_set**     | O(n)  | O(1)*  | O(n)        | N/A              | O(1)*   | N/A          | N/A         | O(1)*  | N/A        | N/A           | N/A           | N/A       | N/A       | N/A          | N/A          | N/A      | O(1) | N/A   | O(1)    |
| **unordered_multiset**    | O(n)  | O(1)*  | O(n)         | N/A              | O(1)*   | N/A          | N/A         | O(1)* | N/A        | N/A           | N/A           | N/A       | N/A       | N/A          | N/A          | N/A      | O(1) | N/A   | O(1)    |
| **unordered_map**         | O(n)  | O(1)*  | O(n)         | O(1)*            | O(1)*   | O(1)         | O(1)*       | O(1)* | N/A        | N/A           | N/A           | N/A       | N/A       | N/A          | N/A          | N/A      | O(1) | N/A   | O(1)    |
| **unordered_multimap**    | O(n)  | O(1)*  | O(n)         | O(1)*            | O(1)*   | O(1)         | O(1)*       | O(1)* | N/A        | N/A           | N/A           | N/A       | N/A       | N/A          | N/A          | N/A      | O(1) | N/A   | O(1)    |
| **stack**                 | O(n)  | N/A    | N/A          | N/A              | N/A     | N/A          | N/A         | N/A   | N/A        | N/A           | N/A           | N/A       | O(1)      | N/A          | O(1)         | O(1)     | O(n) | N/A   | N/A     |
| **queue**                 | O(n)  | N/A    | N/A          | N/A              | N/A     | N/A          | N/A         | N/A   | O(1)       | N/A           | O(1)          | O(1)      | O(1)      | N/A          | N/A          | N/A      | O(n) | N/A   | N/A     |
| **priority_queue**        | O(n)  | N/A    | N/A          | N/A              | N/A     | N/A          | N/A         | N/A   | N/A        | N/A           | N/A           | N/A       | O(log n)  | N/A          | O(log n)     | O(log n) | O(n) | N/A   | N/A     |
| **flat_set**              | O(n)  | O(n)   | O(n)         | N/A              | O(n)    | O(n)         | N/A         | O(n)  | N/A        | N/A           | N/A           | N/A       | N/A       | N/A          | N/A          | N/A      | O(n) | O(n)  | O(1)    |
| **flat_multiset**         | O(n)  | O(n)   | O(n)         | N/A              | O(n)    | O(n)         | N/A         | O(n)  | N/A        | N/A           | N/A           | N/A       | N/A       | N/A          | N/A          | N/A      | O(n) | O(n)  | O(1)    |
| **flat_map**              | O(n)  | O(n)   | O(n)         | O(n)             | O(n)    | O(n)         | O(n)        | O(n)  | N/A        | N/A           | N/A           | N/A       | N/A       | N/A          | N/A          | N/A      | O(n) | O(n)  | O(1)    |
| **flat_multimap**         | O(n)  | O(n)   | O(n)         | O(n)             | O(n)    | O(n)         | O(n)        | O(n)  | N/A        | N/A           | N/A           | N/A       | N/A       | N/A          | N/A          | N/A      | O(n) | O(n)  | O(1)    |



# Reference
https://en.cppreference.com/w/cpp/container

https://docs.google.com/document/d/1EqVB2CqI_GmTnIJlv_QOZYAGVwiEr7pH1QeLCSrWlWY/edit?usp=sharing
{% endraw %}