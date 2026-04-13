---
title: "Summary"
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

---
title: Summary
tags: [CPP]

---


# Call Overridden/Overriding Function Using Pointer
| `virtual` | `override` | Is the prototype of the called function the same as the function defined in the `Base` class, or the same as the function defined in the `Derived` class?" | Which function in `Derived` or `Base` is called? |
|:---------:|:----------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------:|:------------------------------------------------:|
|     O     |     O      |                                                                           `Both`                                                                           |                    `Derived`                     |
|     O     |     O      |                                                                         `Derived`                                                                          |                Compiling error.<br>Intend to call `Derived` but violet rule 2.                 |
|     O     |     O      |                                                                           `Base`                                                                           |                Compiling error.<br>Intend to call `Derived` but no matching function in `Derived`.                 |
|     O     |     X      |                                                                           `Both`                                                                           |                    `Derived`                     |
|     O     |     X      |                                                                         `Derived`                                                                          |                Compiling error<br>Intend to call `Derived` but violet rule 2.                 |
|     O     |     X      |                                                                           `Base`                                                                           |                      `Base`                      |
|     X     |     O      |                                                                           `Both`                                                                           |                Compiling error<br>See rule 1                 |
|     X     |     O      |                                                                         `Derived`                                                                          |                Compiling error<br>See rule 1                 |
|     X     |     O      |                                                                           `Base`                                                                           |                Compiling error<br>See rule 1                 |
|     X     |     X      |                                                                           `Both`                                                                           |                      `Base`                      |
|     X     |     X      |                                                                         `Derived`                                                                          |                Compiling error.<br>Intend to call `Based` but no matching function in `Base`.                |
|     X     |     X      |                                                                           `Base`                                                                           |                      `Base`                      |



# Rules
1. For each function marked `override` in `Derived`, there must be a function marked `virtual` in `Base`.
2. The signature of the overriding function should be the same as the virtual function in the `Base`.