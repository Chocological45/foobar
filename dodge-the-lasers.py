from decimal import Decimal, getcontext

getcontext().prec = 101
sqrt2m1 = Decimal(2).sqrt() - 1


def solution(s):
    n = long(s)

    def s(n):
        if n == 1:
            return 1

        if n < 1:
            return 0

        n1 = long(sqrt2m1 * n)
        return n * n1 + n * (n + 1) // 2 - n1 * (n1 + 1) // 2 - s(n1)

    return str(s(n))

if __name__ == '__main__':
    # Test cases
    print solution('77')


