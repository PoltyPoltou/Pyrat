###############################
# Please put your imports here
from collections import deque
from queue import PriorityQueue
import heapq
import sys
import AIs.backtracking as bt
import AIs.theOne as one
###############################
# Please put your global variables here

MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

globalPath = []

directions = {(0, 1): MOVE_UP, (0, -1): MOVE_DOWN,
              (1, 0): MOVE_RIGHT, (-1, 0): MOVE_LEFT}


def getDirection(direction: tuple, position: tuple) -> str:
    '''
    get two positions and return the move to go from position to direction
    '''
    (fstA, sndA) = direction
    (fstB, sndB) = position
    fst = fstA - fstB
    snd = sndA-sndB
    return directions[(fst, snd)]

# allows to use couple to access data in a matrix


def coupleToIndex(matrix: list, couple: tuple):
    '''
get a list of list, matrix, and a couple and considers them as coordinates
'''
    (a, b) = couple
    return matrix[a][b]


def targetPoint(playerPos: (int, int), mazeMap: dict, target: (int, int), mazeWidth: int, mazeHeight: int, pieceOfCheese: list = [], cheeseValuation: int = 0) -> (int, list):
    '''
    see targetNextCheese for details, here we just go to target instead of a cheese
    Using dijkstra algorithm
    '''
    if playerPos == target:
        return (0, [])
    # setup of dijkstra algorithm
    length, fatherDict = dijkstraMethod(
        playerPos, mazeMap, mazeWidth, mazeHeight)
    # this part is to transform the fatherDict into a path
    iterator = target
    path = []
    weight = 0
    path.append(target)
    while fatherDict[iterator] != playerPos:
        path.append(fatherDict[iterator])
        weight += mazeMap[iterator][fatherDict[iterator]]
        iterator = path[-1]
    return (weight + mazeMap[iterator][playerPos], path)


def targetNextCheese(playerPos: (int, int), mazeMap: dict, piecesOfCheese: list, mazeWidth: int, mazeHeight: int) -> (int, list):
    '''
    mazeMap is the dict discribing the map
    piecesOfCheese the list of the coordinates of the remaining cheeses
    mazeWidth and mazeHeight are the dimensions of the maze
    from the the player's position
    returns the path and weight to the closest cheese
    '''
    if playerPos in piecesOfCheese:
        return (0, [])
    # dijkstra algorithm
    length, fatherDict = dijkstraMethod(
        playerPos, mazeMap, mazeWidth, mazeHeight)
    # we also check which cheese is the closest one and is stored in destination
    destination = piecesOfCheese[0]
    distance = length[destination[0]][destination[1]]
    for pos in piecesOfCheese:
        if distance > coupleToIndex(length, pos):
            distance = coupleToIndex(length, pos)
            destination = pos
    # this part is to transform the fatherDict into a path
    iterator = destination
    path = []
    path.append(destination)
    weight = 0
    while fatherDict[iterator] != playerPos:
        weight += mazeMap[iterator][fatherDict[iterator]]
        path.append(fatherDict[iterator])
        iterator = path[-1]
        fatherDict[iterator]
    return weight, path


def isNextCheeseStillHere(path: list, remainingCheeses: list) -> bool:
    return path[0] in remainingCheeses


def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    point = (mazeWidth//2, mazeHeight//2)

    globalPath.extend(targetPoint(playerLocation, mazeMap,
                                  point, mazeWidth, mazeHeight)[1])

    return


beginFlag = True


def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    # if path is empty it means we can look for another cheese and we go on
    global globalPath
    global beginFlag
    if globalPath == []:
        globalPath.extend(targetNextCheese(playerLocation, mazeMap,
                                           piecesOfCheese, mazeWidth, mazeHeight)[1])
        beginFlag = False
    if not isNextCheeseStillHere(globalPath, piecesOfCheese) and not beginFlag:
        globalPath = targetNextCheese(
            playerLocation, mazeMap, piecesOfCheese, mazeWidth, mazeHeight)[1]
    return getDirection(globalPath.pop(), playerLocation)


def dijkstraMethod(playerPos: (int, int), mazeMap: dict, mazeWidth: int, mazeHeight: int, pieceOfCheese: list = [], cheeseValuation: int = 0):
    heap = []
    fatherDict = {playerPos: (-1, -1)}
    heapq.heappush(heap, (0, playerPos))
    length = [[float('inf') for i in range(mazeHeight)]
              for i in range(mazeWidth)]
    x, y = playerPos
    length[x][y] = 0
    # loop while we do not have explored every node
    while heap != []:
        (weight, vertice) = heapq.heappop(heap)
        for elmt in mazeMap[vertice].keys():
            x, y = elmt
            if coupleToIndex(length, elmt) > weight + mazeMap[vertice][elmt]:
                # affects the new weight if it is better than the previous one
                if elmt in heap:
                    heap[heap.index((coupleToIndex(length, elmt), elmt))] = (
                        weight + mazeMap[vertice][elmt], elmt)
                    length[x][y] = weight + mazeMap[vertice][elmt]
                else:
                    length[x][y] = weight + mazeMap[vertice][elmt]
                    heapq.heappush(heap, (length[x][y], elmt))
                # adds or update the father's elmt, which is vertice
                fatherDict.pop(elmt, True)
                fatherDict.update({elmt: vertice})
    return length, fatherDict
