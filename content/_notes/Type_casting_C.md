---


---


# Type casting \(C\)

a cast operator does not mean ==pretend these bits have a different type, and treat them accordingly==; it is a conversion operator, and by definition it yields an rvalue, which cannot be assigned to, or incremented with ++.

## Implicit type casting
![image](https://hackmd.io/_uploads/HJKCNG0-A.png =50%x)

### Example
```c=
short a=10; //initializing variable of short data type
int b; //declaring int variable
b=a; //implicit type casting
```
It is possible for implicit conversions to lose information, signs can be lost (when `signed` is implicitly converted to `unsigned`), and overflow can occur (when `long` is implicitly converted to `float`).
## Explicit type casting
```c=
float a = 1.2;
int b = (int)a + 1;
```

# Type punning and strick aliasing rule
## Example
The following sequence violates strick aliasing rule:
```c=
bool isNegative(float x) {
    unsigned int *ui = (unsigned int *)&x;
    return *ui & 0x80000000;
}
```
The following sequence is type punning and suffer from undefined behavior.:
```c=
bool isPositive(float x) {
                                                                                                         
    union {
        uint32_t ui; 
        float d;
    } my_union = { .d = x };
 
    return (my_union.ui & 0x80000000)==0;
}
```
> § 6.5.2.3/3, footnote 97, ISO/IEC 9899:2018, 2018, p. 59: If the member used to read the contents of a union object is not the same as the member last used to store a value in the object, the appropriate part of the object representation of the value is reinterpreted as an object representation in the new type as described in 6.2.6 (a process sometimes called “type punning”). This might be a trap representation.


# Use cases
1. Between two arithmetic types
```c=
double pi = 3.14159;
int integer_part = (int)pi;  // Casting double to int, result is 3
```
2. Between a pointer type and an integer type:
```c=
char* buffer = "Hello";
uintptr_t address = (uintptr_t)buffer;  // Casting pointer to integer
```
3. Between two pointer types:
```c=
int x = 10;
char* ptr = (char*)&x;  // Casting an int pointer to a char pointer
```
4. Between a cv-qualified and cv-unqualified type:
```c=
void print_value(int* ptr) {
    // Function does not modify the value pointed by ptr
    printf("Value: %d\n", *ptr);
}

int main() {
    const int num = 10;
    // Correctly passing pointer for non-modifying usage
    print_value((int*)&num);
    return 0;
}
```
5. A combination of (4) and either (1), (2), or (3):
```c=
const int* nums = (const int[3]){1, 2, 3};
int* modifiable_nums = (int*)nums;  // Casting away const from a pointer type
```

# Reference
[Aliasing (computing)](https://en.wikipedia.org/wiki/Aliasing_(computing)#Aliased_pointers)
[Type punning](https://en.wikipedia.org/wiki/Type_punning)
[Understanding Strict Aliasing](https://cellperformance.beyond3d.com/articles/2006/06/understanding-strict-aliasing.html)