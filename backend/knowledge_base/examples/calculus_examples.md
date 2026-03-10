# Example 1

Problem:
Find the derivative of y = x^3 * tan(x)

Topics:
calculus

Structure:
polynomial * trigonometric

Key Insight:
Two functions multiplied → Apply Product Rule.

Solution:
Apply u'v + uv'
u = x^3, u' = 3x^2
v = tan(x), v' = sec^2(x)
dy/dx = 3x^2 tan(x) + x^3 sec^2(x)


# Example 2

Problem:
Find dy/dx for y = (e^x + 1) / (e^x - 1)

Topics:
calculus

Structure:
function / function

Key Insight:
Division of functions → Apply Quotient Rule.

Solution:
Apply (vu' - uv') / v^2
u = e^x + 1, u' = e^x
v = e^x - 1, v' = e^x
Numerator = (e^x - 1)(e^x) - (e^x + 1)(e^x)
          = e^2x - e^x - (e^2x + e^x)
          = -2e^x
Denominator = (e^x - 1)^2
dy/dx = -2e^x / (e^x - 1)^2


# Example 3

Problem:
Find dy/dx if y = (sin x)^(ln x)

Topics:
calculus, 

Structure:
function^function

Key Insight:
Variable base and variable exponent → Apply Logarithmic Differentiation.

Solution:
Take ln of both sides:
ln(y) = ln(x) * ln(sin x)
Differentiate implicitly:
(1/y)y' =[ln(x) * (1/sin x)*cos x] + [ln(sin x) * (1/x)]
y' = y *[ln(x)cot(x) + ln(sin x)/x]
Substitute y back:
y' = (sin x)^(ln x) *[ln(x)cot(x) + ln(sin x)/x]


# Example 4

Problem:
Find dy/dx for y = tan⁻¹[ (3x - x^3) / (1 - 3x^2) ] where |x| < 1/√3

Topics:
calculus, inverse_trigonometry 

Structure:
inverse_trigonometric(rational_function)

Key Insight:
Standard Substitution. The term inside looks like the tan(3θ) identity.

Solution:
Let x = tan(θ) → θ = tan⁻¹(x)
Expression becomes tan⁻¹( tan(3θ) ) = 3θ
y = 3tan⁻¹(x)
Differentiate:
dy/dx = 3 / (1 + x^2)


# Example 5

Problem:
If x = a(θ + sin θ) and y = a(1 - cos θ), find d²y/dx² at θ = π/2

Topics:
calculus, trigonometric

Structure:
parametric_second_derivative

Key Insight:
Find first derivative dy/dx using parametric rule, then differentiate w.r.t x (requires Chain Rule dt/dx).

Solution:
1. dx/dθ = a(1 + cos θ)
2. dy/dθ = a(sin θ)
3. dy/dx = (a sin θ) / (a(1+cos θ)) = sin θ / (2cos²(θ/2)) = (2sin(θ/2)cos(θ/2))/(2cos²(θ/2)) = tan(θ/2)
4. d²y/dx² = d/dx(tan(θ/2))
   = sec²(θ/2) * (1/2) * (dθ/dx)  <-- Chain Rule Step
   = 0.5 sec²(θ/2) * [1 / a(1 + cos θ)]
At θ = π/2:
   = 0.5 * sec²(π/4) * [1 / a(1+0)]
   = 0.5 * 2 * (1/a)
   = 1/a


# Example 6

Problem:
If f(x) = x + tan x and g(x) is the inverse of f(x), find g'(x).

Topics:
calculus, inverse_functions

Structure:
inverse_derivative

Key Insight:
Use Inverse Function Theorem: g'(x) = 1 / f'(g(x)). Note that finding g(x) explicitly is impossible here.

Solution:
g'(x) = 1 / f'( g(x) )
Find f'(x) = 1 + sec^2(x)
Therefore, g'(x) = 1 /[1 + sec^2( g(x) )]


# Example 7

Problem:
Find the derivative of the determinant:
| x      x^2 |
| x^3    2x  |

Topics:
calculus, matrix

Structure:
determinant_differentiation

Key Insight:
Differentiate row by row and sum the determinants.

Solution:
Row 1 diff: | 1   2x |
            | x^3 2x |
Row 2 diff: | x   x^2 |
            | 3x^2 2  |
Total = (2x - 2x^4) + (2x - 3x^4)
      = 4x - 5x^4
(Verification: Original Det = 2x^2 - x^5. Deriv = 4x - 5x^4. Matches.)


# Example 8

Problem:
Evaluate lim(x→0) (e^x - 1 - x) / x^2

Topics:
calculus, limits

Structure:
indeterminate_limit (0/0)

Key Insight:
Direct substitution yields 0/0. Apply L'Hôpital's Rule (potentially more than once) since numerator and denominator are differentiable.

Solution:
Direct substitution: (1 - 1 - 0) / 0 = 0/0.
Apply L'Hôpital's (1st time):
Derivative of num: e^x - 1
Derivative of den: 2x
New limit: lim(x→0) (e^x - 1) / 2x
Direct substitution: (1 - 1) / 0 = 0/0.
Apply L'Hôpital's (2nd time):
Derivative of num: e^x
Derivative of den: 2
New limit: lim(x→0) e^x / 2
Evaluate: e^0 / 2 = 1/2


# Example 9

Problem:
Evaluate lim(x→0) (cos x)^(1/x^2)

Topics:
calculus, limits, trigonometric

Structure:
function^function limit

Key Insight:
As x→0, cos(0) = 1 and 1/0^2 → ∞. This is a 1^∞ form. Use the e^[lim (f(x)-1)*g(x)] shortcut.

Solution:
f(x) = cos x, g(x) = 1/x^2
Limit = e^[ lim(x→0) (cos x - 1) * (1/x^2) ]
Focus on the exponent limit: lim(x→0) (cos x - 1) / x^2
Multiply by conjugate or use L'Hôpital's / Taylor expansion.
Using standard limit: 1 - cos x ~ x^2 / 2 for small x.
So, (cos x - 1) / x^2 = -1/2.
Exponent limit = -1/2.
Final Answer: e^(-1/2) = 1 / √e


# Example 10

Problem:
Find dy/dx if x^3 + y^3 = 6xy

Topics:
calculus, derivatives

Structure:
implicit_equation

Key Insight:
y cannot be easily isolated. Differentiate both sides with respect to x, remembering to use the Chain Rule for y terms and the Product Rule for the xy term.

Solution:
Differentiate term by term:
d/dx(x^3) = 3x^2
d/dx(y^3) = 3y^2 * (dy/dx)
d/dx(6xy) = 6 [ x*(dy/dx) + y*(1) ] (Product Rule)
Equation becomes:
3x^2 + 3y^2(dy/dx) = 6x(dy/dx) + 6y
Divide by 3:
x^2 + y^2(dy/dx) = 2x(dy/dx) + 2y
Group dy/dx terms:
y^2(dy/dx) - 2x(dy/dx) = 2y - x^2
(dy/dx)[y^2 - 2x] = 2y - x^2
dy/dx = (2y - x^2) / (y^2 - 2x)


# Example 11

Problem:
A farmer has 40 meters of fencing to enclose a rectangular garden. What dimensions maximize the area of the garden?

Topics:
calculus, simple_optimization

Structure:
word_problem_max_min

Key Insight:
Set up a primary equation to maximize (Area) and a secondary equation (Perimeter constraint) to reduce the primary equation to a single variable.

Solution:
1. Constraint: Perimeter = 2x + 2y = 40 → x + y = 20 → y = 20 - x
2. Objective Function: Area A = x * y
3. Substitute constraint into objective: A(x) = x(20 - x) = 20x - x^2
4. Find critical points:
   A'(x) = 20 - 2x
   Set A'(x) = 0 → 2x = 20 → x = 10
5. Verify it's a maximum:
   A''(x) = -2. Since A''(x) < 0, the curve is concave down, confirming a local maximum.
6. Find y: y = 20 - 10 = 10
Dimensions: 10m by 10m (Area = 100 sq meters).


# Example 12

Problem:
Find the local maximum and minimum values of f(x) = x^3 - 6x^2 + 9x + 1

Topics:
calculus, simple_optimization

Structure:
polynomial_extrema

Key Insight:
Find critical points by setting f'(x) = 0, then use the Second Derivative Test to classify them.

Solution:
1. Find f'(x):
   f'(x) = 3x^2 - 12x + 9
2. Set f'(x) = 0:
   3(x^2 - 4x + 3) = 0
   3(x - 1)(x - 3) = 0
   Critical points: x = 1, x = 3
3. Find f''(x):
   f''(x) = 6x - 12
4. Classify using f''(x):
   At x = 1: f''(1) = 6(1) - 12 = -6 (Negative → Concave Down → Local Maximum)
   At x = 3: f''(3) = 6(3) - 12 = 6 (Positive → Concave Up → Local Minimum)
5. Find function values:
   Local Max value = f(1) = 1 - 6 + 9 + 1 = 5
   Local Min value = f(3) = 27 - 54 + 27 + 1 = 1

# Example 13

Problem:
Evaluate ∫ x² * e^x dx

Topics:
calculus, integration

Structure:
integration_by_parts_repeated

Key Insight:
The integrand is a product of a polynomial (x²) and an exponential (e^x). Apply Integration by Parts (ILATE: Algebraic before Exponential). Since the polynomial has degree 2, the rule must be applied twice — each application reduces the power of the polynomial by one.

Solution:
Apply IBP: ∫ u dv = uv - ∫ v du
Round 1: Let u = x², dv = e^x dx
=> du = 2x dx, v = e^x
∫ x² e^x dx = x² e^x - ∫ 2x e^x dx

Round 2: Evaluate ∫ 2x e^x dx
Let u = 2x, dv = e^x dx
=> du = 2 dx, v = e^x
∫ 2x e^x dx = 2x e^x - ∫ 2 e^x dx = 2x e^x - 2e^x

Substitute back:
∫ x² e^x dx = x² e^x - (2x e^x - 2e^x) + C
= x² e^x - 2x e^x + 2e^x + C
= e^x(x² - 2x + 2) + C


# Example 14

Problem:
Evaluate ∫ (2x + 3) / √(x² + 3x + 5) dx

Topics:
calculus, integration

Structure:
integration_by_substitution_algebraic

Key Insight:
The numerator (2x + 3) is the exact derivative of the expression inside the square root (x² + 3x + 5). This signals a direct substitution: let t = x² + 3x + 5, which transforms the integral into a simple power rule form.

Solution:
Let t = x² + 3x + 5
dt/dx = 2x + 3  =>  dt = (2x + 3) dx
Substitute:
∫ (2x + 3) / √(x² + 3x + 5) dx = ∫ (1/√t) dt
= ∫ t^(-1/2) dt
= t^(1/2) / (1/2) + C
= 2√t + C
Substitute back t = x² + 3x + 5:
= 2√(x² + 3x + 5) + C


# Example 15

Problem:
Evaluate ∫ sin³(x) dx

Topics:
calculus, integration, trigonometric

Structure:
integration_trig_power_reduction

Key Insight:
Odd powers of sin(x) or cos(x) are handled by splitting off one factor (sin x or cos x) to pair with dx, and converting the remaining even power using the Pythagorean identity sin²x = 1 - cos²x. This sets up a clean substitution.

Solution:
Split: ∫ sin³(x) dx = ∫ sin²(x) * sin(x) dx
Replace sin²(x) = 1 - cos²(x):
= ∫ (1 - cos²x) sin(x) dx
Let t = cos(x) => dt = -sin(x) dx => sin(x) dx = -dt
= ∫ (1 - t²)(-dt)
= -∫ (1 - t²) dt
= -(t - t³/3) + C
= -cos(x) + cos³(x)/3 + C


# Example 16

Problem:
Verify Rolle's Theorem for f(x) = x³ - 6x² + 11x - 6 on [1, 3], and find the value of c.

Topics:
calculus, mean_value_theorems

Structure:
rolles_theorem_verification

Key Insight:
Check all three conditions of Rolle's Theorem: continuity on [a,b], differentiability on (a,b), and f(a) = f(b). If satisfied, set f'(c) = 0 and solve within the open interval to find the guaranteed point c.

Solution:
Step 1 - Check conditions:
f(x) is a polynomial → continuous on [1, 3] and differentiable on (1, 3). ✓
f(1) = 1 - 6 + 11 - 6 = 0
f(3) = 27 - 54 + 33 - 6 = 0
f(1) = f(3) = 0 ✓
All three conditions satisfied.

Step 2 - Find c:
f'(x) = 3x² - 12x + 11
Set f'(c) = 0:
3c² - 12c + 11 = 0
c = [12 ± √(144 - 132)] / 6 = [12 ± √12] / 6 = 2 ± (1/√3)
c = 2 - 1/√3 ≈ 1.42  and  c = 2 + 1/√3 ≈ 2.58
Both values lie in (1, 3). ✓
Rolle's Theorem is verified.


# Example 17

Problem:
Find the absolute maximum and minimum values of f(x) = x³ - 3x² + 1 on [-1/2, 4].

Topics:
calculus, simple_optimization

Structure:
global_extrema_closed_interval

Key Insight:
On a closed interval, the absolute extrema occur either at critical points inside the interval OR at the endpoints. Evaluate f at all critical points and both endpoints, then compare all values. Never skip the endpoint check.

Solution:
Step 1 - Find critical points:
f'(x) = 3x² - 6x = 3x(x - 2)
f'(x) = 0  =>  x = 0 or x = 2
Both lie in [-1/2, 4]. ✓

Step 2 - Evaluate f at critical points and endpoints:
f(-1/2) = (-1/2)³ - 3(-1/2)² + 1 = -1/8 - 3/4 + 1 = 1/8
f(0) = 0 - 0 + 1 = 1
f(2) = 8 - 12 + 1 = -3
f(4) = 64 - 48 + 1 = 17

Step 3 - Compare all values:
{1/8, 1, -3, 17}
Absolute Maximum = 17 at x = 4
Absolute Minimum = -3 at x = 2


# Example 18

Problem:
Find the derivative of f(x) = x² from first principles (definition of derivative).

Topics:
calculus, derivatives

Structure:
first_principles_derivative

Key Insight:
Apply the limit definition f'(x) = lim(h→0) [f(x+h) - f(x)] / h directly. Expand f(x+h), cancel the f(x) terms, factor out h from the numerator to cancel with the denominator, then evaluate the limit.

Solution:
f(x) = x², so f(x + h) = (x + h)² = x² + 2xh + h²
f'(x) = lim(h→0) [(x² + 2xh + h²) - x²] / h
= lim(h→0) [2xh + h²] / h
= lim(h→0) h(2x + h) / h
= lim(h→0) (2x + h)
= 2x