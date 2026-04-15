---


---

# Fundamental Theorems of Linear Algebra
Given an $m\times n$ matrix $A_{m\times n}:\mathbb{R}^{n}\longrightarrow\mathbb{R}^{m}$, we have the following two theorems:

## Part 1
* $n=\dim(\mathbb{R}^{n})=\dim N(A)+\dim C(A^{T}).$
* $m=\dim(\mathbb{R}^{m})=\dim N(A^{T})+\dim C(A).$

proof.


:::success
We can take the following extreme example to memorize that theorem:
$\begin{bmatrix}
0 & 0 & 0\\
0 & 0 & 0\\
\end{bmatrix}_{m\times n}
\begin{bmatrix}
x\\
y\\
z\\
\end{bmatrix}_{n\times1}=0$
In this case, $\text{rank}(A)=0$ and $\dim N(A)=n$, so the theorem is $n=\dim N(A)+\text{rank}(A)$.
:::

## Part 2
* The nullspace and the row space are orthogonal in $\mathbb{R}^{n}$.
i.e, $N(A)=C(A^{T})^{\perp}$.
* The left nullspace and the column space are orthogonal in $\mathbb{R}^{m}$.
i.e, $N(A^{T})=C(A)^{\perp}$.

proof.

<img src="https://hackmd.io/_uploads/B1hxmO3ja.png" width="60%">


# Reference
* [線性代數基本定理 (一)](https://ccjou.wordpress.com/2009/03/23/%E7%B7%9A%E6%80%A7%E4%BB%A3%E6%95%B8%E5%9F%BA%E6%9C%AC%E5%AE%9A%E7%90%86-%E4%B8%80/)
* [線性代數基本定理 (二)](https://ccjou.wordpress.com/2009/05/06/%E7%B7%9A%E6%80%A7%E4%BB%A3%E6%95%B8%E5%9F%BA%E6%9C%AC%E5%AE%9A%E7%90%86-%E4%BA%8C/)