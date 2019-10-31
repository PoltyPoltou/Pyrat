import AIs.dijkstra as dj
import AIs.backtracking as bt
import AIs.opt as opt
TEAMNAME = "The One"


def isNextCheeseStillHere(path: list, remainingCheeses: list) -> bool:
    return path[0] in remainingCheeses


def isTrapped(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, cheeseToTake) -> (bool, list):
    l1 = dj.targetPoint(
        playerLocation, mazeMap, cheeseToTake, mazeWidth, mazeHeight)
    l2 = dj.targetPoint(opponentLocation, mazeMap,
                        l1[1][0], mazeWidth, mazeHeight)
    if l1[0] > l2[0]:
        if len(piecesOfCheese) < 2:
            return False, []
        cheeseAvailable = [
            cheese for cheese in piecesOfCheese if cheese != l1[1][0]]
        ourPath = dj.targetNextCheese(
            playerLocation, mazeMap, cheeseAvailable, mazeWidth, mazeHeight)
        return l1[0] > l2[0], ourPath[1]
    else:
        return False, []


def tryIntercept(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese) -> (bool, list):
    l1 = dj.targetNextCheese(
        opponentLocation, mazeMap, piecesOfCheese, mazeWidth, mazeHeight)
    l2 = dj.targetPoint(playerLocation, mazeMap,
                        l1[1][0], mazeWidth, mazeHeight)
    return l1[0] > l2[0], l2[1]


def trySecondIntercept(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese) -> (bool, list):
    if len(piecesOfCheese) < 2:
        return False, []
    firstCheese = dj.targetNextCheese(
        opponentLocation, mazeMap, piecesOfCheese, mazeWidth, mazeHeight)
    numberOneCheese = getCheeseNumber(firstCheese[1][0])
    secondCheese = min([bt.cheesesPath[numberOneCheese][i] for i in range(len(
        originalCheese)) if i != numberOneCheese and originalCheese[i] in piecesOfCheese], key=lambda couple: couple[0])
    ourPath = dj.targetPoint(playerLocation, mazeMap,
                             secondCheese[1][0], mazeWidth, mazeHeight)
    return ourPath[0] < firstCheese[0] + secondCheese[0], ourPath[1]


def tryBestIntercept(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, heatMap) -> (bool, list):
    if len(piecesOfCheese) < 2:
        return False, []
    firstCheese = dj.targetNextCheese(
        opponentLocation, mazeMap, piecesOfCheese, mazeWidth, mazeHeight)
    cheeseAvailable = [
        cheese for cheese in piecesOfCheese if cheese != firstCheese[1][0]]
    ourPath = dj.targetNextCheese(
        playerLocation, mazeMap, cheeseAvailable, mazeWidth, mazeHeight)
    theirPath = dj.targetNextCheese(
        opponentLocation, mazeMap, cheeseAvailable, mazeWidth, mazeHeight)
    intercept = trySecondIntercept(
        mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese)
    heatMapTab = getTemperature(heatMap, piecesOfCheese)
    if 1/dj.coupleToIndex(heatMapTab, ourPath[1][0])*(ourPath[0] < theirPath[0]) > 1/dj.coupleToIndex(heatMapTab, intercept[1][0])*(intercept[0]):
        return ourPath[0] < theirPath[0], ourPath[1]
    else:
        return intercept


heatMap = {}


def genHeatMap(mazeMap, mazeWidth, mazeHeight, piecesOfCheese):
    hMap = {}
    for cheese in piecesOfCheese:
        length, dictionnary = dj.dijkstraMethod(
            cheese, mazeMap, mazeWidth, mazeHeight)
        length = [[length[x][y]*(length[x][y] < 50)
                   for y in range(len(length[0]))] for x in range(len(length))]
        hMap.update({cheese: length})
    global heatMap
    heatMap = hMap
    return hMap


def getTemperature(heatMap, cheesesRemaining):
    temperatureMap = heatMap[cheesesRemaining[0]].copy()
    width = len(temperatureMap)
    height = len(temperatureMap[0])
    nbCheese = len(cheesesRemaining)
    for x in range(width):
        for y in range(height):
            for index in range(1, nbCheese):
                temperatureMap[x][y] += heatMap[cheesesRemaining[index]][x][y]
    return temperatureMap


def targetByHeat(heatMap, cheesesRemaining):
    m = getTemperature(heatMap, cheesesRemaining)
    low = [min(m[x]) for x in range(len(m))]
    lowest = min(low)
    x = low.index(lowest)
    y = m[x].index(lowest)
    return (x, y)


def getCheeseNumber(cheesePosition: (int, int)) -> int:
    return originalCheese.index(cheesePosition)


def tryWinningPosition(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese):
    pass


originalCheese = []
path = []


def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    originalCheese.extend(piecesOfCheese.copy())
    bt.computeCheesePath(mazeMap, piecesOfCheese,
                         mazeWidth, mazeHeight, playerLocation)
    genHeatMap(mazeMap, mazeWidth, mazeHeight, piecesOfCheese)
    path.extend(dj.targetPoint(playerLocation, mazeMap,
                               (mazeWidth // 2, mazeHeight // 2), mazeWidth, mazeHeight)[1])


attitude: str = "Ants"
opponentReacting = {"intercept2": False,
                    "intercept1": False, "defence":    False}
excpectedOpponentPosition = []


def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    global path
    global attitude
    if path == []:
        path.extend(dj.targetNextCheese(playerLocation, mazeMap,
                                        piecesOfCheese, mazeWidth, mazeHeight)[1])
        attitude = "greedy"

    interception = tryIntercept(
        mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese)
    if interception[0] and not opponentReacting["intercept1"] and (attitude == "greedy" or attitude == "Ants"):
        path = interception[1]
        attitude = "intercept1"
    elif not opponentReacting["intercept2"] and (attitude == "greedy" or attitude == "Ants"):
        secondIntercept = tryBestIntercept(
            mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, heatMap)
        if secondIntercept[0]:
            attitude = "intercept2"
            path = secondIntercept[1]
    if not isNextCheeseStillHere(path, piecesOfCheese):
        path = dj.targetNextCheese(
            playerLocation, mazeMap, piecesOfCheese, mazeWidth, mazeHeight)[1]
        attitude = "greedy"
    test = isTrapped(mazeMap, mazeWidth, mazeHeight,
                     playerLocation, opponentLocation, piecesOfCheese, path[0])
    if test[0]:
        print("IT'S A TRAP")
        attitude = "defence"
        path = test[1]
    if excpectedOpponentPosition != []:
        if excpectedOpponentPosition.pop() != opponentLocation:
            print("Opponent reacting to" + attitude)
            opponentReacting[attitude] = True

    return dj.getDirection(path.pop(), playerLocation)
