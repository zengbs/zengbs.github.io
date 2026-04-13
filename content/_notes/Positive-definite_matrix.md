---
title: Positive-definite matrix


---

If a symmetic maxtrix $A$ is positive-definite then the following statements are equivalent:
 1. $\mathbf{v}^TA\mathbf{v}>0$ for all nonzero vector $\mathbf{v}$.
 2. All eigenvalues of $A$ are positive.
 3. All pivots are positive.
 4. All upper left determinants are positive.


**Proof: 1 $\Longrightarrow$ 2:**

$\begin{align}
&A\mathbf{v}=\lambda\mathbf{v}\\
\Longrightarrow&\mathbf{v}^TA\mathbf{v}=\lambda||\mathbf{v}||^2\\
\Longrightarrow&\lambda||\mathbf{v}||^2>0\\
\Longrightarrow&\lambda>0
\end{align}$


**Proof: 2 $\Longrightarrow$ 1:**
Since $A$ is symmetric and all eigenvalues are real, by the Spectral theorem, there is an orthogonal matrix $Q$ such that $A=Q^{T}\Lambda Q$.
$\begin{align}
&\mathbf{v}^TA\mathbf{v}=\mathbf{v}^T(Q^{T}\Lambda Q)\mathbf{v}\\
=&(Q\mathbf{v})^{T}\Lambda(Q\mathbf{v})\\
=&y^{T}\Lambda y\\
=&\sum_{i=0}^{N}\lambda_{i}(y_{i})^2>0
\end{align}$
, where $y=Q\mathbf{v}$

**Proof: 2 $\Longleftrightarrow$ 3**:
$\begin{align}
&U=EA\\
\Longrightarrow&UE^{T}=EAE^{T}\\
\Longrightarrow&D=EAE^{T}
\end{align}$
, where $U$ is upper triangular matrix, $E$ elimination matrix, $D$ diagonal matrix with pivots. Alternatively, we can use Cholesky decomposition to obtain $D=L^{-1}A(L^{T})^{-1}=L^{-1}A(L^{-1})^{T}$, where $L$ is invertible since $L$ is always a lower triangular matrix with unit diagonal entries.

On the other hand, we decompose $A$ with the Spectral theorem:
$\begin{align}
&A=Q\Lambda Q^{T}\\
\Longrightarrow&\Lambda=Q^{-1}A(Q^{T})^{-1}\\
\Longrightarrow&\Lambda=(Q^{-1})A(Q^{-1})^{T}\\
\end{align}$

By [Sylvester's law of inertia](https://en.wikipedia.org/wiki/Sylvester%27s_law_of_inertia), $\Lambda$ and $D$ has the same positive and negative elements as $Q^{-1}$ and $E$(or $L^{-1}$) are invertible.