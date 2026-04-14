---


---

# Theorem
1. For every $n\times n$ matrix $A$, there exists an invertible matrix $M$ such that $A=MJM^{-1}$, where

$\begin{align}
J=\begin{bmatrix}
J_1 &  &  \\
    & \ddots &  \\
    &  & J_p 
\end{bmatrix}
\end{align}$ and $\begin{align}
J_i=\begin{bmatrix}
\lambda_{i}  &   1         &        &         \\
             & \lambda_{i} & \ddots &         \\
             &             & \ddots & 1       \\
             &             &        & \lambda_{i}
\end{bmatrix}
\end{align}$.

2. Every $n\times n$ matrix $A$ has $n$ linearly independent generalized eigenvectors associated with it and can be shown to be similar to an "almost diagonal" matrix $J$ in Jordan normal form.
3. If $\lambda$ is an eigenvalue of algebraic multiplicity $\mu$, then $A$ will have $\mu$ linearly independent generalized eigenvectors corresponding to $\lambda$.
# Example

$\begin{align}
A=\begin{bmatrix}
0 & 0 & 0 & 0 & -1 & -1 \\
0 & -8 & 4 & -3 & 1 & -3 \\
-3 & 13 & -8 & 6 & 2 & 9 \\
-2 & 14 & -7 & 4 & 2 & 10 \\
1 & -18 & 11 & -11 & 2 & -6 \\
-1 & 19 & -11 & 10 & -2 & 7
\end{bmatrix}
\end{align}$

The characteristic polynomial of this matrix is $(t+1)^5(t-2)$.

$\begin{align}
A+I=\begin{bmatrix}
 1 & 0 & 0 & 0 & -1 & -1 \\
0 & -7 & 4 & -3 & 1 & -3 \\
-3 & 13 & -7 & 6 & 2 & 9 \\
-2 & 14 & -7 & 5 & 2 & 10 \\
1 & -18 & 11 & -11 & 3 & -6 \\
-1 & 19 & -11 & 10 & -2 & 8
\end{bmatrix}
\end{align}$
$\Longrightarrow\text{rank}(A+I)=2=r_{1}$.

$\begin{align}
(A+I)^2=\begin{bmatrix}
1 & -1 & 0 & 1 & -2 & -3 \\
-2 & -16 & 9 & -11 & 4 & -3 \\
-1 & 37 & -18 & 17 & 2 & 21 \\
1 & 35 & -18 & 19 & -2 & 15 \\
-1 & -53 & 27 & -28 & 2 & -24 \\
2 & 52 & -27 & 29 & -4 & 21
\end{bmatrix}
\end{align}$
$\Longrightarrow\text{rank}(A+I)^2=4=r_{2}$.
$\Longrightarrow\text{rank}(A+I)^3=5=r_{3}$.
$\Longrightarrow (A+I)^3\bf{v}=0$ has 5 linearly independent solutions ${v_{1}\cdots}v_{5}$.
$\Longrightarrow$ there are five generalized eigenvectors ${v_{1}\cdots}v_{5}$ with rank 3 associated with $\lambda=-1$.
$\Longrightarrow$ The number 3 is the size of the largest Jordan block associated to $\lambda=-1$.

![](https://hackmd.io/_uploads/HJrf1ON1T.png)

$N$ is the smallest integer such that $\text{rank}(A-\lambda I)^{N}=$ algebraic multiplicity of $\lambda$.

$\begin{align}
r_{1}&=\dim(V)-\text{rank}(A-\lambda I)\\
r_{2}&=\dim(V)-\text{rank}(A-\lambda I)^2\\
&\vdots\\
r_{N}&=\dim(V)-\text{rank}(A-\lambda I)^N
\end{align}$

$r_{k}$ is the number of linearly independent solutions of $(A-\lambda I)^{k}$.

---
$\begin{align}
s_{1}&=r_{1}\\
s_{2}&=r_{2}-r_{1}\\
&\vdots\\
s_{N}&=r_{N}-r_{N-1}
\end{align}$

$s_{k}$ is the number of Jordan blocks of size at least $k\times k$ associated with $\lambda$. 

---
$\begin{align}
m_{1}&=s_{1}-s_{2}\\
m_{2}&=s_{2}-s_{3}\\
m_{3}&=s_{3}-s_{4}\\
\vdots\\
m_{N-1}&=s_{N-1}-s_{N}\\
m_{N}&=s_{N}
\end{align}$

$m_{k}$ is the number of Jordan block of size $k\times k$ associated with $\lambda$.

## Jordan form
$\begin{align}
J=\begin{bmatrix}
\color{\red}{-1} & \color{\red}1  & 0 & 0 & 0 & 0 \\
\color{\red}0  & \color{\red}{-1} & 0 & 0 & 0 & 0 \\
0  & 0  & \color{\purple}{-1} & \color{\purple}{1} & \color{\purple}{0} & 0 \\
0  & 0  &  \color{\purple}{0} & \color{\purple}{-1} & \color{\purple}{1} & 0 \\
0  & 0  & \color{\purple}{0} & \color{\purple}{0} & \color{\purple}{-1} & 0 \\
0  & 0  & 0 & 0 & 0 & \color{\green}{2}
\end{bmatrix}
\end{align}$

## Super Jordan blocks
$\begin{align}
J(\lambda_{1})=
\begin{bmatrix}
\color{\red}{-1} & \color{\red}1  & 0 & 0 & 0  \\
\color{\red}0  & \color{\red}{-1} & 0 & 0 & 0  \\
0  & 0  & \color{\purple}{-1} & \color{\purple}{1} & \color{\purple}{0}  \\
0  & 0  &  \color{\purple}{0} & \color{\purple}{-1} & \color{\purple}{1}  \\
0  & 0  & \color{\purple}{0} & \color{\purple}{0} & \color{\purple}{-1}
\end{bmatrix}
\end{align}$, $\begin{align}
J(\lambda_{2})=
\begin{bmatrix}
\color{\green}{2} 
\end{bmatrix}
\end{align}$

## Jordan blocks
$\begin{align}
J_{1}(\lambda_{1})=
\begin{bmatrix}
\color{\red}{-1} & \color{\red}{1}  \\
\color{\red}0  & \color{\red}{-1}\\
\end{bmatrix}
\end{align}$, $\begin{align} J_{2}(\lambda_{1})=
\begin{bmatrix}
 \color{\purple}{-1} & \color{\purple}{1} & \color{\purple}{0}  \\
  \color{\purple}{0} & \color{\purple}{-1} & \color{\purple}{1}  \\
 \color{\purple}{0} & \color{\purple}{0} & \color{\purple}{-1}
\end{bmatrix}
\end{align}$, $\begin{align}
J_{1}(\lambda_{2})=
\begin{bmatrix}
\color{\green}{2} 
\end{bmatrix}
\end{align}$

Lemma 1:
$\begin{align}
\text{rank}(A-\lambda_{i} I)^{p}=\text{rank}(J-\lambda_{i} I)^{p}
\end{align}$ for each $\lambda_{i}$.

Lemma 2:
$\begin{align}
\text{rank}(J-\lambda_{i} I)^{p}=n-\left[\beta_{i}-\text{rank}(J(\lambda_{i})-\lambda_{i} I_{\beta_{i}})^{p}\right]
\end{align}$ for each $\lambda_{i}$.


$\begin{align}
&\text{rank}(A-\lambda_{i} I)^{p-1}-\text{rank}(A-\lambda_{i} I)^{p}\\
=&\text{rank}(J(\lambda_{i})-\lambda_{i} I_{\beta_{i}})^{p-1}-\text{rank}(J(\lambda_{i})-\lambda_{i} I_{\beta_{i}})^{p}
\end{align}$


# Reference
https://empslocal.ex.ac.uk/people/staff/rjchapma/courses/jcf.pdf
https://ccjou.wordpress.com/2009/07/15/jordan-%e5%85%b8%e5%9e%8b%e5%bd%a2%e5%bc%8f-%e4%b8%8a/
https://ccjou.wordpress.com/2009/07/17/jordan-%e5%85%b8%e5%9e%8b%e5%bd%a2%e5%bc%8f-%e4%b8%8b/
https://ccjou.wordpress.com/2010/11/10/jordan-%E5%BD%A2%E5%BC%8F%E5%A4%A7%E8%A7%A3%E8%AE%80-%E4%B8%8A/
https://ccjou.wordpress.com/2010/11/17/jordan-%E5%BD%A2%E5%BC%8F%E5%A4%A7%E8%A7%A3%E8%AE%80-%E4%B8%8B/
https://en.wikipedia.org/wiki/Generalized_eigenvector