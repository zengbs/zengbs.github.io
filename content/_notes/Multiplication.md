---
title: Multiplication
tags: [linear-algebra]

---

$\displaystyle c_{ij}=\sum_{k=1}^{m}a_{ik}b_{kj}$.
$C_{N\times M}=A_{N\times K}B_{K\times M}$.


# ijk
```c=
for (int i=0;i<N;i++){
    for (int j=0;j<N;j++){
        r = 0;
        for (int k=0;k<N;k++){
            r += a[i][k]*b[k][j];
        }
        c[i][j] = r;
    }
}
```
![image](https://hackmd.io/_uploads/SkP_cO16a.png =25%x)

# jik
```c=
for (int j=0;j<N;j++){
    for (int i=0;i<N;j++){
        c[i][j] = 0;
        for (int k=0;k<N;k++){
            c[i][j] += a[i][k]*b[k][j];
        }
    }
```
![image](https://hackmd.io/_uploads/rJUModk6a.png =25%x)


# kij
```c=
for (int k=0;k<N;k++){
    for (int i=0;i<N;i++){
        r = a[i][k];
        for (int j=0;j<N;j++){
            c[i][j] += r*b[k][j];
        }
    }
```
![image](https://hackmd.io/_uploads/BkO7sOkTa.png =25%x)


# ikj
```c=
for (int i=0;i<N;i++){
    for (int k=0;k<N;k++){
        r = a[i][k];
        for (int j=0;j<N;j++){
            c[i][j] += r*b[k][j];
        }
    }
```
![image](https://hackmd.io/_uploads/rJKVoOkTT.png =25%x)


# jki
```c=
for (int j=0;j<N;j++){
    for (int k=0;k<N;k++){
        r = b[k][j];
        for (int i=0;i<N;i++){
            c[i][j] += a[i][k]*r;
        }
    }
```
![image](https://hackmd.io/_uploads/HyqrsOkpa.png =25%x)


# kji
```c=
for (int k=0;k<N;k++){
    for (int j=0;j<N;j++){
        b[k][j] = 0;
        for (int i=0;i<N;i++){
            c[i][j] += a[i][k]*r;
        }
    }
```
![image](https://hackmd.io/_uploads/SJ9IodJa6.png =25%x)



# Block ijk
```c=
// Assuming the matrix and blocks are square
void MatrixBlockMultiplication( int *M1, int M1R, int M1C, int *M2, int M2R, int M2C, int *M3, int BSize )
{
   for (int bi=0;bi<M2C/BSize;bi++){
      for (int bj=0;bj<M1R/BSize;bj++){
         for (int bk=0;bk<M1C/BSize;bk++){
            for (int i=bi*BSize;i<(bi+1)*BSize;i++){
               for (int j=bj*BSize;j<(bj+1)*BSize;j++){
                  for (int k=bk*BSize;k<(bk+1)*BSize;k++){

                     M3[M2C*i+j] += M1[M1C*i+k] * M2[M2C*k+j];

                  }
               }
            }
         }
      }
   }
}
```

## Cache Miss Analysis
Assuming cache line size is 8 elements.
The number of cache miss in a single block is $B^2/8$.
For each block in $C$, we have to calculate $2M/B$ blocks.
So there are $(B^2/8)(2M/B)(M/B)^2=M^3/(4B)^2$ cache miss.


# Reference
* https://cs.brown.edu/courses/cs033/lecture/18cacheX.pdf
* http://www.cse.iitm.ac.in/~rupesh/teaching/hpc/jun16/examples-cache-mm.pdf
* https://jukkasuomela.fi/cache-blocking-demo/