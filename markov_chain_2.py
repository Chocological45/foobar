from __future__ import division
from itertools import starmap
from itertools import compress
from operator import mul
import fractions


def solution(m):
    """
    Given a matrix, m, calculate the probabilities of paths to terminal states
    Where a terminal state is defined as a list of 0's where length is the x dimension
    of matrix m.
    - Normalize the matrix probability values
    - Compute the probability distribution from the normalized matrix
    - Compute the greatest common denominator (gcd) of our fractional values
    """
    # Assume that terminal state is a list of 0's with length of a row from matrix m
    # check for each row if it is a terminal state
    t_states = list()
    for i in range(len(m)):
        if all(p == 0 for p in m[i]):
            t_states.append(True)
        else:
            t_states.append(False)

    # Get our normalized matrix, m
    n_matrix = normalize(m)

    # Compute the probability distribution vector of our normalized matrix
    p_dist = compute_dist(n_matrix)

    # Get the numerators and denominators using our distribution vector as values for Fraction()
    numerators = list()
    denominators = list()
    for val in p_dist:
        numerators.append(fractions.Fraction(val).limit_denominator().numerator)
        denominators.append(fractions.Fraction(val).limit_denominator().denominator)

    # Calculate the factor by which the denominator value must change to
    # reach the gcd (max(denominators))
    factors = list()
    for d in denominators:
        factors.append(max(denominators) / d)

    # Calculate a list of the new numerator values using the factors from the denominators
    new_numerators = list()
    for i in range(len(numerators)):
        new_numerators.append(numerators[i] * factors[i])

    output = list(map(int, compress(new_numerators, t_states)))
    output.append(lcm_for_arrays(denominators))
    print(output)
    #return output


def normalize(m):
    p_matrix = list()

    for i in range(len(m)):
        den_sum = sum(m[i])
        row = list()

        if all(p == 0 for p in m[i]):
            for _ in m[i]:
                row.append(0)
            row[i] = 1
            p_matrix.append(row)
        else:
            for j in m[i]:
                if j != 0:
                    row.append(j / den_sum)
                else:
                    row.append(0)

            p_matrix.append(row)

    return p_matrix


def compute_dist(n):
    vector = n[0]

    for i in range(100000000):
        vector = [sum(starmap(mul, zip(vector, col))) for col in zip(*n)]

    return vector


def lcm(a, b):
    result = a * b / fractions.gcd(a, b)

    return result


def lcm_for_arrays(args):
    array_length = len(args)
    if array_length <= 2:
        return lcm(*args)

    initial = lcm(args[0], args[1])
    i = 2
    while i < array_length:
        initial = lcm(initial, args[i])
        i += 1
    return initial


if __name__ == '__main__':
    # Test cases

    solution([[0, 1, 0, 0, 0, 1],   # <- s0
              [4, 0, 0, 3, 2, 0],   # <- s1
              [0, 0, 0, 0, 0, 0],   # <- s2
              [0, 0, 0, 0, 0, 0],   # <- s3
              [0, 0, 0, 0, 0, 0],   # <- s4
              [0, 0, 0, 0, 0, 0]])  # <- s5