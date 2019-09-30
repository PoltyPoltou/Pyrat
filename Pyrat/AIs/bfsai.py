###############################
# Please put your imports here
from collections import deque
import test as t
###############################
# Please put your global variables here

MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'
directions = {(0, 1): MOVE_UP, (0, -1): MOVE_DOWN,
              (1, 0): MOVE_RIGHT, (-1, 0): MOVE_LEFT}
path = []

# return the move to do when you want to go from position to direction


def getDirection(direction, position):
    (fstA, sndA) = direction
    (fstB, sndB) = position
    fst = fstA - fstB
    snd = sndA-sndB
    return directions[(fst, snd)]

# allows to use couple to access data in a matrix


def coupleToIndex(matrix, couple):
    (a, b) = couple
    return matrix[a][b]

# BFS algorithm, playerPos is the starting point of the alg


def targetNextCheese(playerPos, mazeMap, piecesOfCheese):
    queue = []
    fatherDic = {playerPos: (-1, -1)}  # dictionary of the father of each node
    queue.append(playerPos)
    cheeseFound = False
    while queue != [] and not cheeseFound:
        vertice = queue.pop(0)
        for elmt in mazeMap[vertice].keys():
            if elmt not in fatherDic.keys():
                fatherDic.update({elmt: vertice})
                queue.append(elmt)
            if elmt in piecesOfCheese:  # we break the loop if we found a cheese as it is the closest one
                cheeseFound = True
                destination = elmt
                
    iterator = destination
    path.append(destination)
    while fatherDic[iterator] != playerPos:
        path.append(fatherDic[iterator])
        iterator = path[-1]

# we compute a first path to the nearest cheese in advance


def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    targetNextCheese(playerLocation, mazeMap, piecesOfCheese)
    return

# then we make a move or if there is no move available we recreate a path to the nearest neighboor


def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    if path == []:
        targetNextCheese(playerLocation, mazeMap, piecesOfCheese)
    goal = path.pop()
    return getDirection(goal, playerLocation)
