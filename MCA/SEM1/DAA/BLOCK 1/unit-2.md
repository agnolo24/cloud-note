
**2.0 Introduction & 2.1 Objectives**

In algorithm analysis, knowing computational complexity allows us to determine how long an algorithm will run, how much memory it requires, and whether a problem is practically solvable. Asymptotic behavior focuses on the growth rate of a function $f(n)$ as input size $n \to \infty$, ignoring small values of $n$.

---

**2.2 Useful Mathematical Functions & Notations**

**2.2.1 Summation & Product**

1. **Summation (**$\sum$**):** Sum of arithmetic sequences:
    - **Sum of first** $n$ **positive integers**:$$\sum_{i=1}^{n} i = 1 + 2 + \dots + n = \frac{n(n+1)}{2}$$
    - **Sum of squares**:$$\sum_{i=1}^{n} i^2 = 1^2 + 2^2 + \dots + n^2 = \frac{n(n+1)(2n+1)}{6}$$
    - **Sum of cubes**: $$\sum_{i=1}^{n} i^3 = 1^3 + 2^3 + \dots + n^3 = \left[\frac{n(n+1)}{2}\right]^2$$
2. **Product (**$\prod$**):** Shorthand representation for products: $$\prod_{i=1}^{n} i = 1 \times 2 \times \dots \times n = n!$$

**2.2.2 Functions: Floor & Ceiling**

For any real number $x$, floor $\lfloor x \rfloor$ rounds down to the nearest integer, and ceiling $\lceil x \rceil$ rounds up to the nearest integer: $$x - 1 < \lfloor x \rfloor \le x \le \lceil x \rceil < x + 1$$

**2.2.3 Logarithms & Modular Arithmetic**

- **Logarithm Rules**:
    1. $\log_a (bc) = \log_a b + \log_a c$
    2. $\log_a (b^n) = n \log_a b$
    3. $\log_b a = \frac{1}{\log_a b}$
    4. $\log_a (1/b) = -\log_a b$
    5. $a^{\log_b c} = c^{\log_b a}$
- **Modular Arithmetic (**$b \bmod n$**)**:For integer dividend $b$ and positive divisor $n$, $b \bmod n = r$ where $0 \le r < n$ such that $b = k \cdot n + r$.
    - **Example 1:** $42 \bmod 11 = 9$ (since $42 = 3 \times 11 + 9$).
    - **Example 2:** $-42 \bmod 11 = 2$ (since $-42 = (-4) \times 11 + 2$).

---

**2.3 Mathematical Expectation**

In average-case analysis, mathematical expectation calculates the expected value $E(v)$ over probabilistic inputs: $$E(v) = \sum_{i=1}^{n} p_i v_i = p_1 v_1 + p_2 v_2 + \dots + p_n v_n$$ where $v_i$ is the value and $p_i$ is its probability of occurrence.

- **Textbook Example (MCA Student Marks):
    - $0\% - 20\%$ (midpoint 10): $8\%$ students $\to 10 \times 0.08 = 0.8$
    - $20\% - 40\%$ (midpoint 30): $20\%$ students $\to 30 \times 0.20 = 6.0$
    - $40\% - 60\%$ (midpoint 50): $40\%$ students $\to 50 \times 0.40 = 20.0$
    - $60\% - 80\%$ (midpoint 70): $20\%$ students $\to 70 \times 0.20 = 14.0$
    - $80\% - 100\%$ (midpoint 90): $12\%$ students $\to 90 \times 0.12 = 10.8$
    - **Expected Marks** $E = 0.8 + 6.0 + 20.0 + 14.0 + 10.8 = 47\%$

---

**2.4 Principle of Mathematical Induction**

Used to prove mathematical statements for all natural numbers $n$ using three steps:

1. **Induction Base:** Prove statement is true for initial value $n = 1$ (or starting base value).
2. **Induction Hypothesis:** Assume statement holds true for $n = k$ ($k \ge 1$).
3. **Induction Step:** Prove statement holds true for $n = k + 1$ using the hypothesis.

**Worked Example: Prove** $\sum_{i=1}^n i = \frac{n(n+1)}{2}$

1. **Base Step (**$n=1$**):** L.H.S $= 1$, R.H.S $= \frac{1(1+1)}{2} = 1$. True.
2. **Hypothesis:** Assume $1 + 2 + \dots + k = \frac{k(k+1)}{2}$.
3. **Induction Step (**$n=k+1$**):** $$1 + 2 + \dots + k + (k+1) = \frac{k(k+1)}{2} + (k+1) = (k+1)\left[\frac{k}{2} + 1\right] = \frac{(k+1)(k+2)}{2}$$ Hence proved for all $n \ge 1$.

---

**Check Your Progress 1 (Fully Solved)**

- **Q1: Prove** $1^2 + 2^2 + \dots + n^2 = \frac{n(n+1)(2n+1)}{6}$
    - **Base Step (**$n=1$**):** $1^2 = 1$; R.H.S $= \frac{1(1+1)(2(1)+1)}{6} = \frac{6}{6} = 1$. True.
    - **Hypothesis:** Assume $1^2 + 2^2 + \dots + k^2 = \frac{k(k+1)(2k+1)}{6}$.
    - **Induction Step (**$n=k+1$**):** $$1^2 + 2^2 + \dots + k^2 + (k+1)^2 = \frac{k(k+1)(2k+1)}{6} + (k+1)^2$$ $$= \frac{(k+1)[k(2k+1) + 6(k+1)]}{6} = \frac{(k+1)(2k^2 + 7k + 6)}{6} = \frac{(k+1)(k+2)(2k+3)}{6}$$ Which matches $\frac{(k+1)[(k+1)+1][2(k+1)+1]}{6}$. Hence proved.
- **Q2: Prove** $2^0 + 2^1 + 2^2 + \dots + 2^n = 2^{n+1} - 1$
    - **Base Step (**$n=0$**):** $2^0 = 1$; R.H.S $= 2^{0+1} - 1 = 1$. True.
    - **Hypothesis:** Assume $\sum_{i=0}^k 2^i = 2^{k+1} - 1$.
    - **Induction Step (**$n=k+1$**):** $$\sum_{i=0}^{k+1} 2^i = (2^{k+1} - 1) + 2^{k+1} = 2 \cdot 2^{k+1} - 1 = 2^{(k+1)+1} - 1$$ Hence proved.

---

**2.5 & 2.6 Asymptotic Analysis & Notations**

Asymptotic notations characterize the growth rate of running time functions for large $n$:

1. **Big-**$O$ **Notation (Upper Bound)**17**:** $f(n) = O(g(n))$ if there exist positive constants $c$ and $n_0$ such that: $$f(n) \le c \cdot g(n) \quad \text{for all } n \ge n_0$$
    - **Worked Proof 1:** Show $3n^2 + 4n - 2 = O(n^2)$: $$3n^2 + 4n - 2 \le 3n^2 + 4n^2 = 7n^2$$ Taking $c = 6$ (or $c \ge 5$) and $n_0 = 1$, $3n^2 + 4n - 2 \le 6n^2$ holds for all $n \ge 1$. Thus $3n^2 + 4n - 2 = O(n^2)$.
    - **Worked Proof 2:** Disprove $n^3 = O(n^2)$: If $n^3 \le c \cdot n^2$, dividing by $n^2$ gives $n \le c$ for all $n \ge n_0$, which is impossible as $n \to \infty$.
2. **Big-**$\Omega$ **Notation (Lower Bound):$f(n) = \Omega(g(n))$ if there exist positive constants $c$ and $n_0$ such that: $$f(n) \ge c \cdot g(n) \quad \text{for all } n \ge n_0$$
3. **Big-**$\Theta$ **Notation (Tight Bound): $f(n) = \Theta(g(n))$ if there exist positive constants $c_1, c_2$ and $n_0$ such that: $$0 \le c_1 g(n) \le f(n) \le c_2 g(n) \quad \text{for all } n \ge n_0$$
    - **Theorem:** $f(n) = \Theta(g(n))$ if and only if $f(n) = O(g(n))$ and $f(n) = \Omega(g(n))$.

**Polynomial Degree Theorems**

For any polynomial $f(n) = a_m n^m + a_{m-1} n^{m-1} + \dots + a_1 n + a_0$ with $a_m > 0$:

- **Theorem 1:** $f(n) = O(n^m)$
- **Theorem 2:** $f(n) = \Omega(n^m)$
- **Theorem 3:** $f(n) = \Theta(n^m)$

---

**Check Your Progress 2 (Complete Solved Solutions)**

- **a)** $4n^2 + 7n + 12 = O(n^2)$
    - **Proof:** $4n^2 + 7n + 12 \le 5n^2$ holds for $c = 5$ and $n \ge 9$. **True**.
- **b)** $\log n + \log(\log n) = O(\log n)$
    - **Proof:** $\log n + \log(\log n) \le 2 \log n$ holds for $c = 2$ and $n \ge 2$ (since $1 + 0 \le 2$). **True**.
- **c)** $3n^2 + 7n - 5 = \Theta(n^2)$
    - **Proof:** $1 \cdot n^2 \le 3n^2 + 7n - 5 \le 10 \cdot n^2$ holds simultaneously for $c_1 = 1, c_2 = 10, n \ge 2$. **True**.
- **d)** $2^{n+1} = O(2^n)$
    - **Proof:** $2^{n+1} = 2 \cdot 2^n \le c \cdot 2^n$ holds for $c = 2$. **True**.
- **e)** $2^{2n} = O(2^n)$
    - **Proof:** $2^{2n} = 4^n \le c \cdot 2^n \implies 2^n \le c$, impossible as $n \to \infty$. **False** ($2^{2n} \neq O(2^n)$).
- **f) Does** $f(n) = O(g(n))$ **imply** $g(n) = O(f(n))$**?**
    - **Proof:** No. Counterexample: $n = O(n^2)$ is true, but $n^2 \neq O(n)$. **False**.
- **g)** $\max\{f(n), g(n)\} = \Theta(f(n) + g(n))$
    - **Proof:** $\frac{1}{2}(f(n) + g(n)) \le \max\{f(n), g(n)\} \le 1 \cdot (f(n) + g(n))$ holds for $c_1 = \frac{1}{2}, c_2 = 1$. **True**.
- **h) Does** $f(n) = O(g(n))$ **imply** $2^{f(n)} = O(2^{g(n)})$**?**
    - **Proof:** No. Counterexample: Let $f(n) = 2n, g(n) = n$. $2n = O(n)$ is true, but $2^{2n} = 4^n \neq O(2^n)$. **False**.
- **i)** $f(n) + g(n) = \Theta(\min\{f(n), g(n)\})$
    - **Proof:** No. Counterexample: $f(n) = 2n, g(n) = n^2 \implies (2n + n^2) \neq \Theta(n)$. **False**.
- **j)** $33n^2 + 4n = \Omega(n^3)$
    - **Proof:** $33n^2 + 4n \ge c \cdot n^3 \implies \frac{33}{n} + \frac{4}{n^2} \ge c$, impossible as $n \to \infty$. **False**.
- **k)** $f(n) + g(n) = O(n^2)$ **where** $f(n) = 2n^2 - 3n + 5$ **and** $g(n) = n \log n + 10$
    - **Proof:** $h(n) = f(n) + g(n) = 2n^2 + n \log n - 3n + 15 \le 4n^2$ holds for $c = 4, n_0 \ge 4$. **True**.