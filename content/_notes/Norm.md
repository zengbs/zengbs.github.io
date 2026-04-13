---


---



# Norm

# Matrix norm
Given a matrix $A\in\mathbb{R}^{m\times n}$


## Frobenius norm

$\displaystyle||A||_{F}=\sqrt{\sum_{i,j}^{m,n}|a_{ij}|^2}=\sqrt{\text{tr}(A^{*}A)}=\sqrt{\sum_{i=1}^{\min\{m,n\}}\sigma_{i}^{2}}$,
where $A^{*}$ is conjugate transpose of $A$, $\sigma_{i}$ are the singular values of $A$.

# $L_{p}$-norm
* If $p=+\infty$, $\displaystyle||\pmb{x}||_{\infty}=\max_{i}|x_{i}|$.
* If $p>0$, $\displaystyle||\pmb{x}||_{p}=\left(\sum_{i}|x_{i}|^{p}\right)^{1/p}$.
* If $p=0$, $||x||_{0}$ counts the number of non-zero components of $x$.