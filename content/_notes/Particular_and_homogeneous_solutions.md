---


---

Particular solution, lying in the row space, is the solution to $Ax_{r}=b$.
Homogeneous solution, lying in the nullspace, is the solution to $Ax_{n}=0$.
The general solution turns out to be $x=x_{r}+\omega x_{n}$, where $\omega$ is a constant.
# Properties
* Every vector in the column space comes from one and only one vector in the row space.
    * Proof: Given $x_{r}$ and $x_{r}'$ in the row space, if $Ax_{r}=Ax_{r}'$, $x_{r}-x_{r}'$ must also be in the nullspace. Therefore $x_{r}-x_{r}'$ is zero vector, and thus $x_{r}=x_{r}'$.
* $x_{r}$ and $x_{n}$ are always perpendicular to each other since the row space and nullspace are orthogonal.

<img src="https://hackmd.io/_uploads/r19a8_hja.png" width="60%">
