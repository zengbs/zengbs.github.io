---
title: Projection


---

# Problem Statement

Given $n$ independent vectors $\pmb{a}_{1},\dots,\pmb{a}_{n}$ in $\mathbb{R}^{m}$. Find a vector in $\text{span}\{\pmb{a}_{1},\dots,\pmb{a}_{n}\}$, the vector is closest to a given vector $\pmb{b}$.

# Projection Matrix

Let $\pmb{p}=A\hat{x}=\mathbb{P}\pmb{b}$, where $\pmb{p}$ is the projection, $A$ is the matrix $[\pmb{a}_1, \dots, \pmb{a}_n]$, $\mathbb{P}$ is the projection matrix.

Since $\pmb{b}-\pmb{p}=\pmb{b}-A\pmb{\hat{x}}$ is perpendicular to each vector in the subspace $\text{span}\{\pmb{a}_{1},\dots,\pmb{a}_{n}\}$, we have

$0=\begin{bmatrix}
-\pmb{a}_1^{T}-\\
\vdots\\
-\pmb{a}_n^{T}-\\
\end{bmatrix}
\begin{bmatrix}
\pmb{b}-A\hat{\pmb{x}}
\end{bmatrix}=A^{T}(\pmb{b}-A\hat{\pmb{x}})$
$\Longrightarrow A^{T}A\hat{x}=A^{T}b$
$\Longrightarrow \hat{x}=(A^{T}A)^{-1}A^{T}b$
$\Longrightarrow A\hat{x}=A(A^{T}A)^{-1}A^{T}b$
$\Longrightarrow \mathbb{P}=A(A^{T}A)^{-1}A^{T}$

* In the first arrow, $A$ is not full column rank; thus we cannot multiply $(A^{T})^{-1}$ on both side to obtain $A\hat{x}$.
* In the second arrow, we have employed the property: if $A$ is full column rank, then $A^{T}A$ is invertible.
* $\hat{x}$ always lies in the row space since $\dim N(A)=0$.
* $\hat{x}=\arg\min||b-Ax||^{2}$
![BJyweJFsa-1](https://hackmd.io/_uploads/BkC36ohjp.png =50%x)
