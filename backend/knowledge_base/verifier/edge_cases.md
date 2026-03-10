# Standard Limits

Topic: calculus, limits
Edge Cases:
lim x→0  sin(x)/x        = 1
lim x→0  tan(x)/x        = 1
lim x→0  (1 - cos x)/x²  = 1/2
lim x→0  (e^x - 1)/x     = 1
lim x→0  ln(1 + x)/x     = 1
lim x→∞  (1 + 1/x)^x     = e
lim x→0  (1 + x)^(1/x)   = e

Note:
These are memorised results — do not apply L'Hôpital's to them directly.
Recognising these forms inside a larger limit is a key speed optimisation.


# Indeterminate Forms

Topic: calculus, limits
Edge Cases:
0/0    → L'Hôpital's Rule or factoring/rationalising
∞/∞    → L'Hôpital's Rule or divide numerator and denominator by highest power
0 * ∞  → rewrite as 0/(1/∞) or ∞/(1/0) to get 0/0 or ∞/∞
∞ - ∞  → rationalise or find common denominator to reduce to 0/0
1^∞    → use e^[lim (f-1)*g] shortcut
0^0    → take log, convert to 0/0 form
∞^0    → take log, convert to 0*∞ form

Note:
Always identify the indeterminate form before choosing a method.
L'Hôpital's Rule requires the 0/0 or ∞/∞ form specifically — it cannot be applied to other forms directly.


# Division by Zero

Topic: algebra, calculus
Edge Cases:
Any expression a/0 is undefined — not infinity.
In limits, a/0 form (where a ≠ 0) indicates the limit is ±∞ or does not exist (check left/right limits).
0/0 is indeterminate — the actual limit may be any finite value or ∞.

Examples:
lim x→2  (x+1)/(x-2): numerator → 3, denominator → 0 → limit is ±∞ (check sides).
lim x→2  (x^2-4)/(x-2): 0/0 form → factor → lim (x+2) = 4.


# Derivative at a Sharp Corner or Cusp

Topic: calculus
Edge Cases:
A function is not differentiable at a point where:
- There is a sharp corner (e.g. |x| at x = 0)
- There is a vertical tangent
- The function is discontinuous

Example:
f(x) = |x|: left derivative at 0 = -1, right derivative at 0 = +1. Since they differ, f'(0) does not exist.
f(x) = x^(1/3): has a vertical tangent at x = 0 → not differentiable there.


# Continuity vs Differentiability

Topic: calculus
Edge Cases:
Differentiable → always continuous.
Continuous → NOT necessarily differentiable (e.g. |x| is continuous but not differentiable at 0).
Discontinuous → never differentiable at that point.

Example:
f(x) = |x - 2|: continuous everywhere, not differentiable at x = 2.


# Zero Determinant (Singular Matrix)

Topic: linear_algebra
Edge Cases:
|A| = 0 → matrix is singular.
Consequences:
- No inverse exists
- System Ax = b may have no solution or infinitely many (never a unique solution)
- Eigenvalue λ = 0 is present
- Rows/columns are linearly dependent

Example:
A = [[2,4],[1,2]]: |A| = 4 - 4 = 0 → singular.
System 2x + 4y = 6, x + 2y = 3: infinite solutions (dependent equations).
System 2x + 4y = 6, x + 2y = 4: no solution (inconsistent).


# Repeated Eigenvalues

Topic: linear_algebra
Edge Cases:
A repeated eigenvalue does not guarantee a repeated eigenvector.
Algebraic multiplicity = how many times λ appears as a root of the characteristic equation.
Geometric multiplicity = number of linearly independent eigenvectors for λ.
If geometric < algebraic multiplicity → matrix is NOT diagonalizable.

Example:
A = [[5,1],[0,5]]: eigenvalue λ = 5 with algebraic multiplicity 2.
(A - 5I) = [[0,1],[0,0]]: only one independent eigenvector → not diagonalizable.


# Probability: Mutually Exclusive vs Independent

Topic: probability
Edge Cases:
Mutually exclusive: P(A ∩ B) = 0. They cannot both happen.
Independent: P(A ∩ B) = P(A)*P(B). One happening does not affect the other.
These are NOT the same — two mutually exclusive events (both with P > 0) are never independent.

Example:
Rolling a die: A = {1,2,3}, B = {4,5,6}.
Mutually exclusive: A ∩ B = ∅. But P(A)*P(B) = 1/4 ≠ 0 → not independent.


# Geometric Series: r = 1 Edge Case

Topic: algebra
Edge Cases:
S_n = a(1 - r^n)/(1 - r) is undefined when r = 1.
When r = 1: all terms equal a, so S_n = n*a directly.
When r = -1: series alternates, partial sums oscillate between a and 0 — no sum formula applies.

Example:
2 + 2 + 2 + ... (10 terms): r = 1 → S_10 = 10 * 2 = 20.


# Binomial Theorem: Negative or Fractional Exponent

Topic: algebra
Edge Cases:
The standard Binomial Theorem T_{r+1} = nCr * a^(n-r) * b^r applies only for positive integer n.
For negative or fractional n, the expansion is an infinite series and nCr is replaced by the generalised binomial coefficient.
Convergence requires |x| < 1.

Example:
(1 + x)^(-1) = 1 - x + x^2 - x^3 + ... (infinite series, valid for |x| < 1).
(1 + x)^(1/2) = 1 + x/2 - x^2/8 + ... (infinite series, valid for |x| < 1).


# Integration: Constant of Integration

Topic: calculus
Edge Cases:
Every indefinite integral requires + C (constant of integration).
Omitting C is incorrect and loses the general solution.
In definite integrals, C cancels and is not written.

Example:
∫ 2x dx = x^2 + C  (not just x^2).
∫[0 to 3] 2x dx = [x^2 + C]_0^3 = (9 + C) - (0 + C) = 9.  C cancels.


# L'Hôpital's Rule: Confirm Form Before Applying

Topic: calculus, limits
Edge Cases:
L'Hôpital's Rule is only valid for 0/0 or ∞/∞ forms.
Applying it to a non-indeterminate limit gives a wrong answer.

Example:
lim x→0  (x^2 + 1)/x: numerator → 1, denominator → 0. This is 1/0, NOT 0/0.
Limit is ∞ (does not exist as finite). Do not apply L'Hôpital's.

Correct check: always substitute first. Only apply L'Hôpital's if result is 0/0 or ∞/∞.


# Derangement: D_0 and D_1

Topic: algebra, combinatorics
Edge Cases:
D_0 = 1 (empty arrangement — vacuously a derangement).
D_1 = 0 (one object must go to its correct position — no derangement possible).
D_2 = 1 (only one way: swap the two).
D_3 = 2.

Note:
These base cases are required when computing partial derangements for small n-r values.
Forgetting D_1 = 0 is a common error in derangement problems.


# Bayes' Theorem: Exhaustive and Mutually Exclusive Causes

Topic: probability
Edge Cases:
Bayes' Theorem requires that the prior events E₁, E₂, ..., Eₙ are mutually exclusive and exhaustive (they partition the entire sample space).
If they do not cover all cases or overlap, the Law of Total Probability in the denominator is invalid.

Example:
If P(E₁) + P(E₂) + P(E₃) ≠ 1, the partition is incomplete — recheck the problem setup before applying Bayes'.


# Modulus / Absolute Value Equations: Spurious Solutions

Topic: algebra
Edge Cases:
When solving |f(x)| = g(x), the equation g(x) ≥ 0 is a necessary condition.
Solutions where g(x) < 0 are spurious (extraneous) and must be rejected.

Example:
|x + 1| = x - 3.
Case 1: x + 1 = x - 3 → 1 = -3 (no solution).
Case 2: -(x + 1) = x - 3 → x = 1.
Check: g(1) = 1 - 3 = -2 < 0 → rejected.
No valid solution.