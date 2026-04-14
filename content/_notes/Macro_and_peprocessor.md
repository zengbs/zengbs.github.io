---


---


# Macro and peprocessor

## Basic usage
```c=
#include<stdio.h>
#define MAX 100
int main()
{
    printf("max is %d", MAX);
    return 0;
}
```
Output: `max is 100`

---

### Pitfalls
```c=
#include <stdio.h>
 
#define square(x) x*x
int main()
{
    int x = 36/square(6);
    printf("%d", x);
    return 0;
}
```
Output: `36`

---
## Stringizing operator (#)
https://gcc.gnu.org/onlinedocs/cpp/Stringizing.html
```c=
#include <stdio.h>
#define mkstr(s) #s
int main(void)
{
    printf(mkstr(geeksforgeeks));
    return 0;
}
```
Output: `geeksforgeeks`

### Application

```c=
#include<stdio.h>


#define GIT_SHA1   123456
#define STR( x )                #x
#define SHOW_MACRO( x )         STR( x )

int main()
{
  printf( "%s\n", SHOW_MACRO( GIT_SHA1 ));
  printf( "%s\n", STR( GIT_SHA1 ));

  return 0;
}

```

Output:
```
123456
GIT_SHA1
```

Conclusion:
1. `STR(GIT_SHA1)` is replaced by `"GIT_SHA1"`, even if `GIT_SHA1` has been defined previously.
2. `SHOW_MACRO( GIT_SHA1 )` is replaced by `SHOW_MACRO(123456)`.
3. `SHOW_MACRO(123456)` is replaced by `"123456"`.

Hence preprocessor performs the stringizing operator and then replace macro.

---
## Concatenation (##)
https://gcc.gnu.org/onlinedocs/cpp/Concatenation.html
```c=
#include <stdio.h>
#define concat(a, b) a##b
int main(void)
{
    int xy = 30;
    printf("%d", concat(x, y));
    return 0;
}
```
Output: 30

---
## Variadic Macros
https://gcc.gnu.org/onlinedocs/cpp/Variadic-Macros.html


```c=
#define MACRO_VA_ARGS(...) RESULT(__VA_ARGS__)

MACRO_VA_ARGS()
MACRO_VA_ARGS(one)
MACRO_VA_ARGS(two,three)
MACRO_VA_ARGS(foo, bar, baz)
```
When this source file is preprocessed (`gcc -E -P basics.c`), it prints 
```c=
RESULT()
RESULT(one)
RESULT(two,three)
RESULT(foo, bar, baz)
```
### Application

```c=
#include <stdio.h>

#define TQ84_PRINTF(FORMAT, ...) printf("tq84: " FORMAT "\n", __VA_ARGS__)

int main() {

  TQ84_PRINTF("%d", 42);
  TQ84_PRINTF("%s, %s", "Hello", "world");
  TQ84_PRINTF("%d %f %s", 99, 3.14, "An int and a float");

}
```

## Common Predefined Macros (GNU extension)

## Pitfalls
[Macro Pitfalls](https://gcc.gnu.org/onlinedocs/cpp/Macro-Pitfalls.html#Macro-Pitfalls)