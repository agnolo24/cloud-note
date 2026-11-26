
2.0 & 2.1 Introduction: Why Do We Need Proofs?

In everyday life, if someone tells you, _"I am stronger than you,"_ your natural reaction is to look at them and say: **"Prove it!"**. In that physical situation, proof might mean a demonstration of strength1. Similarly, the world demands verifiable evidence before accepting a scientist's predictions or a historian's claims.

In mathematics, if you want a statement to be accepted as true, you must provide **mathematically acceptable evidence** showing that it is **universally true**. That evidence takes the form of a **logically valid argument**.

---

2.2 What is a Proof?

1. The Anatomy of an Argument

An **argument** in mathematics or logic is defined as a finite sequence of statements: $$p_1, p_2, \dots, p_n, p$$ such that: $$(p_1 \land p_2 \land \dots \land p_n) \rightarrow p$$

- Each statement $p_1, p_2, \dots, p_n$ is called a **premise** (or an assumption, or a hypothesis).
- The final statement $p$ is called the **conclusion**.

**Definition:** A **proof** of a proposition $p$ is a mathematical argument consisting of a sequence of statements $p_1, p_2, \dots, p_n$ from which $p$ logically follows. The statement that is proved to be true is called a **theorem**.

---

📖 Example 1 (from Source): Set Intersection

**Problem:** Give an argument to show that the mathematical statement: _"For any two sets_ $A$ _and_ $B$_,_ $A \cap B \subseteq A$_"_ is true.

**Solution / Argument:**

1. Let $x$ be an arbitrary element of $A \cap B$.
2. Then $x \in A$ and $x \in B$, by definition of intersection '$\cap$'.
3. Therefore, $x \in A$.
4. Since this holds for every $x \in A \cap B$, by definition of subset '$\subseteq$', we conclude: $$A \cap B \subseteq A \quad \blacksquare$$

---

💡 A Crucial Distinction: $\rightarrow$ versus $\Rightarrow$

- $r \rightarrow s$ is a compound proposition (material implication) that is either True or False depending on the truth values of $r$ and $s$.
- $r \Rightarrow s$ denotes logical implication: it means **"**$s$ **is true whenever** $r$ **is true"**. By contraposition, it also means _"_$r$ _is false whenever_ $s$ _is false".

---

2. Theorems, Disproofs, and Conjectures

- **Theorem:** A statement that has been proved true by a valid argument.
- **Disproof:** A proof that a statement $p$ is false (meaning its negation $\sim p$ is proved to be true).
- **Conjecture:** A statement that mathematicians suspect or feel is true, but which has neither been proved nor disproved.
    - If a conjecture is eventually proved, it becomes a **theorem**.
    - If it is disproved, its negation becomes a theorem!

🕵️ The Story of Goldbach’s Conjecture (1742)

The mathematician Christian Goldbach stated:

_"For every_ $n \in \mathbb{N}$_, if_ $n$ _is even and_ $n > 2$_, then_ $n$ _is the sum of two primes."

- $4 = 2 + 2$
- $6 = 3 + 3$
- $8 = 3 + 5$
- $10 = 3 + 7 = 5 + 5$

To this day, **no one has been able to prove or disprove Goldbach's conjecture**. Even though computers have verified it for billions of numbers, checking individual examples is not a proof because natural numbers are infinite.

---

3. The 4 Types of Premises Used in a Proof

In any valid mathematical proof, every single statement must be justified by one of **four types of premises**:

1. **A proposition proved earlier** (e.g., using the division algorithm to prove that complex roots of a real polynomial occur in conjugate pairs).
2. **A proposition that follows logically from earlier lines in the proof** (as in step 3 of Example 1 above).
3. **An axiom (or postulate):** A mathematical fact that has never been proved, but is universally accepted as true (e.g., _"two distinct points determine a unique line"_).
4. **A definition of a mathematical term** (e.g., the definitions of '$\cap$' and '$\subseteq$' used in Example 1).

---

4. Detecting Flawed Reasoning: The Story of Maya's Homework

Not every sequence of statements forms a valid argument. Consider this narrative from the source:

_Premise 1:_ **"If Maya sees the movie, she won't finish her homework."**
_Premise 2:_ **"Maya won't finish her homework."**
_Conclusion:_ **"Therefore, Maya sees the movie."**

Why is this argument invalid?

Let $p$: _"Maya sees the movie"_ and $q$: _"Maya won't finish her homework". The argument claims: $$[(p \rightarrow q) \land q] \Rightarrow p$$

Let's test this with a truth table:

|$p$|$q$|$p \rightarrow q$|Premises: $(p \rightarrow q) \land q$|Conclusion: $p$|
|---|---|---|---|---|
|**T**|**T**|**T**|**T**|**T**|
|**T**|**F**|**F**|**F**|**T**|
|**F**|**T**|**T**|**T**|**F** (⚠️ Failure!)|
|**F**|**F**|**T**|**F**|**F**|

In **Row 3**, both premises are **True** (Maya didn't do her homework, and the implication holds), but the conclusion $p$ is **False** (she did _not_ see the movie—perhaps she fell ill or visited a friend)! Because the conclusion can be false when the premises are true, the argument is **invalid** (a logical fallacy).

---

The 4 Fundamental Rules of Inference

To construct proofs without drawing huge truth tables, we use four standard valid argument forms called **rules of inference**:

1. Law of Detachment (_Modus Ponens_)

- Meaning: _Modus ponens_ is Latin for **"method of affirmation"**. The conclusion $q$ is "detached" from the conditional premise.
- Form: $$\begin{array}{l} p \rightarrow q \\ p \\ \hline \therefore q \end{array} \quad \text{i.e., } [(p \rightarrow q) \land p] \Rightarrow q$$16
- **Story:**
    - _"If Kali can draw, then she will get a job."_
    - _"Kali can draw."_
    - _"Therefore, Kali will get a job."_

2. Law of Contraposition (_Modus Tollens_)

- Meaning: _Modus tollens_ is Latin for **"method of denial"**.
- Form: $$\begin{array}{l} p \rightarrow q \\ \sim q \\ \hline \therefore \sim p \end{array} \quad \text{i.e., } [(p \rightarrow q) \land \sim q] \Rightarrow \sim p$$15
- **Story:**
    - _"If Kali can draw, then she will get a job."_
    - _"Kali will not get a job."_
    - _"Therefore, Kali can't draw."_

3. Disjunctive Syllogism

- Form: $$\begin{array}{l} p \lor q \\ \sim p \\ \hline \therefore q \end{array} \quad \text{i.e., } [(p \lor q) \land \sim p] \Rightarrow q$$17
- **Story (from E4(i)):**
    - _"Either Munna will cook or Munni will practise Karate."_
    - _"Munna will not cook."_
    - _"Therefore, Munni will practise Karate."_

4. Hypothetical Syllogism

- Form: $$\begin{array}{l} p \rightarrow q \\ q \rightarrow r \\ \hline \therefore p \rightarrow r \end{array} \quad \text{i.e., } [(p \rightarrow q) \land (q \rightarrow r)] \Rightarrow (p \rightarrow r)$$17
- **Story (from E4(ii)):**
    - _"If Madhu is a 'sarpanch', she will head the 'panchayat'."_17
    - _"If Madhu heads the 'panchayat', she will decide on property disputes."_17
    - _"Therefore, if Madhu is a 'sarpanch', she will decide on property disputes."_17

---

✏️ Check Your Understanding: Section 2.2 Exercises

Before we move into Section 2.3's proof methods, try these questions directly from the course text:

1. **Exercise E1:** In school algebra, we prove: $(x + y)^2 = x^2 + 2xy + y^2$ for $x, y \in \mathbb{R}$ Which premise type justifies writing $(x + y)^2 = (x + y)(x + y)$?
2. **Exercise E2:** Is every statement a theorem? Why?
3. **Exercise E3:** Check whether the following argument is valid or invalid using a truth table: $$(p \rightarrow q \lor \sim r) \land (q \rightarrow p) \Rightarrow (p \rightarrow r)$$
4. **Exercise E4(iii):** Check if this argument is valid:
    - _"Either Munna will cook or Munni will practise Karate."_
    - _"If Munni practises Karate, then Munna studies."_
    - _"Munna does not study."_
    - _"Therefore, Munni will practise Karate."_