---
title: "Operator ++ and --"
date: 2026-04-13T15:32:37+08:00
draft: false
---

---
title: Operator ++ and --
tags: [CPP]

---

1. To distinguish the declaration of the postfix operators from the declaration of the prefix operators, the declarations for the overloaded increment and decrement postfix operators have an extra parameter of type `int`.
   ```c++
   class ScreenPtr {
   public:
      // prefix operators
      Screen& operator++();
      Screen& operator--();
      // postfix operators
      Screen& operator++(int);
      Screen& operator--(int);
   };
   ```
   
```c++
#include <iostream>
#include <string>


class Screen {
public:
   Screen(int x, int y) : m_x(x), m_y(y){};
private:
   int m_x;
   int m_y;
};

class ScreenPtr{
public:
   ScreenPtr( Screen& s, size_t arraySize = 0)
           : m_ptr(&s), m_size(arraySize), m_offset(0){};

   // prefix operators
   Screen& operator++();
   Screen& operator--();
   // postfix operators
   Screen& operator++(int);
   Screen& operator--(int);
private:
   Screen* m_ptr;
   size_t m_size;
   size_t m_offset;
};

Screen& ScreenPtr::operator++()
{
   if ( m_size == 0 ){
      std::cout << "Cannot increment pointer to single object" << std::endl;
      return *m_ptr;
   }

   if ( m_size == m_offset ){
      std::cout << "Already one past the end of the array" << std::endl;
      return *m_ptr;
   }
   ++m_offset;
   return *++m_ptr;
}

Screen& ScreenPtr::operator++(int)
{
   if ( m_size == 0 ){
      std::cout << "Cannot increment pointer to single object" << std::endl;
      return *m_ptr;
   }

   if ( m_size == m_offset ){
      std::cout << "Already one past the end of the array" << std::endl;
      return *m_ptr;
   }
   ++m_offset;
   return *m_ptr++;
}

int main(){
   Screen s(5, 6);
   ScreenPtr sptr(s);
   return 0;
}
```