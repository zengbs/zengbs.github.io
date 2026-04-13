---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

###### tags: `CPP`
# Reference

* **Declaration and initialization**: Pointers are declared using the * symbol, and they are initialized with the address of the object they point to. References are declared using the & symbol, and they are initialized with the object they refer to.
* **Memory allocation**: Pointers are stored in memory separately from the objects they point to, and they require dynamically allocated memory. References, on the other hand, do not require dynamically allocated memory, as they simply provide an alternative name for an object.
* **Changeability**: Pointers can be changed to point to different objects at any time, while references cannot be changed to refer to a different object after they are initialized.
* **Nullability**: Pointers can be set to the null pointer value (nullptr), which indicates that they do not point to any object. References cannot be set to null, as they must always refer to an object.
* **Syntax**: Pointers and references have different syntax when used to access the objects they point to or refer to. To access the object pointed to by a pointer, you must dereference the pointer using the * operator. To access the object referred to by a reference, you can simply use the reference's name.
{% endraw %}