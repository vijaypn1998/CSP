# CSP
Project Title

CSP Encoding Problem
Description

This project demonstrates an implementation of a Constraint Satisfaction Problem (CSP) solver using heuristics like Most Constrained Variable, Most Constraining Variable, and Least Constraining Value. The program supports forward checking and domain ordering to efficiently solve CSPs.

The solver accepts input files describing variables, domains, and constraints, and outputs the solutions or indicates failure when no solution exists.
Features

    Dynamic variable and value ordering for optimal CSP solving.
    Heuristics for constraint optimization:
        Most Constrained Variable
        Most Constraining Variable
        Least Constraining Value
    Forward checking to reduce invalid assignments.
    Detailed logging for each solution or failure.

How to Run

    Prerequisites: Ensure Python 3.x is installed on your system.

    Input Format:
        Variables File: Defines the variables and their respective domains.
        Conditions File: Specifies constraints between variables.
        Backtrack Limit: Determines the maximum number of backtracking steps.

    Usage:

python3 main.py <variable_file> <condition_file> <backtrack_limit>

Example:

    python3 main.py variables.txt conditions.txt 100

    Outputs:
        Solution: Lists assignments for all variables satisfying the constraints.
        Failure: Indicates the failure to find a solution after the specified backtrack limit.

Example Input and Output

Input:

    variables.txt

X1:1,2,3
X2:2,3
X3:1,3

conditions.txt

    X1 > X2
    X2 != X3

Command:

python3 main.py variables.txt conditions.txt 100

Output:

1. X1 = 3, X2 = 2, X3 = 1 fail
2. X1 = 3, X2 = 1, X3 = 3 solution
...
