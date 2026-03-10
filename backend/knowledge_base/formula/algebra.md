# Vieta's Formulas (Quadratic)

Topic: algebra, quadratics
Key Pattern: ax^2 + bx + c = 0
Formula:
Sum of roots (α + β) = -b / a
Product of roots (αβ) = c / a

When to use:
When a problem involves the sum, product, or a symmetric expression of the roots of a quadratic equation without needing to find the exact roots.

Example:
If roots are α, β, find α^2 + β^2 using (α+β)^2 - 2αβ.


# Logarithm Properties (Product, Quotient, Power)

Topic: algebra, logarithms
Key Pattern: log_b(x)
Formula:
log_b(xy) = log_b(x) + log_b(y)
log_b(x/y) = log_b(x) - log_b(y)
log_b(x^n) = n * log_b(x)

When to use:
When simplifying logarithmic expressions, expanding single logs, or combining multiple logs into a single log equation to solve for a variable.

Example:
log_2(x) + log_2(x-1) becomes log_2[x(x-1)]


# Base Change Rule (Logarithms)

Topic: algebra, logarithms
Key Pattern: log_a(b)
Formula:
log_a(b) = log_c(b) / log_c(a)
Special case: log_a(b) = 1 / log_b(a)

When to use:
When evaluating or simplifying logarithms that have different bases, allowing you to convert them all to a common base (like base 10 or base e).

Example:
log_2(3) * log_3(4) = (ln 3 / ln 2) * (ln 4 / ln 3) = ln 4 / ln 2 = 2


# Arithmetic Progression (Nth Term & Sum)

Topic: algebra, sequences_and_series
Key Pattern: a, a+d, a+2d, ...
Formula:
Nth term: T_n = a + (n-1)d
Sum of n terms: S_n = (n/2) *[2a + (n-1)d] OR (n/2) * (a + l) where l is the last term.

When to use:
When dealing with a sequence where the difference between consecutive terms is constant. 

Example:
Find the 10th term of 2, 5, 8... -> a=2, d=3, T_10 = 2 + 9(3) = 29


# Geometric Progression (Nth Term & Sum)

Topic: algebra, sequences_and_series
Key Pattern: a, ar, ar^2, ...
Formula:
Nth term: T_n = a * r^(n-1)
Sum of n terms: S_n = a(1 - r^n) / (1 - r) for r < 1, OR a(r^n - 1) / (r - 1) for r > 1.

When to use:
When a sequence involves a constant multiplier (common ratio) between consecutive terms.

Example:
Sum of first 5 terms of 3, 6, 12... -> a=3, r=2, S_5 = 3(2^5 - 1) / (2 - 1)


# Infinite Geometric Series Sum

Topic: algebra, sequences_and_series
Key Pattern: S_∞ = a + ar + ar^2 + ... (where |r| < 1)
Formula:
S_∞ = a / (1 - r)

When to use:
When adding an infinite number of terms in a geometric sequence whose common ratio is strictly between -1 and 1.

Example:
1 + 1/2 + 1/4 + 1/8 + ... = 1 / (1 - 0.5) = 2


# Binomial Theorem (General Term)

Topic: algebra, binomial_theorem
Key Pattern: (x + y)^n
Formula:
General Term: T_{r+1} = nCr * (x)^(n-r) * (y)^r
where nCr = n! / [r!(n-r)!]

When to use:
When finding a specific term, coefficient, or term independent of x in a large binomial expansion without expanding the whole expression.

Example:
Find the 3rd term of (2x + 3)^5. Here r=2, T_3 = 5C2 * (2x)^3 * (3)^2.


# Euler's Formula (Complex Numbers)

Topic: algebra, complex_numbers
Key Pattern: z = x + iy
Formula:
z = r * e^(iθ) = r(cos θ + i sin θ)
where r = |z| = √(x^2 + y^2) and θ = arg(z) = tan⁻¹(y/x)

When to use:
When multiplying, dividing, or finding large powers/roots of complex numbers.

Example:
(1 + i)^10 is easiest solved by converting 1+i to √2 * e^(iπ/4) first.


# Newton's Sums

Topic: algebra, theory_of_equations, 
Key Pattern: ax^2 + bx + c = 0 and S_n = α^n + β^n
Formula:
a(S_n) + b(S_{n-1}) + c(S_{n-2}) = 0

When to use:
When a problem asks to evaluate a large power sum (like α^10 + β^10) or a ratio of such sums for the roots of a polynomial.

Example:
If α, β are roots of x^2 - 6x - 2 = 0, evaluate (a_10 - 2a_8) / (2a_9) where a_n = α^n - β^n.


# Stars and Bars (Beggar's Method)

Topic: algebra, combinatorics, 
Key Pattern: x_1 + x_2 + ... + x_r = n (Non-negative integers)
Formula:
Total number of solutions = (n + r - 1) C (r - 1)

When to use:
When distributing 'n' identical items among 'r' distinct groups, or finding the number of non-negative integral solutions to a linear equation.

Example:
Find the number of non-negative integral solutions to x + y + z = 10.


# Derangements

Topic: algebra, combinatorics, 
Key Pattern: n objects, none in their original position
Formula:
D_n = n! *[ 1 - 1/1! + 1/2! - 1/3! + ... + (-1)^n / n! ]
Recursive: D_n = (n-1)(D_{n-1} + D_{n-2})

When to use:
When finding the number of ways to arrange items such that absolutely NO item goes to its designated/correct spot (e.g., letters in wrong envelopes).

Example:
Number of ways to put 5 different letters into 5 addressed envelopes such that no letter goes to the correct envelope (D_5 = 44).


# Properties of Adjoint Matrix

Topic: algebra, matrices, 
Key Pattern: |adj(A)| or adj(adj(A))
Formula:
1. |adj(A)| = |A|^(n-1)
2. adj(adj(A)) = |A|^(n-2) * A
3. |adj(adj(A))| = |A|^((n-1)^2)
(where n is the order of the square matrix A)

When to use:
When a problem asks for the determinant of an adjoint matrix or nested adjoints, which would be computationally impossible to find by calculating the actual matrices.

Example:
If A is a 3x3 matrix with |A| = 4, find |adj(adj(A))|.


# Nth Roots of Unity

Topic: algebra, complex_numbers, 
Key Pattern: z^n = 1
Formula:
Roots: z = e^(i * 2kπ/n) for k = 0, 1, ..., n-1
Sum of roots: 1 + α + α^2 + ... + α^(n-1) = 0
Product of roots: 1 * α * α^2 * ... * α^(n-1) = (-1)^(n-1)

When to use:
When dealing with regular polygons centered at the origin in the complex plane, or simplifying massive algebraic polynomials like z^(n-1) + z^(n-2) + ... + 1 = 0.

Example:
Simplify (z - α_1)(z - α_2)...(z - α_{n-1}) where α_k are the complex roots of unity.


# Rotation Theorem (Coni Method)

Topic: algebra, complex_numbers, 
Key Pattern: Triangle vertices z1, z2, z3
Formula:
(z_3 - z_1) / (z_2 - z_1) = |z_3 - z_1| / |z_2 - z_1| * e^(iθ)
where θ is the directed angle from vector (z_2 - z_1) to (z_3 - z_1).

When to use:
When a problem involves rotating a line segment in the complex plane, or proving geometric properties (like equilateral or isosceles right triangles) using complex coordinates.

Example:
Find the third vertex of an equilateral triangle if two vertices are z1 and z2.



# AM-GM Inequality

Topic: algebra, inequalities
Key Pattern: Maximize/minimize a product or sum with a constraint
Formula:
(a + b)/2 ≥ √(ab)
Equality when a = b.
General form: (a₁ + a₂ + ... + aₙ)/n ≥ (a₁a₂...aₙ)^(1/n)

When to use:
When optimizing or bounding expressions where you need to find the maximum product for a fixed sum, or minimum sum for a fixed product.

Example:
If x + y = 10, find the maximum value of xy. By AM-GM, xy ≤ ((x+y)/2)^2 = 25. Maximum is 25 at x = y = 5.

# Cauchy-Schwarz Inequality

Topic: algebra, inequalities
Key Pattern: Bound a dot product in terms of magnitudes
Formula:
(a₁² + a₂² + ...)(b₁² + b₂² + ...) ≥ (a₁b₁ + a₂b₂ + ...)²
Equality when a₁/b₁ = a₂/b₂ = ...

When to use:
When bounding sums of products or proving inequalities involving squares.

Example:
Prove (a² + b²)(x² + y²) ≥ (ax + by)² for all real a, b, x, y.

# Modulus Equation

Topic: algebra, equations
Key Pattern: |x − a| = b
Formula:
x = a + b  or  x = a − b
General: |f(x)| = g(x) → f(x) = g(x) or f(x) = −g(x), provided g(x) ≥ 0.

When to use:
When solving absolute value equations. Always verify solutions satisfy the domain condition g(x) ≥ 0.

Example:
|x − 3| = 5 → x = 3 + 5 = 8 or x = 3 − 5 = −2.