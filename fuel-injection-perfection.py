"""
Commander Lambda has asked for your help to refine the automatic quantum antimatter fuel injection system for her
LAMBCHOP doomsday device. It's a great chance for you to get a closer look at the LAMBCHOP - and maybe sneak in a bit
of sabotage while you're at it - so you took the job gladly.
Quantum antimatter fuel comes in small pellets, which is convenient since the many moving parts of the LAMBCHOP each
need to be fed fuel one pellet at a time. However, minions dump pellets in bulk into the fuel intake. You need to
figure out the most efficient way to sort and shift the pellets down to a single pellet at a time.
The fuel control mechanisms have three operations:
1) Add one fuel pellet 2) Remove one fuel pellet 3) Divide the entire group of fuel pellets by 2 (due to the
destructive energy released when a quantum antimatter pellet is cut in half, the safety controls will only allow this
to happen if there is an even number of pellets)
Write a function called solution(n) which takes a positive integer as a string and returns the minimum number of
operations needed to transform the number of pellets to 1. The fuel intake control panel can only display a number up
to 309 digits long, so there won't ever be more pellets than you can express in that many digits.
For example:
solution(4) returns 2: 4 -> 2 -> 1
solution(15) returns 5: 15 -> 16 -> 8 -> 4 -> 2 -> 1
"""

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
