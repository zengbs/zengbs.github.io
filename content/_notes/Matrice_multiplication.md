---
title: Matrice multiplication


---

###### tags: `linear-algebra`

# Matrice multiplication
* Column picture of multiplication:
$A\begin{bmatrix}
|   &       & |\\ 
\pmb{b_1} & \dots & \pmb{b_n}\\ 
| &         & |
\end{bmatrix}
=\begin{bmatrix}
|   &       & |\\ 
A\pmb{b_1} & \dots & A\pmb{b_n}\\ 
| &         & |
\end{bmatrix}$

* Row picture of multiplication:
$\begin{bmatrix}
 --  &   \pmb{a_{1}}    & --\\ 
 & \vdots & \\ 
-- &     \pmb{a_{n}}    & --
\end{bmatrix}B
=\begin{bmatrix}
--   &    \pmb{a_{1}}B   & --\\ 
 & \vdots & \\ 
-- &    \pmb{a_{n}}B     & --
\end{bmatrix}$

* Column-row picture of multiplication:
$\begin{bmatrix}
|   &       & |\\ 
\pmb{a_1} & \dots & \pmb{a_n}\\ 
| &         & |
\end{bmatrix}\begin{bmatrix}
--   &   \pmb{b_1}    & -- \\ 
 & \vdots & \\ 
--   &   \pmb{b_n}    & --
\end{bmatrix}
=\begin{bmatrix}
\pmb{a_1b_1}+\dots+\pmb{a_nb_n}
\end{bmatrix}$

* Block multiplication
$\begin{bmatrix}
A_{11} & A_{12}\\ 
A_{21} & A_{22}\\
\end{bmatrix}\begin{bmatrix}
B_{11} & B_{12}\\
B_{21} & B_{22}\\
\end{bmatrix}
=\begin{bmatrix}
A_{11}B_{11}+A_{12}B_{21} & \dots \\
A_{21}B_{11}+A_{22}B_{21} & \dots \\
\end{bmatrix}$

In $\text{dim}(A)=\text{dim}(B)=$ $n$ by $n$, time complexity of $AB$ is $O(n^3)$.
* Schoolbook algorithm
* Strassen's algorithm
# Matrix inversion
[The invertible matrix theorem](https://en.wikipedia.org/wiki/Invertible_matrix#The_invertible_matrix_theorem)

The inverse of $A_{n\times n}$ exist iff
* $A$ is full rank
## Gauss-Jordan elimination
## Cayley–Hamilton method
## Cholesky decomposition
## Newton's method
## Blockwise inversion
## Eigendecomposition
# Solving linear system
$A\pmb{x}=\pmb{b}$
## Find inverse of $A$
## Gauss-Jordan method
## Gaussian elimination
## Jacobi iteraton
## Gauss-Seidel iteration
## SOR iteration

# Matrix decomposition
## $LU$ decomposition
[Motivation](https://www.cl.cam.ac.uk/teaching/1314/NumMethods/supporting/mcmaster-kiruba-ludecomp.pdf)
## Eigendecomposition (spectral decomposition)
* Applicable to: square matrix A with linearly independent eigenvectors (not necessarily distinct eigenvalues).
* $A=VDV^{-1}$
Proof
$A\pmb{v_{i}}=\lambda\pmb{v_{i}}$
$\Longrightarrow A[\pmb{v_1}\dots\pmb{v_{n}}]=[\lambda_{1}\pmb{v_1}\dots\lambda_{n}\pmb{v_{n}}]$
$\Longrightarrow AV=[\pmb{v_1}\dots\pmb{v_n}]
\begin{bmatrix}
\lambda_{1} &        & 0          \\
            & \ddots &            \\
          0 &        & \lambda_{n}\\
\end{bmatrix}\\
\Longrightarrow AV=VD \text{ (a.k.a the eigenvalue equation)}\\
\Longrightarrow A=VDV^{-1} \text{ (}V\text{ is invertible iff. all eigen vectors are linearly independent)}$

## Jordan decomposition
## Singular value decomsition
## Pseudoinverse
## Linear least square problem