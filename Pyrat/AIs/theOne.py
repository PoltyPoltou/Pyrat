import AIs.dijkstra as dj
import AIs.backtracking as bt
import AIs.opt as opt
TEAMNAME = "The One"


def isNextCheeseStillHere(path: list, remainingCheeses: list) -> bool:
    return path[0] in remainingCheeses


def isTrapped(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese) -> bool:
    l1 = dj.targetNextCheese(
        playerLocation, mazeMap, piecesOfCheese, mazeWidth, mazeHeight)
    l2 = dj.targetPoint(opponentLocation, mazeMap,
                        l1[1][0], mazeWidth, mazeHeight)
    return l1[0] > l2[0]


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
    path.extend(dj.targetPoint(playerLocation, mazeMap,
                               (mazeWidth // 2, mazeHeight // 2), mazeWidth, mazeHeight)[1])


WAIT_TURN = 40
turns = 0


def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    global path
    if path == []:
        path.extend(dj.targetNextCheese(playerLocation, mazeMap,
                                        piecesOfCheese, mazeWidth, mazeHeight)[1])
    interception = tryIntercept(
        mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese)
    if interception[0]:
        path = interception[1]
        print("intercept")
    else:
        secondIntercept = trySecondIntercept(
            mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese)
        if secondIntercept[0]:
            print("second intercept")
            path = secondIntercept[1]
    if not isNextCheeseStillHere(path, piecesOfCheese):
        path = dj.targetNextCheese(
            playerLocation, mazeMap, piecesOfCheese, mazeWidth, mazeHeight)[1]
    if isTrapped(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese):
        intercept = trySecondIntercept(
            mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese)
        if intercept[0]:
            print("IT'S A TRAP")
            path = intercept[1]
    return dj.getDirection(path.pop(), playerLocation)
