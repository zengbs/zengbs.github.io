---
title: Eigenvalues and eigenvectors
tags: [linear-algebra]

---

###### tags: `linear-algebra`

# Eigenvalues and eigenvectors



## The equation of eigenvalues
If $(A-\lambda I)x=0$ has a nonzero solution, $A-\lambda I$ is singular.
i.e., det$(A-\lambda I)=0$


## Eigendecomposition
$AS=S\Lambda$, $A=S\Lambda S^{-1}$, or $\Lambda=S^{-1}\Lambda S$.

Proof:
$AS=A\begin{bmatrix}
|   &       & |\\ 
\pmb{x_1} & \dots & \pmb{x_n}\\ 
| &         & |
\end{bmatrix}=
\begin{bmatrix}
|   &       & |\\ 
\lambda_{1}\pmb{x_1} & \dots & \lambda_{n}\pmb{x_n}\\ 
| &         & |
\end{bmatrix}\\
=\begin{bmatrix}
|   &       & |\\ 
\pmb{x_1} & \dots & \pmb{x_n}\\ 
| &         & |
\end{bmatrix}\begin{bmatrix}
\lambda_{1} &        & 0          \\
            & \ddots &            \\
          0 &        & \lambda_{n}\\
\end{bmatrix}=S\Lambda$

## Properties
* $\lambda_{1}\lambda_{2}\dots\lambda_{n}=\text{det}(A)$.
* $\lambda_{1}+\lambda_{2}+\dots+\lambda_{n}=\text{trace}(A)$.
* $A$ is invertible $\Longleftrightarrow$ none of its eigenvalue is zero.
If one of eigenvalue is zero, the linear transformation crushs 2D space to 1D space, leading to the loss of information. Thus, the transformation is not invertible.
![](https://i.imgur.com/vx3P3P9.gif =70%x)
* $A$ is diagonalizable $\Longleftrightarrow$ $\dim(\text{span}(\text{Eigenvectors}))=n$
* $A$ is diagonalizable $\Longleftrightarrow$ the two eigenvectors can be rotated to be aligned with vertical/horizontal axes. (that's why original eigenvectors should be independent)
$A=\begin{bmatrix}
  6 &  -1\\ 
  2 &  3
\end{bmatrix}=\begin{bmatrix}
  1 &  1\\ 
  1 &  2
\end{bmatrix}\begin{bmatrix}
  5 &  0\\ 
  0 &  4
\end{bmatrix}\begin{bmatrix}
  2 &  -1\\ 
  -1 &  1
\end{bmatrix}$
![](https://hackmd.io/_uploads/rJfUQ1116.gif =70%x)
* $A$ is diagonalizable $\Longrightarrow$ $A$ is invertible.
***False***! For example, $A=\begin{bmatrix}
  1 &  0\\ 
  0 &  0
\end{bmatrix}$ is diagonalizable (the eigenvector $\begin{bmatrix}1\\0\end{bmatrix}$ and arbitrary eigenvector which is not parallel to the other, both of them span the eigenspace of dimension 2) but it is not invertible (one of eigenvalue is zero).
![](https://i.imgur.com/YQYabW7.gif =70%x)
* $A$ is invertible $\Longrightarrow$ $A$ is diagonalizable.
***False***! For example, $A=\begin{bmatrix}
  1 &  1\\ 
  0 &  1
\end{bmatrix}$ is invertible but has only one eigenvector $\begin{bmatrix}
  1\\ 
  0
\end{bmatrix}$.
![](https://i.imgur.com/8KlQrQF.gif =70%x)
* $A$ is diagonalizable and none of its eigenvalue is zero $\Longrightarrow$ $A$ is invertible.
* $A$ is invertible and "$\dim(\text{Eigenspace})=n$" $\Longrightarrow$ $A$ is diagonalizable.
* Eigenvalues are distinct $\Longrightarrow$ eigenvectors are independent.
    * If a circle maps to an ecllipse, eigenvectors associated with distinct eigenvalues are not parallel.
    * If a circle maps to a line, one eigenvector parallel to the line, and the other is chosen not to parallel to the line.
* Eigenvalues are distinct $\Longrightarrow$ the matrix is diagonalizable\.
* For any positive integer $k$, the eigenvalues of $A^{k}$ are $\lambda_{i}^{k}$.
* The eigenvalues of $A^{-1}$ are $1/\lambda_{i}$.
* $A$ and $B$ are diagonalizable and $AB=BA$ $\Longleftrightarrow$ they share the same eigenvector matrix.
* The number of non-trivial eigenvectors of a matrix is equal to the number of non-zero eigenvalues of that matrix.
## Applications
* Finding closed-form expression from recurrence relation
* Solving ODE


# Reference
* [Eigshow](https://www.geogebra.org/m/JP2XZpzV)
* [Eigenvectors of repeated eigenvalues](https://www.youtube.com/watch?v=rNosSJudzco)