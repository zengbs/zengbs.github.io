---
title: "Numeric promotions"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: Numeric promotions
tags: [CPP]

---


# Integral Promotion
* `signed char` or `signed short` can be converted to `int`.
* `unsigned char`, `char8_t`, and `unsigned short` can be converted to `int` if int can hold the entire range of the type, or `unsigned int` otherwise.
* If `char` is signed by default, it follows the `signed char` conversion rules above. If it is unsigned by default, it follows the `unsigned char` conversion rules above.
* `bool` can be converted to `int`, with `false` becoming 0 and `true` becoming 1.
# Floating-point Promotion
* `float` can be converted to a value of type `double`.


{% endraw %}