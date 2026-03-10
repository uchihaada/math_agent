# Example 1

Problem:

Find

d/dx | x 1 |
| x² x |

Topics:
calculus, linear_algebra

Structure:
determinant_derivative

Difficulty:
jee_advanced

Key Insight:
Differentiate determinant row-wise.

Solution:
| x 1 |
| x² x |

Determinant = x² − x² = 0

Derivative = 0

# Example 2

Problem:

Find probability that coefficient of x³ in (1+x)⁶ is even.

Topics:
probability, combinatorics, algebra

Structure:
binomial_probability

Difficulty:
jee_main

Key Insight:
Use the Binomial Theorem general term T_{r+1} = nCr to find the specific coefficient, then check its parity directly.

Solution:

Coefficient = 6C3 = 20
Even → Probability = 1

# Example 3

Problem:

Evaluate

lim x→0 ln(1+x)/x

Topics:
calculus, logarithms

Structure:
standard_limit

Difficulty:
jee_main

Key Insight:
Use the standard Maclaurin expansion ln(1+x) ≈ x for small x, or recognise this as the standard limit definition of the natural logarithm derivative at x = 0.

Solution:

Using Taylor expansion

ln(1+x) ≈ x

Limit = 1

# Example 4

Problem:

Maximize xy given x + y = 10

Topics:
calculus, inequalities

Structure:
optimization_constraint

Difficulty:
jee_main

Key Insight:
Use AM-GM.

Solution:

x+y=10
Max xy occurs at x=y=5

Max = 25

# Example 5

Problem:
Find the area enclosed between y = x² and y = x + 2.

Topics:
calculus, algebra

Structure:
area_between_curves

Difficulty:
jee_main

Key Insight:
Find the intersection points by solving the curves simultaneously (algebra). Then integrate the difference (upper curve minus lower curve) between those bounds (calculus). Always sketch or verify which curve is on top within the interval.

Solution:
Step 1 - Find intersection points:
x² = x + 2
x² - x - 2 = 0
(x - 2)(x + 1) = 0
x = -1 and x = 2

Step 2 - Identify upper and lower curves on [-1, 2]:
At x = 0: y = x + 2 gives 2, y = x² gives 0.
So (x + 2) is the upper curve.

Step 3 - Integrate:
Area = ∫[-1 to 2] [(x + 2) - x²] dx
= [x²/2 + 2x - x³/3] from -1 to 2
= (2 + 4 - 8/3) - (1/2 - 2 + 1/3)
= (18/3 - 8/3) - (3/6 - 12/6 + 2/6)
= 10/3 - (-7/6)
= 10/3 + 7/6
= 20/6 + 7/6
= 27/6 = 9/2


# Example 6

Problem:
Let X be the number of heads when a fair coin is tossed n times. Using the Binomial distribution mean and variance formulas, find n if the mean of X is 6 and the variance is 2.

Topics:
probability, algebra

Structure:
binomial_mean_variance_solve

Difficulty:
jee_main

Key Insight:
Write down the two Binomial distribution formulas for Mean (np) and Variance (npq) as a system of two equations in two unknowns (n and p). Divide variance by mean to find q, then find p, then n.

Solution:
Mean = np = 6  --- (1)
Variance = npq = 2  --- (2)
Divide (2) by (1):
q = 2/6 = 1/3
p = 1 - q = 2/3
From (1): n * (2/3) = 6  =>  n = 9
Verify: Variance = 9 * (2/3) * (1/3) = 2. ✓
Final Answer: n = 9


# Example 7

Problem:
Solve the system using matrices:
x + y + z = 6
2x + y − z = 1
x + 2y + z = 9

Topics:
linear_algebra, algebra

Structure:
matrix_inverse_system_solve

Difficulty:
jee_main

Key Insight:
Write the system as AX = B. If |A| ≠ 0, the unique solution is X = A⁻¹B. Find A⁻¹ using the adjoint method: A⁻¹ = adj(A) / |A|. This is more systematic than substitution for 3×3 systems.

Solution:
A = [[1,1,1],[2,1,-1],[1,2,1]], X = [x,y,z]^T, B = [6,1,9]^T

Step 1 - Find |A|:
Expanding along Row 1:
|A| = 1(1+2) - 1(2+1) + 1(4-1) = 3 - 3 + 3 = 3 ≠ 0 (unique solution exists)

Step 2 - Find cofactors and adj(A):
C₁₁ = +(1·1 - (-1)·2) = 3
C₁₂ = -(2·1 - (-1)·1) = -3
C₁₃ = +(2·2 - 1·1) = 3
C₂₁ = -(1·1 - 1·2) = 1
C₂₂ = +(1·1 - 1·1) = 0
C₂₃ = -(1·2 - 1·1) = -1
C₃₁ = +(1·(-1) - 1·1) = -2
C₃₂ = -(1·(-1) - 1·2) = 3
C₃₃ = +(1·1 - 1·2) = -1
adj(A) = [[3,1,-2],[-3,0,3],[3,-1,-1]]

Step 3 - Compute adj(A)·B:
Row 1: 3(6) + 1(1) + (-2)(9) = 18 + 1 - 18 = 1
Row 2: -3(6) + 0(1) + 3(9) = -18 + 0 + 27 = 9
Row 3: 3(6) + (-1)(1) + (-1)(9) = 18 - 1 - 9 = 8

X = (1/|A|) · [1, 9, 8]^T = (1/3) · [1, 9, 8]^T
x = 1/3,  y = 3,  z = 8/3

Verification:
Eq1: 1/3 + 3 + 8/3 = 18/3 = 6 ✓
Eq2: 2/3 + 3 - 8/3 = 3/3 = 1 ✓
Eq3: 1/3 + 6 + 8/3 = 27/3 = 9 ✓
Final Answer: x = 1/3, y = 3, z = 8/3