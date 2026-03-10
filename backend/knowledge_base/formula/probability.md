# Addition Theorem of Probability

Topic: probability
Key Pattern: P(A ∪ B) or "Probability of A or B"
Formula:
P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
For 3 events: 
P(A ∪ B ∪ C) = P(A) + P(B) + P(C) - P(A∩B) - P(B∩C) - P(C∩A) + P(A∩B∩C)

When to use:
When finding the probability of at least one of multiple events occurring. If events are mutually exclusive, P(A ∩ B) = 0.

Example:
Finding the probability of drawing a King OR a Heart from a standard deck of cards.


# Conditional Probability

Topic: probability
Key Pattern: P(A | B) or "Probability of A given B"
Formula:
P(A | B) = P(A ∩ B) / P(B), provided P(B) > 0

When to use:
When evaluating the probability of an event (A) occurring after it is already known that another event (B) has occurred, effectively reducing the sample space to B.

Example:
Probability that the sum of two dice is 8, GIVEN that both dice show even numbers.


# Multiplication Theorem & Independent Events

Topic: probability
Key Pattern: P(A ∩ B)
Formula:
General: P(A ∩ B) = P(A) * P(B | A)
For Independent Events: P(A ∩ B) = P(A) * P(B)

When to use:
When finding the probability of two or more events happening simultaneously or sequentially. Use the independent form if the occurrence of one event doesn't affect the other (e.g., drawing with replacement).

Example:
Drawing two cards one after another WITH replacement and getting two Aces: (4/52) * (4/52).


# Law of Total Probability

Topic: probability, 
Key Pattern: P(A) = Σ P(E_i) * P(A | E_i)
Formula:
P(A) = P(E₁)P(A | E₁) + P(E₂)P(A | E₂) + ... + P(Eₙ)P(A | Eₙ)

When to use:
When a final outcome (Event A) can occur via several distinct, mutually exclusive and exhaustive pathways or initial conditions (E₁, E₂, etc.), and you need the overall probability of A.

Example:
Finding the probability of drawing a red ball when it could be drawn from either Bag 1, Bag 2, or Bag 3.


# Bayes' Theorem (Reverse Probability)

Topic: probability, 
Key Pattern: P(E_i | A)
Formula:
P(E_i | A) = [ P(E_i) * P(A | E_i) ] /[ Σ P(E_k) * P(A | E_k) ]

When to use:
When the final outcome is already known to have happened (Event A), and you need to trace backwards to find the probability that it originated from a specific initial path or cause (E_i).

Example:
A test for a disease is positive (Event A). What is the probability the patient actually has the disease (Path E₁) rather than it being a false positive (Path E₂)?


# Binomial Probability Distribution

Topic: probability, statistics
Key Pattern: n trials, exactly r successes
Formula:
P(X = r) = ⁿC_r * p^r * q^(n-r)
Mean (μ) = np
Variance (σ²) = npq

When to use:
When an experiment consists of a fixed number of independent identical trials (n), each with only two possible outcomes (success p, failure q = 1-p), and you want the probability of exactly 'r' successes.

Example:
A coin is flipped 10 times. Find the probability of getting exactly 6 heads.


# Infinite Geometric Probability Series

Topic: probability, sequences_and_series, 
Key Pattern: Alternating turns, infinite game
Formula:
Sum of infinite GP: S_∞ = a / (1 - r)
Where 'a' is the probability of winning on the first possible turn, and 'r' is the probability of a complete cycle of failures returning the turn to the player.

When to use:
When two or more players take turns in a game that conceptually could go on forever until someone wins (e.g., flipping a coin until someone gets a Head). 

Example:
Player A and B alternately roll a die. The first to roll a 6 wins. Find the probability that Player A wins the game.


# Geometrical Probability

Topic: probability, geometry, 
Key Pattern: Continuous sample space (Length, Area, or Volume)
Formula:
P(E) = (Measure of favorable region) / (Measure of total sample space)

When to use:
When the outcomes are infinite and continuous (e.g., choosing a random point on a line segment, inside a circle, or within a 3D figure) rather than discrete countable events.

Example:
A point is chosen at random inside a circle. Find the probability that it is closer to the center than to the boundary.


# Mathematical Expectation (Expected Value)

Topic: probability, statistics
Key Pattern: E(X) or "Expected number of..."
Formula:
Mean / Expected Value: E(X) = Σ [x_i * P(X = x_i)]
Variance: Var(X) = E(X²) - [E(X)]²

When to use:
When finding the average or long-term expected outcome of a random variable, often requiring the summation of an Arithmetico-Geometric Progression (AGP).

Example:
Find the expected number of coin tosses required to get the first Head.


# Partial Derangements

Topic: probability, combinatorics, 
Key Pattern: Exactly 'r' matches out of 'n' objects
Formula:
Number of ways = ⁿC_r * D_{n-r}
Probability = (ⁿC_r * D_{n-r}) / n!
(where D_k is the derangement of k objects)

When to use:
When a problem specifies that exactly a certain number of objects (r) are in their correct positions, and the rest (n-r) are in the wrong positions.

Example:
Probability that exactly 2 out of 5 letters go into their correct envelopes.


# Permutations

Topic: probability, combinatorics
Key Pattern: Ordered arrangement of r items from n distinct items
Formula:
nPr = n! / (n − r)!

When to use:
When the order of selection matters (e.g., arranging books on a shelf, awarding 1st/2nd/3rd place).

Example:
Number of ways to arrange 3 letters from {A, B, C, D} = 4P3 = 4!/1! = 24.


# Combinations

Topic: probability, combinatorics
Key Pattern: Unordered selection of r items from n distinct items
Formula:
nCr = n! / [r!(n − r)!]

When to use:
When the order of selection does not matter (e.g., choosing a committee, selecting balls from a bag).

Example:
Number of ways to choose 3 students from a class of 10 = 10C3 = 120.


# Random Variable

Topic: probability
Key Pattern: X maps outcomes → real numbers
Formula:
X: Ω → R (function from sample space to real numbers).
Discrete: takes countable values with P(X = xᵢ) = pᵢ where Σpᵢ = 1.
Continuous: described by a probability density function f(x) where ∫f(x)dx = 1.

When to use:
When assigning numerical values to outcomes of a random experiment in order to compute probabilities, expectations, or variances.

Example:
Rolling a die: X = number shown. P(X = k) = 1/6 for k = 1, 2, 3, 4, 5, 6.


# Variance Properties

Topic: probability
Key Pattern: Spread of a distribution
Formula:
Var(X) = E(X²) − [E(X)]²
Var(aX + b) = a² Var(X)
Var(X + Y) = Var(X) + Var(Y) if X and Y are independent.

When to use:
When measuring how spread out the values of a random variable are from its mean, or when transforming random variables linearly.

Example:
If E(X) = 3 and E(X²) = 13, then Var(X) = 13 − 9 = 4, so standard deviation = 2.


# Poisson Approximation

Topic: probability, statistics
Key Pattern: n large, p small, np = λ moderate
Formula:
λ = np
P(X = k) = e^(−λ) * λ^k / k!
Mean = λ, Variance = λ.

When to use:
When approximating Binomial(n, p) where n is very large and p is very small (rare events), making direct binomial calculation impractical.

Example:
A factory produces defective items with probability 0.002. In 1000 items, P(exactly 3 defective) ≈ e^(−2) * 2³ / 3! ≈ 0.180 (λ = 2).