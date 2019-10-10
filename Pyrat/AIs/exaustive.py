import AIs.backtracking as bt

MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'
directions = {(0, 1): MOVE_UP, (0, -1): MOVE_DOWN,
              (1, 0): MOVE_RIGHT, (-1, 0): MOVE_LEFT}


path = []


def exaustiveSearch(nbCheese: int) -> list:
    '''
    we iterate every permutation to find the best one and get every cheese the fastest way possible
    metagraph must be initialized with bt.computeCheesePath
    nbCheese is the number of cheese in the maze
    '''
    #we generate every permutation of cheeses
    permutations = [[x] for x in range(nbCheese)]
    while len(permutations[0]) != nbCheese:
        permutations = [
            perm + [j] for perm in permutations for j in range(nbCheese) if j not in perm]
    #we iterate over every permutation to find the best one
    bestScore = float('inf')
    bestPerm = []
    for perm in permutations:
        if bt.evaluatePath(perm) < bestScore:
            bestPerm = perm
            bestScore = bt.evaluatePath(perm)
    #we return the best one
    return bt.getPath(bestPerm)


def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    bt.computeCheesePath(mazeMap, piecesOfCheese,
                         mazeWidth, mazeHeight, playerLocation)
    global path
    path = exaustiveSearch(len(piecesOfCheese))
    return


def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    return bt.dj.getDirection(path.pop(), playerLocation)



