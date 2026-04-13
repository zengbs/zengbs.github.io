---
title: "Arithmetic conversion"
date: 2026-04-13T15:32:36+08:00
draft: false
render_with_liquid: false
---

---
title: Arithmetic conversion
tags: [CPP]

---

# Arithmetic Conversion

Rank:
```
long double (highest rank)
double
float
long long
long
int (lowest rank)
```

Step 1:
If one operand is an integral type and the other a floating point type, the integral operand is converted to the type of the floating point operand (no integral promotion takes place). Otherwise, any integral operands are numerically promoted to either `int` or `unsigned int`.

Step 2:
After promotion, if one operand is `signed` and the other `unsigned`, special rules apply (see below) Otherwise, the operand with lower rank is converted to the type of the operand with higher rank.

:::info
* If the rank of the `unsigned` operand is greater than or equal to the rank of the `signed` operand, the `signed` operand is converted to the type of the `unsigned` operand.
* If the type of the `signed` operand can represent all the values of the type of the `unsigned` operand, the type of the `unsigned` operand is converted to the type of the `signed` operand.
* Otherwise both operands are converted to the corresponding `unsigned` type of the `signed` operand.
:::