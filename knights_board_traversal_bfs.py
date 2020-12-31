from collections import deque


class Node:
    """
    Node class to define a node for a binary tree traversal.
    x, y are the coordinate positions of a node on the chess board
    dist is the minimum distance from the source
    """

    def __init__(self, x, y, dist=0):
        self.x = x
        self.y = y
        self.dist = dist

    def __hash__(self):
        return hash((self.x, self.y, self.dist))

    def __eq__(self, other):
        return (self.x, self.y, self.dist) == (other.x, other.y, other.dist)


def solution(src, dest):
    """
    Convert the src and dest provided to their coordinates in the chess board
    then use these coordinates to search for the shortest path.
    """
    # Define a board position lookup table
    board = [[0, 1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13, 14, 15],
             [16, 17, 18, 19, 20, 21, 22, 23], [24, 25, 26, 27, 28, 29, 30, 31],
             [32, 33, 34, 35, 36, 37, 38, 39], [40, 41, 42, 43, 44, 45, 46, 47],
             [48, 49, 50, 51, 52, 53, 54, 55], [56, 57, 58, 59, 60, 61, 62, 63]]

    # Constant value for square board dimensions
    N = 8

    src_node = None
    dest_node = None

    # Get the x, y positions of src and dest cells
    for x in range(N):
        for y in range(N):
            if board[x][y] == src:
                src_node = Node(x, y)
            if board[x][y] == dest:
                dest_node = Node(x, y)

    # Search for the shortest path from src to dest and compute it's length
    path_length = search(src_node, dest_node, N)
    print(path_length)
    return path_length


def neighbours(x, y, N):
    """
    Get the neighbouring positions to a particular coordinate pos using knight's rule:
    - Get the x, y values of the position
    - For all potential knight moves compute the new x and y values
    - Check if these coordinates are within the bounds of the board
    - If so add it to a set of legal actions
    - Return the actions
    """
    actions = set()

    # All the potential moves that can be made by a knight
    knight_moves = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]

    # Compute the new x, y values
    for move in knight_moves:
        new_x = x + move[0]
        new_y = y + move[1]

        # Check if the new x, y values are within the bounds of the board
        if not(new_x >= N or new_x < 0 or new_y >= N or new_y < 0):
            actions.add((new_x, new_y))

    return actions


def search(src, dest, N):
    """
    BFS tree traversal using nodes in a queue.
    We will use deque from collections here as it has O(1) time complexity
    as opposed to list.pop() which has O(n) time complexity.
    """
    # Initialize a queue and enqueue the src node
    queue = deque()
    queue.append(src)

    # Initialize an empty set of explored positions
    explored = set()

    # While nodes in queue
    while queue:
        # Pop the front node from the queue
        node = queue.popleft()

        # Get the x, y and dist values from the node
        x = node.x
        y = node.y
        dist = node.dist

        # If the current node is the destination, return the distance
        if x == dest.x and y == dest.y:
            return dist

        # If node is a new node then explore it
        if node not in explored:
            explored.add(node)

            for action in neighbours(x, y, N):
                queue.append(Node(action[0], action[1], dist + 1))

    # If no path exists return a length of 0
    return 0


if __name__ == '__main__':
    # Test cases
    solution(0, 1)
    solution(19, 36)
    solution(0, 63)
