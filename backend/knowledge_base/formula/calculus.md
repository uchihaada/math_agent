# Power Rule

Topic: calculus
Key Pattern: x^n
Formula:
d/dx(x^n) = n * x^(n-1)

When to use:
When differentiating a standard polynomial term where the base is a variable and the exponent is a constant.

Example:
d/dx(x^5) = 5x^4


# Chain Rule

Topic: calculus
Key Pattern: f(g(x))
Formula:
d/dx[f(g(x))] = f'(g(x)) * g'(x)

When to use:
When differentiating a function inside another function (composite functions).

Example:
d/dx[sin(x^2)]


# Product Rule

Topic: calculus
Key Pattern: f(x) * g(x)
Formula:
d/dx[uv] = u'v + uv'

When to use:
When differentiating a term consisting of two distinct functions multiplied together.

Example:
d/dx[x^2 * e^x]


# Quotient Rule

Topic: calculus
Key Pattern: f(x) / g(x)
Formula:
d/dx [u/v] = (vu' - uv') / v^2

When to use:
When differentiating a fraction where both numerator and denominator depend on x.

Example:
d/dx [ln(x) / x]


# Logarithmic Differentiation (Variable Base & Power)

Topic: calculus
Key Pattern: u(x)^v(x)
Formula:
dy/dx = y *[ (v(x)/u(x))*u'(x) + ln(u(x))*v'(x) ]

When to use:
When the function has a variable in the base AND the exponent, or when differentiating a massive product/quotient chain.

Example:
d/dx[x^sin(x)]


# Inverse Function Theorem

Topic: calculus
Key Pattern: d/dx(f^-1(x))
Formula:
(f⁻¹)'(x) = 1 / f'( f⁻¹(x) ) OR dy/dx = 1 / (dx/dy)

When to use:
When finding the derivative of an inverse function without explicitly solving for the inverse first, or given relation x = f(y).

Example:
If x = e^y + y, find dy/dx.


# Parametric Differentiation

Topic: calculus
Key Pattern: x=f(t), y=g(t)
Formula:
dy/dx = (dy/dt) / (dx/dt)
d²y/dx² = d/dt(dy/dx) * (dt/dx)

When to use:
When x and y are linked via a third parameter (t or θ). Note the Chain Rule requirement for the second derivative.

Example:
x = 2at, y = at^2


# Differentiation of Determinants

Topic: calculus, matrix
Key Pattern: | matrix(x) |
Formula:
If Δ(x) = | R1 |
          | R2 |
Then Δ'(x) = | R1' | + | R1  |
             | R2  |   | R2' |
(Sum of determinants where one row is differentiated at a time).

When to use:
When the function is defined as a determinant dependent on x.

Example:
d/dx of a 3x3 determinant where elements are functions of x.


# Leibniz Rule (Nth Derivative)

Topic: calculus, series
Key Pattern: d^n/dx^n[u(x)v(x)]
Formula:
(uv)ₙ = uₙv + nC1 uₙ₋₁v₁ + nC2 uₙ₋₂v₂ + ... + uvₙ

When to use:
To find the Nth order derivative of a product of two functions (usually one polynomial and one transcendental).

Example:
Find the 10th derivative of x^2 * sin(x).


# L'Hôpital's Rule

Topic: calculus, limits
Key Pattern: lim(x→a) [f(x) / g(x)] = 0/0 or ±∞/±∞
Formula:
lim(x→a)[f(x) / g(x)] = lim(x→a) [f'(x) / g'(x)]

When to use:
When evaluating a limit results in an indeterminate fraction (0/0 or ∞/∞). Must check the indeterminate form before applying.

Example:
lim(x→0) [sin(x) / x] -> Apply rule -> lim(x→0)[cos(x) / 1] = 1


# 1^∞ Limit Form

Topic: calculus, limits
Key Pattern: lim(x→a)[f(x)]^g(x) where f(x)→1 and g(x)→∞
Formula:
L = e^[ lim(x→a) (f(x) - 1) * g(x) ]

When to use:
When evaluating limits of exponential functions that result in the 1^∞ indeterminate form. 

Example:
lim(x→0) (1 + x)^(1/x) = e^[ lim(x→0) (1 + x - 1) * (1/x) ] = e^1 = e


# Limit Definition of the Derivative (First Principles)

Topic: calculus, derivatives
Key Pattern: f'(x)
Formula:
f'(x) = lim(h→0)[f(x + h) - f(x)] / h

When to use:
When a problem explicitly asks to find the derivative "by first principles" or when standard derivative rules do not apply (e.g., piecewise functions at the boundary).

Example:
f'(x) for x^2 is lim(h→0)[(x+h)^2 - x^2] / h


# Implicit Differentiation

Topic: calculus, derivatives
Key Pattern: F(x, y) = 0
Formula:
d/dx [f(y)] = f'(y) * (dy/dx)
Shortcut: dy/dx = - (∂F/∂x) / (∂F/∂y)

When to use:
When x and y are mixed together in an equation and it is difficult or impossible to isolate y explicitly. 

Example:
x^2 + y^2 = 25


# First Derivative Test (Critical Points)

Topic: calculus, simple_optimization
Key Pattern: f'(x) = 0 or f'(x) is undefined
Formula:
Set f'(x) = 0 to find critical points (c).
If f'(x) changes from + to - at c, it's a Local Maximum.
If f'(x) changes from - to + at c, it's a Local Minimum.

When to use:
When finding the local extrema (minimums or maximums) or intervals of increase/decrease for a function.

Example:
Find where f(x) = x^2 - 4x reaches a minimum.


# Second Derivative Test (Concavity & Extrema)

Topic: calculus, simple_optimization
Key Pattern: f''(c) where f'(c) = 0
Formula:
If f''(c) > 0, the curve is concave up → Local Minimum.
If f''(c) < 0, the curve is concave down → Local Maximum.
If f''(c) = 0, the test is inconclusive (use First Derivative Test).

When to use:
When confirming if a critical point is a maximum or minimum, or when finding inflection points (where f''(x) = 0).

Example:
Check if the critical point x = 2 in f(x) = x^2 - 4x is a min or max.


# Global Extrema (Closed Interval Method)

Topic: calculus, simple_optimization
Key Pattern: Max/Min of f(x) on [a, b]
Formula:
1. Find critical points c in (a, b).
2. Evaluate f(c) for all critical points.
3. Evaluate f(a) and f(b) (endpoints).
4. The largest value is the Absolute Max; the smallest is the Absolute Min.

When to use:
When optimizing a continuous function over a strictly bounded interval.

Example:
Find the absolute maximum of f(x) = x^3 - 3x on[-2, 3].


# Taylor Series

Topic: calculus, series
Key Pattern: f(x) expansion near a point

Formula:
Taylor expansion about x = a:

f(x) = f(a)

f'(a)(x−a)

f''(a)(x−a)² / 2!

f'''(a)(x−a)³ / 3! + ...

When to use:
When approximating functions or evaluating difficult limits.

Example:
Approximate e^x near x=0.


# Maclaurin Series

Topic: calculus, series
Key Pattern: f(x) expansion near x = 0
Formula:
Maclaurin is Taylor at a = 0: f(x) = Σ f⁽ⁿ⁾(0)/n! * xⁿ
Common expansions:
e^x = 1 + x + x²/2! + x³/3! + ...
sin x = x − x³/3! + x⁵/5! − ...
cos x = 1 − x²/2! + x⁴/4! − ...
ln(1+x) = x − x²/2 + x³/3 − ...

When to use:
For evaluating limits and approximations near x = 0.

Example:
lim x→0 (sin x − x)/x³ → substitute sin x ≈ x − x³/6, giving limit = −1/6.

# Rolle's Theorem

Topic: calculus, mean_value_theorems
Key Pattern: f(a) = f(b) on [a, b]
Formula:
If f(x) is continuous on [a, b], differentiable on (a, b), and f(a) = f(b),
then ∃ c ∈ (a, b) such that f'(c) = 0.

When to use:
When a function starts and ends at the same value and you need to prove the existence of a horizontal tangent between those points.

Example:
Verify Rolle's theorem for f(x) = x² − 4x + 3 on [1, 3]. f(1) = f(3) = 0, f'(x) = 2x − 4 = 0 → c = 2 ∈ (1, 3). ✓

# Mean Value Theorem (MVT)

Topic: calculus, mean_value_theorems
Key Pattern: Average rate of change over [a, b]
Formula:
If f(x) is continuous on [a, b] and differentiable on (a, b),
then ∃ c ∈ (a, b) such that f'(c) = (f(b) − f(a)) / (b − a).

When to use:
When you need to prove the existence of a point where the instantaneous slope equals the average slope over an interval.

Example:
Verify MVT for f(x) = x² on [1, 3]. Average slope = (9−1)/(3−1) = 4. f'(x) = 2x = 4 → c = 2 ∈ (1, 3). ✓

# Definite Integral

Topic: calculus, integration
Key Pattern: ∫_a^b f(x) dx
Formula:
∫_a^b f(x) dx = F(b) − F(a), where F'(x) = f(x).

When to use:
When computing the net area under a curve between two bounds.

Example:
Evaluate ∫₀² x² dx = [x³/3]₀² = 8/3 − 0 = 8/3.

# Integration by Parts

Topic: calculus, integration
Key Pattern: ∫ u(x) * v(x) dx (product of two functions)
Formula:
∫ u dv = uv − ∫ v du
Choose u using ILATE priority: Inverse trig > Logarithmic > Algebraic > Trigonometric > Exponential.

When to use:
When integrating a product of two functions where substitution does not simplify the integral.

Example:
Evaluate ∫ x e^x dx. Let u = x, dv = e^x dx → du = dx, v = e^x. Answer: x e^x − e^x + C.


# Integration by Substitution

Topic: calculus, integration

Formula:

If x = g(t)

∫ f(g(t)) g'(t) dt = ∫ f(x) dx

When to use:
When the integrand contains a function along with its derivative.

Example:
Evaluate ∫ 2x cos(x²) dx.