---
title: "Argument Passing in C++"
date: 2026-04-13T15:32:36+08:00
draft: false
---

---
title: Argument Passing in C++
tags: [CPP]

---

# Default Arguments

## Calling Functions with Default Arguments
0. Declaration in header:
	```c++
	typedef string::size_type sz;
	string screen(sz ht = 24, sz wid = 80, char backgrnd = ' ');
	```
1. If we want to use the default argument, we omit that argument when we call the function.
	```c++
	string window;
	window = screen();             // equivalent to screen(24,80,' ')
	window = screen(66);           // equivalent to screen(66,80,' ')
	window = screen(66, 256);      // screen(66,256,' ')
	window = screen(66, 256, '#'); // screen(66,256,'#')
	```
2. The default arguments are used for the trailing (right-most) arguments of a call.
	```c++
	window = screen(, , '?'); // error: can omit only trailing arguments
	window = screen('?');     // calls screen('?',80,' ')
	```
:::info
Ordering the parameters so that those least likely to use a default value appear first and those most likely to use a default appear last.
:::

## Default Arguments Declarations
1. We cannot change an already declared default value
	```c++
    string screen(sz ht, sz wid, char backgrnd=' '); // first declaration
	string screen(sz ht, sz wid, char backgrnd='*'); // error: redeclaration
	string screen(sz ht, sz wid, char backgrnd=' '); // error: redeclaration
	```
3. But we can add a default argument as follows
	```c++
    // ok: adds default arguments
	string screen(sz ht=24, sz wid=80, char backgrnd);
	```

## Default Argument Initializers
Names used as default arguments are resolved in the scope of the function declaration. The value that those names represent is evaluated at the time of the call:
```c++
// the declarations of wd , def, and ht must appear outside a function
sz wd = 80;
char def = ' ';
sz ht();
string screen(sz = ht(), sz = wd, char = def);
string window = screen(); // calls screen(ht(), 80, ' ')

void f2()
{
    def = '*';         // changes the value of a default argument
    sz wd = 100;       // hides the outer definition of wd but does not change the default
    window = screen(); // calls screen(ht(), 80, '*')
}
```