# Logarithm

Topic: algebra, calculus
Constraint:
log_b(x) requires x > 0 and base b > 0, b ≠ 1.

Details:
- Natural log ln(x): requires x > 0
- log_b(f(x)): requires f(x) > 0 — solve f(x) > 0 to find the domain
- ln(0) and ln(negative) are undefined

Example:
log_2(x - 3): requires x - 3 > 0 → domain is x > 3.
log(x^2 - 4): requires x^2 - 4 > 0 → x < -2 or x > 2.


# Square Root / Even Roots

Topic: algebra, calculus
Constraint:
sqrt(f(x)) requires f(x) ≥ 0 (for real values).
nth root with even n: requires f(x) ≥ 0.
nth root with odd n: defined for all real f(x).

Example:
sqrt(4 - x^2): requires 4 - x^2 ≥ 0 → -2 ≤ x ≤ 2.
sqrt(x - 1) + sqrt(3 - x): requires x ≥ 1 AND x ≤ 3 → domain is [1, 3].


# Rational Expressions (Division)

Topic: algebra, calculus
Constraint:
f(x) / g(x) requires g(x) ≠ 0.

Details:
- Find all x where denominator = 0 and exclude from domain
- In limits: denominator = 0 triggers indeterminate form check

Example:
1 / (x^2 - 1): denominator zero at x = ±1 → domain is ℝ \ {-1, 1}.
(x - 2) / (x^2 - 5x + 6): factor denominator → (x-2)(x-3) = 0 at x = 2, 3. Exclude both.


# Inverse Trigonometric Functions

Topic: algebra, calculus
Constraint:
asin(x) and acos(x): require -1 ≤ x ≤ 1.
atan(x): defined for all real x.
asin and atan range: [-π/2, π/2].
acos range: [0, π].

Example:
asin(2x - 1): requires -1 ≤ 2x - 1 ≤ 1 → 0 ≤ x ≤ 1.


# Trigonometric Functions

Topic: calculus
Constraint:
tan(x) and sec(x): undefined at x = π/2 + nπ (n ∈ ℤ).
cot(x) and csc(x): undefined at x = nπ (n ∈ ℤ).
sin(x) and cos(x): defined for all real x, range [-1, 1].

Example:
tan(x): domain is ℝ \ {π/2 + nπ}.


# Probability Values

Topic: probability
Constraint:
0 ≤ P(A) ≤ 1 for any event A.
P(impossible event) = 0.
P(certain event) = 1.
Sum of all probabilities in a sample space = 1: Σ P(xᵢ) = 1.

Details:
- If a computed probability is negative or > 1, the setup is wrong
- P(A) + P(A') = 1 always holds

Example:
If P(A) = 0.7 and P(B) = 0.5, then P(A ∩ B) ≤ min(0.7, 0.5) = 0.5.
If P(A ∪ B) = P(A) + P(B) − P(A ∩ B) > 1, recheck the given values.


# Binomial Distribution Parameters

Topic: probability
Constraint:
n must be a positive integer (number of trials).
0 < p < 1 (probability of success).
q = 1 - p (probability of failure).
r must satisfy 0 ≤ r ≤ n.

Example:
n = 10, p = 1/6 are valid.
n = -3 or p = 1.5 are invalid.


# Geometric Progression Infinite Sum

Topic: algebra
Constraint:
S_∞ = a / (1 - r) is only valid when |r| < 1.
If |r| ≥ 1, the series diverges and has no finite sum.

Example:
1 + 2 + 4 + ...: r = 2, |r| > 1 → no finite sum (diverges).
1 + 1/2 + 1/4 + ...: r = 1/2, |r| < 1 → S_∞ = 1/(1-1/2) = 2.


# Determinant and Matrix Inverse

Topic: linear_algebra
Constraint:
A matrix A is invertible (non-singular) only if |A| ≠ 0.
If |A| = 0, the matrix is singular: no inverse exists, and any system Ax = b has either no solution or infinitely many.

Example:
A = [[1,2],[2,4]]: |A| = 4 - 4 = 0 → singular, no inverse.
Cramer's Rule is only applicable when |A| ≠ 0.


# Eigenvalues and Diagonalization

Topic: linear_algebra
Constraint:
An n×n matrix is diagonalizable only if it has n linearly independent eigenvectors.
A matrix with repeated eigenvalues may or may not be diagonalizable — check eigenvector count.

Example:
Identity matrix I has eigenvalue 1 with multiplicity n but is already diagonal (diagonalizable).
A = [[2,1],[0,2]] has eigenvalue 2 with multiplicity 2 but only one independent eigenvector → not diagonalizable.


# Definite Integral

Topic: calculus
Constraint:
f(x) must be defined and integrable on the closed interval [a, b].
If f(x) has a discontinuity or singularity within [a, b], it is an improper integral — treat separately.

Example:
∫[0 to 2] 1/(x-1) dx: integrand undefined at x = 1 ∈ [0, 2] → improper integral, split at x = 1.
∫[-1 to 1] sqrt(1 - x^2) dx: valid, integrand defined on [-1, 1].


# Logarithmic Differentiation

Topic: calculus
Constraint:
When applying logarithmic differentiation to y = f(x)^g(x), the base f(x) must be positive.
If f(x) can be negative, use |f(x)| inside the log and handle sign separately.

Example:
y = (x^2 + 1)^sin(x): x^2 + 1 > 0 always → safe to take ln directly.
y = x^x: requires x > 0.


# Combination and Permutation

Topic: algebra, combinatorics
Constraint:
nCr and nPr require 0 ≤ r ≤ n and both n, r must be non-negative integers.
nC0 = nCn = 1.
nCr = nC(n-r) (symmetry property).

Example:
10C3 = 10C7 = 120.
5C6 is undefined (r > n).