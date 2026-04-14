---


---



# Register

1. how to reduce the number of registers?
2. Why GPU has limited register? but CPU has not?
From ISO C11:6.7.1.6:
    > A declaration of an identifier for an object with storage-class specifier register suggests that access to the object be as fast as possible. The extent to which such suggestions are effective is implementation-defined.
4. What happened when the usage of register exceed the limit? spilling? or fail to launch kernel?

Each thread has its own instruction address counter and ==register state==, and carries out the current instruction on its own data.

Shared memory is partitioned among thread blocks resident on the SM and registers are partitioned among threads.