---
title: Diagonalizable matrix


---

###### tags: `linear-algebra`


# Diagonalizable matrix
## Definition
A **square** matrix $A$ is diagonalizable if there exists an invertible matrix $P$, and a diagonal matrix $D$ such that $AP=PD$, or $A=PDP^{-1}$.

## Theorem
A square matrix is diagonalizable if and only if one of them is true:
   1. Geometric multiplicity is equal to algebraic multiplicity for each $\lambda_{i}$.
   2. The sum of algebraic multiplicities is equal to the sum of geometric multiplicities.
       * Since geometric multiplicity is always less than or equal to algebraic multiplicity.
   4. The sum of geometric multiplicities is equal to the size of $A$.
       * Since the size of square matrix is always equal to the sum of algebraic multiplicities. This is the result of the fundamental theorem of algebra. 

## Geometric multiplicity
Geometric multiplicity is defined as the dimension of the space spanned by the eigenvectors associated with a $\lambda_{i}$. I.e. $\dim(\text{span}\{u:(A-\lambda_{i} I)u=0\})$

## Algebraic multiplicity
Algebraic multiplicity is defined by $\displaystyle \mu(\lambda_{i})$, where $\mu(\lambda_{i})$ is the repitition of $\lambda_{i}$.I.e. $(\lambda-\lambda_{i})^{\mu(\lambda_{i})}=0$