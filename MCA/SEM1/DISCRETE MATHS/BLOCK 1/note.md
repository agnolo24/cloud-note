# 1.0 

### INTRODUCTION
Human reasoning and scientific advancement led to the formal study of logic, which evolved from Aristotle's early Greek philosophy into modern symbolic logic through the mathematical work of Leibniz and George Boole. This text introduces a unit on symbolic logic (or propositional calculus), which provides a mathematical framework to formalise arguments, test their validity, and identify logical fallacies.

Key Unit Sections

• Acceptable Sentences (Sec. 1.2): Introduces "statements" or "propositions," which are sentences that hold a definitive truth value of either True (T) or False (F).

• Propositional Calculus (Sec. 1.3): Explores how simple propositions are linked into complex compound statements using logical connectives ("and", "or", "not", "implies", "implies and is implied by") and explains how to build truth tables for them.

• Statement Equivalence (Sec. 1.4): Examines the specific conditions under which two different statements are logically identical and can be substituted for one another.

• Quantification & Notation (Sec. 1.5): Defines the standard terminology and notations used to quantify objects within a logical statement.

# 1.1

### OBJECTIVES
After reading this unit, you should be able to:

- distinguish between propositions and non-propositions;

- construct the truth table of any compound proposition;

- identify and use logically equivalent statements;

- identify and use logical quantifiers.

# 1.2

### PROPOSITIONS
**In mathematical logic, a proposition (or statement) is a declarative sentence that is uniformly true or uniformly false (never both), and whose truth value is universally agreed upon by everyone.**

To be accepted as a proposition, a sentence must meet two main conditions:

```
1. It must be a declarative sentence: Orders, questions, and exclamations are not propositions because they do not declare a fact.

2. It must have a universal truth value: Subjective statements where opinions differ (e.g., personal opinions or preferences) cannot be propositions.
```

Examples of Propositions vs. Non-Propositions:

    - Valid Propositions (General):
        - “In 2003, the President of India was a woman.” (Universally false)
        
        - “An elephant weighs more than a human being.” (Universally true)
        
        - “An egg has protein in it.” (Universally true)
        
        - “The Prime Minister of India has to be a man.” (Universally false)
        
    - Invalid Propositions (Subjective or Non-Declarative):
        - “Women are more intelligent than men.” (Rejected because people disagree; not universally true or false)
        
        - “Watch the film.” (Rejected because it is an order)
        
        - “How wonderful!” (Rejected because it is an exclamation)
        
        - “What did you say?” (Rejected because it is a question)
        
**Mathematical Propositions and Open Sentences**

Mathematical statements can also be classified as propositions:

    - Two plus two equals four. (True)
    
    - Two plus two equals five. (False)
    
    - x + y > 0 for x > 0 and y > 0. (True)
    
    - A set with n elements has 2n subsets. (Out of these four examples, three are true and one—"Two plus two equals five"—is false).


The Role of Variables (Open Sentences):

    - An algebraic sentence like x + y > 0 is not a proposition on its own because its truth value cannot be determined unless the values of $x$ and $y$ are known (e.g., it is false when $x = 1, y = -2$, but true when $x = 1, y = 0$).
    
    - However, when specific constraints are added—such as x + y > 0 for x > 0, y > 0—it becomes a valid proposition.
    
    
**proposition notation**
    - Propositions are typically denoted using lowercase letters (such as 'p' or 'q').
    
    - Examples of Notation:
        - p:Ice is always cold.
        
        - q:cos^2 θ + sin^2 θ  = 1 for θ ∈ [0, 2π]
        
**Truth Values (T and F)**

      - Every proposition has a definitive truth value that is either True (T) or False (F), but never both.
      
      - Examples: 
            - The truth value of “Ice melts at 30°C.” is F (False).
            
            - The truth value of “x^2 >= 0 for x ∈ R” is T (True).  
        
---


# 1.3 

### LOGICAL CONNECTIVES
***Logical connectives are words and phrases used to combine simpler statements into more complex ones in mathematical logic.***

Examples: 'and', 'or', 'if ... then', 'if and only if'.

There are 6 logical connections in total, but hear we only have 5 to learn, they are:
```
- Disjunction

- Conjection

- Negation

- Conditional Connection

- Precedence Rule
```
