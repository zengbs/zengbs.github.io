---
title: Singular-value decomposition


---

###### tags: `linear-algebra`


# Singular-value decomposition

For all real matrix $A_{m\times n}$ with a rank $r\leq\min\{m,n\}$, the matrix $A^{T}A$ is symmetric. As a result, all eigenvalues of $A^{T}A$ are non-negative, and all eigenvector of $A^{T}A$ are perpendicular to one another.

On the basis of the above statement, we write $A^{T}A\pmb{v}_{i}=\sigma_{i}^{2}\pmb{v}_{i}$ (Equation 1), where $\pmb{v}_{i}$ is a unit eigenvector of $A^{T}A$.

Multiplying $A$ on both sides of Eq. (1) yields $AA^{T}(A\pmb{v}_{i})=\sigma_{i}^{2}(A\pmb{v}_{i})$, indicating $AA^{T}$ has an eigenvector $A\pmb{v}_{i}$ with eigenvalue $\sigma_{i}^{2}$.

On the other hand, multiplying $\pmb{v}_{i}^{T}$ on both sides of Eq. (1) shows that the length of $A\pmb{v}_{i}$ is $\sigma_{i}$ ($||A\pmb{v}_{i}||^2=\pmb{v}_{i}^{T}A^{T}A\pmb{v}_{i}=\sigma_{i}^{2}\pmb{v}_{i}^{T}\pmb{v}_{i}=\sigma_{i}^{2}$), and we hope $\pmb{u}_{i}$ is also a unit vector. So we define $\pmb{u}_{i}=\frac{1}{\sigma_{i}}A\pmb{v}_{i}$, and thus $AA^{T}\pmb{u}_{i}=\sigma_{i}^2\pmb{u}_{i}$.

A similar method can be employed to derive $\pmb{v}_{i}=\frac{1}{\sigma_{i}}A^{T}\pmb{u}_{i}$.

Up to this point, we have the following equations:
* $A^{T}A\pmb{v}_{i}=\sigma_{i}^{2}\pmb{v}_{i}$, $i=1\dots n$
* $AA^{T}\pmb{u}_{i}=\sigma_{i}^2\pmb{u}_{i}$, $i=1\dots m$
* $\displaystyle\pmb{v}_{i}=\frac{1}{\sigma_{i}}A^{T}\pmb{u}_{i}$, $i=1\dots r$
* $\displaystyle\pmb{u}_{i}=\frac{1}{\sigma_{i}}A\pmb{v}_{i}$, $i=1\dots r$

With $\pmb{v}_{i}$ and $\pmb{u}_{i}$ as columns of $V$ and $U$, you see what we are asking for:

$A[\pmb{v}_{1},\cdots,\pmb{v}_{r},\pmb{v}_{r+1},\cdots,\pmb{v}_{n}]_{n\times n}=[\pmb{u}_{1},\cdots,\pmb{u}_{r},\pmb{u}_{r+1},\cdots,\pmb{u}_{m}]_{m\times m}\begin{bmatrix}
\sigma_{1} &        & 0         & 0       & \cdots & 0     \\
           & \ddots &           & \vdots  & \ddots & \vdots\\
         0 &        & \sigma_{r}& 0       & \cdots & 0     \\
         0 & \cdots &    0      & 0       & \cdots & 0     \\
    \vdots & \ddots & \vdots    & \vdots  & \ddots & \vdots\\
         0 & \cdots &    0      & 0       & \cdots & 0     \\
\end{bmatrix}_{m\times n}$,
where $\pmb{v}_{1},\cdots,\pmb{v}_{r}$ are unit eigenvector of $A^{T}A$, and $\pmb{u}_{1},\cdots,\pmb{u}_{r}$ are unit eigenvector of $AA^{T}$.

For value of $i$ that greater than $r$, $\pmb{v_{i}}$ and $\pmb{u_{i}}$ may be choosen arbitrary, but we hope both $V$ and $U$ are orthonormal matrice. Thus, we set $\pmb{v_{i}}$ and $\pmb{u_{i}}$ as the orthonormal basis of the null space of $A$ and $A^{T}$, respectively (see [Gram–Schmidt process](/ZRdTho_eSFuonEn1XrEQBA)).

In the matrix notation that is

$\begin{align}&AV=U\Sigma\\
&\Longrightarrow A_{m\times n}=U_{m\times m}\Sigma_{m\times n} V^{T}_{n\times n}\end{align}$

# Existness
# Uniqueness

# Properties
* $V^{T}V=I$
* $U^{T}U=I$
* $U^{T}=U^{-1}$
* $V^{T}=V^{-1}$
* $A^{T}A=V\Sigma$
* $A=U\Sigma V^{T}=\sum_{i=1}^{r}\sigma_{i}\pmb{u}_{i}\pmb{v}_{i}^{T}$, where $r\leq\min\{m,n\}$
* The number of non-zero singular values is equal to the rank of matrix.
* $U$ and $V$ contain orthonormal bases for all four subspaces:
    * First $r$ columns of $V$ $\Longrightarrow$ row space of $A$.
    * Last $n-r$ columns of $V$ $\Longrightarrow$ nullspace of $A$.
    * First $r$ columns of $U$ $\Longrightarrow$ column space of $A$.
    * Last $m-r$ columns of $U$ $\Longrightarrow$ nullspace of $A^{T}$.

# Applications

* Given a matrix $B_{m\times n}$, find $E$ such that $||B-E||_{F}^{2}$ is minimum subject to $rank(E)=k-1$, where $k=\min\{m,n\}$.
Since [Frobenius norm](https://hackmd.io/gbeF96jBRg21mYtdHeXCJA#Frobenius-norm) equals the square root of the sum of the squared sigular values, we can reduce the number of singular vales of $B$ as more as we can to minimize $||B-E||_{F}$ as follows:
    a. Decompose $B$ with SVD, i.e. $B=\sum_{i}^{k}\sigma_{i}\pmb{u}_{i}\pmb{v}_{i}^{T}$.
    b. Let $E$ be $\sigma_{1}\pmb{u}_{1}\pmb{v}_{1}^{T}$.
    c. $||B-E||_{F}^{2}$ is minimized at $\sum_{k=2}^{r}\sigma_{k}^{2}$ when the largest sigular values of $B-E$ is set to zero, which is what we have done we create $E$.
* Given a matrix $B$, find a unit vector $\pmb{r}$ such that $(||B\pmb{r}||_{2})^{2}$ is minimized.
    a. Decompose $B$ with SVD, i.e. $B=\sum_{i}^{k}\sigma_{i}\pmb{u}_{i}\pmb{v}_{i}^{T}$.
    b. $||B\pmb{r}||_{2}^{2}=||\sum_{i}(\pmb{u}_{i}\sigma_{i}\pmb{v}_{i}^{T}\pmb{r})||_{2}^{2}$.
    c. Let $a_{i}=\sigma_{i}\pmb{v}_{i}^{T}\pmb{r}$, $||B\pmb{r}||_{2}^{2}=||\sum_{i}(a_{i}\pmb{u}_{i})||_{2}^{2}=\sum_{j}(\sum_{i}(a_{i}u_{i}^{j}))^{2}$.
    d. We can easily see that when $\pmb{r}=\pmb{v}_{r}$, the right singular vector of $B$ corresponding to the smallest singular value of $B$, $||B\pmb{r}||_{2}^{2}$ is minimized at $\sum_{j}(\sigma_{r}u_{r}^{j})^{2}=\sigma_{r}^{2}||\pmb{u}_{r}||_{2}^{2}$ ($a_{r}=\sigma_{r}$ and $a_{i\neq r}=0$).
* [Total least squares](/4VkAIZXGRiiQTucWyDJ8tg)
* [Low-rank approximation (Eckart–Young theorem)](/Z0t3H8mJQd6nLqv2Q-i8iA)
# Reference
* [Image Compression with Singular Value Decomposition](http://timbaumann.info/svd-image-compression-demo/)
* [THE SINGULAR VALUE DECOMPOSITION](https://peterbloem.nl/blog/pca-4)
* [線代啟示錄](https://ccjou.wordpress.com/tag/svd/page/2/)
* [線性代數基本定理 (三)](https://ccjou.wordpress.com/2009/05/15/%E7%B7%9A%E6%80%A7%E4%BB%A3%E6%95%B8%E5%9F%BA%E6%9C%AC%E5%AE%9A%E7%90%86-%E4%B8%89/)