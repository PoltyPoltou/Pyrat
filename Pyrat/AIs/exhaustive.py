import AIs.backtracking as bt

MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'
directions = {(0, 1): MOVE_UP, (0, -1): MOVE_DOWN,
              (1, 0): MOVE_RIGHT, (-1, 0): MOVE_LEFT}


path = []


def exhaustiveSearch(nbCheese: int) -> list:
    '''
    we iterate every permutation to find the best one and get every cheese the fastest way possible
    metagraph must be initialized with bt.computeCheesePath
    nbCheese is the number of cheese in the maze
    '''
    # we generate every permutation of cheeses
    permutations = [[x] for x in range(nbCheese)]
    while len(permutations[0]) != nbCheese:
        permutations = [
            perm + [j] for perm in permutations for j in range(nbCheese) if j not in perm]
    # we iterate over every permutation to find the best one
    bestScore = float('inf')
    bestPerm = []
    for perm in permutations:
        if bt.evaluatePath(perm) < bestScore:
            bestPerm = perm
            bestScore = bt.evaluatePath(perm)
    # we return the best one
    return bt.getPath(bestPerm)


def recursive(size, metagraph, perm=[-1], weight=0):
    if len(perm) != size:
        lst = [recursive(size, metagraph, perm + [i], weight + metagraph[perm[-1]][i][0])
               for i in range(size) if i not in perm]
        lst.sort(key=lambda couple: couple[0])
        return lst[0]
    else:
        return (weight, perm)


def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    bt.computeCheesePath(mazeMap, piecesOfCheese,
                         mazeWidth, mazeHeight, playerLocation)
    global path
    path = exhaustiveSearch(len(piecesOfCheese))
    return


def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    return bt.dj.getDirection(path.pop(), playerLocation)
