---
title: LU decomposition


---






# Principal Leading Submatrix
For $k \le n$, the $k\times k$ principal leading submatrix of $A_{n\times n}$ is defined to be the square matrixsuch that $A_{TL} \in \mathbb{C}^{k\times k}$ such that $\begin{bmatrix}A_{TL}&A_{TR}\\A_{BL}&A_{BR}\end{bmatrix}$.
 

# Existness and Uniqueness
* Let $A\in\mathbb{C}^{m\times n}$ and $m \ge n$ have linearly independent columns. Then $A$ has a unique $LU$ factorization if and only if all its principal leading submatrices are nonsingular. (with implicit ones on $L$'s diagonal)
* If one of principal leading submatrice is singular, then the fatorization exist, but if so it is not unique.

# Crout's Algorithm with Partial Pivoting
## Error Analysis
## Time Complexity
