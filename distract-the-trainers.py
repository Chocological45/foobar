from fractions import gcd


def solution(banana_list):
    # Recursive matching algorithm
    def matching(u, match, seen):
        for v in range(n):

            if graph[u][v] and seen[v] == False:
                seen[v] = True

                if match[v] == -1 or matching(match[v], match, seen):
                    match[v] = u
                    return True
        return False

    # Get the length of the list and make a graph
    n = len(banana_list)
    graph = [[None] * n for _ in range(n)]

    for i in range(n):
        for j in range(i, n):
            graph[i][j] = check_finite(banana_list[i], banana_list[j])
            graph[j][i] = graph[i][j]

    match = [-1] * n

    result = 0
    for i in range(n):
        seen = [False] * n
        if matching(i, match, seen):
            result += 1

    return n - 2 * (result // 2)


def check_finite(x, y):
    z = (x + y) / gcd(x, y)
    return (z & (z - 1)) != 0


if __name__ == '__main__':
    # Test cases
    #print(solution([1,1]))
    print(solution([1, 7, 3, 21, 13, 19]))