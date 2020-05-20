from collections import deque
from itertools import product, combinations

n = 8 # board size

directions = ((1, 0), (-1, 0), (0, 1), (0, -1) # rook moves
#            ,(1, 1), (-1, -1), (1, -1), (-1, 1) # uncomment for queen moves
)

def bfs(neighbors, root):
    """Breadth-first search.

    Given a graph neighbors:V->V* and a root vertex, returns (p, d),
    where p[v] is the predecessor of v on the path from the root, and
    d[v] is the distance to v from the root.
    """
    queue = deque([root])
    parent = {root: None}
    distance = {root: 0}
    while queue:
        vertex = queue.popleft()
        for neighbor in neighbors(vertex):
            if neighbor not in parent:
                parent[neighbor] = vertex
                distance[neighbor] = distance[vertex] + 1
                queue.append(neighbor)
    return (parent, distance)

def orbit(pieces):
    """Orbit of dihedral group action on rooks on a chess board."""
    for k in range(4):
        yield pieces
        yield tuple(sorted((n - 1 - x, y) for (x, y) in pieces))    # reflect
        pieces = tuple(sorted((n - 1 - y, x) for (x, y) in pieces)) # rotate

def neighbors(pieces):
    """Sliding rook (or queen) digraph.

    Given a vertex represented by a (sorted) list of (x, y) coordinates
    of rooks (or queens) on a chess board, with 0 <= x,y < board_size,
    return sequence of neighbor vertices, each obtained by sliding a
    piece along its rank or file (or diagonal) as far as possible,
    "blocked" only by another piece or the edge of the board.
    """

    # Check each piece and possible move direction.
    for index, (x0, y0) in enumerate(pieces):
        for (dx, dy) in directions:

            # Move until we reach the board's edge or another piece.
            for d in range(n):
                x, y = (x0 + (d + 1) * dx, y0 + (d + 1) * dy)
                if not (0 <= x < n) or not (0 <= y < n) or (x, y) in pieces:

                    # If there is room to move, return the resulting vertex.
                    if d > 0:
                        neighbor = list(pieces)
                        neighbor[index] = (x0 + d * dx, y0 + d * dy)
                        yield min(orbit(tuple(sorted(neighbor))))
                    break

if __name__ == '__main__':
    for n in range(2, 13, 2):
        
        # Compute all states reachable from 4 pieces in the 4 corners.
        print('Solving', n, 'by', n, 'board...')
        p, d = bfs(neighbors, ((0, 0), (0, n - 1), (n - 1, 0), (n - 1, n - 1)))

        # Display (reversed) list of states to move all 4 pieces to the center.
        c = n // 2 - 1
        pieces = ((c, c), (c, c + 1), (c + 1, c), (c + 1, c + 1))
        print(d[pieces], 'moves:')
        while pieces:
            print(pieces)
            pieces = p[pieces]

        # Check if all unreachable states are one move away from the large
        # connected component.
        print('Counting states...')
        unreachable = {min(orbit(pieces)) for pieces in
                       combinations(product(range(n), range(n)), 4)} - p.keys()
        print(len(p), 'reachable')
        print(len(unreachable), 'unreachable')
        print(all(all(w in p for w in neighbors(v)) for v in unreachable))
