# Example 1

Problem:
Two unbiased dice are thrown. Find the probability that the sum of the numbers appearing is 8, given that both dice show even numbers.

Topics:
probability

Structure:
conditional_probability

Key Insight:
Identify the reduced sample space (Condition B: both dice are even) and the target event (Event A: sum is 8) that exists strictly within that reduced space. Apply P(A | B) = P(A ∩ B) / n(B).

Solution:
Let B = event that both dice show even numbers.
Outcomes for B: (2,2), (2,4), (2,6), (4,2), (4,4), (4,6), (6,2), (6,4), (6,6)
n(B) = 9
Let A = event that the sum is 8.
We need A ∩ B (sum is 8 AND both are even):
Outcomes for A ∩ B: (2,6), (4,4), (6,2)
n(A ∩ B) = 3
By formula: P(A | B) = n(A ∩ B) / n(B)
= 3 / 9
= 1 / 3


# Example 2

Problem:
Bag I contains 3 Red and 4 Black balls. Bag II contains 4 Red and 5 Black balls. One bag is chosen at random and a ball is drawn from it. If the drawn ball is Red, what is the probability that it was drawn from Bag II?

Topics:
probability, 

Structure:
bayes_theorem

Key Insight:
The final event (Red ball is drawn) has already occurred. We are asked for the probability of a specific prior cause (Bag II was chosen). This requires Bayes' Theorem.

Solution:
Let E₁ = Event of choosing Bag I -> P(E₁) = 1/2
Let E₂ = Event of choosing Bag II -> P(E₂) = 1/2
Let A = Event of drawing a Red ball.
P(A | E₁) = probability of Red from Bag I = 3/7
P(A | E₂) = probability of Red from Bag II = 4/9

Apply Bayes' Theorem to find P(E₂ | A):
Numerator = P(E₂) * P(A | E₂) = (1/2) * (4/9) = 2/9
Denominator (Total Probability) =[P(E₁)*P(A|E₁)] + [P(E₂)*P(A|E₂)]
= [(1/2) * (3/7)] + [(1/2) * (4/9)]
= 3/14 + 2/9
= (27 + 28) / 126
= 55 / 126

P(E₂ | A) = Numerator / Denominator
= (2/9) / (55/126)
= (2/9) * (126/55)
= 28 / 55


# Example 3

Problem:
A pair of dice is thrown 4 times. If getting a doublet is considered a success, find the probability of obtaining exactly 2 successes.

Topics:
probability, statistics

Structure:
binomial_distribution

Key Insight:
This is a repeated independent trial scenario (4 throws) with a clear binary outcome (doublet or not doublet). Use the Binomial Probability formula ⁿC_r * p^r * q^(n-r).

Solution:
Total outcomes when throwing a pair of dice = 36.
Doublets = (1,1), (2,2), (3,3), (4,4), (5,5), (6,6) -> 6 outcomes.
Probability of success (p) = 6/36 = 1/6
Probability of failure (q) = 1 - 1/6 = 5/6
Number of trials (n) = 4
Number of desired successes (r) = 2

P(X = 2) = ⁴C₂ * (p)² * (q)²
= 6 * (1/6)² * (5/6)²
= 6 * (1/36) * (25/36)
= 25 / 216


# Example 4

Problem:
A and B take turns rolling a fair six-sided die. The first person to roll a 6 wins. If A rolls first, find the probability that A wins the game.

Topics:
probability, sequences_and_series, 

Structure:
infinite_game_geometric_series

Key Insight:
The game can technically go on infinitely. A can win on the 1st, 3rd, 5th, 7th... roll. Formulate the probability of A winning as an infinite Geometric Progression (GP).

Solution:
Probability of rolling a 6 (success, p) = 1/6
Probability of not rolling a 6 (failure, q) = 5/6

Ways A can win:
1. A wins on 1st turn: probability = p = 1/6
2. A wins on 3rd turn (A fails, B fails, A wins): probability = q * q * p = (5/6)² * (1/6)
3. A wins on 5th turn: probability = q⁴ * p = (5/6)⁴ * (1/6)
... and so on.

Total Probability P(A wins) = (1/6) + (1/6)(5/6)² + (1/6)(5/6)⁴ + ...
This is an infinite GP.
First term (a) = 1/6
Common ratio (r) = (5/6)² = 25/36

Apply infinite GP sum formula: S_∞ = a / (1 - r)
= (1/6) / (1 - 25/36)
= (1/6) / (11/36)
= (1/6) * (36/11)
= 6 / 11


# Example 5

Problem:
If P(A ∪ B) = 3/4 and P(A) = 1/3, find P(B) if A and B are independent events.

Topics:
probability, algebra

Structure:
independent_events_algebra

Key Insight:
Since A and B are independent, substitute P(A ∩ B) with the product P(A) * P(B) inside the Addition Theorem equation, then solve for the unknown P(B).

Solution:
Addition Theorem: P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
Because A and B are independent: P(A ∩ B) = P(A) * P(B)
Substitute into the theorem:
P(A ∪ B) = P(A) + P(B) - P(A)P(B)
3/4 = 1/3 + P(B) - (1/3)P(B)
3/4 - 1/3 = P(B) *[1 - 1/3]
(9 - 4) / 12 = P(B) * (2/3)
5/12 = P(B) * 2/3
P(B) = (5/12) * (3/2)
P(B) = 15 / 24
P(B) = 5 / 8


# Example 6

Problem:
A point is selected at random inside a circle of radius R. What is the probability that the point is closer to the center of the circle than to its boundary?

Topics:
probability, geometry, 

Structure:
geometrical_probability_area

Key Insight:
Because the sample space is continuous (all points in a circle), use areas instead of counting. Find the geometric boundary where a point is equidistant from the center and the edge.

Solution:
Let the distance of the chosen point from the center be 'r'.
Distance to the center = r
Distance to the boundary = R - r
For the point to be closer to the center: r < R - r
2r < R
r < R/2
This means the favorable region is a smaller concentric circle of radius R/2.
Area of total sample space = πR²
Area of favorable region = π(R/2)² = (πR²) / 4
P(Closer to center) = (Favorable Area) / (Total Area)
= [(πR²) / 4] / [πR²]
= 1 / 4


# Example 7

Problem:
A fair coin is tossed repeatedly until a Head appears. Find the expected number of tosses required.

Topics:
probability, sequences_and_series, 

Structure:
expected_value_agp

Key Insight:
Set up a probability distribution for the random variable X (number of tosses). The expectation E(X) forms an Arithmetico-Geometric Progression (AGP) that extends to infinity.

Solution:
Let X be the number of tosses.
P(X = 1) = 1/2 (H)
P(X = 2) = (1/2)² (TH)
P(X = 3) = (1/2)³ (TTH)
General term: P(X = n) = (1/2)ⁿ
Expected Value E(X) = Σ [n * P(X = n)] from n=1 to ∞
E(X) = 1(1/2) + 2(1/2)² + 3(1/2)³ + ...
Let S = 1/2 + 2/4 + 3/8 + 4/16 + ...  (Eq 1)
Multiply by common ratio (1/2):
(1/2)S = 1/4 + 2/8 + 3/16 + ...  (Eq 2)
Subtract Eq 2 from Eq 1 (shift by one term):
S - (1/2)S = 1/2 + (2/4 - 1/4) + (3/8 - 2/8) + ...
(1/2)S = 1/2 + 1/4 + 1/8 + ...
The right side is an infinite GP with a=1/2, r=1/2.
Sum of GP = (1/2) / (1 - 1/2) = 1
(1/2)S = 1
S = 2
Final Answer: The expected number of tosses is 2.


# Example 8

Problem:
There are 4 addressed envelopes and 4 corresponding letters. If the letters are placed randomly into the envelopes, find the probability that exactly 1 letter is placed in the correct envelope.

Topics:
probability, combinatorics, 

Structure:
partial_derangement

Key Insight:
Separate the problem into two distinct independent choices: Pick which 1 letter is correct (Combinations), and force the remaining 3 letters to be completely wrong (Derangements).

Solution:
Total number of ways to place 4 letters in 4 envelopes = 4! = 24.
Step 1: Choose exactly 1 letter to be in the correct envelope.
Number of ways = ⁴C₁ = 4
Step 2: The remaining 3 letters must go to the WRONG envelopes. This is a complete derangement of 3 items (D₃).
Formula: Dₙ = n!(1/0! - 1/1! + 1/2! - 1/3! + ... + (-1)ⁿ/n!)
D₃ = 3! * (1/2! - 1/3!) = 6 * (1/2 - 1/6) = 6 * (2/6) = 2.
(Alternatively, it's a known fact that D₃ = 2).
Total favorable ways = ⁴C₁ * D₃
= 4 * 2 = 8
Probability = Favorable / Total
= 8 / 24
= 1 / 3

# Example 9

Problem:
In a class, 40% of students study Maths, 50% study Science, and 20% study both. A student is selected at random. Find the probability that the student studies (a) at least one of the two subjects, and (b) neither subject.

Topics:
probability

Structure:
addition_theorem_application

Key Insight:
"At least one" directly maps to P(A ∪ B). Apply the Addition Theorem: P(A ∪ B) = P(A) + P(B) - P(A ∩ B). "Neither" is the complement of "at least one", so use P(neither) = 1 - P(A ∪ B).

Solution:
P(M) = 0.4,  P(S) = 0.5,  P(M ∩ S) = 0.2

(a) P(M ∪ S) = P(M) + P(S) - P(M ∩ S)
= 0.4 + 0.5 - 0.2
= 0.7

(b) P(neither) = 1 - P(M ∪ S) = 1 - 0.7 = 0.3


# Example 10

Problem:
A factory has three machines A, B, and C producing 50%, 30%, and 20% of total output respectively. The defect rates are 2%, 3%, and 4%. A randomly selected item is found to be defective. Find the probability that it was produced by machine B.

Topics:
probability

Structure:
law_of_total_probability_and_bayes

Key Insight:
This is a two-part problem. First use the Law of Total Probability to find P(Defective) across all machines. Then apply Bayes' Theorem to reverse-condition: given defective, find the probability it came from B.

Solution:
Let A, B, C = events that the item came from machine A, B, C.
Let D = event that the item is defective.
P(A) = 0.5,  P(B) = 0.3,  P(C) = 0.2
P(D|A) = 0.02,  P(D|B) = 0.03,  P(D|C) = 0.04

Step 1 - Law of Total Probability:
P(D) = P(A)P(D|A) + P(B)P(D|B) + P(C)P(D|C)
= (0.5)(0.02) + (0.3)(0.03) + (0.2)(0.04)
= 0.010 + 0.009 + 0.008
= 0.027

Step 2 - Bayes' Theorem:
P(B|D) = P(B) * P(D|B) / P(D)
= (0.3 * 0.03) / 0.027
= 0.009 / 0.027
= 1/3


# Example 11

Problem:
On average, a call centre receives 4 calls per minute. Using the Poisson distribution, find the probability that in a given minute (a) exactly 2 calls arrive, and (b) at most 1 call arrives.

Topics:
probability, statistics

Structure:
poisson_distribution_application

Key Insight:
Whenever the problem gives an average rate of occurrence (λ) for rare/independent events over a fixed interval (time, area, volume), use the Poisson formula P(X = k) = e^(-λ) λ^k / k!. For "at most" questions, add up P(X = 0) + P(X = 1) + ... up to the required term.

Solution:
λ = 4 (calls per minute)

(a) P(X = 2):
P(X = 2) = e^(-4) * 4² / 2!
= e^(-4) * 16 / 2
= 8 * e^(-4)
≈ 8 * 0.01832
≈ 0.1465

(b) P(X ≤ 1) = P(X = 0) + P(X = 1):
P(X = 0) = e^(-4) * 4⁰ / 0! = e^(-4) ≈ 0.01832
P(X = 1) = e^(-4) * 4¹ / 1! = 4e^(-4) ≈ 0.07326
P(X ≤ 1) ≈ 0.01832 + 0.07326 ≈ 0.0916


# Example 12

Problem:
A discrete random variable X has the following distribution:
X:     1    2    3    4    5
P(X): 0.1  0.2  0.3  0.2  k
Find k, then compute E(X) and Var(X).

Topics:
probability, statistics

Structure:
variance_expected_value_full

Key Insight:
Use the fact that all probabilities must sum to 1 to find k first. Then compute E(X) = Σ x·P(x) and E(X²) = Σ x²·P(x) separately. Finally use the shortcut formula Var(X) = E(X²) - [E(X)]² — never try to compute Var(X) = Σ (x - μ)² P(x) directly as it is far more tedious.

Solution:
Step 1 - Find k:
0.1 + 0.2 + 0.3 + 0.2 + k = 1
0.8 + k = 1  =>  k = 0.2

Step 2 - Compute E(X):
E(X) = 1(0.1) + 2(0.2) + 3(0.3) + 4(0.2) + 5(0.2)
= 0.1 + 0.4 + 0.9 + 0.8 + 1.0
= 3.2

Step 3 - Compute E(X²):
E(X²) = 1²(0.1) + 2²(0.2) + 3²(0.3) + 4²(0.2) + 5²(0.2)
= 0.1 + 0.8 + 2.7 + 3.2 + 5.0
= 11.8

Step 4 - Compute Var(X):
Var(X) = E(X²) - [E(X)]²
= 11.8 - (3.2)²
= 11.8 - 10.24
= 1.56