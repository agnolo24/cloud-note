**4.0 Introduction & 4.1 Objectives**

The complexity analysis of iterative algorithms is generally straightforward, whereas recursive algorithms require setting up a **recurrence relation** (or recurrence equation)1. Once a recurrence equation is defined, asymptotic bounds ($\Theta, O$) can be obtained using specific mathematical techniques.

**Objectives**

- **Define** recurrence relations.
- **Construct** recurrence relations for simple recursive algorithms.
- **List and apply** the three primary techniques for solving recurrence relations:
    1. **Substitution Method**
    2. **Recursion Tree Method**
    3. **Master Method**

---

**4.2 Recurrence Relation**

A **recurrence relation** describes the running time of a recursive algorithm by expressing the function value for an input size $n$ in terms of its value on smaller subproblems.

Like all recursive definitions, every recurrence relation consists of two mandatory parts:

1. **Initial Condition(s) / Base Case(s):** One or more fixed conditions where recursion terminates without calling itself.
2. **Recursive Step:** An equation specifying how larger terms are derived from preceding smaller terms.

---

**Introductory Examples**

**Example 1: Fibonacci Sequence**

The sequence $f_0, f_1, f_2, \dots$ is defined as: $$f_n = \begin{cases} 0 & \text{if } n = 0 \\ 1 & \text{if } n = 1 \\ f_{n-1} + f_{n-2} & \text{if } n \ge 2 \end{cases}$$

- **Base Step:** $f_0 = 0$, $f_1 = 1$.
- **Recursive Step:** $f_2 = f_1 + f_0 = 1 + 0 = 1$; $f_3 = f_2 + f_1 = 1 + 1 = 2$; $f_4 = 2 + 1 = 3$.

**Example 2: Factorial Function (**$n!$**)**

```
int fact(int n) {
    if (n == 0) return 1;
    else return n * fact(n - 1);
}
```

- Let $T(n)$ be the number of multiplications required:
    - For $n = 0$: $0$ multiplications $\implies T(0) = 0$ (or $1$ basic return operation).
    - For $n > 1$: $1$ multiplication plus a recursive call on $(n-1)$.
- **Recurrence Relation**8: $$T(n) = \begin{cases} 1 & \text{if } n = 0 \\ 1 + T(n-1) & \text{if } n > 0 \end{cases}$$

**Example 3: Power Function (**$x^n$**)**

```
Algorithm Power(x, n)
1: if (n == 0) return 1
2: if (n == 1) return x
3: else return x * Power(x, n - 1)
```

- **Base Case:** At $n = 0$ or $n = 1$, one comparison and one return take constant time $a$.
- **Recursive Step:** For $n > 1$, one recursive call on $(n-1)$ plus basic constant operations $b$: $$T(n) = \begin{cases} a & \text{if } n = 0 \text{ or } 1 \quad \text{(Base case)} \\ T(n-1) + b & \text{if } n > 1 \quad \text{(Recursive step)} \end{cases}$$

**Example 4: Compound Interest Formulation**

- An investment of Rs. 5000 at 15% annual compound interest.
- Let $T_n$ denote the amount at the end of year $n$: $$T_n = T_{n-1} + 0.15 T_{n-1} = 1.15 T_{n-1} \quad (n \ge 1)$$ with base value $T_0 = 5000$.
- Expanding for $n$ years: $$T_n = (1.15)^n \cdot 5000$$

---

**4.3 Methods for Solving Recurrence Relations**

---

**4.3.1 Substitution Method**

The substitution method is the reverse of mathematical induction: we start with $n$ and work backward. It consists of two steps:

1. **Step 1:** Guess the form of the asymptotic bound.
2. **Step 2:** Use **Mathematical Induction** to establish whether the guess is correct and find the constants.

**Worked Example: Solve** $T(n) = 2T(\lfloor n/2 \rfloor) + n$

- **Step 1 (Guess):** Since the recurrence matches Merge Sort, guess $T(n) \le c \cdot n \log_2 n$ (i.e., $O(n \log n)$).
- **Step 2 (Induction Base):**
    - For $n = 1$, $c \cdot 1 \log 1 = 0$, which contradicts $T(1) = 1$.
    - For $n = 2$: $T(2) = 2T(1) + 2 = 2(1) + 2 = 4$.
    - Bound: $c \cdot 2 \log_2 2 = 2c$. The inequality $4 \le 2c$ holds for all $c \ge 2$.
- **Step 3 (Inductive Step):** Assume the bound holds for $\lfloor n/2 \rfloor$, i.e., $T(\lfloor n/2 \rfloor) \le c \lfloor n/2 \rfloor \log_2 \lfloor n/2 \rfloor$: $$T(n) \le 2\left(c \frac{n}{2} \log_2 \frac{n}{2}\right) + n$$ $$T(n) \le c n (\log_2 n - \log_2 2) + n$$ $$T(n) \le c n \log_2 n - c n + n$$ $$T(n) \le c n \log_2 n - (c - 1)n$$ For any $c \ge 1$, $-(c - 1)n \le 0$: $$T(n) \le c n \log_2 n$$
- **Conclusion:** $T(n) = O(n \log n)$.

**Remark:** Making a good initial guess requires experience, so the substitution method is less commonly used as a primary constructive tool.

---

**4.3.2 Recursion Tree Method**

A **recursion tree** is a visual representation showing how a recurrence is broken down across levels until reaching the boundary conditions.

It is particularly suitable for divide-and-conquer recurrences of the form: $$T(n) = a T\left(\frac{n}{b}\right) + f(n) \quad (a \ge 1, b > 1)$$

**Procedure for Solving with a Recursion Tree**

1. **Root Node:** Place $f(n)$ at the root with $a$ child nodes, each of size $T(n/b)$.
2. **Expand Levels:** Replace each subproblem node with its non-recursive cost $f(n/b)$ and branch into its subproblems.
3. **Row-Sum (Per-Level Cost):** Calculate the sum of costs of all nodes at that level.
4. **Column-Sum (Total Cost):** Sum the costs across all levels from the root down to the leaf level: $$\text{Total Cost} = \sum_{i=0}^{k} (\text{cost at level } i)$$

```
               f(n)                    <--- Level 0 Cost = f(n)
             /   |  \
        f(n/b) f(n/b) f(n/b) ...       <--- Level 1 Cost = a * f(n/b) (Row-Sum)
        /  \   /  \   /  \
      ...  ... ... ... ... ...
     T(1) T(1) T(1) T(1) T(1) T(1)     <--- Leaf Level Cost (Total Leaves * T(1))
     |---------------------------|
           Total Column-Sum = T(n)
```

---

**Example 1: Solve** $T(n) = 2T(n/2) + n$

- **Level 0 (Root):** Cost $= n$.
- **Level 1:** $2$ nodes of size $n/2 \implies \frac{n}{2} + \frac{n}{2} = n$.
- **Level 2:** $4$ nodes of size $n/4 \implies 4 \times \frac{n}{4} = n$.
- **Tree Height (**$k$**):** The problem size shrinks as $n \to \frac{n}{2} \to \frac{n}{2^2} \dots \to \frac{n}{2^k} = 1 \implies k = \log_2 n$.
- **Total Cost:** $$T(n) = \sum_{i=0}^{\log_2 n} n = n \log_2 n \implies \mathbf{\Theta(n \log_2 n)}$$

---

**Example 2: Solve** $T(n) = T(n/3) + T(2n/3) + n$

- **Level 0:** Cost $= n$.
- **Level 1:** Children have costs $\frac{n}{3}$ and $\frac{2n}{3}$. Row cost $= \frac{n}{3} + \frac{2n}{3} = n$.
- **Level 2:** Children have costs $\frac{n}{9}, \frac{2n}{9}, \frac{2n}{9}, \frac{4n}{9}$. Row cost $= n$.
- **Path Lengths to Leaves:**
    - **Shortest path:** $n \to \frac{n}{3} \dots \implies (n/3)^k = 1 \implies \text{height} = \log_3 n$.
    - **Longest path:** $n \to \frac{2n}{3} \dots \implies \left(\frac{2}{3}\right)^k n = 1 \implies \text{height} = \log_{3/2} n$.
- **Bounds:**
    - Upper bound: $T(n) \le n \log_{3/2} n = O(n \log_2 n)$.
    - Lower bound: $T(n) \ge n \log_3 n = \Omega(n \log_2 n)$.
- **Conclusion:** Since $T(n) = O(n \log n)$ and $T(n) = \Omega(n \log n)$, $T(n) = \Theta(n \log_2 n)$.

---

**Example 3: Tower of Hanoi** $T(n) = 2T(n-1) + 1$ **with** $T(1) = 1$

- **Level 0:** Cost $= 1 = 2^0$.
- **Level 1:** $2$ nodes each of cost $1 \implies 2^1$.
- **Level 2:** $4$ nodes each of cost $1 \implies 2^2$.
- **Height:** Subproblem size decreases by $1$ at each step ($n \to n-1 \to \dots \to 1$), giving height $= n - 1$.
- **Total Cost (Geometric Series):** $$T(n) = 1 + 2^1 + 2^2 + \dots + 2^{n-1} = \frac{1(2^n - 1)}{2 - 1} = 2^n - 1$$
- **Conclusion:** $T(n) = \Theta(2^n)$.

---

**4.3.3 Master Method**

The Master Method provides a direct formula to solve divide-and-conquer recurrences of the form: $$T(n) = a T\left(\frac{n}{b}\right) + f(n)$$ where $a \ge 1$ and $b > 1$ are constants, and $f(n)$ is an asymptotically positive function.

To find the solution, compare $f(n)$ with the watershed term $n^{\log_b a}$:

| Case       | Condition                                                                                                                     | Dominant Factor                       | Solution $T(n)$                      |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- | ------------------------------------ |
| **Case 1** | $f(n) = O(n^{\log_b a - \epsilon})$ for some constant $\epsilon > 0$                                                          | $n^{\log_b a}$ is polynomially larger | $T(n) = \Theta(n^{\log_b a})$        |
| **Case 2** | $f(n) = \Theta(n^{\log_b a})$                                                                                                 | Both grow at the same rate            | $T(n) = \Theta(n^{\log_b a} \log n)$ |
| **Case 3** | $f(n) = \Omega(n^{\log_b a + \epsilon})$ for some constant $\epsilon > 0$, **and** $a f(n/b) \le c f(n)$ for constant $c < 1$ | $f(n)$ is polynomially larger29       | $T(n) = \Theta(f(n))$                |

---

**Master Method Solved Examples**

- **Example 1:** $T(n) = 9T(n/3) + n$
    - $a = 9$, $b = 3$, $f(n) = n$.
    - Compute: $n^{\log_b a} = n^{\log_3 9} = n^2$.
    - Compare: $f(n) = n = O(n^{2 - 1})$ with $\epsilon = 1$.
    - **Result (Case 1):** $T(n) = \Theta(n^2)$.
- **Example 2:** $T(n) = T(2n/3) + 1$
    - $a = 1$, $b = 3/2$, $f(n) = 1$.
    - Compute: $n^{\log_{3/2} 1} = n^0 = 1$.
    - Compare: $f(n) = 1 = \Theta(1)$.
    - **Result (Case 2):** $T(n) = \Theta(n^0 \log n) = \mathbf{\Theta(\log n)}$.

---

**4.5 Solutions to Check Your Progress Questions**

---

**Check Your Progress 1**

**Q1. Write recurrence relations for the following recursive functions:**

- **(a)** **Fast_Power(x, n)**

```
Fast_Power(x, n):
  if (n == 0) return 1;
  elseif (n == 1) return x;
  elseif ((n % 2) == 0) return Fast_Power(x, n/2) * Fast_Power(x, n/2);
  else return x * Fast_Power(x, n/2) * Fast_Power(x, n/2);
```

- **Solution:** At each step, the problem size halves ($n/2$). In the worst case (odd powers), two recursive calls of size $n/2$ are made along with constant arithmetic operations: $$T(n) = \begin{cases} a & \text{if } n = 0 \text{ or } 1 \quad \text{(Base case)} \\ T(n/2) + b & \text{if } n \ge 2 \quad \text{(Recursive step)} \end{cases}$$
- **(b)** **Fibonacci(n)**

```
Fibonacci(n):
  if (n == 0) return 0;
  if (n == 1) return 1;
  return Fibonacci(n-1) + Fibonacci(n-2);
```

- **Solution:** Two recursive calls on $(n-1)$ and $(n-2)$ plus a constant check cost $b$: $$T(n) = \begin{cases} a & \text{if } n = 0 \text{ or } 1 \quad \text{(Base case)} \\ T(n-1) + T(n-2) + b & \text{if } n \ge 2 \quad \text{(Recursive step)} \end{cases}$$

---

**Q2. Solve using the Recursion Tree Method:**

- **(a)** $T(n) = 4T(n/2) + n$
    - **Level 0:** $n$.
    - **Level 1:** $4$ subproblems of size $n/2 \implies 4 \times (n/2) = 2n$.
    - **Level 2:** $16$ subproblems of size $n/4 \implies 16 \times (n/4) = 4n$.
    - **Level** $i$**:** $2^i n$.
    - **Height:** $k = \log_2 n$.
    - **Total Sum:** $$T(n) = n(1 + 2 + 4 + \dots + 2^{\log_2 n}) = n \left[\frac{2^{\log_2 n + 1} - 1}{2 - 1}\right] = n(2n - 1) = 2n^2 - n \implies \mathbf{\Theta(n^2)}$$

---

**Check Your Progress 2**

**Q1. State Case 1 and Case 2 of the Master Method:**

- **Case 1:** If $f(n) = O(n^{\log_b a - \epsilon})$ for some $\epsilon > 0$, then $T(n) = \Theta(n^{\log_b a})$.
- **Case 2:** If $f(n) = \Theta(n^{\log_b a})$, then $T(n) = \Theta(n^{\log_b a} \log n)$.

---

**Q2. Solve using the Master Theorem:**

- **(a)** $T(n) = 4T(n/2) + n$
    - $a = 4, b = 2, f(n) = n$.
    - $n^{\log_b a} = n^{\log_2 4} = n^2$.
    - Since $f(n) = n = O(n^{2 - 1})$ with $\epsilon = 1$, apply **Case 1**: $$\mathbf{T(n) = \Theta(n^2)}$$
- **(b)** $T(n) = 4T(n/2) + n^2$
    - $a = 4, b = 2, f(n) = n^2$.
    - $n^{\log_b a} = n^{\log_2 4} = n^2$.
    - Since $f(n) = n^2 = \Theta(n^2)$, apply **Case 2**: $$\mathbf{T(n) = \Theta(n^2 \log n)}$$