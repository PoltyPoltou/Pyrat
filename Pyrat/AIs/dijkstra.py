###############################
# Please put your imports here
from collections import deque
from queue import PriorityQueue
import heapq
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


def targetNextCheese(playerPos, mazeMap, piecesOfCheese, mazeHeight, mazeWidth):
    heap = []
    fatherDic = {playerPos: (-1, -1)}
    heapq.heappush(heap, (0, playerPos))
    length = [[float('inf') for i in range(mazeHeight)]
              for i in range(mazeWidth)]
    length[0][0] = 0
    while heap != []:
        (weight, vertice) = heapq.heappop(heap)
        for elmt in mazeMap[vertice].keys():
            x, y = elmt
            if coupleToIndex(length, elmt) > weight + mazeMap[vertice][elmt]:
                if elmt in heap:
                    heap[heap.index((coupleToIndex(length, elmt), elmt))] = (
                        weight + mazeMap[vertice][elmt], elmt)
                    length[x][y] = weight + mazeMap[vertice][elmt]
                else:
                    length[x][y] = weight + mazeMap[vertice][elmt]
                    heapq.heappush(heap, (length[x][y], elmt))
                fatherDic.pop(elmt, True)
                fatherDic.update({elmt: vertice})
    destination = piecesOfCheese[0]
    distance = length[destination[0]][destination[1]]
    for (x, y) in piecesOfCheese:
        if distance > length[x][y]:
            distance = length[x][y]
            destination = (x, y)
    iterator = destination
    path.append(destination)
    while fatherDic[iterator] != playerPos:
        path.append(fatherDic[iterator])
        iterator = path[-1]
    return path


def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    targetNextCheese(playerLocation, mazeMap,
                     piecesOfCheese, mazeHeight, mazeWidth)
    return


def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    if path == []:
        targetNextCheese(playerLocation, mazeMap,
                         piecesOfCheese, mazeHeight, mazeWidth)
    goal = path.pop()
    return getDirection(goal, playerLocation)
