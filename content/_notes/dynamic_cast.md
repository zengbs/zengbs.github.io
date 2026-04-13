---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

# Legal Cases
```c++=
#include <iostream>
#include <typeinfo>

class Base {
public:
    virtual ~Base() {} // Polymorphic base class
};

class Derived : public Base {
public:
    void sayHello() { std::cout << "Hello from Derived!" << std::endl; }
};

class DerivedAgain : public Derived {};

int main() {

    Derived* dptr = new DerivedAgain();
    DerivedAgain* daptr = dynamic_cast<DerivedAgain*>(dptr);
    if (!daptr){
       std::cout << "fail" << std::endl;
    }else{         
       std::cout << "succeed!" << std::endl;
    }           
    delete dptr;

    // Rule 1: Downcasting - Pointer type
    Derived d;
    Base* basePtr = &d; // upcast, dynamic_cast may be used, but unnecessary
    Derived* derivedPtr = dynamic_cast<Derived*>(basePtr); // Valid downcast
    if (derivedPtr) {
        derivedPtr->sayHello(); // Output: Hello from Derived!
    }

    // Rule 2: Invalid downcast returns null (pointer type)
    Base* anotherBasePtr = new Base(); // Points to a Base object
    Derived* invalidDerivedPtr = dynamic_cast<Derived*>(anotherBasePtr); // Invalid downcast
    if (!invalidDerivedPtr) {
        std::cout << "Invalid downcast returned null pointer." << std::endl;
    }
    delete anotherBasePtr;

    // Rule 3: Reference type casting
    try {
        Base& baseRef = d;
        Derived& derivedRef = dynamic_cast<Derived&>(baseRef); // Valid reference cast
        derivedRef.sayHello(); // Output: Hello from Derived!
    } catch (const std::bad_cast& e) {
        std::cout << "Reference cast failed: " << e.what() << std::endl;
    }

    // Rule 4: Valid runtime type check for polymorphic objects
    try {
        Base* baseObj = new Derived();
        Derived& derivedRef = dynamic_cast<Derived&>(*baseObj); // Valid reference cast
        derivedRef.sayHello(); // Output: Hello from Derived!
        delete baseObj;
    } catch (const std::bad_cast& e) {
        std::cout << "Runtime type check failed: " << e.what() << std::endl;
    }

    return 0;
}
```

# Illegal Cases
```c++=
#include <iostream>
#include <typeinfo>

class Base {
public:
    // No virtual function here, so this class is not polymorphic
};

class Derived : public Base {
    // Derived does not add any virtual function
};

class Unrelated {
    // Unrelated class, no relationship with Base or Derived
};

int main() {
    // Rule: Casting on non-polymorphic types (fails to compile)
    Base baseObj;
    Derived* invalidCast1 = dynamic_cast<Derived*>(&baseObj); // Invalid: Base is not polymorphic
    // Error: Cannot use dynamic_cast with non-polymorphic types.

    // Rule: Casting unrelated types (fails to compile)
    Unrelated unrelatedObj;
    Base* invalidCast2 = dynamic_cast<Base*>(&unrelatedObj); // Invalid: No relationship between Base and Unrelated
    // Error: Cannot cast unrelated types with dynamic_cast.

    // Rule: Undefined behavior for reference casts when the object is not of the correct type
    try {
        Base& invalidRef = dynamic_cast<Base&>(unrelatedObj); // Undefined behavior: unrelatedObj is not a Base
    } catch (const std::bad_cast& e) {
        std::cout << "Caught std::bad_cast: " << e.what() << std::endl;
    }
    // Undefined behavior: Attempting to cast an unrelated type as a reference.

    return 0;
}

```
{% endraw %}