---
title: Symmetric matrix


---

###### tags: `linear-algebra`

# Symmetric matrix
## Spectral theorem
* Every symmetric matrix can be decomposed into $\displaystyle A=Q\Lambda Q^{T}$ with real eigenvalues in $\Lambda$ and orthornomal eigenvectors in $Q$. i.e. $\displaystyle A=Q\Lambda Q^{T}=Q\Lambda Q^{-1}$. Moreover, we can also replace $Q^{-1}$ by $\tilde{Q}$. As a result, $A=\tilde{Q}^{-1}\Lambda\tilde{Q}=\tilde{Q}^{T}\Lambda\tilde{Q}$
Proof: [here](https://brilliant.org/wiki/spectral-theorem/#:~:text=change%20of%20basis.-,Proof%20of%20Spectral%20Theorem,M%20M%20M%20are%20real.&text=For%20n%20%3D%201%20%2C%20n%20%3D,v%2C%20where%20M%20%3D%20%CE%BB%20.)
## Theorem
* Every symmetric matrix is diagonalizable, since all eigenvectors stay perpendicular. 
* The eigenvalues of a real symmetric matrix are real.
Proof: 
$A\pmb{x}=\lambda\pmb{x}$
$\Longleftrightarrow A\bar{\pmb{x}}=\bar{\lambda}\bar{\pmb{x}}$ (complex conjugate)
$\Longleftrightarrow \bar{\pmb{x}}^{T}A=\bar{\pmb{x}}^{T}\bar{\lambda}$ (transpose)
Now, taking the dot product of $A\pmb{x}=\lambda\pmb{x}$ with $\bar{\pmb{x}}$ gives $\bar{\pmb{x}}^{T}A\pmb{x}=\bar{\pmb{x}}^{T}\lambda\pmb{x}$,
and taking the dot product of $\bar{\pmb{x}}^{T}A=\bar{\pmb{x}}^{T}\bar{\lambda}$ with $\pmb{x}$ gives $\bar{\pmb{x}}^{T}A\pmb{x}=\bar{\pmb{x}}^{T}\bar{\lambda}\pmb{x}$
Thus, $\bar{\pmb{x}}^{T}\lambda\pmb{x}=\bar{\pmb{x}}^{T}\bar{\lambda}\pmb{x}$, indicating $\bar{\lambda}=\lambda$.
* $A$ is real symmetric matrix $\Longrightarrow$ eigenvectors of $A$ are perpenticular each other.
Proof:
Suppose $A\pmb{x}=\lambda_{1}\pmb{x}$, and $A\pmb{y}=\lambda_{2}\pmb{y}$. Taking the dot product of the first eqation with $\pmb{y}$ yields
$(\lambda_{1}\pmb{x})^{T}\pmb{y}=(A\pmb{x})^{T}\pmb{y}=\pmb{x}^{T}A^{T}\pmb{y}=\pmb{x}^{T}A\pmb{y}=\pmb{x}^{T}\lambda_{2}\pmb{y}$
$\Longrightarrow \pmb{x}^{T}\lambda_{1}\pmb{y}=\pmb{x}^{T}\lambda_{2}\pmb{y}$
$\Longrightarrow\pmb{x}^{T}\pmb{y}=0$, since $\lambda_{1}\neq\lambda_{2}$.
![](https://i.imgur.com/d7o6hco.gif =60%x)
* If $A$ is symmetric, the number of positive/negative eigenvalues equals to the number of positive/negative pivots.
* Rank of a symmetric matrix $A$ is equal to the number of non-zero eigenvalues of $A$.

# Reference
* [Symmetric Matrix Properties and Applications: A Guide](https://builtin.com/data-science/symmetric-matrix)