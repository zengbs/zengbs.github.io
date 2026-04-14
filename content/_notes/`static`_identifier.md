---
date: 2026-04-13T15:32:38+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

# Satic local variable
Space scope: block
Time scope: from the line where `static` var. is used to the end of program.
# Static global variable
Space scope: The file which `static` global var. is used.
Time scope: The entire program.
# Static function
Space scope: The file which `static` function is used.
# Static member variable in a class
A static data member of a class is shared among all instances of the class.
## Usage (initialization)
```c++=
class MyClass{
public:
    getCounter(...);
    static int counter;
}

// Initialize static member variable
int MyClass::counter = 0;

int main(){

}
```
# Static member function in a class
A static member function of a class can be called on the class itself, rather than on instances of the class. It does not have access to the this pointer, and can only access static data members and other static member functions.
## Usage
```c++=
class MyClass{
public:
    static getCounter(...);
    static int counter;
}

// Initialize static member variable
int MyClass::counter = 0;

int main(){
    MyClass::getCounter();
}
```
# Summary
![](https://hackmd.io/_uploads/H1YGo32PC.png)

{% endraw %}