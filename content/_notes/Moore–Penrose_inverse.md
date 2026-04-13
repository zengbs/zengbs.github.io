---


---


# Moore–Penrose Inverse

# Definition
* $AA^{+}$ acts like weak identity:
    * $(AA^{+})A=A$
* $A^{+}$ acts like weak inverse:
    * $A^{+}AA^{+}=A^{+}$
* $AA^{+}$ is Hermitian:
    * $(AA^{+})^{*}=AA^{+}$
* $A^{+}A$ is Hermitian:
    * $(A^{+}A)^{*}=A^{+}A$
# Properties
* For any matrix $A$ there is one and only one pseudoinverse $A^{+}$.
* $(A^{+})^{+}=A$.
* $(A^{T})^{+}=(A^{+})^{T}$, $\left(\overline{A}\right)^{+}=\overline{\left(A^{+}\right)}$, $(A^{*})^{+}=(A^{+})^{*}$.
* $(\alpha A)^{+}=\alpha^{-1}A^{+}$.

# Constructions
1. [Rank decomposition](/5sKfwHskQI2DmFsByE1y0Q)

If $A=BC$, then $A^{+}=C^{+}B^{+}=C^{*}(CC^{*})^{-1}(B^{*}B)^{-1}B^{*}$.

3. [QR decomposition](/BP8u2tvsRqCwfBr0lMTmcQ)
4. [Singular-value decomposition](/sZjk4W-VQCiBPRv0axX8tg)

If $A=U\Sigma V^{*}$ then $A^{+}=V\Sigma^{+} U^{*}$. The pseudoinverse of $\Sigma$ can be obtained by taking the reciprocal of each non-zero element on the diagonal, leaving the zeros in place, and then transposing the matrix.
See [proof](https://ccjou.wordpress.com/2009/06/10/%E9%80%9A%E9%81%8E%E6%8E%A8%E5%B0%8E%E5%81%BD%E9%80%86%E7%9F%A9%E9%99%A3%E8%AA%8D%E8%AD%98%E7%B7%9A%E6%80%A7%E4%BB%A3%E6%95%B8%E7%9A%84%E6%B7%B1%E5%B1%A4%E7%B5%90%E6%A7%8B/).
# Applications
1. [Ordinary Least Square](/RV-xGxoNR5a55aYWzvAotA)
![image](https://hackmd.io/_uploads/BJRXgpwiT.png)
3. Minimum-norm solution to a linear system
![image](https://hackmd.io/_uploads/HkjflTPop.png)


# Reference
* [Topics in Abstract Algebra/Linear algebra](https://en.wikibooks.org/wiki/Topics_in_Abstract_Algebra/Linear_algebra#The_Moore-Penrose_inverse)
* [Moore-Penrose 偽逆矩陣](https://ccjou.wordpress.com/2013/07/03/moore-penrose-%e5%81%bd%e9%80%86%e7%9f%a9%e9%99%a3/)
* [偽逆矩陣與轉置矩陣的二三事](https://ccjou.wordpress.com/2012/07/06/%E5%81%BD%E9%80%86%E7%9F%A9%E9%99%A3%E8%88%87%E8%BD%89%E7%BD%AE%E7%9F%A9%E9%99%A3%E7%9A%84%E4%BA%8C%E4%B8%89%E4%BA%8B/)
* [通過推導偽逆矩陣認識線性代數的深層結構](https://ccjou.wordpress.com/2009/06/10/%E9%80%9A%E9%81%8E%E6%8E%A8%E5%B0%8E%E5%81%BD%E9%80%86%E7%9F%A9%E9%99%A3%E8%AA%8D%E8%AD%98%E7%B7%9A%E6%80%A7%E4%BB%A3%E6%95%B8%E7%9A%84%E6%B7%B1%E5%B1%A4%E7%B5%90%E6%A7%8B/)
* [Generalized inverse](https://en.wikipedia.org/wiki/Generalized_inverse)