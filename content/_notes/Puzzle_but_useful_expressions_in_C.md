---
title: Puzzle but useful expressions in C


---

# Puzzle but useful expressions in C
###### tags: `C`


# [Short-ciruit evaluation](https://en.wikipedia.org/wiki/Short-circuit_evaluation)
* The logical operators (e.g., `||` and `&&`) do not evaluate their second argument if the result of the expression can be determined by evaluating the first argument. e.g.,
    * `a && 5/a` will never cause a division by zero.
    * `p && p++` will never cause the dereferencing a null pointer.

