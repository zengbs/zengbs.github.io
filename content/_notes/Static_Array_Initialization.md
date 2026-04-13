---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
tags: [CPP]

---

# Static Array Initialization
1. Each element in turn is initialized with the default Account constructor.
2. Those elements without an explicit set of constructor arguments are initialized with the default constructor of the class.
3. The declaration `Account *pact = new Account[ 10 ];` creates an array of ten `Account` class objects allocated on the heap. Each is initialized with the `Account` class default constructor.
```c++
#include <iostream>
#include <string>
#include <array>

class Image {
public:
   Image(){ _name = "default_name"; _index = -1; }
   Image(const std::string& name, int index) : _name(name), _index(index) {}
   ~Image() {
       _name.clear();
       _index = -1;
   }
   std::string& getName() { return _name; }
   int getIndex() { return _index; }
private:
   std::string _name;
   int _index;
};

int main() {

    const int len = 4;

    Image images1[len];             // calls default ctor len times
    std::array<Image, len> images2; // calls default ctor len times

    std::cout << "Case 1:" << std::endl;

    for ( auto & img : images1){
       std::cout << img.getName() << ", " << img.getIndex() << std::endl;
    }

    std::cout << "\nCase 2:" << std::endl;
    Image images3[] = {
        Image("edwd", 2),
        Image(),
    };

    for ( auto & img : images3){
       std::cout << img.getName() << ", " << img.getIndex() << std::endl;
    }

    std::cout << "\nCase 3:" << std::endl;
    Image images4[4] = {
        Image("edwd", 2),
        Image(),
    };

    for ( auto & img : images4){
       std::cout << img.getName() << ", " << img.getIndex() << std::endl;
    }

    std::cout << "\nCase 4:" << std::endl;
    Image *images5 = new Image[3];
    for ( int i=0;i<3;i++ ){
       std::cout << images5[i].getName() << ", " << images5[i].getIndex() << std::endl;
    }
    delete [] images5;
    return 0;
}
```

# Heap Array Initialization

# Vector of Class Objects

The initialization of the elements, `vector< Point > vec( 5 )`, occurs as follows:
1. A temporary object of the underlying class type is created. The default constructor of the class is applied to create it.
2. The copy constructor is applied to each element of the vector in turn, initializing each class object with a copy of the temporary class object.
3. The temporary class object is destroyed.

The cost of initializing the vector is greater: (1) the construction and destruction of the temporary object, of course, and (2) copy constructors generally tend to be computationally more complex than default constructors.

As a general design rule, then, a vector of class objects is best suited for **element insertion only**; that is, we define an empty vector. If we have precalculated the number of elements to be inserted, or have a good guess as to the size, we reserve the associated memory. We then proceed with element insertion. Forx example:

```c++
#include <iostream>
#include <string>
#include <vector>

class Image {
public:
   Image(){ _name = "default_name"; _index = -1; }
   Image(const std::string& name, int index) : _name(name), _index(index) {}
   ~Image() {
       _name.clear();
       _index = -1;
   }
   std::string& getName() { return _name; }
   int getIndex() { return _index; }
private:
   std::string _name;
   int _index;
};

int main() {

    // significant overhead, do not use it
    // std::vector<Image>(Image());

    std::vector<Image> vec;

    // reserve capacity
    vec.reserve(10);

    for(int i=0;i<10;i++){
       vec.emplace_back(Image("dqwd", i));
    }

    for(auto& img : vec){
       std::cout << img.getName() << ", " << img.getIndex() << std::endl;
    }

    return 0;
}
```
{% endraw %}