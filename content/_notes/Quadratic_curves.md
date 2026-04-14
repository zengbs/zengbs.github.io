---


---

$f(x,y)=Ax^2+Bxy+Cy^2+Dx+Ey+F=0$

Subsituting $x=X+x_{0}$ and $y=Y+y_{0}$ into $f(x,y)$ gives

$\begin{align}
&AX^2+BXY+CY^2\\
&+(2Ax_{0}+By_{0}+D)X\\
&+(Bx_{0}+2y_{0}C+E)Y\\
&+\underbrace{(Ax_{0}^2+Bx_{0}y_{0}+Cy_{0}^2+Dx_{0}+Ey_{0}+F)}_{F'}=0
\end{align}$

If there is a shift $(x_{0}, y_{0})$ causing linear terms vanish, $B^2-4AC\neq 0$. 

The original equation becomes
$AX^2+BXY+CY^2+F'=0$

If $F'= 0$, we obtaian two intersected straint lines.

If $F'\neq 0$, $A'X^2+B'XY+C'Y^2=1$, where $A'=-A/F'$, $B'=-B/F'$, $C'=-C/F'$.

$\begin{align}
&\begin{bmatrix}
X & Y \\
\end{bmatrix}
\begin{bmatrix}
A' & B'/2 \\
B'/2 & C' 
\end{bmatrix}
\begin{bmatrix}
X \\
Y 
\end{bmatrix}=1\\
&\Longrightarrow \mathbf{x}^{T}A\mathbf{x}=1
\end{align}$




|       Column 1        |       Column 2       |           |
|:---------------------:|:--------------------:|:---------:|
|   Positive-definite   | $A>0$ and $AC-B^2>0$ |  Ellipse  |
|   Negative-definite   | $A<0$ and $AC-B^2>0$ |  Ellipse  |
|      Indefinite       |      $AC-B^2<0$      | Hyperbola |
| Positive-semidefinite | $A>0$ and $AC-B^2=0$ | parabola  |
| Negative-semidefinite | $A>0$ and $AC-B^2=0$ | parabola  |
