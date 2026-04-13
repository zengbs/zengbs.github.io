---
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

# `string` to `int`
```c++=
std::string str = "123";
int num = std::stoi(str);
```
# `int` to `string`
```c++=
int num = 123;
std::string str = std::to_string(num);
```
# `char` to `int`
```c++=
 char ch = 'A';
 int a = ch-'0';
```
# `int` to `char`
```c++=
int a = 6;
char ch = a;
```
# `string` to `char`
```c++=
std::string str = "A";
char ch = str[0];
```
# `char` to `string`
```c++=
char ch = 'A';
std::string str(1, ch);
```
{% endraw %}