###############################
# Please put your imports here
import AIs.dijkstra as dj
#import dijkstra as dj
###############################
# Please put your global variables here

cheesesPath = []

# return the weight of the greediest path


def greedIsFeed(beginLocation, mazeMap, piecesOfCheese, mazeWidth, mazeHeight, availableCheeses = []):
    if availableCheeses == []:
        availableCheeses = [*range(len(piecesOfCheese))]
        playerPos = -1
    else:
        playerPos = piecesOfCheese.index(beginLocation)
    weight = 0
    path = []
    cheesesRemaining = availableCheeses.copy()
    while cheesesRemaining != []:
        index = 1
        bestIndex = 0
        bestWeight = cheesesPath[playerPos][cheesesRemaining[0]][0]
        while index < len(cheesesRemaining):
            if cheesesPath[playerPos][cheesesRemaining[index]][0] < bestWeight:
                bestIndex = index
                bestWeight = cheesesPath[playerPos][cheesesRemaining[index]][0]
            index += 1
        w, p = cheesesPath[playerPos][cheesesRemaining[bestIndex]]
        playerPos = cheesesRemaining.pop(bestIndex)
        weight += w
        path = p + path
    
    return (weight, path)

# estimate the lower bound of the total weight of current solution (in progress)
# for now it is estimated one move for each cheese not picked up plus the actual weight


def lowerBound(constructingSolution, mazeMap, playerPos, piecesOfCheese,mazeWidth, mazeHeight):
    weight = cheesesPath[-1][constructingSolution[0]][0]
    for i in range(len(constructingSolution) - 1):
        weight += cheesesPath[constructingSolution[i]][constructingSolution[i + 1]][0]
    lastPos = piecesOfCheese[constructingSolution[-1]]
    furthestCouple = (0,lastPos)
    for pos in [x for x in range(len(piecesOfCheese)) if x not in constructingSolution]:
        x, y = piecesOfCheese[pos]
        if furthestCouple[0] < abs(lastPos[0] - x) + abs(lastPos[1] - y):
            furthestCouple = (abs(lastPos[0] - x) + abs(lastPos[1] - y), pos)
    return weight + furthestCouple[0]
# warning modifies the list perm, returns it just in case


def firstPerm(size, perm):
    for i in range(size):
        if i not in perm:
            perm.append(i)
    return perm

# finds the next permutation in the lexicographic order (thx wikipedia)


def nextPerm(lst, size):
    newLst = lst.copy()
    if len(lst) < size:
        i = 1
        while [] == [x for x in range(lst[-i] + 1, size) if x not in newLst[:len(lst) - i]]:
            i+=1
        newLst[-i] = [x for x in range(lst[-i] + 1, size) if x not in newLst[:len(lst) - i]][0]
        numbersAvailable = [x for x in range(size) if x not in newLst][:i-1]
        for j in range(len(lst) - 1, len(lst) - i , -1):
            newLst[j] = numbersAvailable.pop()
        result = newLst
    else:
        k = -1
        for acc in range(len(lst) - 1):
            if lst[acc] < lst[acc + 1]:
                k = acc
        if k == -1:
            return []  # when it has reached the end of permutation
        l = -1
        for acc in range(len(lst)):
            if lst[k] < lst[acc]:
                l = acc
        newLst[k], newLst[l] = newLst[l], newLst[k]
        temp = newLst[k+1:]
        temp.reverse()
        result = newLst[:k+1] + temp
    return result

def evaluatePath(cheesesPerm, beginLocation, mazeMap, piecesOfCheese, mazeWidth, mazeHeight):
    weight, p = cheesesPath[-1][cheesesPerm[0]]
    for i in range(len(cheesesPerm)-1):
        weight += cheesesPath[cheesesPerm[i]][cheesesPerm[i+1]][0]
    return weight


def getPath(cheesesPerm, beginLocation, mazeMap, piecesOfCheese, mazeWidth, mazeHeight):
    p = cheesesPath[-1][cheesesPerm[0]][1].copy()
    for i in range(len(cheesesPerm)-1):
        p = cheesesPath[cheesesPerm[i]][cheesesPerm[i+1]][1] + p
    return p
# solutions are just the order of the cheeses taken (in respect to the list piecesOfCheese)

def lastPerm(lst, size):
    if lst == []:
        return False
    return [] == [x for x in range(lst[-1]+1,size) if x not in lst]


def backtracking(mazeMap, piecesOfCheese, playerLocation, mazeWidth, mazeHeight):
    n = len(piecesOfCheese)
    bestScore,path = greedIsFeed(playerLocation,mazeMap,piecesOfCheese, mazeWidth, mazeHeight)
    lst = [0]
    while lst != [x for x in range(n - 1, -1, -1)]:
        if lowerBound(lst, mazeMap, playerLocation, piecesOfCheese,mazeWidth, mazeHeight) > bestScore:
            while lastPerm(lst, n):
                lst.pop()
            if lst == []:
                lst = [x for x in range(n - 1, -1, -1)]
            else:
                lst = nextPerm(lst, n)
                if len(lst) == n:
                    score = evaluatePath(lst,playerLocation,mazeMap,piecesOfCheese,mazeWidth, mazeHeight)
                    if score < bestScore:
                        bestScore = score
                        path = getPath(lst,playerLocation,mazeMap,piecesOfCheese,mazeWidth, mazeHeight)
        elif len(lst) != n:
            lst.append([x for x in range(n) if x not in lst][0])
        else:
            score = evaluatePath(lst,playerLocation,mazeMap,piecesOfCheese,mazeWidth, mazeHeight)
            if score < bestScore:
                bestScore = score
                path = getPath(lst,playerLocation,mazeMap,piecesOfCheese,mazeWidth, mazeHeight)
            while lastPerm(lst, n):
                lst.pop()
            if lst == []:
                lst = [x for x in range(n - 1, -1, -1)]
            else:
                lst = nextPerm(lst, n)
    return path

globalPath = []

def computeCheesePath(mazeMap, piecesOfCheese, mazeWidth, mazeHeight, playerLocation):
    cheesesPath.extend([[] for i in range(len(piecesOfCheese)+1)])
    for i in range(len(piecesOfCheese)):
        for j in range(i,len(piecesOfCheese)):
            if i != j:
                cheesesPath[i].append(dj.targetPoint(piecesOfCheese[i], mazeMap, piecesOfCheese[j], mazeWidth, mazeHeight))
                w, p = cheesesPath[i][-1]
                p = p.copy()
                p.pop(0)
                p.append(piecesOfCheese[i])
                p.reverse()
                cheesesPath[j].append((w,p))
            else:
                cheesesPath[i].append((0, []))
        cheesesPath[-1].append(dj.targetPoint(playerLocation, mazeMap, piecesOfCheese[i], mazeWidth, mazeHeight))
        w, p = cheesesPath[-1][-1]
        p = p[:]
        p.pop(0)
        p.append(playerLocation)
        p.reverse()
        cheesesPath[i].append((w,p))
    cheesesPath[-1].append((0,[]))

def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    computeCheesePath(mazeMap, piecesOfCheese, mazeWidth, mazeHeight, playerLocation)
    order = greedIsFeed(playerLocation, mazeMap, piecesOfCheese, mazeWidth, mazeHeight)
    globalPath.extend(order[1])
    f = open("greed.csv","a")
    f.write(str(order[0]) + "\n")
    f.close()
    return 


def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    
    return dj.getDirection(globalPath.pop(),playerLocation)


cheese = [(10, 7), (3, 12), (17, 2), (3, 3), (17, 11), (4, 7), (16, 7), (8, 1), (12, 13), (8, 4), (12, 10), (9, 8), (11, 6), (1, 14), (19, 0), (4, 8), (16, 6), (2, 9), (18, 5), (2, 0), (18, 14), (6, 11), (14, 3), (0, 11), (20, 3), (5, 10), (15, 4), (8, 14), (12, 0), (9, 9), (11, 5), (0, 7), (20, 7), (6, 5), (14, 9), (2, 5), (18, 9), (8, 12), (12, 2), (6, 3), (14, 11)]
maze = {(0, 0): {(0, 1): 1, (1, 0): 1}, (0, 1): {(0, 0): 1, (1, 1): 9}, (0, 2): {(1, 2): 1}, (0, 3): {(0, 4): 1}, (0, 4): {(0, 3): 1, (1, 4): 1}, (0, 5): {(1, 5): 
1, (0, 6): 1}, (0, 6): {(0, 5): 1, (1, 6): 1}, (0, 7): {(1, 7): 1}, (0, 8): {(0, 9): 1, (1, 8): 1}, (0, 9): {(0, 8): 1}, (0, 10): {(0, 11): 1}, (0, 11): {(0, 10): 1, (0, 12): 1}, (0, 12): {(1, 12): 1, (0, 13): 1, (0, 11): 1}, (0, 13): {(0, 12): 1, (0, 14): 1}, (0, 14): {(0, 13): 1, (1, 14): 1}, (1, 0): {(2, 0): 1, (0, 0): 1}, (1, 1): {(1, 2): 1, (0, 1): 9}, (1, 2): {(0, 2): 1, (1, 1): 1, (1, 3): 1, (2, 2): 1}, (1, 3): {(1, 4): 1, (2, 3): 1, (1, 2): 1}, (1, 4): {(1, 5): 1, (1, 3): 1, (0, 4): 1}, (1, 5): {(0, 5): 1, (2, 5): 1, (1, 4): 1}, (1, 6): {(0, 6): 1}, (1, 7): {(2, 7): 1, (0, 7): 1}, (1, 8): {(1, 9): 1, (0, 8): 
1}, (1, 9): {(1, 8): 1, (1, 10): 6}, (1, 10): {(1, 9): 6, (2, 10): 1}, (1, 11): {(2, 11): 1}, (1, 12): {(0, 12): 1, (2, 12): 1}, (1, 13): {(2, 13): 1, (1, 14): 1}, (1, 14): {(1, 13): 1, (0, 14): 1}, (2, 0): {(1, 0): 1}, (2, 1): {(3, 1): 1}, (2, 2): {(1, 2): 1}, (2, 3): {(1, 3): 1}, (2, 4): {(2, 5): 8}, (2, 5): 
{(1, 5): 1, (2, 4): 8, (3, 5): 1}, (2, 6): {(3, 6): 1}, (2, 7): {(1, 7): 1, (3, 7): 1, (2, 8): 1}, (2, 8): {(2, 7): 1, (2, 9): 1}, (2, 9): {(2, 8): 1, (3, 9): 1}, (2, 10): {(1, 10): 1, (2, 11): 1}, (2, 11): {(2, 12): 1, (2, 10): 1, (1, 11): 1}, (2, 12): {(2, 11): 1, (1, 12): 1}, (2, 13): {(1, 13): 1, (2, 14): 4, (3, 13): 1}, (2, 14): {(2, 13): 4}, (3, 0): {(3, 1): 1}, (3, 1): {(2, 1): 1, (3, 0): 1, (3, 2): 1, (4, 1): 1}, (3, 2): {(3, 1): 1, (4, 2): 1, (3, 3): 1}, 
(3, 3): {(3, 2): 1, (4, 3): 1}, (3, 4): {(3, 5): 10}, (3, 5): {(2, 5): 1, (4, 5): 1, (3, 4): 10}, (3, 6): {(2, 6): 1, (3, 7): 1}, (3, 7): {(2, 7): 1, (3, 8): 1, (3, 6): 1}, (3, 8): {(3, 7): 1}, (3, 9): {(4, 9): 1, (3, 10): 1, (2, 9): 1}, (3, 10): {(3, 9): 1, (3, 11): 1}, (3, 11): {(4, 11): 1, (3, 12): 1, (3, 10): 1}, (3, 12): {(3, 11): 1, (4, 12): 1, (3, 13): 1}, (3, 13): {(3, 12): 1, (4, 13): 1, (3, 14): 5, (2, 13): 1}, (3, 14): {(3, 13): 5, (4, 14): 1}, (4, 0): 
{(4, 1): 1}, (4, 1): {(4, 0): 1, (3, 1): 1}, (4, 2): {(3, 2): 1}, (4, 3): {(4, 4): 1, (3, 3): 1}, (4, 4): {(4, 5): 1, (4, 3): 1, (5, 4): 1}, (4, 5): {(3, 5): 1, (4, 4): 1, (4, 6): 9, (5, 5): 1}, (4, 6): {(4, 7): 1, (4, 5): 9, (5, 6): 1}, (4, 7): {(4, 6): 1, (4, 8): 1}, (4, 8): {(4, 7): 1, (4, 9): 1}, (4, 9): {(3, 9): 1, (5, 9): 1, (4, 8): 1, (4, 10): 1}, (4, 10): {(4, 9): 1}, (4, 11): {(3, 11): 1, (5, 11): 1}, (4, 12): {(3, 12): 1}, (4, 13): {(3, 13): 1, (5, 13): 
1}, (4, 14): {(3, 14): 1, (5, 14): 1}, (5, 0): {(6, 0): 1}, (5, 1): {(5, 2): 6}, (5, 2): {(6, 2): 1, (5, 3): 1, (5, 1): 6}, (5, 3): {(5, 2): 1, (5, 4): 1}, 
(5, 4): {(5, 3): 1, (6, 4): 1, (4, 4): 1}, (5, 5): {(4, 5): 1}, (5, 6): {(4, 6): 1}, (5, 7): {(5, 8): 4}, (5, 8): {(5, 9): 1, (5, 7): 4}, (5, 9): {(5, 8): 1, (4, 9): 1, (5, 10): 1}, (5, 10): {(6, 10): 7, (5, 9): 1}, (5, 11): {(4, 11): 1, (5, 12): 1}, (5, 12): {(5, 11): 1}, (5, 13): {(4, 13): 1, (6, 13): 1}, (5, 14): {(4, 14): 1}, (6, 0): {(5, 0): 1, (6, 1): 1}, (6, 1): {(7, 1): 1, (6, 0): 1}, (6, 2): {(5, 2): 1, (6, 3): 1}, (6, 3): {(6, 2): 1, (7, 3): 1}, (6, 4): 
{(5, 4): 1, (7, 4): 1}, (6, 5): {(6, 6): 1, (7, 5): 1}, (6, 6): {(7, 6): 1, (6, 5): 1}, (6, 7): {(6, 8): 6}, (6, 8): {(6, 9): 1, (6, 7): 6}, (6, 9): {(6, 10): 1, (6, 8): 1, (7, 9): 1}, (6, 10): {(5, 10): 7, (6, 9): 1, (6, 11): 1}, (6, 11): {(6, 10): 1, (6, 12): 1}, (6, 12): {(6, 11): 1}, (6, 13): {(6, 14): 1, (5, 13): 1}, (6, 14): {(6, 13): 1}, (7, 0): {(8, 0): 1}, (7, 1): {(6, 1): 1, (8, 1): 1, (7, 2): 1}, (7, 2): {(7, 3): 1, (7, 1): 1}, (7, 3): {(6, 3): 1, (7, 2): 1}, (7, 4): {(6, 4): 1}, (7, 5): {(6, 5): 1}, (7, 6): {(6, 6): 1, (7, 7): 1}, (7, 7): {(7, 6): 1, (7, 8): 1, (8, 7): 1}, (7, 8): {(7, 7): 1}, (7, 9): {(7, 10): 1, (6, 9): 1}, (7, 10): {(7, 9): 1, (7, 11): 1}, (7, 11): {(7, 12): 1, (7, 10): 1}, (7, 12): {(7, 11): 1, (7, 13): 2}, (7, 13): {(7, 12): 2, (8, 13): 1}, (7, 14): {(8, 14): 3}, (8, 0): {(7, 0): 1, (9, 0): 1}, (8, 1): {(7, 1): 1}, (8, 2): {(8, 3): 1}, (8, 3): {(8, 2): 1, (8, 4): 1}, (8, 4): {(8, 5): 9, (9, 4): 1, (8, 3): 1}, (8, 5): {(8, 4): 9}, (8, 6): {(9, 6): 1}, (8, 7): {(9, 7): 1, (7, 7): 1, (8, 8): 1}, (8, 8): {(8, 7): 1}, (8, 9): {(8, 10): 1}, (8, 10): {(8, 9): 1, (9, 10): 8, (8, 11): 1}, (8, 11): {(8, 12): 7, (8, 10): 1}, (8, 12): {(8, 11): 7, (9, 12): 1}, (8, 13): {(7, 13): 1, (9, 13): 1}, (8, 14): {(7, 14): 3, (9, 14): 1}, (9, 0): {(9, 1): 1, (8, 0): 1}, (9, 1): {(9, 2): 1, (9, 0): 1}, (9, 2): {(9, 1): 1, (10, 2): 1}, (9, 3): {(9, 4): 1, (10, 3): 1}, (9, 4): {(9, 3): 1, (9, 5): 1, (8, 4): 1}, (9, 5): {(9, 4): 1, (10, 5): 1}, (9, 6): {(8, 6): 1, (9, 7): 1}, (9, 7): {(8, 7): 1, (10, 7): 1, (9, 6): 1}, (9, 8): {(9, 9): 1, (10, 8): 1}, (9, 9): {(9, 8): 1, (9, 10): 1}, (9, 10): {(8, 10): 8, (9, 9): 1}, (9, 11): {(10, 11): 1, (9, 12): 1}, (9, 12): {(8, 12): 1, (9, 11): 1, (9, 13): 1, (10, 12): 1}, (9, 13): {(8, 13): 1, (9, 12): 1, (10, 13): 1, (9, 14): 1}, (9, 14): {(8, 14): 1, (9, 13): 1, (10, 14): 1}, (10, 0): {(11, 
0): 1}, (10, 1): {(11, 1): 1}, (10, 2): {(11, 2): 1, (9, 2): 1}, (10, 3): {(11, 3): 1, (9, 3): 1}, (10, 4): {(10, 5): 1}, (10, 5): {(9, 5): 1, (10, 4): 1}, 
(10, 6): {(11, 6): 1, (10, 7): 9}, (10, 7): {(9, 7): 1, (11, 7): 1, (10, 8): 9, (10, 6): 9}, (10, 8): {(9, 8): 1, (10, 7): 9}, (10, 9): {(11, 9): 1, (10, 10): 1}, (10, 10): {(10, 9): 1}, (10, 11): {(9, 11): 1, (11, 11): 1}, (10, 12): {(9, 12): 1, (11, 12): 1}, (10, 13): {(9, 13): 1}, (10, 14): {(9, 14): 1}, (11, 0): {(12, 0): 1, (11, 1): 1, (10, 0): 1}, (11, 1): {(12, 1): 1, (11, 2): 1, (10, 1): 1, (11, 0): 1}, (11, 2): {(12, 2): 1, (11, 3): 1, (11, 1): 1, (10, 2): 1}, (11, 3): {(10, 3): 1, (11, 2): 1}, (11, 4): {(12, 4): 8, (11, 5): 1}, (11, 5): {(11, 6): 1, (11, 4): 1}, (11, 6): {(11, 5): 1, (10, 6): 1}, (11, 7): {(12, 7): 1, (10, 7): 1, (11, 8): 1}, (11, 8): {(12, 8): 1, (11, 7): 1}, (11, 9): {(11, 10): 1, (10, 9): 1}, (11, 10): {(11, 11): 1, (11, 9): 1, (12, 10): 1}, (11, 11): {(11, 10): 1, (10, 11): 1}, (11, 12): {(11, 13): 1, (10, 12): 1}, (11, 13): {(11, 12): 1, (11, 14): 1}, (11, 14): {(11, 13): 1, (12, 14): 1}, (12, 0): {(13, 0): 3, (11, 0): 1}, (12, 1): {(13, 1): 1, (11, 1): 1}, (12, 2): {(12, 3): 7, (11, 2): 1}, (12, 3): {(12, 2): 7, (12, 4): 1}, (12, 4): {(12, 5): 1, (11, 4): 8, (12, 3): 1}, (12, 5): {(12, 4): 1}, (12, 6): {(12, 7): 1}, (12, 7): {(11, 7): 1, (13, 7): 1, (12, 6): 1}, (12, 8): {(11, 8): 1}, (12, 9): {(12, 10): 9}, (12, 10): {(12, 9): 9, (11, 10): 1, (12, 11): 1}, (12, 11): {(12, 12): 1, (12, 10): 1}, (12, 12): {(12, 11): 1}, (12, 13): {(13, 13): 1}, (12, 
14): {(13, 14): 1, (11, 14): 1}, (13, 0): {(12, 0): 3}, (13, 1): {(13, 2): 2, (12, 1): 1}, (13, 2): {(13, 3): 1, (13, 1): 2}, (13, 3): {(13, 2): 1, (13, 4): 1}, (13, 4): {(13, 5): 1, (13, 3): 1}, (13, 5): {(13, 4): 1, (14, 5): 1}, (13, 6): {(13, 7): 1}, (13, 7): {(13, 8): 1, (13, 6): 1, (12, 7): 1}, (13, 8): {(14, 8): 1, (13, 7): 1}, (13, 9): {(14, 9): 1}, (13, 10): {(14, 10): 1}, (13, 11): {(14, 11): 1, (13, 12): 1}, (13, 12): {(13, 11): 1, (13, 13): 1}, (13, 13): {(14, 13): 1, (12, 13): 1, (13, 12): 1}, (13, 14): {(12, 14): 1}, (14, 0): {(14, 1): 1}, (14, 1): {(14, 0): 1, (15, 1): 1}, (14, 2): {(14, 3): 1}, (14, 3): {(14, 4): 1, (14, 2): 1}, (14, 4): {(15, 4): 7, (14, 5): 1, (14, 3): 1}, (14, 5): {(14, 4): 1, (14, 6): 1, (13, 5): 1}, (14, 6): {(14, 5): 1, (14, 7): 6}, (14, 7): {(14, 6): 6}, (14, 8): {(13, 8): 1, (14, 9): 1}, (14, 9): {(14, 8): 1, (13, 9): 1}, (14, 10): {(15, 10): 1, (13, 10): 1}, (14, 11): {(14, 12): 1, 
(13, 11): 1}, (14, 12): {(15, 12): 1, (14, 11): 1}, (14, 13): {(13, 13): 1, (14, 14): 1}, (14, 14): {(15, 14): 1, (14, 13): 1}, (15, 0): {(16, 0): 1}, (15, 
1): {(16, 1): 1, (14, 1): 1}, (15, 2): {(15, 3): 1}, (15, 3): {(16, 3): 1, (15, 2): 1}, (15, 4): {(14, 4): 7, (15, 5): 1}, (15, 5): {(15, 6): 1, (16, 5): 1, (15, 4): 1}, (15, 6): {(15, 5): 1, (15, 7): 4}, (15, 7): {(15, 6): 4}, (15, 8): {(16, 8): 1}, (15, 9): {(16, 9): 1}, (15, 10): {(15, 11): 1, (14, 10): 1, (16, 10): 1}, (15, 11): {(15, 12): 1, (15, 10): 1}, (15, 12): {(14, 12): 1, (15, 11): 1, (15, 13): 6}, (15, 13): {(15, 12): 6}, (15, 14): {(14, 14): 1}, (16, 0): {(17, 0): 1, (15, 0): 1}, (16, 1): {(17, 1): 1, (15, 1): 1}, (16, 2): {(17, 2): 1}, (16, 3): {(17, 3): 1, (15, 3): 1}, (16, 4): {(16, 5): 1}, (16, 5): 
{(17, 5): 1, (15, 5): 1, (16, 6): 1, (16, 4): 1}, (16, 6): {(16, 7): 1, (16, 5): 1}, (16, 7): {(16, 8): 1, (16, 6): 1}, (16, 8): {(16, 7): 1, (16, 9): 9, (15, 8): 1}, (16, 9): {(17, 9): 1, (16, 10): 1, (16, 8): 9, (15, 9): 1}, (16, 10): {(16, 9): 1, (16, 11): 1, (15, 10): 1}, (16, 11): {(16, 10): 1, (17, 11): 1}, (16, 12): {(17, 12): 1}, (16, 13): {(16, 14): 1, (17, 13): 1}, (16, 14): {(16, 13): 1}, (17, 0): {(17, 1): 5, (16, 0): 1}, (17, 1): {(17, 2): 1, (16, 1): 1, (17, 0): 5, (18, 1): 1}, (17, 2): {(17, 3): 1, (16, 2): 1, (17, 1): 1}, (17, 3): {(16, 3): 1, (17, 2): 1, (17, 4): 1}, (17, 4): {(17, 5): 1, (17, 3): 1}, (17, 5): {(16, 5): 1, (17, 4): 1, (18, 5): 1}, (17, 6): {(17, 7): 1}, (17, 7): {(18, 7): 1, (17, 6): 1, (17, 8): 1}, (17, 8): {(18, 8): 1, (17, 7): 1}, (17, 9): {(18, 9): 1, (16, 9): 1, (17, 10): 10}, (17, 10): {(17, 9): 10}, (17, 11): {(17, 12): 1, (16, 11): 1}, (17, 12): {(17, 13): 1, (16, 12): 1, (17, 11): 1}, (17, 13): {(18, 13): 1, (17, 14): 1, (17, 12): 1, (16, 13): 1}, (17, 14): {(17, 13): 1}, (18, 0): {(18, 1): 4}, (18, 1): {(19, 1): 1, (18, 0): 4, (17, 
1): 1}, (18, 2): {(18, 3): 1, (19, 2): 1}, (18, 3): {(18, 2): 1, (18, 4): 1, (19, 3): 1}, (18, 4): {(19, 4): 1, (18, 3): 1}, (18, 5): {(18, 6): 1, (17, 5): 
1}, (18, 6): {(18, 7): 1, (18, 5): 1}, (18, 7): {(19, 7): 1, (17, 7): 1, (18, 6): 1}, (18, 8): {(17, 8): 1}, (18, 9): {(19, 9): 1, (18, 10): 8, (17, 9): 1}, (18, 10): {(18, 9): 8}, (18, 11): {(19, 11): 1}, (18, 12): {(19, 12): 1}, (18, 13): {(17, 13): 1}, (18, 14): {(19, 14): 1}, (19, 0): {(19, 1): 1, (20, 0): 
1}, (19, 1): {(18, 1): 1, (19, 0): 1}, (19, 2): {(20, 2): 1, (18, 2): 1}, (19, 3): {(18, 3): 1}, (19, 4): {(19, 5): 6, (18, 4): 1}, (19, 5): {(19, 6): 1, (19, 4): 6}, (19, 6): {(19, 5): 1, (20, 6): 1}, (19, 7): {(18, 7): 1, (20, 7): 1}, (19, 8): {(20, 8): 1}, (19, 9): {(20, 9): 1, (18, 9): 1, (19, 10): 1}, (19, 10): {(19, 9): 1, (19, 11): 1, (20, 10): 1}, (19, 11): {(19, 10): 1, (18, 11): 1, (19, 12): 1}, (19, 12): {(20, 12): 1, (19, 13): 1, (19, 11): 1, (18, 12): 1}, (19, 13): {(19, 12): 1, (20, 13): 9}, (19, 14): {(18, 14): 1, (20, 14): 1}, (20, 0): {(20, 1): 1, (19, 0): 1}, (20, 1): {(20, 2): 1, (20, 0): 1}, (20, 
2): {(19, 2): 1, (20, 1): 1, (20, 3): 1}, (20, 3): {(20, 4): 1, (20, 2): 1}, (20, 4): {(20, 3): 1}, (20, 5): {(20, 6): 1}, (20, 6): {(20, 5): 1, (19, 6): 1}, (20, 7): {(19, 7): 1}, (20, 8): {(20, 9): 1, (19, 8): 1}, (20, 9): {(19, 9): 1, (20, 8): 1}, (20, 10): {(20, 11): 1, (19, 10): 1}, (20, 11): {(20, 10): 1}, (20, 12): {(19, 12): 1}, (20, 13): {(20, 14): 1, (19, 13): 9}, (20, 14): {(20, 13): 1, (19, 14): 1}}
'''computeCheesePath(maze,cheese,21,15,(20,14))
file = open("metagraph.py","w")
file.write(str(cheesesPath))
file.close()
print(greedIsFeed((0,0),maze,cheese,21,15)[0])'''