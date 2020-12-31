"""
Doomsday Fuel
=============
Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as
raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may
be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel.
Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state
of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions
it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each
time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).
You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms
that the ore can become, but you haven't seen all of them.
Write a function answer(m) that takes an array of array of non-negative ints representing how many times that state
has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each
terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in
simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a
path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The
ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the
fraction is simplified regularly.
For example, consider the matrix m:
[
    [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
    [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
    [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
    [0,0,0,0,0,0],  # s3 is terminal
    [0,0,0,0,0,0],  # s4 is terminal
    [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].
Languages
=========
To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java
Test cases
==========
Inputs:
    (int) m = [
               [0, 2, 1, 0, 0],
               [0, 0, 0, 3, 4],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]
           ]
Output:
    (int list) [7, 6, 8, 21]
Inputs:
    (int) m = [
               [0, 1, 0, 0, 0, 1],
               [4, 0, 0, 3, 2, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0]
           ]
Output:
    (int list) [0, 3, 2, 9, 14]
"""


from fractions import Fraction
from fractions import gcd
import copy


def solution(m):
    """
    Find the probabilities of ending up at a terminal state from state s0
    To solve this problem we will utilise a pythonic approach to Absorbing Markov Chains
    and matrix manipulation operations

    Processing Absorbing Markov Chains:
    - Order our input matrix into standard form such that the order is absorbing states
    followed by transient states

    - Compute the Identity matrix, and sub matrices R, Q

    - Calculate matrix F = (I-Q)^-1

    - Calculate F * R to get our limiting matrix FR

    - Process our probability values and denominator to return

    Let's assume that a 3x3 matrix in python is the equivalent of the following:
    matrix = [[a1, a2, a3],
              [b1, b2, b3],
              [c1, c2, c3]]

    To make our lives easier we will handle all decimal values as fractions
    For computational simplicity we will avoid attempting to reformat the matrix into
    a standard form matrix
    """
    # Lists of indexes to use as pointers to values in the matrix m
    absorbing_states = list()
    non_absorbing_states = list()

    for i, row in enumerate(m):
        if sum(row) == 0:
            absorbing_states.append(i)

        else:
            non_absorbing_states.append(i)

    # If the matrix, m has dimensions 1x1 then the only state available is absorbing
    if len(absorbing_states) == 1:
        return [1, 1]

    # Solving our transition matrix starts here
    # Convert the values in non absorbing states to fractions
    m = normalize(m)

    # Get the sub matrices R and Q from the normalized matrix, m using the (non) absorbing indexes
    # as well as the identity matrix I which will be the same dimensions of matrix Q
    R = subset(m, non_absorbing_states, absorbing_states)       # non absorbing values and absorbing values
    Q = subset(m, non_absorbing_states, non_absorbing_states)   # non absorbing values and absorbing values
    I = identity(len(Q))                                        # Identity matrix

    # Compute the fundamental matrix, F = (I - Q)^-1
    F = (inverse(subtract(I, Q)))

    # Compute the FR = F * R. At this point we have the fractional probabilities
    FR = multiply(F, R)

    # Use a generator to get a list of all the denominators and get the LCM of that list
    # This will be the common denominator of the list of fractions FR[0]
    denominator = list_lcm([fraction.denominator for fraction in FR[0]])

    # Use a generator to get a list of new numerator values
    # new numerator = (numerator * common denominator) / denominator
    output = [fraction.numerator * denominator / fraction.denominator for fraction in FR[0]]

    output.append(denominator)

    print(output)
    return output


def multiply(a, b):
    """
    Multiply matrix a with matrix b. Return the outcome c
    # Multiply operation example
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]

    c = [[1*5 + 2*7, 1*6 + 2*8], [3*5 + 4*7, 3*6 + 4*8]]
    c = [[19, 22], [43, 50]]
    """
    # Row = len(m), Col = len(m[0])
    rows = len(a)
    cols = len(b[0])

    # Make the resulting matrix c for a * b
    c = list()
    for row in range(rows):
        c += [[0] * cols]

    for row in range(rows):                                 # Loop through the row indexes in a
        for col in range(cols):                             # Loop through the column indexes in b
            dot_product = Fraction(0, 1)
            for i in range(len(a[0])):                      # Loop through the column indexes in a
                dot_product += a[row][i] * b[i][col]        # Calculate the dot product of the values

            c[row][col] = dot_product                       # Append the dot product for values to the correct spot in
                                                            # the resulting matrix c

    return c


def identity(n):
    """
    Take dimension n and compute it's identity matrix
    """
    m_identity = list()
    for row in range(n):
        m_identity += [[0] * n]
        m_identity[row][row] = Fraction(1, 1)

    return m_identity


def subtract(a, b):
    """
    Take two matrices; a, b and subtract them from each other
    # Subtraction operation example
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]

    c = [[1-5, 2-6], [3-7, 4-8]]
    c = [[-4, -4], [-4, -4]]
    """
    c = list()
    for i, row in enumerate(a):                 # Loop for all rows in matrix a and get a tuple (index, row)
        new_col = list()                        # Initialize a new list
        for j, col in enumerate(row):           # Loop for all the columns in a row and get a tuple (index, column)
            new_col.append(a[i][j] - b[i][j])   # The new row of the output matrix will be the difference between the
                                                # two values

        c.append(new_col)                       # Append the new column of values to the array

    return c


def normalize(m):
    p_matrix = copy.deepcopy(m)

    for i in range(len(m)):
        row_sum = sum(m[i])
        if row_sum != 0:
            for j, cell in enumerate(m[i]):
                p_matrix[i][j] = Fraction(cell, row_sum)

    return p_matrix


def lcm(x, y):
    """
    Return the Lowest common multiple of two values x and y
    LCM(x,y) = xy / GCD(x,y)
    """
    return x * y / gcd(x, y)


def list_lcm(l):
    """
    Take a list of values, l and return the lcm of those values
    """
    # Iterate through l and find the LCM
    if len(l) <= 2:
        return lcm(*l)

    #lcm_i = lcm(l[0], l[1])
    #i = 2
    ##while i < len(l):
    #    lcm_i = lcm(lcm_i, l[i])
    lcm_i = lcm(l[0], l[1])
    for i in range(len(l)):
        lcm_i = lcm(lcm_i, l[i])

    return lcm_i


def subset(m, rows, cols):
    """
    Create a new matrix and get the values from matrix m for row, col
    This will effectively get a subset of the matrix
    """
    sub_set = list()

    for row in rows:
        values = list()
        for col in cols:
            values.append(m[row][col])

        sub_set.append(values)

    return sub_set



def multiply_row_of_square_matrix(m, row, k):
    n = len(m)
    row_operator = identity(n)
    row_operator[row][row] = k
    return multiply(row_operator, m)
def add_multiple_of_row_of_square_matrix(m, source_row, k, target_row):
    # add k * source_row to target_row of matrix m
    n = len(m)
    row_operator = identity(n)
    row_operator[target_row][source_row] = k
    return multiply(row_operator, m)
def invert_matrix(m):
    n = len(m)
    assert(len(m) == len(m[0]))
    inverse = identity(n)
    for col in xrange(n):
        diagonal_row = col
        assert(m[diagonal_row][col] != 0)
        k = Fraction(1, m[diagonal_row][col])
        m = multiply_row_of_square_matrix(m, diagonal_row, k)
        inverse = multiply_row_of_square_matrix(inverse, diagonal_row, k)
        source_row = diagonal_row
        for target_row in xrange(n):
            if source_row != target_row:
                k = -m[target_row][col]
                print(k)
                m = add_multiple_of_row_of_square_matrix(m, source_row, k, target_row)
                print(m)
                inverse = add_multiple_of_row_of_square_matrix(inverse, source_row, k, target_row)
                print(inverse)
    # that's it!
    return inverse


def inverse(m):
    """
    To get the inverse of M we must do the following operation:

    M^-1 = ( M | I )
    Where I will be the identity matrix for m
    """
    # Compute identity matrix using n as 1-dimension of 2d matrix m
    n = len(m)
    inverse_m = identity(n)


    # First set of operations
    for row in range(n):
        k = Fraction(1, m[row][row])
        m = row_multiplication(m, k, row, row)
        inverse_m = row_multiplication(inverse_m, k, row, row)
        for t_row in range(n):
            if row != t_row:
                k = -m[t_row][row]

                m = row_multiplication(m, k, t_row, row)

                inverse_m = row_multiplication(inverse_m, k, t_row, row)

    return inverse_m



def row_multiplication(m, k, row1, row2):
    """
    Helper function to compute elementary row operation
    """
    n = len(m)
    i = identity(n)
    i[row1][row2] = k
    return multiply(i, m)



if __name__ == '__main__':
    # Test cases

    solution([[0, 1, 0, 0, 0, 1],   # <- s0
              [4, 0, 0, 3, 2, 0],   # <- s1
              [0, 0, 0, 0, 0, 0],   # <- s2
              [0, 0, 0, 0, 0, 0],   # <- s3
              [0, 0, 0, 0, 0, 0],   # <- s4
              [0, 0, 0, 0, 0, 0]])  # <- s5
