# Matrix Multiplication

Topic: linear_algebra
Key Pattern: C = A * B
Formula:
If A is an m × n matrix and B is an n × p matrix, C is an m × p matrix.
c_{ij} = (Row i of A) • (Column j of B) = Σ (a_{ik} * b_{kj}) for k=1 to n.

When to use:
When finding the product of two matrices. Note that AB is generally not equal to BA, and the inner dimensions must match (n = n).

Example:
Multiplying a 2x3 matrix by a 3x2 matrix yields a 2x2 matrix.


# Determinant of a 2x2 Matrix

Topic: linear_algebra
Key Pattern: |A| or det(A) for A = [[a, b], [c, d]]
Formula:
|A| = ad - bc

When to use:
To find the determinant of a 2x2 matrix, which determines if the matrix is invertible (non-zero determinant) or singular (zero determinant), and represents the area scaling factor of the linear transformation.

Example:
Find the determinant of [[3, 4], [1, 2]].


# Inverse of a 2x2 Matrix

Topic: linear_algebra
Key Pattern: A⁻¹
Formula:
A⁻¹ = (1 / |A|) * [ [d, -b], [-c, a] ]
where |A| = ad - bc.

When to use:
When solving matrix equations of the form Ax = b (where x = A⁻¹b) or finding the reverse linear transformation. The matrix must be non-singular (|A| ≠ 0).

Example:
Finding the inverse of A = [[4, 7], [2, 6]].


# Matrix Transpose Properties

Topic: linear_algebra
Key Pattern: A^T or A'
Formula:
1. (A^T)^T = A
2. (A + B)^T = A^T + B^T
3. (kA)^T = k(A^T)
4. Reversal Rule: (AB)^T = B^T A^T

When to use:
When manipulating algebraic expressions involving transposed matrices, especially when proving whether a matrix is symmetric (A^T = A) or skew-symmetric (A^T = -A).

Example:
Simplifying the expression (ABC)^T to C^T B^T A^T.


# Trace of a Matrix

Topic: linear_algebra
Key Pattern: Tr(A)
Formula:
Tr(A) = a_{11} + a_{22} + ... + a_{nn} (Sum of principal diagonal elements)
Property: Tr(A) = Sum of all eigenvalues of A.
Property: Tr(AB) = Tr(BA)

When to use:
When a problem asks for the sum of the eigenvalues, or when evaluating the diagonal sum of a square matrix without needing the full matrix.

Example:
Find the trace of a 3x3 matrix whose diagonal elements are 2, -1, and 5.


# Cramer's Rule

Topic: linear_algebra
Key Pattern: Ax = B (System of linear equations)
Formula:
x_i = |A_i| / |A|
where |A| is the determinant of the coefficient matrix, and |A_i| is the determinant of the matrix formed by replacing the i-th column of A with the constant vector B.

When to use:
When solving small systems of linear equations (2x2 or 3x3) where the coefficient matrix is non-singular (|A| ≠ 0).

Example:
Solving 2x + 3y = 8 and 3x - y = 1 for x and y.


# Characteristic Equation (Eigenvalues of 2x2)

Topic: linear_algebra
Key Pattern: |A - λI| = 0
Formula:
For a 2x2 matrix A, the characteristic polynomial simplifies to:
λ² - Tr(A)λ + |A| = 0
where λ represents the eigenvalues.

When to use:
When finding the eigenvalues of a 2x2 matrix quickly without explicitly setting up and expanding the |A - λI| determinant.

Example:
Finding the eigenvalues for A = [[3, 1], [2, 4]].


# Rank of a Matrix
Topic: linear_algebra, 
Key Pattern: rank(A)
Formula:
The rank of a matrix is the number of non-zero rows in its Row-Echelon Form (REF).
Property: rank(A) ≤ min(m, n).

When to use:
To check if a system of linear equations has a unique solution, infinite solutions, or no solution (Rouché–Capelli theorem).

Example:
Rank of [[1, 2], [2, 4]].


# Consistency of Linear Equations (Rouché–Capelli)
Topic: linear_algebra, 
Key Pattern: Ax = B
Formula:
1. rank(A) ≠ rank(A|B) → No solution (Inconsistent).
2. rank(A) = rank(A|B) = number of variables → Unique solution.
3. rank(A) = rank(A|B) < number of variables → Infinite solutions.

When to use:
When solving systems where the determinant might be zero.

Example:
Determine if x + y = 2 and 2x + 2y = 4 is consistent.


# Cayley-Hamilton Theorem
Topic: linear_algebra, 
Key Pattern: A satisfies its characteristic equation
Formula:
If P(λ) = det(A - λI) = 0 is the characteristic equation, then P(A) = 0.

When to use:
To find the inverse of a matrix or express higher powers of A (like A⁴) in terms of A and I.

Example:
Find A⁻¹ given A² - 5A + 6I = 0.


# Adjoint of a Matrix
Topic: linear_algebra
Key Pattern: adj(A)
Formula:
adj(A) = [C_{ij}]^T where C_{ij} are the cofactors of A.
Property: A * adj(A) = |A| * I.

When to use:
When finding the inverse of matrices larger than 2x2.

Example:
Finding the inverse of a 3x3 matrix.


# Eigenvalues and Trace/Determinant Relationship
Topic: linear_algebra, 
Key Pattern: λ₁, λ₂, λ₃
Formula:
1. Σ λ_i = Tr(A)
2. Π λ_i = |A|
3. Eigenvalues of A^k are λ_i^k
4. Eigenvalues of A⁻¹ are 1/λ_i

When to use:
To quickly find properties of eigenvalues without solving the characteristic polynomial.

Example:
If A has eigenvalues 1, 2, 3, find |A|.


# Idempotent and Involutory Matrices
Topic: linear_algebra, 
Key Pattern: A² = A or A² = I
Formula:
- Idempotent: A² = A (Eigenvalues are 0 or 1)
- Involutory: A² = I (Eigenvalues are ±1)
- Nilpotent: A^k = 0 (Eigenvalues are 0)

When to use:
When a problem specifies these properties to simplify massive matrix powers.

Example:
If A is idempotent, what is A^100? (Ans: A)


# Leibniz Rule for Integral Differentiation
Topic: calculus, 
Key Pattern: d/dx ∫[g(x) to h(x)] f(x, t) dt
Formula:
d/dx ∫[g(x) to h(x)] f(x, t) dt = f(x, h(x)) * h'(x) - f(x, g(x)) * g'(x) + ∫[g(x) to h(x)] ∂f/∂x dt

When to use:
When you have an integral where the variable x appears in the bounds OR inside the function.

Example:
Find f'(x) if f(x) = ∫[0 to x] sin(x+t) dt.


# Properties of Definite Integrals (King's Property)
Topic: calculus, integration
Key Pattern: ∫[a to b] f(x) dx
Formula:
∫[a to b] f(x) dx = ∫[a to b] f(a + b - x) dx

When to use:
The most important tool for evaluating difficult definite integrals in JEE. Use it when you see x in the numerator of a fraction.

Example:
∫[0 to π/2] [sin x / (sin x + cos x)] dx = π/4


# Linear Transformation

Topic: linear_algebra
Key Pattern: T(x) = Ax (matrix-vector product as a map)
Formula:
T: Rⁿ → Rᵐ defined by T(x) = Ax, where A is an m × n transformation matrix.
Properties: T(u + v) = T(u) + T(v) and T(cu) = cT(u).

When to use:
When representing geometric operations (rotation, scaling, reflection, projection) as matrix multiplications, or when checking if a map between vector spaces is linear.

Example:
The matrix A = [[0, −1], [1, 0]] represents a 90° counterclockwise rotation in R².


# Eigenvectors

Topic: linear_algebra
Key Pattern: Av = λv (vector direction preserved under transformation)
Formula:
A v = λ v, where λ = eigenvalue and v = eigenvector (v ≠ 0).
To find eigenvectors: solve (A − λI)v = 0 after finding eigenvalues λ.

When to use:
After finding eigenvalues, to determine the directions that are scaled (but not rotated) by the transformation. Essential for diagonalization.

Example:
For A = [[3, 1], [2, 4]] with λ = 5, solve (A − 5I)v = 0 → v = [1, 2]^T.


# Orthogonal Matrix

Topic: linear_algebra
Key Pattern: AᵀA = I
Formula:
A matrix A is orthogonal if AᵀA = AAᵀ = I.
Properties: A⁻¹ = Aᵀ, and |A| = ±1.
Columns (and rows) form an orthonormal set.

When to use:
When working with rotation/reflection matrices, or checking if a change-of-basis matrix preserves distances and angles (isometry).

Example:
A = [[cos θ, −sin θ], [sin θ, cos θ]] is orthogonal: AᵀA = I and |A| = 1.


# Diagonalization

Topic: linear_algebra
Key Pattern: A = PDP⁻¹
Formula:
A = PDP⁻¹, where D is the diagonal matrix of eigenvalues and P is the matrix of corresponding eigenvectors as columns.
A^n = PD^nP⁻¹ (efficient computation of matrix powers).

When to use:
When computing high powers of a matrix, or solving systems of differential equations. A matrix is diagonalizable if it has n linearly independent eigenvectors.

Example:
If A has eigenvalues 2, 3 with eigenvectors v₁, v₂, then A^10 = P * diag(2^10, 3^10) * P⁻¹.