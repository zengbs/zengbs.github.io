---
title: "Selecting a Conversion"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---
title: Selecting a Conversion
tags: [CPP]

---

1. The conversion performed by a conversion function can be followed by a standard conversion to bring the result of the conversion function to the target type of the conversion. Similarly, the conversion performed by a constructor can be preceded by a standard conversion to bring the value to be converted to the type of the constructor parameter. I.e.,
    *  Conversion Function ==> Standard Conversion
    *  Standard Conversion ==> Constructor
2. If two conversion functions (constructors) can be used, the standard conversion sequence following (preceding) the conversion function is used to select ***the best user-defined conversion sequence***.
    ```c++
    #include <iostream>
    
    class Student {
    public:
       Student( int id ) : m_id(id) {
          std::cout << "Called constructor: int -> Student\n";
       }
       Student( unsigned short id ) : m_id(static_cast<unsigned short>(id)) {
          std::cout << "Called constructor: unsigned short -> Student\n";
       }
       operator short();
       operator long();
    private:
       int m_id;
    };
    
    Student::operator short(){
       std::cout << "Called conversion function: Student -> short\n";
       return static_cast<short>(m_id);
    }
    
    Student::operator long(){
       std::cout << "Called conversion function: Student -> long\n";
       return static_cast<unsigned short>(m_id);
    }
    
    int main(){
    
       short id = 0;
    
       // Standard conversion (promotion): short to int
       // Constructor: convert int to Student
       Student daniel(id);
    
       // User-defined conversion: convert Student to short
       // Standard conversion (promotion): short to int
       int fid = daniel;
       std::cout << "fid = " << fid << "\n";
    
       return 0;
    }
    ```
4. All possible conversion sequences may be equally good, in which case we say that the conversion is ambiguous. In this case no implicit conversion is applied by the compiler.
5. The programmer can indicate the conversion sequence to be used by specifying an explicit cast.
6. Ambiguity when selecting a user-defined conversion sequence for an implicit conversion may also arise when two classes define conversions to each other.
    ```c++
    #include <iostream>
    
    class Teacher;  // Forward declaration for use in Student
    
    class Student {
    public:
        Student(Teacher& t);  // Constructor taking Teacher&
    
        void show() const {
            std::cout << "Student created with ID = " << m_id << std::endl;
        }
    private:
        int m_id;
    };
    
    class Teacher {
    public:
        Teacher(int id) : m_id(id) {}
    
        // User-defined conversion from Teacher to Student
        operator Student() {
            std::cout << "Converting Teacher to Student...\n";
            return Student(*this);  // Uses Student(Teacher&) constructor
        }
        int getID() const { return m_id; }
    private:
        int m_id;
    };
    
    // Define Student constructor after Teacher is fully defined
    Student::Student(Teacher& t) : m_id(t.getID()) {}
    
    int main() {
        Teacher t1(42);
    
        // Implicit conversion: Teacher → Student using Teacher::operator Student()
        // Implicit conversion: Teacher → Student using Student::Student( Teacher& )
        Student s1 = t1; // Error: ambiguous
    
        // Explicit conversion also possible
        Student s2 = static_cast<Student>(t1);
        s2.show();
    
        return 0;
    }
    ```
    However, the version below is ambigous as `Box::operator SimplePolygon<int>` was not instantiated.
    ```c++
    #include <iostream>
    
    template<typename C>
    class SimplePolygon;
    
    template<typename C>
    class Box {
    public:
       Box(C x, C y) : _x(x), _y(y) {}
       template<typename D>
       operator SimplePolygon<D>  (){
          std::cout << "Calls Box::operator\n";
          return { _x, _y };
       }
       C getX() { return _x; }
       C getY() { return _y; }
    private:
       C _x;
       C _y;
    };
    
    
    
    template<typename C>
    class SimplePolygon {
    public:
       SimplePolygon(Box<C>& box) : _x(box.getX()), _y(box.getY()) { std::cout << "Calls SimplePolygon()\n"; }
    private:
       C _x;
       C _y;
    };
    
    int main() {
    
       Box<int> box(1,2);
       
       // Calls SimplePolygon()
       SimplePolygon<int> sp = box;
    
       return 0;
    }
    ```
# Candidate Functions
1. For arguments and parameters of class type, the set of possible conversions must include the user-defined conversion sequences we introduced in the previous section. The third step of the function overload resolution process must therefore rank user-defined conversion sequences.
4. If a function call has an argument that is an object of class type, a pointer to a class type, a reference to a class type, or a pointer to a member of a class, the candidate functions are the union of the following functions (visible at the point of call):
    * the functions have the same name as the function called
    * the functions declared within the namespace where the class type is defined
    * the functions that are declared as friends within the class member list.

# Candidate Functions for Function Calls in Class Scope
1. When a function call of the form `calc(t)` appears in class scope (in a member function, for example), the set containing the function declarations visible at the point of the call may contain functions that are not member functions.
2. Name resolution is used to find the set of candidate functions visible at the point of the call.

# Ranking User-Defined Conversion Sequence
1. The best viable function is the function for which
    * The conversions applied to the arguments are no worse than the conversions necessary to call any other viable function, and
    * The conversions on some arguments are better than the conversions necessary for the same arguments when calling any other viable function.
2. A standard conversion sequence is always better than a user-defined conversion sequence for ***the best viable function***.
3. For the selection of ***the best viable function***, if two user-defined conversion sequences use different conversion functions or use different constructors, both conversion sequences are considered equally good.
    ```c++
    #include <iostream>
    
    class Student {
    public:
        Student(short id) : m_id(id) {}
        operator float(){ return m_id; }
        operator int(){ return m_id; }
        void show() const {
            std::cout << "Student created with ID = " << m_id << std::endl;
        }
    private:
        short m_id;
    };
    
    void addOne( int ia ){
       std::cout << "Calls addOne(int)\n";
       std::cout << "ia = " << ia+1 << "\n";
    };
    
    void addOne( double fa ){
       std::cout << "Calls addOne(unsigned short)\n";
       std::cout << "fa = " << fa+1 << "\n";
    };
    
    int main() {
    
        Student daniel(static_cast<short>(1));
    
        // addOne(int)  : Student -> int   ->    int (exact match)
        // addOne(float): Student -> float -> double (conversion)
        addOne(daniel); // Error: ambiguous
    
        return 0;
    }
    ```
5. For the selection of ***the best viable function***, if two user-defined conversion sequences use the ***same*** conversion function, then the rank of the standard conversion sequence that follows the conversion function is used to select the best user-defined conversion sequence.
    ```c++
    #include <iostream>
    
    class Student {
    public:
        Student(short id) : m_id(id) {}
        operator short(){ return m_id; }
        void show() const {
            std::cout << "Student created with ID = " << m_id << std::endl;
        }
    private:
        short m_id;
    };
    
    void addOne( int ia ){
       std::cout << "Calls addOne(int)\n";
       std::cout << "ia = " << ia+1 << "\n";
    };
    
    void addOne( unsigned short ia ){
       std::cout << "Calls addOne(unsigned short)\n";
       std::cout << "ia = " << ia+1 << "\n";
    };
    
    int main() {
    
        Student daniel(static_cast<short>(1));
    
        // addOne(int)           : Student -> short -> int (promotion)
        // addOne(unsigned short): Student -> short -> unsigned short
        addOne(daniel);
    
        return 0;
    }
    ```
7. Only one user-defined conversion can be part of a user-defined conversion sequence. 
{% endraw %}