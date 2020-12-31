import time


def solution(M, F):
    # First we convert our string values to positive long integers
    m, f = int(M), int(F)
    # Set a counter for the cycles taken
    cycles = 0
    # Repeat the process while the minimum value between m and f is not 1. We use the min
    # value as this will reach 1 before the other and we only need to assess M OR F is not 1
    while min(m, f) != 1:
        # Check that the values will result into a valid solution. Do so by checking if
        # m%f or f%m is 0. If not return impossible
        if max(m, f) % min(m, f) == 0:
            return 'impossible'

        # Increment the cycles counter using floor division
        cycles += max(m, f) // min(m, f)
        # Standard euclidean algorithm. Make m the min value and f max % min
        m, f = min(m, f), max(m, f) % min(m, f)

    # Add max - 1 to cycles and return. This is the total number of cycles required
    return str(cycles + max(m, f) - 1)


if __name__ == '__main__':
    # Test cases
    start = time.time()
    print(solution('4', '7'))
    print("--- %s seconds ---" % (time.time() - start))

    '''
    5.60283660889e-05
    
    '''