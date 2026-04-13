---
title: "Numeric conversions"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: Numeric conversions
tags: [CPP]

---

# Numeric Conversion
### 1. Integral Type to Integral Type (excluding integral promotions)
```c++
short s = 3; // convert int to short (unsafe)
long l = 3; // convert int to long (safe)
char ch = s; // convert short to char (unsafe)
unsigned int u = 3; // convert int to unsigned int (unsafe)
```
### 2. Floating-point Type to Floating-point Type  (excluding floating point promotions)
```c++
float f = 3.0; // convert double to float (unsafe)
long double ld = 3.0; // convert double to long double (safe)
```
### 3. Floating-point Type to Integral Type
```c++
int i = 3.5; // convert double to int (unsafe)
```
### 4. Integral Type to Floating-point Type
```c++
double d = 3; // convert int to double (safe)
```
### 5. Integral or Floating-point Type to Bool Type
```c++
bool b1 = 3; // convert int to bool (safe)
bool b2 = 3.0; // convert double to bool (unsafe, becasuse of NaN?)
```


## Other Implicit Conversions
### Array to Pointer Conversion
```c++
int ia[10];
int *ip = ia;
```
### Pointer Conversion
```c++
int* ip;
void* vp = ip;
```
### Conversion to `bool`
```c++
int* ip = new int(100);
if (ip)
```
### Conversion to `const`
```c++
int i;
const int& ri = i;
const int* pi = &i;
```

{% endraw %}