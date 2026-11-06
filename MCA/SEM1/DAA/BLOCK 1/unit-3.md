
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

````
Algorithm Evaluate_Horner(A, n, x)
/* Input: Array A[0..n] containing coefficients of polynomial of degree n, point x
   Output: Value of polynomial at point x */

p = A[n];                       // Initialize with leading coefficient
for i = n-1 down to 0 do
    p = p * x + A[i];           // 1 multiplication + 1 addition per step
return p;
``` [13, 14]

---

#### **Worked Trace Examples & Solved Problems (Horner's Rule)**

* **Example 1: Evaluate \\(P(x) = 3x^2 + 5x + 6\\) at \\(x = 3\\)** [14]
  * **Nested Form:** \\(P(x) = (3x + 5)x + 6\\) [14]
  * **Step 1:** Initial assignment \\(p = a[15] = 3\\) [14].
  * **Iteration 1 (\\(i=1\\)):** \\(p = (3 \times 3) + 5 = 9 + 5 = 14\\) [14].
  * **Iteration 2 (\\(i=0\\)):** \\(p = (14 \times 3) + 6 = 42 + 6 = \mathbf{48}\\) [14].

* **Check Your Progress 1 (Q2): Evaluate \\(P(x) = 3x^4 + 2x^3 - 5x + 7\\) at \\(x = 2\\) using Horner's Rule** [6, 12]
  * **Degree \\(n = 4\\).** Coefficient array \\(A = [a_0, a_1, a_2, a_3, a_4] = [7, -5, 0, 2, 3]\\) [6].
  * **Initial:** \\(p = A[16] = 3\\) [6].
  * **Iteration 1 (\\(i=3\\)):** \\(p = (2 \times 3) + A[17] = 6 + 2 = 8\\) [6].
  * **Iteration 2 (\\(i=2\\)):** \\(p = (2 \times 8) + A[15] = 16 + 0 = 16\\) [6].
  * **Iteration 3 (\\(i=1\\)):** \\(p = (2 \times 16) + A[18] = 32 + (-5) = 27\\) [6].
  * **Iteration 4 (\\(i=0\\)):** \\(p = (2 \times 27) + A = 54 + 7 = \mathbf{61}\\) [6].

---

### **3.4.3 Matrix Multiplication (Order \\(n \times n\\))**

Multiplying two square matrices \\(A_{n \times n}\\) and \\(B_{n \times n}\\) to yield product matrix \\(C_{n \times n}\\) [19]:

#### **C Program Code Structure:**
```c
for (i = 0; i < n; i++) {                 // Outer loop: O(n)
    for (j = 0; j < n; j++) {             // Middle loop: O(n)
        c[i][j] = 0;                      // O(1)
        for (k = 0; k < n; k++) {         // Inner loop: O(n)
            c[i][j] = c[i][j] + a[i][k] * b[k][j]; // O(1) constant work
        }
    }
}
``` [20-22]

#### **Complexity Analysis:**
* Outer loop runs \\(n\\) times [20].
* Middle loop runs \\(n\\) times [20].
* Inner loop runs \\(n\\) times, performing 1 multiplication, 1 addition, and 1 assignment per iteration [21].
* **Total Time Complexity:** \\(n \times n \times n = \mathbf{O(n^3)}\\) [21, 23].

---

### **3.4.4 Exponent Evaluation (Binary Exponentiation)**

Evaluating \\(a^n\\) via brute-force multiplying \\(a\\) by itself takes \\(n-1\\) multiplications (\\(O(n)\\)) [24, 25]. 
To speed this up for cryptographic applications, **Binary Exponentiation** splits exponent \\(n\\) into its binary representation of length \\(s = \lfloor \log_2 n \rfloor + 1\\) bits, achieving **\\(O(\log_2 n)\\) complexity** [24, 26, 27].

---

#### **1. Left-to-Right Binary Exponentiation**
Processes bits of exponent \\(n\\) from **Most Significant Bit (MSB)** down to **Least Significant Bit (LSB)** [28].

```text
Algorithm Left_To_Right_Exponentiation(A, s, a)
/* Input: Array A[s] storing binary representation of exponent n, base a
   Output: a^n */

result = a;
for i = s-2 down to 0 do
    result = result * result;         // Square current value
    if A[i] == 1 then
        result = result * a;          // Multiply by base 'a' if bit is 1
return result;
``` [28]

* **Trace Example: Compute \\(a^{17}\\)** [28, 29]
  * Exponent \\(n = 17 = 10001_2\\), string length \\(s = 5\\) bits (\\(A[16]=1, A[17]=0, A[15]=0, A[18]=0, A=1\\)) [28].
  * **Initial:** `result = a` [28, 29].
  * **Iteration 1 (\\(i=3\\), bit \\(0\\)):** `result` \\(= a \cdot a = a^2\\) [29].
  * **Iteration 2 (\\(i=2\\), bit \\(0\\)):** `result` \\(= a^2 \cdot a^2 = a^4\\) [29].
  * **Iteration 3 (\\(i=1\\), bit \\(0\\)):** `result` \\(= a^4 \cdot a^4 = a^8\\) [29].
  * **Iteration 4 (\\(i=0\\), bit \\(1\\)):** `result` \\(= a^8 \cdot a^8 = a^{16}\\); since bit is \\(1\\), `result` \\(= a^{16} \cdot a = \mathbf{a^{17}}\\) [29].
  * **Total Multiplications:** **5** (instead of 16 in brute force) [29].

---

#### **2. Right-to-Left Binary Exponentiation**
Processes bits of exponent \\(n\\) from **LSB** up to **MSB** [27].

```text
Algorithm Right_To_Left_Exponentiation(A, s, a)
/* Input: Array A[s] storing binary representation of exponent n, base a
   Output: a^n */

x = a;
if A == 1 then result = a else result = 1;

for i = 1 to s-1 do
    x = x * x;                        // Square base power
    if A[i] == 1 then
        result = result * x;          // Accumulate into result if bit is 1
return result;
``` [27, 30]

---

#### **Check Your Progress 3 (Q1): Trace \\(a^{283}\\) for both methods** [22, 31, 32]
Exponent \\(n = 283 = 100011011_2\\), string length \\(s = 9\\) bits [22, 32].

##### **A. Left-to-Right Trace for \\(a^{283}\\):**

| Iteration | Bit Index (\\(i\\)) | Bit Value | Operations & Intermediate `result` |
| :---: | :---: | :---: | :--- |
| **Init** | 8 | 1 | `result = a` [22] |
| **1** | 7 | 0 | `(a)^2 = a^2` [22] |
| **2** | 6 | 0 | `(a^2)^2 = a^4` [22] |
| **3** | 5 | 0 | `(a^4)^2 = a^8` [22] |
| **4** | 4 | 1 | `(a^8)^2 * a = a^{17}` [22] |
| **5** | 3 | 1 | `(a^{17})^2 * a = a^{35}` [32] |
| **6** | 2 | 0 | `(a^{35})^2 = a^{70}` [32] |
| **7** | 1 | 1 | `(a^{70})^2 * a = a^{141}` [32] |
| **8** | 0 | 1 | `(a^{141})^2 * a = \mathbf{a^{283}}` [32] |

##### **B. Right-to-Left Trace for \\(a^{283}\\):**

| Iteration | Bit Index (\\(i\\)) | Bit Value | Power Value (\\(x\\)) | Accumulated `result` |
| :---: | :---: | :---: | :---: | :--- |
| **Init** | 0 | 1 | \\(a\\) | `result = a` (since \\(A=1\\)) [32] |
| **1** | 1 | 1 | \\(a^2\\) | `a * a^2 = a^3` [32] |
| **2** | 2 | 0 | \\(a^4\\) | `a^3` [32] |
| **3** | 3 | 1 | \\(a^8\\) | `a^3 * a^8 = a^{11}` [32] |
| **4** | 4 | 1 | \\(a^{16}\\) | `a^{11} * a^{16} = a^{27}` [32] |
| **5** | 5 | 0 | \\(a^{32}\\) | `a^{27}` [32] |
| **6** | 6 | 0 | \\(a^{64}\\) | `a^{27}` [32] |
| **7** | 7 | 0 | \\(a^{128}\\) | `a^{27}` [32] |
| **8** | 8 | 1 | \\(a^{256}\\) | `a^{27} * a^{256} = \mathbf{a^{283}}` [32] |

* **Complexity bound for both methods:** \\(s - 1 \le \text{multiplications} \le 2(s - 1) \implies \mathbf{O(\log_2 n)}\\) [27, 31, 33].

---

### **3.4.5 Searching & Sorting Algorithms**

#### **1. Linear Search Complexity Summary**
In Linear Search over an array of size \\(n\\), comparison is the key operation [31, 34]:

| Case | Condition | Comparisons | Complexity |
| :--- | :--- | :---: | :---: |
| **Best Case** | Element found at first position (\\(A\\)) [35]. | \\(1\\) [35] | **\\(O(1)\\)** [35, 36] |
| **Worst Case** | Element at last position (\\(A[n-1]\\)) or not present [35]. | \\(n\\) [35] | **\\(O(n)\\)** [35, 36] |
| **Average Case** | Element found halfway into the list [35]. | \\(n/2\\) [35] | **\\(O(n)\\)** [35, 36] |

---

#### **2. Bubble Sort Algorithm & Optimizations**

* **Version 1 (Basic Bubble Sort):**
  Uses two nested loops, each iterating \\(n-1\\) times without checking if the array is already sorted [4, 37]:
  \\[T(n) = (n-1)(n-1) \cdot C = C n^2 - 2Cn + C \implies \mathbf{O(n^2)}\\] [4, 37]

* **Version 2 & 3 (Flag-Optimized Bubble Sort):**
  Adds a boolean swap flag (`swapped = false`). If a full inner pass completes without making any swaps, the algorithm halts early [4, 23].
  * **Worst Case:** Reverse-sorted array \\(\implies \mathbf{O(n^2)}\\) [23, 38, 39].
  * **Best Case:** Already-sorted array \\(\implies \mathbf{O(n)}\\) (the inner loop runs only 1 pass of \\(n-1\\) comparisons to verify order) [23, 38].

---
````