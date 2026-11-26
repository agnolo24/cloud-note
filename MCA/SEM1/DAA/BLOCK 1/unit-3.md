
**3.0 Introduction & 3.1 Objectives**

Computational complexity measures the processing time required by an algorithm to produce a result for an input of size $n$. In practice, we focus primarily on **worst-case time complexity** (Big-$O$ notation), which gives the maximum time guaranteed for any input of size $n$.

By the end of this unit, you will be able to analyze:

- Control structures (loops, conditional statements, nested loops, logarithmic loops).
- **Summation algorithms** (e.g., sum of cubes).
- **Polynomial evaluation** (Brute Force vs. **Horner’s Rule**).
- **Matrix Multiplication** of order $n \times n$.
- **Exponent Evaluation** via **Binary Exponentiation** (Left-to-Right & Right-to-Left).
- **Searching & Sorting** (**Linear Search** and **Bubble Sort** versions).

---

**3.2 A Brief Review of Asymptotic Notations**

Before analyzing code fragments, remember our three primary bounds from Unit 2:

- **Big-**$O$ **(Worst Case / Upper Bound):** Maximum steps required.
- **Big-**$\Omega$ **(Best Case / Lower Bound):** Minimum steps required.
- **Big-**$\Theta$ **(Tight Bound):** Sandwiching upper and lower bounds.

When analyzing simple code in this unit, three general rules apply:

1. Default to **Big-**$O$ worst-case running time.
2. **Ignore low-order terms** (e.g., $3n^2 + 5n \implies O(n^2)$).
3. **Ignore constant coefficients** (e.g., $6n \implies O(n)$).

---

**3.3 Analysis of Control Constructs (Looping & Conditional Rules)**

The running time of any program code fragment is determined by its basic control constructs:

**1. Constant Time** $O(1)$ **— Simple Statements**

Basic assignment statements, arithmetic operations, or single conditions execute in a fixed number of operations independent of input size $n$.

```
int x;
x = x + 5;
x = x - 5;
```

- **Complexity:** $O(1)$.

---

**2. Linear Time** $O(n)$ **— Single Loops**

A single loop where the loop counter is incremented or decremented by a constant step value $c$ runs $n/c$ times.

```
for (int i = 1; i <= n; i += c) {
    // simple statement(s) - O(1)
}
```

or

```
for (int i = n; i > 0; i -= c) {
    // simple statement(s) - O(1)
}
```

- **Complexity:** $O(n)$.

---

**3. Quadratic / Polynomial Time** $O(n^2)$ **— Nested Loops**

When loops are nested inside each other, the total time complexity is the product of the iteration counts of the outer and inner loops.

```
for (int i = 1; i <= n; i += c) {
    for (int j = 1; j <= n; j += c) {
        // simple statement(s)
    }
}
```

- **Outer loop:** Runs $O(n)$ times.
- **Inner loop:** Runs $O(n)$ times for every single outer iteration.
- **Total Complexity:** $O(n) \times O(n) = \mathbf{O(n^2)}$.

---

**4. Logarithmic Time** $O(\log n)$ **— Multiplication/Division Loops**

If the loop index is **multiplied or divided by a constant factor** $c$ (where $c > 1$) in each step, the loop executes $\lfloor \log_c n \rfloor + 1$ times.

```
for (int i = 1; i <= n; i *= c) {
    // simple statement(s)
}
```

or

```
for (int i = n; i > 0; i /= c) {
    // simple statement(s)
}
```

- **Complexity:** $O(\log n)$.

---

**5. Consecutive Loops — Additive Rule**

When two or more independent loops run one after another, their total time is the sum of their individual complexities.

```
for (int i = 1; i <= n; i++) { // Loop 1: O(n)
    // simple statement
}
for (int j = 1; j <= n; j++) { // Loop 2: O(n)
    for (int k = 1; k <= n; k++) { // Inner: O(n^2)
        // simple statement
    }
}
```

- **Total Time:** $T(n) = O(n) + O(n^2) = \mathbf{O(n^2)}$ (since higher order term dominates)


**3.4 Analysis of Simple Algorithms**

To simplify complexity analysis, we adhere to three foundational rules:

1. **Default to Big-**$O$ **Worst-Case:** We evaluate the maximum steps required for any input of size $n$.
2. **Ignore Low-Order Terms:** In polynomial running times, only the term with the highest growth rate is kept (e.g., $3n^2 + 5n \to O(n^2)$).
3. **Ignore Constant Coefficients:** Constant factors are dropped (e.g., $6n \to O(n)$).

---

**3.4.1 A Summation Algorithm (Sum of** $n$ **Cubes)**

To compute the sum of the first $n$ cube numbers $\sum_{i=1}^n i^3 = 1^3 + 2^3 + \dots + n^3$:

**Algorithm / Code:**

```
int sum_of_n_cube(int n) {
    int i, tempresult;
    tempresult = 0;                     // Step 1: O(1)
    for (i = 1; i <= n; i++) {           // Step 2: Loop runs n times
        tempresult = tempresult + i * i * i; // Step 3: O(1) constant work per iteration
    }
    return tempresult;                  // Step 4: O(1)
}
```

**Complexity Analysis:**

- The initial assignment `tempresult = 0` takes constant time $O(1)$.
- The `for` loop executes $n$ iterations2. Inside the loop, computing `i * i * i` (2 multiplications), 1 addition, and 1 assignment takes a constant amount of time $O(1)$.
- Total loop execution time $= n \times O(1) = O(n)$.
- The `return` statement takes constant time $O(1)$.
- **Total Time Complexity:** $T(n) = O(1) + O(n) + O(1) = \mathbf{O(n)}$.

---

**3.4.2 Polynomial Evaluation Algorithm**

A general polynomial of degree $n$ is expressed as: $$P(x) = a_n x^n + a_{n-1} x^{n-1} + a_{n-2} x^{n-2} + \dots + a_1 x^1 + a_0 x^0$$ where $a_0, a_1, \dots, a_n$ are coefficients and $x$ is the evaluation point.

In C programming, a polynomial term is represented using a structure:

```
struct polynomial {
    int coefficient;
    int exponent;
};
```

---

**Method 1: Brute Force Approach**

Each term is evaluated independently one by one: $$P(x) = a_n \cdot \underbrace{x \cdot x \cdots x}_{n \text{ times}} + a_{n-1} \cdot \underbrace{x \cdot x \cdots x}_{n-1 \text{ times}} + \dots + a_1 \cdot x + a_0$$

- **Multiplication Count:**
    - Term 1 ($a_n x^n$): requires $n$ multiplications.
    - Term 2 ($a_{n-1} x^{n-1}$): requires $n-1$ multiplications.
    - Term 3 ($a_{n-2} x^{n-2}$): requires $n-2$ multiplications.
    - Last terms ($a_1 x$ and $a_0$): require $1$ and $0$ multiplications respectively.
- **Total Multiplications (Worst Case):** $$T(n) = n + (n-1) + (n-2) + \dots + 2 + 1 = \frac{n(n+1)}{2} = \mathbf{O(n^2)}$$

---

**Method 2: Horner's Rule (Horner's Method)**

Horner's Rule parenthesizes the polynomial to factor out $x$ at each step: $$P(x) = (\dots(((a_n \cdot x + a_{n-1}) \cdot x + a_{n-2}) \cdot x + \dots + a_1) \cdot x + a_0$$

- **Multiplication Count:**
    - Every term requires **exactly 1 multiplication**.
- **Total Multiplications (Worst Case):** $$T(n) = \sum_{i=1}^n 1 = n \implies \mathbf{O(n)}$$

**Pseudocode for Horner's Rule:**

```
Algorithm Evaluate_Horner(A, n, x)
/* Input: Array A[0..n] of coefficients of degree n polynomial, evaluation point x
   Output: Value of polynomial at point x */

p = A[n];                       // Step 1: Initialize with leading coefficient
for i = n-1 down to 0 do        // Step 2: Loop n times
    p = p * x + A[i];           // 1 multiplication + 1 addition per pass
return p;                       // Step 3: Return result
```

- **Multiplication Count:** Exactly $1$ multiplication per loop iteration.
- **Total Multiplications:** $T(n) = \sum_{i=1}^n 1 = n \implies \mathbf{O(n)}$.


**3.4.3 Matrix Multiplication (Order** $n \times n$**)**

Multiplying two $n \times n$ matrices $A$ and $B$ to produce matrix $C$:

```
for (i = 0; i < n; i++) {                 // Outer loop: n iterations
    for (j = 0; j < n; j++) {             // Middle loop: n iterations
        c[i][j] = 0;
        for (k = 0; k < n; k++) {         // Inner loop: n iterations
            c[i][j] = c[i][j] + a[i][k] * b[k][j]; // 1 multiplication + 1 addition
        }
    }
}
```

- **Complexity Analysis:** Three nested loops, each running $n$ times.
- **Total Time Complexity:** $n \times n \times n = \mathbf{O(n^3)}$.

---

**3.4.4 Exponent Evaluation (Binary Exponentiation)**

To compute $a^n$, brute-force multiplication takes $n-1$ multiplications ($O(n)$). **Binary Exponentiation** converts $n$ into binary representation of length $s = \lfloor \log_2 n \rfloor + 1$ bits, reducing complexity to $O(\log_2 n)$

**1. Left-to-Right Binary Exponentiation**

Processes exponent bits from Most Significant Bit (MSB) to Least Significant Bit (LSB).

```
Algorithm Left_To_Right_Exponentiation(A, s, a)
result = a;
for i = s-2 down to 0 do
    result = result * result;         // Square current value
    if A[i] == 1 then
        result = result * a;          // Multiply by base a if bit is 1
return result;
```

**2. Right-to-Left Binary Exponentiation**

Processes exponent bits from LSB to MSB.

```
Algorithm Right_To_Left_Exponentiation(A, s, a)
x = a;
if A == 1 then result = a else result = 1;
for i = 1 to s-1 do
    x = x * x;                        // Square base power
    if A[i] == 1 then
        result = result * x;          // Accumulate if bit is 1
return result;
```

---

**Worked Trace Problem (Check Your Progress 3, Q1): Trace** $a^{283}$

Exponent $n = 283 = 100011011_2$, binary length $s = 9$ bits.

- **Left-to-Right Trace (**$a^{283}$**):**

| Iteration | Bit Index ($i$) | Bit Value ($A[i]$) | Operation & `result` State        |
| --------- | --------------- | ------------------ | --------------------------------- |
| **Init**  | $8$             | $1$                | `result` $= a$                    |
| **1**     | $7$             | $0$                | $(a)^2 =$ $a^2$                   |
| **2**     | $6$             | $0$                | $(a^2)^2 =$ $a^4$                 |
| **3**     | $5$             | $0$                | $(a^4)^2 =$ $a^8$                 |
| **4**     | $4$             | $1$                | $(a^8)^2 \cdot a =$ $a^{17}$      |
| **5**     | $3$             | $1$                | $(a^{17})^2 \cdot a =$ $a^{35}$   |
| **6**     | $2$             | $0$                | $(a^{35})^2 =$ $a^{70}$           |
| **7**     | $1$             | $1$                | $(a^{70})^2 \cdot a =$ $a^{141}$  |
| **8**     | $0$             | $1$                | $(a^{141})^2 \cdot a =$ $a^{283}$ |

- **Right-to-Left Trace (**$a^{283}$**):**

| Iteration | Bit Index ($i$) | Bit Value ($A[i]$) | Power ($x$) | Accumulated `result`               |
| --------- | --------------- | ------------------ | ----------- | ---------------------------------- |
| **Init**  | $0$             | $1$                | $a$         | `result` $= a$                     |
| **1**     | $1$             | $1$                | $a^2$       | $a \cdot a^2 =$ $a^3$              |
| **2**     | $2$             | $0$                | $a^4$       | $a^3$                              |
| **3**     | $3$             | $1$                | $a^8$       | $a^3 \cdot a^8 =$ $a^{11}$         |
| **4**     | $4$             | $1$                | $a^{16}$    | $a^{11} \cdot a^{16} =$ $a^{27}$   |
| **5**     | $5$             | $0$                | $a^{32}$    | $a^{27}$                           |
| **6**     | $6$             | $0$                | $a^{64}$    | $a^{27}$                           |
| **7**     | $7$             | $0$                | $a^{128}$   | $a^{27}$                           |
| **8**     | $8$             | $1$                | $a^{256}$   | $a^{27} \cdot a^{256} =$ $a^{283}$ |

- **Complexity Bound:** $s-1 \le \text{multiplications} \le 2(s-1) \implies \mathbf{O(\log_2 n)}$.

---

**3.4.5 Searching & Sorting Algorithms**

**1. Linear Search Complexity**

Searches for an element sequentially in an unsorted array.

| Case             | Condition                                | Comparisons | Time Complexity |
| ---------------- | ---------------------------------------- | ----------- | --------------- |
| **Best Case**    | Target found at 1st index $A$.           | $1$28       | $O(1)$          |
| **Worst Case**   | Target at last index $A[n-1]$ or absent. | $n$28       | $O(n)$          |
| **Average Case** | Target found halfway into array.         | $n/2$28     | $O(n)$          |

---

**2. Bubble Sort Versions & Optimizations**

Compares and swaps adjacent elements if out of order, bubbling the largest unsorted element to the end in each pass.

- **Version 1 (Basic Bubble Sort):** Executes $n-1$ outer passes and $n-1$ inner comparisons unconditionally. $$T(n) = (n-1)(n-1) \cdot C = C n^2 - 2Cn + C \implies \mathbf{O(n^2)}$$
- **Version 3 (Flag-Optimized Bubble Sort):** Introduces boolean `flag = 0` before each inner pass; sets `flag = 1` if a swap occurs14. If no swaps occur (`flag == 0`), the array is sorted and the algorithm terminates immediately.
    - **Worst Case:** Reverse-sorted array $\implies \mathbf{O(n^2)}$.
    - **Best Case:** Already-sorted array $\implies \mathbf{O(n)}$ (requires only $1$ pass of $n-1$ comparisons).