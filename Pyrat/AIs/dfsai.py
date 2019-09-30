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

# dfs algorithm


def targetNextCheese(playerPos, mazeMap, piecesOfCheese):
    queue = []
    fatherDic = {playerPos: (-1, -1)}
    queue.append(playerPos)
    cheeseFound = False
    while queue != [] and not cheeseFound:
        vertice = queue.pop()
        for elmt in mazeMap[vertice].keys():
            if elmt not in fatherDic.keys():
                fatherDic.update({elmt: vertice})
                queue.append(elmt)
            if elmt in piecesOfCheese:
                cheeseFound = True
                destination = elmt
                break
    iterator = destination
    path.append(destination)
    while fatherDic[iterator] != playerPos:
        path.append(fatherDic[iterator])
        iterator = path[-1]


def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    targetNextCheese(playerLocation, mazeMap, piecesOfCheese)
    return


def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    if path == []:
        targetNextCheese(playerLocation, mazeMap, piecesOfCheese)
    goal = path.pop()
    return getDirection(goal, playerLocation)
