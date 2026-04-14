---
date: 2026-04-13T15:32:37+08:00
draft: false
render_with_liquid: false
---

{% raw %}
---

---

1. Should we make namespace operator friends of a class?
   * Best practice:
   Try not to give outside (namespace) operators direct access (friendship) to your class if you can avoid it.
   * Why?
   If you let them use public access functions (like getters, etc.), then later if you change the private structure of your class, you only need to update your class's access functions, not all the external operators.
   ➔ This keeps things easier to maintain.
   * When to use friend?
   If your class does not provide enough public access functions, and the outside operator must look at private data to work, then you have no choice — you must declare the operator as a friend.
2. The use of friend declarations is most common to allow nonmember overloaded operators to access the private members of a class of which it is a friend.
3. The friendship in C++ is granted per function signature, not per function name. So we must explicitly declare each one in the set of overloaded functions as friends if necessary.
   ```c++
   class Screen
   {
      friend ostream& storeOn( ostream &, Screen & );
      friend BitMap& storeOn( BitMap &, Screen & );
      // ...
   };
   ```
4. If a function manipulates objects of two distinct class types, and the function needs to access the nonpublic members of both classes, the function may either be declared as a friend to both classes or made a member function of one class and a friend to the other.
5. If we decide that a function must be made a friend to both classes, the friend declarations are as follows:
   ```c++
   #include <iostream>
   
   class Window;
   class Screen;
   
   class Window {
      friend bool operator==(Window&, Screen&);
   public:
      Window() = default;
      Window(int _blx, int _bly, int _trx, int _try) : m_blx(_blx), m_bly(_bly), m_trx(_trx), m_try(_try) {};
   
   private:
      int m_blx;
      int m_bly;
      int m_trx;
      int m_try;
   };
   
   class Screen {
      friend bool operator==(Window&, Screen&);
   public:
      Screen() = default;
      Screen(int _blx, int _bly, int _trx, int _try) : m_blx(_blx), m_bly(_bly), m_trx(_trx), m_try(_try) {};
   
   private:
      int m_blx;
      int m_bly;
      int m_trx;
      int m_try;
   };
   
   bool operator==(Window& w, Screen& s){
      if      (w.m_blx != s.m_blx) return false;
      else if (w.m_bly != s.m_bly) return false;
      else if (w.m_trx != s.m_trx) return false;
      else if (w.m_try != s.m_try) return false;
      else return true;
   }
   
   int main() {
      Window w{1,2,3,4};
      Screen s{1,2,-2,4};
      if ( w == s ){
         std::cout << "w == s\n";
      }else{
         std::cout << "w != s\n";
      }
      return 0;
   }
   ```
6. If an operator function is a friend of a class, it must be defined in the same namespace as the class it is a friend of in order to participate in Argument-Dependent Lookup (ADL).
   ```c++
   #include <iostream>
   
   namespace NS{
   
      class Window;
      class Screen;
   
      class Window {
         friend bool operator==(Window&, Screen&);
      public:
         Window() = default;
         Window(int _blx, int _bly, int _trx, int _try) : m_blx(_blx), m_bly(_bly), m_trx(_trx), m_try(_try) {};
   
      private:
         int m_blx;
         int m_bly;
         int m_trx;
         int m_try;
      };
   
      class Screen {
         friend bool operator==(Window&, Screen&);
      public:
         Screen() = default;
         Screen(int _blx, int _bly, int _trx, int _try) : m_blx(_blx), m_bly(_bly), m_trx(_trx), m_try(_try) {};
   
      private:
         int m_blx;
         int m_bly;
         int m_trx;
         int m_try;
      };
   
   }
   
   // Error: m_blx, m_bly, m_trx, m_try are private within this context!
   bool operator==(NS::Window& w, NS::Screen& s){
      if      (w.m_blx != s.m_blx) return false;
      else if (w.m_bly != s.m_bly) return false;
      else if (w.m_trx != s.m_trx) return false;
      else if (w.m_try != s.m_try) return false;
      else return true;
   }
   
   int main() {
      NS::Window w{1,2,3,4};
      NS::Screen s{1,2,-2,4};
      if ( w == s ){
         std::cout << "w == s\n";
      }else{
         std::cout << "w != s\n";
      }
      return 0;
   }
   ```
8. If we decide that the function must be made a member function of one class and a friend to another class, the member function declaration and the friend declaration are as follows:
   ```c++
   #include <iostream>
   
   class Screen;
   
   class Window {
   public:
      Window() = default;
      Window(int _blx, int _bly, int _trx, int _try) : m_blx(_blx), m_bly(_bly), m_trx(_trx), m_try(_try) {};
      bool operator==(Screen&);
   
   private:
      int m_blx;
      int m_bly;
      int m_trx;
      int m_try;
   };
   
   class Screen {
      // A member function of a class cannot be declared as a friend
      // of another class until its class definition has been seen. 
      friend bool Window::operator==(Screen&);
   public:
      Screen() = default;
      Screen(int _blx, int _bly, int _trx, int _try) : m_blx(_blx), m_bly(_bly), m_trx(_trx), m_try(_try) {};
   
   private:
      int m_blx;
      int m_bly;
      int m_trx;
      int m_try;
   };
   
   bool Window::operator==(Screen& s){
      if      (m_blx != s.m_blx) return false;
      else if (m_bly != s.m_bly) return false;
      else if (m_trx != s.m_trx) return false;
      else if (m_try != s.m_try) return false;
      else return true;
   }
   
   int main() {
      Window w{1,2,3,4};
      Screen s{1,2,3,4};
      if ( w == s )  std::cout << "w == s\n";
      else           std::cout << "w != s\n";
      return 0;
   }
   ```
{% endraw %}