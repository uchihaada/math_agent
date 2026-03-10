# Product Rule Mistake

Topic: calculus
Common Mistake:
Differentiating a product by differentiating each factor separately without applying the product rule.

Example:
d/dx(x^2 sin x)

Incorrect:
2x * cos x

Correct:
2x sin x + x^2 cos x

Rule:
d/dx(uv) = u'v + uv'


# Quotient Rule Mistake

Topic: calculus
Common Mistake:
Flipping the sign in the quotient rule, or differentiating numerator and denominator independently.

Example:
d/dx(x^2 / sin x)

Incorrect:
(2x) / (cos x)

Correct:
(2x sin x - x^2 cos x) / sin^2(x)

Rule:
d/dx(u/v) = (u'v - uv') / v^2


# Chain Rule Mistake

Topic: calculus
Common Mistake:
Differentiating the outer function correctly but forgetting to multiply by the derivative of the inner function.

Example:
d/dx(sin(x^2))

Incorrect:
cos(x^2)

Correct:
cos(x^2) * 2x

Rule:
d/dx[f(g(x))] = f'(g(x)) * g'(x)


# Implicit Differentiation Mistake

Topic: calculus
Common Mistake:
Forgetting to apply the chain rule when differentiating a term in y with respect to x — omitting the dy/dx factor.

Example:
Differentiate y^3 with respect to x.

Incorrect:
3y^2

Correct:
3y^2 * (dy/dx)

Rule:
Every y term picks up a dy/dx factor via the chain rule.


# Log Domain Mistake

Topic: algebra, calculus
Common Mistake:
Accepting all solutions of a logarithmic equation without checking domain constraints, leading to extraneous roots.

Example:
log_2(x) + log_2(x - 3) = 2

Incorrect:
Solving x^2 - 3x - 4 = 0 gives x = 4 or x = -1. Accepting both.

Correct:
x = -1 is rejected because log_2(-1) is undefined. Final answer: x = 4 only.

Rule:
Always verify that all log arguments are strictly positive in the original equation.


# Vieta's Formula Sign Mistake

Topic: algebra
Common Mistake:
Getting the sign wrong on the sum of roots from Vieta's formulas — using +b/a instead of -b/a.

Example:
x^2 - 5x + 6 = 0

Incorrect:
Sum of roots = +(-5)/1 = -5

Correct:
Sum of roots = -(-5)/1 = 5

Rule:
For ax^2 + bx + c = 0: sum = -b/a, product = c/a.


# Binomial General Term Index Mistake

Topic: algebra
Common Mistake:
Using r instead of r+1 when identifying the term number, leading to an off-by-one error in the index.

Example:
Find the 4th term of (x + 2)^7.

Incorrect:
T_4 = 7C4 * x^3 * 2^4  (using r = 4)

Correct:
T_4 = T_{3+1} = 7C3 * x^4 * 2^3  (r = 3 because T_{r+1} is the general term)

Rule:
General term is T_{r+1} = nCr * a^(n-r) * b^r. For the kth term, set r = k - 1.


# Stars and Bars: Positive vs Non-Negative Mistake

Topic: algebra, combinatorics
Common Mistake:
Applying the non-negative integer formula directly when the problem requires strictly positive integers, without substituting to reduce the constraint.

Example:
Number of positive integral solutions to x + y + z = 10.

Incorrect:
(10 + 3 - 1)C(3 - 1) = 12C2 = 66

Correct:
Substitute x = a+1, y = b+1, z = c+1 → a + b + c = 7.
Answer = (7 + 3 - 1)C(3 - 1) = 9C2 = 36

Rule:
For positive integers (≥ 1): subtract 1 per variable first, then apply (n + r - 1)C(r - 1).


# Matrix Multiplication Order Mistake

Topic: linear_algebra
Common Mistake:
Reversing the order of matrix multiplication. Since AB ≠ BA in general, swapping order gives a wrong result.

Example:
A = [[1,2],[3,4]], B = [[0,1],[1,0]]

Incorrect:
Assuming AB = BA.

Correct:
AB = [[2,1],[4,3]],  BA = [[3,4],[1,2]]  (different matrices)

Rule:
Matrix multiplication is not commutative. Always preserve the stated order.


# Adjoint Determinant Formula Mistake

Topic: algebra, linear_algebra
Common Mistake:
Using |adj(A)| = |A|^n instead of |A|^(n-1), forgetting the exponent is n-1.

Example:
3x3 matrix with |A| = 5.

Incorrect:
|adj(A)| = 5^3 = 125

Correct:
|adj(A)| = 5^(3-1) = 5^2 = 25

Rule:
|adj(A)| = |A|^(n-1) where n is the order of the square matrix.


# Conditional Probability Denominator Mistake

Topic: probability
Common Mistake:
Using the total sample space size as the denominator in a conditional probability instead of the reduced sample space (the given condition).

Example:
P(sum = 8 | both dice show even numbers)

Incorrect:
P = 3/36  (using total outcomes 36 as denominator)

Correct:
P = 3/9 = 1/3  (denominator is 9, the number of outcomes where both dice are even)

Rule:
P(A|B) = P(A ∩ B) / P(B). The denominator is always P(B), not P(total).


# Bayes vs Total Probability Confusion

Topic: probability
Common Mistake:
Using Bayes' Theorem when Law of Total Probability is needed, or vice versa.

Incorrect use:
Finding P(defective item) using Bayes' Theorem.

Correct use:
P(defective) requires Law of Total Probability: P(D) = Σ P(Eᵢ) * P(D|Eᵢ).
Bayes' Theorem is used only when the outcome has already occurred and you need P(cause | effect).

Rule:
Total Probability → finding P(outcome) before it happens.
Bayes' Theorem → finding P(cause) after the outcome is known.


# Binomial Distribution: n and r Confusion

Topic: probability
Common Mistake:
Confusing the number of trials (n) with the number of successes (r) when setting up the binomial formula.

Example:
A coin is tossed 6 times. Find P(exactly 4 heads).

Incorrect:
P = 6C6 * (1/2)^4 * (1/2)^2  (using r = 6 instead of r = 4)

Correct:
P = 6C4 * (1/2)^4 * (1/2)^2 = 15/64

Rule:
P(X = r) = nCr * p^r * q^(n-r). r is the desired successes, n is total trials.


# GP Sum Formula: Wrong Formula for r > 1

Topic: algebra
Common Mistake:
Using S_n = a(1 - r^n)/(1 - r) when r > 1, which gives a negative denominator and wrong sign.

Example:
Sum of first 5 terms of 3, 6, 12, 24, 48  (r = 2)

Incorrect:
S_5 = 3(1 - 2^5)/(1 - 2) = 3(-31)/(-1) = 93  (accidentally correct here but formula form is wrong)

Correct:
Use S_n = a(r^n - 1)/(r - 1) when r > 1:
S_5 = 3(2^5 - 1)/(2 - 1) = 3 * 31 = 93

Rule:
r < 1 → use a(1 - r^n)/(1 - r).  r > 1 → use a(r^n - 1)/(r - 1).


# Eigenvalue vs Eigenvector Confusion

Topic: linear_algebra
Common Mistake:
Substituting the wrong eigenvalue when solving for eigenvectors, or forgetting that eigenvectors are only defined up to a scalar multiple.

Example:
A = [[3,1],[2,4]], eigenvalues λ = 2 and λ = 5.

Incorrect:
Solving (A - 5I)v = 0 but writing the result as the eigenvector for λ = 2.

Correct:
λ = 2 → solve (A - 2I)v = 0 → v = [1, -1]^T
λ = 5 → solve (A - 5I)v = 0 → v = [1, 2]^T

Rule:
Always pair each eigenvector calculation with its own eigenvalue. Any scalar multiple of an eigenvector is also valid.