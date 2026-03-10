# Example 1

Problem:
Given Matrix A = [[1, 2], [3, 4]] and Matrix B = [[2, 0], [1, 2]], find the product AB.

Topics:
linear_algebra

Structure:
matrix_multiplication

Key Insight:
Multiply the rows of the first matrix (A) by the columns of the second matrix (B). The element c_{ij} is the dot product of the i-th row of A and the j-th col of B.

Solution:
Row 1 of A = [1, 2]
Row 2 of A = [3, 4]
Col 1 of B = [2, 1]^T
Col 2 of B = [0, 2]^T

c_11 = (1 * 2) + (2 * 1) = 2 + 2 = 4
c_12 = (1 * 0) + (2 * 2) = 0 + 4 = 4
c_21 = (3 * 2) + (4 * 1) = 6 + 4 = 10
c_22 = (3 * 0) + (4 * 2) = 0 + 8 = 8

AB = [[4, 4],[10, 8]]


# Example 2

Problem:
Find the inverse of the matrix A = [[4, 7], [2, 6]].

Topics:
linear_algebra

Structure:
matrix_inverse_2x2

Key Insight:
Use the standard 2x2 inverse formula: swap the diagonal elements, flip the signs of the off-diagonal elements, and divide the entire matrix by the determinant.

Solution:
1. Find determinant |A|:
   |A| = (4 * 6) - (7 * 2) = 24 - 14 = 10
2. Check if invertible:
   |A| ≠ 0, so A⁻¹ exists.
3. Find the adjugate matrix (swap a,d; negate b,c):
   adj(A) = [[6, -7], 
             [-2, 4]]
4. Multiply by 1/|A|:
   A⁻¹ = (1/10) * [[6, -7], 
                   [-2, 4]]
   A⁻¹ = [[0.6, -0.7], 
          [-0.2, 0.4]]


# Example 3

Problem:
Solve the system of equations using Cramer's Rule: 
2x + 3y = 8
3x - y = 1

Topics:
linear_algebra

Structure:
cramers_rule_system

Key Insight:
Set up the determinant of the coefficients (D), and then find Dx and Dy by replacing the respective columns with the constants. 

Solution:
1. Coefficient Matrix Determinant (D):
   D = | 2   3 |
       | 3  -1 |
   D = (2 * -1) - (3 * 3) = -2 - 9 = -11

2. Determinant for x (Dx): Replace col 1 with [8, 1]^T
   Dx = | 8   3 |
        | 1  -1 |
   Dx = (8 * -1) - (3 * 1) = -8 - 3 = -11

3. Determinant for y (Dy): Replace col 2 with [8, 1]^T
   Dy = | 2   8 |
        | 3   1 |
   Dy = (2 * 1) - (8 * 3) = 2 - 24 = -22

4. Solve for x and y:
   x = Dx / D = -11 / -11 = 1
   y = Dy / D = -22 / -11 = 2
Final Answer: x = 1, y = 2


# Example 4

Problem:
Find the eigenvalues of the matrix A = [[3, 1], [2, 4]].

Topics:
linear_algebra

Structure:
eigenvalues_2x2

Key Insight:
Instead of setting up |A - λI| = 0 manually, use the 2x2 characteristic equation shortcut: λ² - Tr(A)λ + |A| = 0.

Solution:
1. Find the Trace of A (sum of main diagonal):
   Tr(A) = 3 + 4 = 7
2. Find the Determinant of A:
   |A| = (3 * 4) - (1 * 2) = 12 - 2 = 10
3. Set up characteristic equation:
   λ² - 7λ + 10 = 0
4. Solve the quadratic equation for λ:
   (λ - 5)(λ - 2) = 0
   λ = 5 or λ = 2
Final Answer: The eigenvalues are 2 and 5.


# Example 5

Problem:
If A and B are symmetric matrices of the same order, prove that the matrix (AB - BA) is a skew-symmetric matrix.

Topics:
linear_algebra, 

Structure:
matrix_transpose_properties

Key Insight:
A matrix M is symmetric if M^T = M, and skew-symmetric if M^T = -M. Take the transpose of the entire expression (AB - BA) and use the reversal rule (XY)^T = Y^T X^T.

Solution:
Given: A^T = A and B^T = B (since they are symmetric).
Let M = AB - BA.
We need to evaluate M^T:
M^T = (AB - BA)^T
Using property (X + Y)^T = X^T + Y^T:
M^T = (AB)^T - (BA)^T
Using reversal property (XY)^T = Y^T X^T:
M^T = (B^T A^T) - (A^T B^T)
Substitute A^T = A and B^T = B:
M^T = (BA) - (AB)
Factor out a negative sign:
M^T = -(AB - BA)
M^T = -M
Since M^T = -M, the matrix (AB - BA) is purely skew-symmetric.


# Example 6

Problem:
Check the consistency of the system:
x + y + z = 6
x + 2y + 3z = 10
x + 2y + 3z = 12

Topics:
linear_algebra, 

Structure:
system_consistency_check

Key Insight:
Compare rank(A) and rank(Augmented Matrix A|B).

Solution:
A = [[1, 1, 1], [1, 2, 3], [1, 2, 3]]
Augmented A|B = [[1, 1, 1, 6], [1, 2, 3, 10], [1, 2, 3, 12]]
Perform Row Operations:
R2 → R2 - R1: [[1, 1, 1, 6], [0, 1, 2, 4], [1, 2, 3, 12]]
R3 → R3 - R1: [[1, 1, 1, 6], [0, 1, 2, 4], [0, 1, 2, 6]]
R3 → R3 - R2: [[1, 1, 1, 6], [0, 1, 2, 4], [0, 0, 0, 2]]
rank(A) = 2, rank(A|B) = 3.
Since 2 ≠ 3, the system is inconsistent (No solution).


# Example 7

Problem:
Given A = [[1, 2], [2, 1]], use Cayley-Hamilton to find A⁻¹.

Topics:
linear_algebra, 

Structure:
cayley_hamilton_inverse

Key Insight:
A satisfies its own characteristic equation: λ² - Tr(A)λ + |A| = 0.

Solution:
Tr(A) = 2, |A| = 1 - 4 = -3.
Char. Eq: λ² - 2λ - 3 = 0
By C-H Theorem: A² - 2A - 3I = 0
A² - 2A = 3I
Multiply by A⁻¹: A - 2I = 3A⁻¹
A⁻¹ = (1/3) * (A - 2I)
A⁻¹ = (1/3) * ([[1, 2], [2, 1]] - [[2, 0], [0, 2]])
A⁻¹ = (1/3) * [[-1, 2], [2, -1]]


# Example 8

Problem:
Find the adjoint of matrix A = [[1, 2, 3], [0, 1, 4], [5, 6, 0]].

Topics:
linear_algebra

Structure:
matrix_adjoint_3x3

Key Insight:
The adjoint is the transpose of the matrix of cofactors.

Solution:
Cofactor C_11 = +(0 - 24) = -24
Cofactor C_12 = -(0 - 20) = 20
Cofactor C_13 = +(0 - 5) = -5
...calculate all 9 cofactors...
Matrix of cofactors = [[-24, 20, -5],
                       [18, -15, 4],
                       [5, -4, 1]]
Transpose to get adj(A):
adj(A) = [[-24, 18, 5],
          [20, -15, -4],
          [-5, 4, 1]]



# Example 9

Problem:
If A is a 3x3 matrix with eigenvalues 1, -1, and 2, find the value of |A² + 2A|.

Topics:
linear_algebra, 

Structure:
eigenvalues_properties

Key Insight:
If λ is an eigenvalue of A, then f(λ) is an eigenvalue of f(A).

Solution:
Eigenvalues of A: {1, -1, 2}
Eigenvalues of A²: {1², (-1)², 2²} = {1, 1, 4}
Eigenvalues of 2A: {2(1), 2(-1), 2(2)} = {2, -2, 4}
Eigenvalues of (A² + 2A): {1+2, 1-2, 4+4} = {3, -1, 8}
The determinant of a matrix is the product of its eigenvalues:
|A² + 2A| = 3 * (-1) * 8 = -24


# Example 10

Problem:
Evaluate f'(x) if f(x) = ∫[x² to x³] (1/t) dt.

Topics:
calculus, linear_algebra

Structure:
leibniz_rule

Key Insight:
Apply Leibniz Integral Rule for variable bounds.

Solution:
Using formula: d/dx ∫[g(x) to h(x)] f(t) dt = f(h(x))h'(x) - f(g(x))g'(x)
f'(x) = [1 / (x³)] * (3x²) - [1 / (x²)] * (2x)
f'(x) = 3/x - 2/x
f'(x) = 1/x


# Example 11

Problem:
Evaluate I = ∫[0 to π] x sin²x dx.

Topics:
calculus, integration, linear_algebra

Structure:
definite_integral_kings_property

Key Insight:
Use King's Property: ∫[0 to a] f(x) dx = ∫[0 to a] f(a-x) dx to eliminate the 'x' term.

Solution:
I = ∫[0 to π] x sin²x dx  --- (1)
Apply King's Property (a=π):
I = ∫[0 to π] (π - x) sin²(π - x) dx
I = ∫[0 to π] (π - x) sin²x dx  --- (2)
Add (1) and (2):
2I = ∫[0 to π] (x + π - x) sin²x dx
2I = π ∫[0 to π] sin²x dx
Using formula sin²x = (1 - cos 2x)/2:
2I = π * [x/2 - sin(2x)/4] [0 to π]
2I = π * (π/2) = π²/2
I = π²/4

# Example 12

Problem:
Find the eigenvectors of the matrix A = [[3, 1], [2, 4]].

Topics:
linear_algebra

Structure:
eigenvectors_2x2

Key Insight:
First find the eigenvalues using the characteristic equation. Then for each eigenvalue λ, substitute into (A - λI)v = 0 and solve the resulting homogeneous system. The solution (up to a scalar multiple) is the eigenvector for that λ.

Solution:
Step 1 - Find eigenvalues (characteristic equation):
λ² - Tr(A)λ + |A| = 0
λ² - 7λ + 10 = 0  =>  (λ - 5)(λ - 2) = 0
Eigenvalues: λ₁ = 2, λ₂ = 5

Step 2 - Eigenvector for λ₁ = 2:
(A - 2I)v = 0
[[1, 1], [2, 2]] v = 0
Row 1 gives: v₁ + v₂ = 0  =>  v₁ = -v₂
Eigenvector: v₁ = [1, -1]^T  (or any scalar multiple)

Step 3 - Eigenvector for λ₂ = 5:
(A - 5I)v = 0
[[-2, 1], [2, -1]] v = 0
Row 1 gives: -2v₁ + v₂ = 0  =>  v₂ = 2v₁
Eigenvector: v₂ = [1, 2]^T  (or any scalar multiple)


# Example 13

Problem:
Diagonalize the matrix A = [[3, 1], [2, 4]] and use it to compute A⁴.

Topics:
linear_algebra

Structure:
diagonalization_matrix_power

Key Insight:
Form P from eigenvectors as columns and D from eigenvalues on the diagonal. Then A = PDP⁻¹, which gives A^n = PD^nP⁻¹. Computing D^n is trivial — just raise each diagonal entry to the power n.

Solution:
From Example 12: eigenvalues λ₁ = 2, λ₂ = 5 with eigenvectors [1, -1]^T and [1, 2]^T.

Form P and D:
P = [[1, 1], [-1, 2]]
D = [[2, 0], [0, 5]]

Find P⁻¹:
|P| = (1)(2) - (1)(-1) = 3
P⁻¹ = (1/3) * [[2, -1], [1, 1]]

Compute D⁴:
D⁴ = [[2⁴, 0], [0, 5⁴]] = [[16, 0], [0, 625]]

Compute A⁴ = P D⁴ P⁻¹:
P D⁴ = [[1, 1], [-1, 2]] * [[16, 0], [0, 625]]
= [[16, 625], [-16, 1250]]

A⁴ = [[16, 625], [-16, 1250]] * (1/3)[[2, -1], [1, 1]]
= (1/3) * [[32 + 625, -16 + 625], [-32 + 1250, 16 + 1250]]
= (1/3) * [[657, 609], [1218, 1266]]
= [[219, 203], [406, 422]]


# Example 14

Problem:
Show that the matrix A = (1/3) * [[1, 2, 2], [2, 1, -2], [-2, 2, -1]] is orthogonal.

Topics:
linear_algebra

Structure:
orthogonal_matrix_verification

Key Insight:
A matrix is orthogonal if and only if AᵀA = I. This is equivalent to verifying that every column (and row) is a unit vector AND all pairs of columns (and rows) are mutually orthogonal. Check both conditions.

Solution:
Let B = [[1, 2, 2], [2, 1, -2], [-2, 2, -1]], so A = B/3.

Check column dot products of B:
Col 1 · Col 1 = 1² + 2² + (-2)² = 1 + 4 + 4 = 9
Col 2 · Col 2 = 2² + 1² + 2² = 4 + 1 + 4 = 9
Col 3 · Col 3 = 2² + (-2)² + (-1)² = 4 + 4 + 1 = 9
(All columns have magnitude 3, so after dividing by 3, each column of A is a unit vector. ✓)

Col 1 · Col 2 = (1)(2) + (2)(1) + (-2)(2) = 2 + 2 - 4 = 0 ✓
Col 1 · Col 3 = (1)(2) + (2)(-2) + (-2)(-1) = 2 - 4 + 2 = 0 ✓
Col 2 · Col 3 = (2)(2) + (1)(-2) + (2)(-1) = 4 - 2 - 2 = 0 ✓

Since columns of A are orthonormal, AᵀA = I.
Therefore A is an orthogonal matrix. ✓
Also, |A| = (1/3)³ * |B| = (1/27) * 27 = ±1. ✓