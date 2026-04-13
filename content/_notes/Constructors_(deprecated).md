---
title: "Constructors (deprecated)"
date: 2026-04-13T15:32:36+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: Constructors (deprecated)
tags: [CPP]

---

###### tags: `CPP`

# Constructors (deprecated)
* A class constructor provides the opportunity to initialize the new object as it is created and to ensure that member variables contain valid values.
* A ***default constructor*** is a constructor that can be called without arguments. This constructor is invoked by default if you do not explicitly invoke a constructor with given arguments.
```c++
Box myBox; // Invokes the default constructor
```
* If you do not define any constructor for a class—neither a default constructor nor any other constructor—then the compiler generates one for you: a default constructor. 
* It is a special member function of a class that is ***manually/automatically*** executed whenever we create new objects of that class.
* It has ***exact same*** name as the class.
* It does not have any return type at all, not even `void`.
* Parameterized and unparameterized constructor runs manually and automatically, respectively.
* Once you define a constructor, the compiler won’t supply a default constructor
anymore, at least not by default. 
## Defining a Class Constructor
```c++
class{
   public:
      // Constructor (function name should be exactly same as class)
      Box( double length, double width, double height ){
         m_length = length;
         m_width = width;
         m_height = height;
      }
      // Function to calculate the volume of box
      double volume(){
         return m_length * m_width * m_height;
      }
   private:
      double m_length {1.0};
      double m_width {1.0};
      double m_height {1.0};
}

int main()
{
   // Create a box
   Box firstBox {80.0, 50.0, 40.0}; 
   
   // Calculate the box volume
   double firstBoxVolume {firstBox.volume()}; 
   
   std::cout << "Volume of Box object is " << firstBoxVolume << std::endl;
   
   // Box secondBox; // Causes a compiler error message
}

```
## Using the `default` Keyword (C++20)
If you still want to invoke default constructor, even if user-defined constructors present,  you’d have to do is either add the following constructor definition somewhere in the public section of the class:
```c++
Box() {}
```
or
```c++
Box() = default;
```
:::warning
While an explicit empty body definition and a defaulted constructor declaration are nearly equivalent, the use of the default keyword is preferred in modern C++ code.
:::
## Defining out-of-class functions
This is particularly interesting for member functions that have longer function bodies, or for classes with a larger number of members.
```c++
// Class to represent a box
class Box
{
   public:
      Box() = default;
      Box(double length, double width, double height);
      
      double volume(); // Function to calculate the volume of a box
      
   private:
      double m_length {1.0};
      double m_width {1.0};
      double m_height {1.0};
};


// Constructor definition
Box::Box(double length, double width, double height)
{
   std::cout << "Box constructor called." << std::endl;
   m_length = length;
   m_width = width;
   m_height = height;
}

// Member function definition
double Box::volume()
{
   return m_length * m_width * m_height;
}
```
## Default Arguments for Constructor Parameters
Default parameter values for constructors and member functions always go inside the class, not in an external constructor or function definition.
```c++
class Box
{
   public:
      // Constructors
      Box() = default;
      Box(double length = 1.0, double width = 1.0, double height = 1.0);
      
      double volume(); // Function to calculate the volume of a box
   private:
      // Same member variables as always...
};
```
This class will results in compiling error! As the constructor with three parameters allows all three arguments to be omitted, which is indistinguishable from a call to the default constructor.

The obvious solution is to get rid of the defaulted constructor that accepts no parameters in this instance. If you do so, everything compiles and executes okay.
## Using a Member Initializer List
## Using the `explicit` Keyword
## Delegating Constructors
{% endraw %}