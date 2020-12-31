import time


def solution(n):
    """
    Reduce n to 1 and count the number of div2 operations required to achieve this

    We assume n to be a positive integer

    While n is not 1
        If n is even then
            Divide n by 2
        If n is odd then
            If n is 3 or (n-1) has less 1's than (n+1)
                Decrement n
            Otherwise
                Increment n
    """
    n = int(n)

    count = 0

    while n != 1:

        # If n is even then divide it by 2
        if not (n & 1):
            n >>= 1

        elif n == 3 or bin(n - 1).count('1') < bin(n + 1).count('1'):
            n = ~- n  # n-=1

        else:
            n = -~ n  # n+=1

        # Increment the number of steps
        count = -~ count

    # Return the minimum number of steps
    return count


def bits(n):
    count = 0

    while n:
        count += n % 2
        n //= 2

    return count


if __name__ == '__main__':
    # Test cases
    start = time.time()
    solution('15')
    print("--- %s seconds ---" % (time.time() - start))
