---


---


# Ordinary Least Square

## Problem Statement
Given a matrix $A_{m\times n}:\mathbb{R}^{n}\longrightarrow\mathbb{R}^{m}$, how do we find $\pmb{x}$ such that $A\pmb{x}$ and $\pmb{b}$ are close each other enough? i.e., solve $\displaystyle \text{arg min}_{x}||A\pmb{x}-\pmb{b}||$.


## Case 1: $\text{rank}(A)=n$ and $\text{rank}(A)<m$ (i.e., $A$ is full column rank)

Since the vector $A\hat{\pmb{x}}$ always lies in the column space of $A$, the minimum of $||A\hat{\pmb{x}}-\pmb{b}||$ must occur when $A\hat{\pmb{x}}$, say $\pmb{p}$, is the projection of $\pmb{b}$ onto the column space of $A$, which means $\pmb{p}-\pmb{b}$ is perpenticular to each basis of the column space of $A$. In other words, $\pmb{p}-\pmb{b}\in N(A^{T})$.

$\begin{align}
&A^{T}(\pmb{p}-\pmb{b})=0\\
\Longrightarrow&A^{T}\pmb{b}=A^{T}\pmb{p}\\
\Longrightarrow&A^{T}\pmb{b}=A^{T}A\hat{\pmb{x}}\\
\Longrightarrow&\hat{\pmb{x}}=(A^{T}A)^{-1}A^{T} \pmb{b}
\end{align}$

Note that the last line has assumed $\text{rank}(A)=n$, resulting $\text{rank}(A^{T}A)=n$, and thus $A^{T}A$ is invertible.

![image](https://hackmd.io/_uploads/BJyweJFsa.png =50%x)


## Case 2: $\text{rank}(A)<n$ and $\text{rank}(A)<m$ (i.e., $A$ is not full column rank)

All solutions to $A\pmb{x}=\pmb{b}$ are given by:
$\pmb{\hat{x}}=A^{+}\pmb{b}+(I_{n}-A^{+}A)\pmb{\omega}$, for arbitrary $\pmb{\omega}$.
The particular solution $\hat{\pmb{x}}=A^{+}\pmb{b}$ provides the following two propositions:
1. $||A\pmb{x}-\pmb{b}||_{2}\ge||A\hat{\pmb{x}}-\pmb{b}||_{2}$
2. $\hat{\pmb{x}}=A^{+}\pmb{b}$ is the smallest Euclidean norm in the all solutions.


![image](https://hackmd.io/_uploads/HJCVhJKja.png =50%x)

When $A$ has full column rank, $A^{+}=(A^{T}A)^{-1}A^{T}$, resulting in $\hat{\pmb{x}}=(A^{T}A)^{-1}A^{T} \pmb{b}$.

## Reference
* [利用偽逆矩陣解線性方程](https://ccjou.wordpress.com/2009/09/17/%E5%88%A9%E7%94%A8%E5%81%BD%E9%80%86%E7%9F%A9%E9%99%A3%E8%A7%A3%E7%B7%9A%E6%80%A7%E6%96%B9%E7%A8%8B%E5%BC%8F/)
* [Difference between least squares and minimum norm solution](https://math.stackexchange.com/questions/2253443/difference-between-least-squares-and-minimum-norm-solution)
* [從線性變換解釋最小平方近似](https://ccjou.wordpress.com/2009/10/28/%e5%be%9e%e7%b7%9a%e6%80%a7%e8%ae%8a%e6%8f%9b%e8%a7%a3%e9%87%8b%e6%9c%80%e5%b0%8f%e5%b9%b3%e6%96%b9%e8%bf%91%e4%bc%bc/)
* [通過推導偽逆矩陣認識線性代數的深層結構](https://ccjou.wordpress.com/2009/06/10/%E9%80%9A%E9%81%8E%E6%8E%A8%E5%B0%8E%E5%81%BD%E9%80%86%E7%9F%A9%E9%99%A3%E8%AA%8D%E8%AD%98%E7%B7%9A%E6%80%A7%E4%BB%A3%E6%95%B8%E7%9A%84%E6%B7%B1%E5%B1%A4%E7%B5%90%E6%A7%8B/)