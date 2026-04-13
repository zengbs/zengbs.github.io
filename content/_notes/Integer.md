---
title: Integer


---

###### tags: `C`

# Integer

* According to `§ 5.2.4.2.1` in `ISO/IEC 9899:1999`, `sizeof(short)`, `sizeof(int)`, and `sizeof(long)` has bytes ***at least*** 2, 2, 4.
* [`gcc`](https://gcc.gnu.org/onlinedocs/cpp/Common-Predefined-Macros.html) also defines `__SIZEOF_SHORT__`, `__SIZEOF_INT__` and `__SIZEOF_LONG__`, etc, to determine the number of bytes of the C standard data types.
    * See `gcc -dM -E - </dev/null |grep SIZEOF`


## Signed number representations



| Binary value | Unsigned | Two's complement | One's complement |
|:------------:|:--------:|:----------------:|:----------------:|
|     000      |    0     |        0         |        +0        |
|     001      |    1     |        1         |        1         |
|     010      |    2     |        2         |        2         |
|     011      |    3     |        3         |        3         |
|     100      |    4     |        -4        |        -3        |
|     101      |    5     |        -3        |        -2        |
|     110      |    6     |        -2        |        -1        |
|     111      |    7     |        -1        |        -0        |


### One's complement
### Two's complement

## Type
`sizeof(uint3)=12`: Three `unsigned int`
`sizeof(ushort4)=8`: Four `unsigned short`
`sizeof(unsigned)=4`: One `unsigned int`

# FQA
* [What is the reason for explicitly declaring `L` or `UL` for long values?](https://stackoverflow.com/questions/13134956/what-is-the-reason-for-explicitly-declaring-l-or-ul-for-long-values)