---
title: Check integer overflow


---

###### tags: `C`

# Check integer overflow

https://stackoverflow.com/questions/199333/how-do-i-detect-unsigned-integer-multiply-overflow

```c=
bool checkInt32Overflow(int32_t a, int32_t b, int operation, int line)                                    
{
  bool overflow = false;
 
  if (operation == '+')
  {
     if ( ( b > 0 ) && ( a > INT32_MAX-b ) ) overflow = true;
     if ( ( b < 0 ) && ( a < INT32_MIN-b ) ) overflow = true;
 
  }
  else if (operation == '*')
  {
     if (  b != 0 && a > INT32_MAX / b  )    overflow = true;
     if (  b != 0 && a < INT32_MIN / b  )    overflow = true;
 
  }
  else
  {
     printf("something wrong!\n");
     exit(0);
  }
 
# ifdef DEBUG
  if (overflow) printf("a=%d, b=%d, line=%d\n", a, b, line);
# endif
 
  return overflow;
}
```


* [The other method](https://hackmd.io/nAX2S4xIRdOwJvCnBfSggQ?view#Checking-signed-integer-overflow-after-addition-safe).