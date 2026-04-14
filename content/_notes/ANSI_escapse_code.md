---


---


# ANSI escapse code
```c=
#include <stdio.h>                                             
                                                               
int main(void)                                                 
{                                                              
  int i, j, n;                                                 
                                                               
 printf("=================== Syntax ====================\n\n");
 printf("\033[93m^[\033[m\033[96m[CODE\033[mword\033[93m^[\033[m\033[96m[0m\033[m");
 printf(", type ctrl+v and ctrl+[ to get \033[93m^[\033[m  \n\n");                                                                       
                                                               
 printf("============== ANSI escape table ==============\n\n");
  for (i = 0; i < 11; i++) {                                   
    for (j = 0; j < 10; j++) {                                 
      n = 10*i + j;                                            
      if (n > 108) break;                                      
      printf("\033[%dm %3d\033[m", n, n);                      
    }                                                          
    printf("\n");                                              
  }                                                            
  return 0;                                                    
}
```
Output:
![](https://i.imgur.com/msfxhyh.png)


## Bash
