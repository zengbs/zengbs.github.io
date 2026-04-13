---
title: "The data members and member fu"
date: 2026-04-13T15:32:38+08:00
draft: false
---

---
title: The data members and member fu
tags: [CPP]

---

1. The data members and member functions of a `protected` section of a class, although still unavailable to the general program, are available to the derived class.
2. A member is made `private` to a base class if we wish to prevent subsequently derived classes from having direct access to that member.
3. A member is made `protected` if we believe it provides an operation or data storage a subsequently derived class requires direct access to in order for that derived class to be effectively implemented.


# Defining the Base Class
The members of the abstract base class represent:
1. **The set of operations supported by all the derived class query types.** This includes both virtual operations overridden by the derived class types and nonvirtual operations that are shared among the derived classes. We'll look at an example of each.
2. **The set of data members common to the derived classes**. By factoring these members out of the derived classes into our abstract Query class, we are able to access the members independent of the actual type on which we are operating. Again, we'll look at two examples.
3. The peculiar syntax
   ```c++
   virtual void eval() = 0;
   ```
   indicates that no virtual definition is provided for the `eval()` function of an abstract base class. Why? Because there is no meaningful algorithm for it to define. This instance of `eval()` is called a **pure virtual function**.


# Defining the Derived Classes