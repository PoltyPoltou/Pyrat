import AIs.dijkstra as dj
import AIs.backtracking as bt
import AIs.opt as opt
TEAMNAME = "The One"

def isNextCheeseStillHere(path: list, remainingCheeses: list) -> bool:
    return path[0] in remainingCheeses


def tryIntercept(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese) -> (bool, list):
    l1 = dj.targetNextCheese(
        opponentLocation, mazeMap, piecesOfCheese, mazeWidth, mazeHeight)
    l2 = dj.targetPoint(playerLocation, mazeMap,
                        l1[1][0], mazeWidth, mazeHeight)
    return l1[0] > l2[0], l2[1]


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



def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    global path
    print(piecesOfCheese)
    if path == []:
        path.extend(dj.targetNextCheese(playerLocation, mazeMap,
                                        piecesOfCheese, mazeWidth, mazeHeight)[1])
    interception = tryIntercept(
        mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese)
    if interception[0]:
        path = interception[1]
    if not isNextCheeseStillHere(path, piecesOfCheese):
        path = dj.targetNextCheese(
            playerLocation, mazeMap, piecesOfCheese, mazeWidth, mazeHeight)[1]
    return dj.getDirection(path.pop(), playerLocation)
