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
globalPath = []


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


def targetPoint(playerPos, mazeMap, target, mazeWidth, mazeHeight):
    '''
    see targetNextCheese for details, here we just go to target instead of a cheese
    '''
    heap = []
    fatherDic = {playerPos: (-1, -1)}
    heapq.heappush(heap, (0, playerPos))
    length = [[float('inf') for i in range(mazeHeight)]
              for i in range(mazeWidth)]
    length[0][0] = 0
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
                fatherDic.pop(elmt, True)
                fatherDic.update({elmt: vertice})
    # this part is to transform the fatherDict into a path
    iterator = target
    path = []
    weight = 0
    path.append(target)
    while fatherDic[iterator] != playerPos:
        path.append(fatherDic[iterator])
        weight += mazeMap[iterator][fatherDic[iterator]]
        iterator = path[-1]
    return (weight, path)


def targetNextCheese(playerPos: tuple, mazeMap: dict, piecesOfCheese: list, mazeWidth: int, mazeHeight: int) -> list:
    '''
    mazeMap is the dict discribing the map
    piecesOfCheese the list of the coordinates of the remaining cheeses
    mazeWidth and mazeHeight are the dimensions of the maze
    from the the player's position
    returns the path and weight to the closest cheese
    '''
    # setup of dijkstra algorithm
    heap = []
    fatherDic = {playerPos: (-1, -1)}
    heapq.heappush(heap, (0, playerPos))
    length = [[float('inf') for i in range(mazeHeight)]
              for i in range(mazeWidth)]
    length[0][0] = 0
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
                fatherDic.pop(elmt, True)
                fatherDic.update({elmt: vertice})
    # this part is to transform the fatherDict into a path
    # we also check which cheese is the closest one and is stored in destination
    destination = piecesOfCheese[0]
    distance = length[destination[0]][destination[1]]
    for (x, y) in piecesOfCheese:
        if distance > length[x][y]:
            distance = length[x][y]
            destination = (x, y)
    iterator = destination
    path = []
    path.append(destination)
    weight = 0
    while fatherDic[iterator] != playerPos:
        weight += mazeMap[iterator][fatherDic[iterator]]
        path.append(fatherDic[iterator])
        iterator = path[-1]
    return weight, path


def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    globalPath.extend(targetNextCheese(playerLocation, mazeMap,
                                       piecesOfCheese, mazeHeight, mazeWidth)[1])
    return


def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    # if path is empty it means we can look for another cheese and we go on
    if globalPath == []:
        globalPath.extend(targetNextCheese(playerLocation, mazeMap,
                                           piecesOfCheese, mazeHeight, mazeWidth))
    goal = globalPath.pop()
    return getDirection(goal, playerLocation)
