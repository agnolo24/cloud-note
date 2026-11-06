
#### In computer science the algorithm is defined in three ways

1. **A set of rules** for carrying out calculation either by hand or on a machine
2. **A well-defined computational procedure** that takes an input and produces an output
3. **A finite sequence of instructions or steps** to achieve a specific output


#### Example of an Algorithm & Its Essential Properties

An algorithm is **not** programming language code. It is a sequence of computational tasks written in plain language or pseudocode, completely independent of any programming language

**Characteristics / properties of a Good Algorithm**
1. **Input**: Must have 0 or more (a finite number of) inputs
2. **Output**: Must produce at least one output as a result of execution
3. **Definiteness**: Each instruction must be unambiguous, clear, and precisely defined
4. **Effectiveness**: Every step must be basic, feasible, and essential
5. **Finiteness**: An algorithm should be terminate after a finite number of steps


**Desirable Characteristics**
In addition to the 5 essential properties, a well-designed algorithm should be:

- **General:** Able to solve all instances of a problem, not just a single specific case
- **Efficient:** Uses computer resources (time and memory) minimally
- **Understandable:** Clear enough for anyone to comprehend and apply
- **Unique/Unambiguous:** Instructions leave no room for multiple interpretations

**Worked Example: Euclid's GCD Algorithm**

To illustrate how an algorithm works we can take the **Euclid's Algorithm** for finding the **Greatest Common Divisor (GCD)** of two positive integers $a$ and $b$ 

**Pseudocode / Logic:**

```
Algorithm GCD-Euclid(a, b)
// Input: Two positive integers 'a' (dividend) and 'b' (divisor)
// Output: Greatest Common Divisor of a and b

Step 1: If b = 0, return a as the GCD and exit.
Step 2: Else, divide 'a' by 'b' and assign the remainder to 'r' (r = a mod b).
Step 3: Assign the value of 'b' to 'a' (a = b).
Step 4: Assign the value of 'r' to 'b' (b = r).
Step 5: Go back to Step 1.
```

_(In loop notation)_12:

```
while b ≠ 0 do
{
    r ← a mod b;
    a ← b;
    b ← r;
}
return b;
```


**Tracing the Example Problem: Find GCD(1071, 462)**

- **Initial Values:** $a = 1071$, $b = 462$  

1. **Iteration 1:** $r = 1071 \pmod{462} = 147$  

2. Since $r \neq 0$, we update values:
    - $a \leftarrow 462$  
    - $b \leftarrow 147$  

3. Repeat loop.

4. **Iteration 2:** $r = 462 \pmod{147} = 21$  

5. Since $r \neq 0$, we update values:
    - $a \leftarrow 147$  
    - $b \leftarrow 21$  

6. Repeat loop.

7. **Iteration 3:** $r = 147 \pmod{21} = 0$  

8. Since $r = 0$, the algorithm terminates and returns $b = 21$.

- **Final Result:** $\mathbf{\text{GCD}(1071, 462) = 21}$


#### Basic Building Blocks of Algorithms

An algorithm is constructed using **5 fundamental building blocks**:

| #     | Building Block | Common Name           | Purpose                                                               |
| ----- | -------------- | --------------------- | --------------------------------------------------------------------- |
| **1** | **Sequencing** | Step-by-step actions  | Actions executed linearly in the exact order written                  |
| **2** | **Selection**  | Decision              | Choosing which path to execute based on a condition (e.g., `if-else`) |
| **3** | **Iteration**  | Repetition / Loop     | Executing a set of instructions repeatedly until a condition breaks[  |
| **4** | **Procedure**  | Subprogram / Function | Reusable block of code defined once and called multiple times         |
| **5** | **Recursion**  | Self-reference        | A function calling itself with a simplified argument                  |
Taking the Euclid GCD pseudocode above16:

- **Sequencing:** Steps inside the loop ($r \leftarrow a \bmod b$; $a \leftarrow b$; $b \leftarrow r$) always execute in that exact linear order
- **Selection:** The check `while b ≠ 0` decides whether to enter the loop body or skip to `return b`
- **Iteration:** The `while` loop repeating until $b = 0$

**Procedure and Recursion**

1. **Procedure (Function / Subprogram):**
    - Avoids repeating identical sequences of code across an algorithm
    - We define `GCD(a, b)` once as a procedure and invoke it with different arguments whenever needed
2. **Recursion:**
    - A procedure is **recursive** if it calls itself
    - **Mathematical Example (Factorial):**18 $$\text{factorial}(1) = 1 \quad \text{(Base case)}$$ $$\text{factorial}(n) = n \times \text{factorial}(n-1) \quad \text{(Recursive step)}$$
    - **Recursive Pseudocode for Factorial:**

```
Procedure factorial(n)
begin
    if n == 1 then return 1
    else return n * factorial(n - 1)
end
```

- **3 Required Conditions for Successful Recursion:**
    1. System support for function calls (e.g., stack data structure)
    2. A clear **base condition** that halts recursion after finite steps
    3. Arguments in successive calls must get **simpler** (moving towards the base condition)



#### A Survey of Common Running Times

The running time of an algorithm is represented as a function $T(n)$, where $n$ is the input size. Time complexity measures the number of operations executed rather than clock time, ensuring hardware independence

The standard orders of running time growth are:

1. **Constant Time** $O(1)$**:** Execution time is fixed and independent of the input size n
	![[Pasted image 20261104221923.png|293]]

2. **Linear Time** $O(n)$ **/** $O(kn)$**:** Running time grows linearly with input size n
    ![[Pasted image 20261104222231.png|269]]
    - _Example:_ Finding the minimum value in an array in a single pass

3. **Logarithmic Time** $O(\log n)$**:** Time is proportional to the logarithm of the input size n
    ![[Pasted image 20261104222356.png|268]]
    - _Example:_ Binary search

4. $O(n \log n)$ **Time:** Common in divide-and-conquer algorithms that split arrays into equal sub-arrays and solve recursively (This is not that much important)
    - _Examples:_ Merge Sort, Quick Sort

5. **Quadratic Time** $O(n^2)$**:** Arises from nested loops where both outer and inner loops iterate $O(n)$ times
    ![[Pasted image 20261104223018.png|266]]
    - _Examples:_ Elementary sorting algorithms like Bubble Sort, Insertion Sort, Selection Sort

6. **Cubic Time** $O(n^3)$**:** Arises from three nested loops
    ![[Pasted image 20261104223057.png|290]]
    - _Example:_ Standard Matrix Multiplication

7. **Polynomial Time** $O(n^k)$**:** Search over all subsets of size $k$ out of $n$ elements
    ![[Pasted image 20261104223129.png|290]]
    - _Example:_ Finding an independent set of size $k$ in a graph

8. **Exponential Time** $O(2^n)$ **or** $O(n^2 2^n)$**:** Searching through all possible subsets of $n$ elements
	![[Pasted image 20261104223214.png|290]]

9. **Factorial Time** $O(n!)$**:** Growth rate is faster than exponential (This is not that much important)
    - _Example (Bipartite Matching / Perfect Matching):_ Matching $n$ boys and $n$ girls. The 1st boy has $n$ choices, 2nd boy has $(n-1)$ choices, 3rd boy has $(n-2)$ choices, yielding $n(n-1)(n-2)\dots(1) = n!$ total options

---

#### Analysis & Complexity of Algorithm**

The term **"Analysis of Algorithms"** was introduced by **Donald Knuth**. It evaluates an algorithm's efficiency based on two main parameters:

- **Time Complexity:** Measured by counting the number of **key operations** (e.g., number of comparisons in sorting/searching)
- **Space Complexity:** Measured by the maximum memory space required by the algorithm.

**The Three Analysis Cases**

For an input size $n$, the running time complexity function $f(n)$ is analyzed across three cases:

1. **Best Case:** The minimum number of steps taken for any input instance of size n
2. **Worst Case:** The maximum number of steps taken for any input instance of size n
3. **Average Case:** The expected number of steps averaged over all possible input instances of size $n$, calculated using probability expectation: $$\text{Expectation } E = \sum N_i p_i = N_1 p_1 + N_2 p_2 + \dots + N_k p_k$$ where $p_i$ is the probability of occurrence of input state $N_i$.

---

**Worked Example & Trace: Linear Search Complexity Analysis**

**Algorithm Pseudocode:**

```
Algorithm Linear_Search(A, n, x)
/* Input: Array A with n elements, search key x
   Output: Index LOC if x is found, or LOC = 0 if x is not present */

1. Set K = 1 and LOC = 0
2. Repeat steps 3 and 4 while (LOC == 0 and K <= n)
3.   If (x == A[K])
4.     LOC = K
5.   K = K + 1
6. If (LOC == 0)
7.   Print "x is not present in array A"
8. Else
9.   Print "x is present at location LOC"
```

**Complexity Analysis:**

- **Best Case:** $x$ is found at the very first index ($A$). $$\text{Comparisons } C = 1 \implies \mathbf{O(1)}$$
- **Worst Case:** $x$ is at the last index ($A[n]$) or not present in $A$ at all. $$\text{Comparisons } C = n \implies \mathbf{O(n)}$$
- **Average Case:** Assuming $x$ is equally likely to be at any index $1, 2, \dots, n$ with probability $p = \frac{1}{n}$: $$\text{Average Comparisons } E = \sum_{i=1}^{n} i \cdot \frac{1}{n} = \frac{1}{n} \left( \frac{n(n+1)}{2} \right) = \frac{n+1}{2} \approx \frac{n}{2} \implies \mathbf{O(n)}$$

**Key Rule:** Average case analysis is complex because input distributions are hard to predict. Therefore, unless specified otherwise, **we always analyze algorithms in the worst case** as it provides a guaranteed upper bound.

---

**Introduction to Asymptotic Notations**

To express growth rate as $n \to \infty$, three primary asymptotic notations are used19more_horiz:

- **Big-**$O$ **(Big-Oh):** Represents the **Upper Bound** (worst-case maximum steps)
- $\Omega$ **(Big-Omega):** Represents the **Lower Bound** (best-case minimum steps)
- $\Theta$ **(Big-Theta):** Represents the **Tight Bound** (both upper and lower bounds match)

---

**1.6 Types of Problems**

Computing problems are categorized into several domain types

1. **Sorting:** Arranging elements in a specified order (e.g., ascending, alphabetical)
    - Best comparison sorting algorithms take $O(n \log n)$ time
    - **Stability:** A sorting algorithm is **stable** if equal elements retain their original relative positions after sorting
    - **In-Place:** An algorithm is **in-place** if it requires negligible extra memory beyond the input array
2. **Searching:** Finding a key element in a static or dynamic dataset
3. **String Processing:** String matching and pattern identification (e.g., web search engines like Google)
4. **Graph Problems:** Network routing, shortest paths, broadcasting (visiting all nodes), and spanning trees
5. **Combinatorial Problems:** Finding permutations, combinations, or subsets satisfying constraints (e.g., Travelling Salesman Problem, Independent Set, Graph Coloring). These are often the hardest problems as solution space grows rapidly
6. **Geometric Problems:** Algorithms dealing with points, lines, and polygons (e.g., computer graphics, robotics)
    - _Classic Examples:_ **Closest-Pair Problem** (finding two closest points) and **Convex-Hull Problem** (smallest convex polygon enclosing all points)
7. **Numerical Problems:** Solving linear equations, differential equations, integration
    - _Major Issue:_ Accumulation of rounding errors across multiple iterations

---

**1.7 Problem Solving Techniques**

The major design paradigms include:

1. **Divide and Conquer:** Top-down approach. Breaks problem into sub-problems recursively, solves them, and merges results
    - _Examples:_ Binary Search, Quick Sort, Merge Sort, Strassen's Matrix Multiplication

2. **Greedy Technique:** Used for optimization problems (maximizing/minimizing an objective function under constraints) by making locally optimal choices at each step
    - _Examples:_ Kruskal’s MST, Prim’s MST, Dijkstra’s Shortest Path, Fractional Knapsack

3. **Dynamic Programming:** Bottom-up approach. Solves overlapping sub-problems, **stores results in a table**, and reuses them to avoid re-computation
    - _Examples:_ 0/1 Knapsack, Floyd-Warshall All-Pairs Shortest Path, Travelling Salesman Problem, Matrix Chain Multiplication

4. **Branch and Bound:** BFS-like search over a state-space tree for discrete/combinatorial optimization; prunes branches that cannot yield better solutions than the best found so far

5. **Randomized Algorithms:** Uses random numbers/choices during execution for faster computation
    - _Examples:_ Random pivot choice in Quick Sort, random divisor testing for factorization

6. **Backtracking:** DFS-like systematic search through checkpointing; backtracks to previous decision states when a candidate solution fails
    - _Examples:_ 8-Queens Puzzle, Map Coloring, Sudoku

---

**1.8 Deterministic vs Stochastic Algorithms**

- **Deterministic Algorithm:** The output and next state can be completely predicted/determined from the input and current program state
- **Stochastic Algorithm:** Incorporates randomness; future states and outputs cannot be deterministically predicted
- **Application Note:** Deterministic algorithms must be avoided when outputs need to be unpredictable (e.g., card shuffling in a Blackjack game). Pseudo-random number generators can be predictable, so hardware RNGs or cryptographically secure PRNGs with random seeds are used instead.

---
