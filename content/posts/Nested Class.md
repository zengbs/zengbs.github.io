---
title: "Nested Class"
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

---
title: Nested Class
tags: [CPP]

---

# General Rules
1. A nested class is only a type definition, not an object even if it has non-static data members. Creating an object of an Outer class does not create instances of its nested class.
1. A class can be defined within another class. Such a class is called a nested class.
2. Nested Class: inner class, Enclosing class: outer class
4. The definition of a nested class can occur within a public, protected, or private section of its enclosing class.
5. The name of a nested class is visible in its enclosing class scope, but not in other class scopes or in namespace scopes.
    ```c++
    #include <iostream>
    
    class Node {
       public:
       int val = 1;
    };
    
    class Tree {
       class Node {
          public:
          int val = 2;
       };
       public:
       Node node;
    };
    
    Node node;
    
    class List {
       class Node {
          public:
          int val = 3;
       };
       public:
       Node node;
    };
    
    int main(){
    
       std::cout << node.val << std::endl; // 1
    
       Tree tree;
       std::cout << tree.node.val << std::endl; // 2
    
       List list;
       std::cout << list.node.val << std::endl; // 3
    
       return 0;
    }
    ```
6. An enclosing class has no access privileges to the private members of a nested class unless it is declared as a friend of the nested class.
   ```c++
   #include <iostream>
   
   class Outer {
   public:
      class Inner {
      // Grant Outer class full access
      friend class Outer;
      public:
         void showSecret() {
            std::cout << secret << std::endl;
         }
      private:
         int secret = 1;
      };
   
      void accessInner() {
         Inner inner;
         inner.showSecret();
   
         // this line does not work once Outer cannot access private members of Inner
         std::cout << inner.secret << std::endl;
      }
   };
   
   int main(){
      Outer outer;
      outer.accessInner();
      return 0;
   }
   ```
7. As a member of its enclosing class, a nested class has a special privilege: It has unlimited access to its enclosing class's members, even if they are declared private.
	```c++
	#include <iostream>
	
	class Outer {
	public:
	   class Inner {
	   public:
	      void showSecret() {
	         Outer o;
	         std::cout << o.secret << std::endl;
	      }
	   };
	private:
	   int secret = 1;
	};
	
	int main() {
	   Outer::Inner inner;
	   inner.showSecret();
	   return 0;
	}
	```
    However, it is required to define an object of the enclosing class inside the nested class since a nested class is not tied to any specific instance of the enclosing class.
8. Declaring a nested class as a public member of an enclosing class means that the nested class can be used as a type within the entire program.
   ```c++
   #include <iostream>
   
   class Outer {
   public:
      class Inner {
      public:
         void showSecret(Outer& o) {
            std::cout << o.secret << std::endl;
         }
      };
   private:
      int secret = 1;
   };
   
   // the nested class can be used as a type in global scope
   // --> More permissive than we intended
   Outer::Inner *ptr;
   
   int main() {
      Outer::Inner inner;
      Outer outer;
      inner.showSecret(outer);
      return 0;
   }
   ```
10. Member functions and static data members of a nested class do not need to be public to be defined outside the class definition. Even private members of the `Inner` class can be defined in the global scope.
      ```c++
      class Outer {
      private:
         class Inner {
         private:
            Inner(int val);
            int inner_secret;
            static int s_inner;
         };
         int secret;
      };
      
      
      // Definition of constructor
      Outer::Inner::Inner( int val ){
         inner_secret = val;
      }
      
      // Definition of static member
      int Outer::Inner::s_inner = 2;
      
      int main() {
         Outer outer;
         return 0;
      }
      ```
10. A nested class can also be defined outside its enclosing class. A nested class does not have to be a public member of its enclosing class to be defined in global scope.
    ```c++
    class Outer {
    private:
       class Inner; // Cannot be omitted
       int member1;
    };
    
    class Outer::Inner {
       public:
          int member2;
    };
    
    int main() {
       return 0;
    }
    ```
    :::info
    Why would one want to define a nested class outside its class definition? Maybe the nested class supports implementation details for the enclosing class and we don't want the users of the enclosing class to peek at the details of the nested class. For this reason, we don't want to put the definition of the nested class in the header file containing the interface of the enclosing class. 
    :::
11. Until the definition for the nested class has been seen, only pointers and references to the nested class can be declared. If one of these members had been an object instead of a pointer, the member declaration in an enclosing class would cause a compiler error.
    ```c++
    class Outer {
    private:
       class Inner;
       // Inner inner; // Error
       Inner *ptr;     // Okay
    };
    
    class Outer::Inner {
       public:
          int member2;
    };
    
    int main() {
       return 0;
    }
    ```
12. A nested class can be first declared and then later defined in the body of the enclosing class. This allows for nested classes that have members that refer to one another.
    ```c++
    class Outer {
    private:
       class Inner;
       class Ref {
          Inner *ptr;
       };
       class Inner {
          Ref *ptr;
       };
    };
    
    
    int main() {
       return 0;
    }
    ```
13. A nested class may not access the nonstatic members of its enclosing class directly, even though these members are public. Any access to a nonstatic member of the enclosing class requires that it be done through a pointer, reference, or object of the enclosing class.
    ```c++
    #include <iostream>
    
    class Outer {
    public:
       class Inner {
       public:
          void showSecret() {
             std::cout << secret << std::endl;
          }
       };
    private:
       static int secret;
    };
    
    int Outer::secret = 1;
    
    int main() {
       Outer::Inner inner;
       inner.showSecret();
       return 0;
    }
    ```
    
* Although an object of the enclosing class, pointer, or reference to the enclosing class is needed to access the enclosing class nonstatic data members, the nested class may access (1) the static members, (2) type names, (3) and enumerators of the enclosing class directly **(given that these members are public)**. A type name is either a typedef name, the name of an enumeration, or the name of a class.
   ```c++
   #include <iostream>
   
   class Outer {
      public:
      Outer(int outer) : _outer(outer) {}
      using MyInt = int;
      class Inner {
         public:
         Inner(MyInt inner) : _inner(inner) {}
         void showOuter( Outer& outerObj ) {
            std::cout << "outer = " << outerObj._outer << "\n";
         }
         void showStaticOuter( ){
            std::cout << "static outer =" << _s_outer << "\n";
         }
         int _inner;
      };
      int _outer;
      static int _s_outer;
   };
   
   int Outer::_s_outer = -1;
   
   int main() {
      Outer outerObj(1);
      Outer::Inner innerObj(2);
   
      innerObj.showOuter( outerObj );
      innerObj.showStaticOuter();
   }
   ```
    
 # Name Resolution in Nested Class Scope
  
 See [Unqualified Name Lookup](/cmvzTXvfTJOizt_Y9XQgUw). 