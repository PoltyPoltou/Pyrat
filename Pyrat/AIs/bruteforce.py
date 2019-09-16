###############################
# Please put your imports here
import heapq
###############################
# Please put your global variables here

MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'
directions = {(0, 1): MOVE_UP, (0, -1): MOVE_DOWN,
              (1, 0): MOVE_RIGHT, (-1, 0): MOVE_LEFT}


def getDirection(direction, position):
    (fstA, sndA) = direction
    (fstB, sndB) = position
    fst = fstA - fstB
    snd = sndA-sndB
    return directions[(fst, snd)]


def generatePermutations(size):
    if size == 1:
        return [[0]]
    else:
        setup = generatePermutations(size - 1)
        lst = []
        for permutation in setup:
            for i in range(size):
                temp = permutation.copy()
                if i != size - 1:
                    temp.append(temp[i])
                    temp[i] = size - 1
                else:
                    temp.append(size-1)
                lst.append(temp)
        return lst
# return the weight of the tour but in reverse (easier to use with list.pop)


def targetPoint(playerPos, mazeMap, target):
    heap = []
    path = []
    fatherDic = {playerPos: (-1, -1)}
    heapq.heappush(heap, (0, playerPos))
    cheeseFound = False
    while heap != [] and not cheeseFound:
        (weight, vertice) = heapq.heappop(heap)
        for elmt in mazeMap[vertice].keys():
            if elmt not in fatherDic.keys():
                fatherDic.update({elmt: vertice})
                heapq.heappush(heap, (weight + mazeMap[vertice][elmt], elmt))
            if elmt == target:
                cheeseFound = True
                destination = elmt
                break
    iterator = destination
    path.append(destination)
    weight = 0
    while fatherDic[iterator] != playerPos:
        path.append(fatherDic[iterator])
        weight += mazeMap[iterator][path[-1]]
        iterator = path[-1]
    weight += mazeMap[iterator][playerPos]
    return (weight, path)


def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    bestLength = mazeHeight * mazeWidth * 3
    print(bestLength)
    bestPath = []
    print("time allowed %s", timeAllowed)
    for permutation in generatePermutations(len(piecesOfCheese)):
        (length, path) = targetPoint(playerLocation,
                                     mazeMap, piecesOfCheese[permutation[0]])
        for i in range(1, len(permutation)):
            (partialLength, partialPath) = targetPoint(
                piecesOfCheese[permutation[i - 1]], mazeMap, piecesOfCheese[permutation[i]])
            length += partialLength
            path = partialPath + path
        if bestLength > length:
            bestLength = length
            bestPath = path
    return path


def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    print("duh")
    return
