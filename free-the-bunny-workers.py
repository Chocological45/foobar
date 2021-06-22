def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1
        yield tuple(pool[i] for i in indices)


def solution(num_buns, num_required):
    output = []

    combi_one = list(combinations(range(num_buns), num_required))
    total = len(combi_one) * num_required
    repeats = (num_buns - num_required) + 1

    combi_two = list(combinations(range(num_buns), repeats))

    for i in range(num_buns):
        output.append([])

    for i in range(total / repeats):
        for j in combi_two[i]:
            output[j].append(i)

    return output

if __name__ == '__main__':
    # Test cases
    print solution(2, 1)
    print solution(4, 4)
    print solution(5, 3)
    
    
