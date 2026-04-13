---
title: Similar matrix
tags: [linear-algebra]

---

# Definition
If $B=M^{-1}AM$ for an invertble matrix $M$ then $B$ is similar to $A$.




|            Not changed             |     Changed     |
|:----------------------------------:|:---------------:|
|            Eigenvalues$^1$             |  Eigenvectors$^2$   |
|               Trace$^3$                |    Nullspace$^4$   |
|                Rank$^5$                |  Column space$^6$   |
| Number of independent eigenvectors$^{7}$ |    Row space$^8$    |
|            Determinant$^9$             | Left nullspace$^{10}$  |
|            Jordan form$^{11}$             | Singular values$^{12}$ |


**Proof 1 and 2**
$\begin{align}
&A(P^{-1}\mathbf{v})\\
=&(P^{-1}BP)(P^{-1}\mathbf{v})\\
=&P^{-1}B\mathbf{v}\\
=&\lambda (P^{-1}\mathbf{v})
\end{align}$
As a result, $A=P^{-1}BP$ and $B$ have different eigenvectors $P^{-1}\mathbf{v}$ and $\mathbf{v}$, respectively, but associated with the same eigenvalue $\lambda$.

**Proof 3**
$\begin{align}
Tr(A)=Tr(P^{-1}BP)=Tr(P^{-1})Tr(B)Tr(P)=Tr(B)Tr(P^{-1}P)=Tr(B)
\end{align}$

**Proof 5**
Lemma1: If $X$ is invertible, then $\text{null}(XY)=\text{null}(Y)$ 
*Proof:*
$\begin{align}
&\mathbf{v}\in \text{null}(XY)\\
\Longrightarrow&(XY)\mathbf{v}=0\\
\Longrightarrow&Y\mathbf{v}=X^{-1}0=0\\
\Longrightarrow&\mathbf{v}\in\text{null}(Y)
\end{align}$
Proving the opposite way is trivial.

Lemma2: If $X$ and $Y$ have the same dimension and $\text{null}(X) = \text{null}(Y)$, then $\text{rank}(X)=\text{rank}(Y)$ provided by Rank–Nullity theorem.

Lemma3: $\text{rank}(AB)=\text{rank}(B)$ if $A$ is invertible.
*Proof:* 
Using Lemma 1 and 2.

Lemma4: $\text{rank}(AB)=\text{rank}(A)$ if $B$ is invertible.
*Proof:*
$\begin{align}
&rank(AB)=rank((AB)^{T})=rank(B^{T}A^{T})=rank(A^{T})=rank(A)
\end{align}$