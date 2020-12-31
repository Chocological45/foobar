def solution(l):
    """
    Take a list, 'l', of versions and sort it in ascending order

    """
    '''
    def split(ver):
    split_list = list()
    for val in ver.split('.'):
        split_list.append(int(val))

    return split_list
    '''

    l.sort(key=lambda s: [int(u) for u in s.split('.')])

    print(l)
    return l


if __name__ == '__main__':
    # Test cases
    solution(["1.11", "2.0.0", "1.2", "2", "0.1", "1.2.1", "1.1.1", "2.0"])
    solution(["1.1.2", "1.0", "1.3.3", "1.0.12", "1.0.2"])
