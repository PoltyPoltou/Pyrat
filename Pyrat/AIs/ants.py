import random as rd
import AIs.metagraph as mg
import AIs.backtracking as bt
import AIs.dijkstra as dj
import time


def antColonyHeuristic(numberOfAnts, metaGraph):
    antColony = [Ant(3, 1, 0.9) for x in range(numberOfAnts)]
    pheromonesTable = [[0]*(len(metaGraph)-1) for x in range(len(metaGraph)-1)]
    decayRate = 0.1
    begin = time.time()
    best = float('inf')
    bestPath = []
    while time.time() - begin < 1:
        antsWork(antColony, pheromonesTable, metaGraph)
        antColony.sort(key=lambda ant: ant.lastScore)
        if best > antColony[0].lastScore:
            best = antColony[0].lastScore
            bestPath = antColony[0].lastSolution
        pheromoneDecay(pheromonesTable, decayRate)
        daemonWork()
    # print("ants " + str(bestPath))
    return (best, bestPath)


def antsWork(antColony: list, pheromonesTable: list, metaGraph: list):
    for ant in antColony:
        ant.createSolution(pheromonesTable, metaGraph)
    pheromoneDepositElitist(antColony, pheromonesTable, 5)


def pheromoneDecay(pheromonesTable: list, decayRate: float):
    for i in range(len(pheromonesTable)):
        for j in range(len(pheromonesTable[i])):
            pheromonesTable[i][j] *= (1-decayRate)


def pheromoneDeposit(antColony: list, pheromonesTable: list):
    for ant in antColony:
        for i in range(len(ant.lastSolution)-1):
            pheromonesTable[ant.lastSolution[i]
                            ][ant.lastSolution[i+1]] = pheromonesTable[ant.lastSolution[i]
                                                                       ][ant.lastSolution[i+1]] + 1/ant.lastScore


def pheromoneDepositElitist(antColony: list, pheromonesTable: list, rank: int):
    bestAnts = antColony.copy()
    bestAnts.sort(key=lambda ant: ant.lastScore)
    for k in range(rank):
        ant = bestAnts[k]
        for i in range(len(ant.lastSolution)-1):
            pheromonesTable[ant.lastSolution[i]
                            ][ant.lastSolution[i+1]] += (rank-k)/ant.lastScore


def daemonWork():
    pass


class Ant:
    def __init__(self, alpha, beta, exploitationRatio):
        self.lastSolution = []
        self.lastScore = -1
        self.alpha = alpha
        self.beta = beta
        self.exploitationRatio = exploitationRatio

    def createSolution(self, pheromones: list, metaGraph: list):
        solution = [-1]
        score = 0
        nbCheese = len(metaGraph) - 1
        for step in range(len(metaGraph)-1):
            randExplo = rd.random()
            weightsNotNormalized = []
            for j in range(nbCheese):
                if j not in solution:
                    weightsNotNormalized.append(pheromones[solution[-1]][j]**self.alpha + 1/metaGraph[solution[-1]]
                                                [j][0]**self.beta)
                else:
                    weightsNotNormalized.append(0)
            # there is a chance to just take the best path instead
            if randExplo > self.exploitationRatio:
                # we are normalizing after for efficiency
                totalWeight = sum(weightsNotNormalized)
                weights = [x / totalWeight for x in weightsNotNormalized]
                randFloat = rd.random()
                index = 0
                totalCap = 0
                while index != nbCheese-1 and randFloat >= totalCap + weights[index]:
                    index += 1
                    totalCap += weights[index]

            else:
                index = weightsNotNormalized.index(max(weightsNotNormalized))
            solution.append(index)
            score += metaGraph[solution[-2]][index][0]
        self.lastSolution = solution[1:]
        self.lastScore = score


path = []
order = 0
index = 0
originalCheese = []


def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    global originalCheese
    originalCheese = piecesOfCheese[:]
    bt.computeCheesePath(mazeMap, piecesOfCheese,
                         mazeWidth, mazeHeight, playerLocation)
    global order
    order = antColonyHeuristic(20, bt.cheesesPath)[1]
    path.extend(bt.cheesesPath[-1][order[index]][1])
    return


def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    global index
    global path
    l1 = dj.targetNextCheese(
        opponentLocation, mazeMap, piecesOfCheese, mazeWidth, mazeHeight)
    l2 = dj.targetPoint(playerLocation, mazeMap,
                        l1[1][0], mazeWidth, mazeHeight)
    if l1[0] > l2[0]:
        path = []
        path.extend(l2[1])
        index = order.index(originalCheese.index(path[0]))
    if path == []:
        lastIndex = index
        index += 1
        if index < len(order) and originalCheese[order[index]] not in piecesOfCheese:
            i = 1
            bestIndex = 0
            cheesesRemaining = [x for x in range(
                len(originalCheese)) if originalCheese[x] in piecesOfCheese]
            bestWeight = bt.cheesesPath[order[lastIndex]
                                        ][cheesesRemaining[0]][0]
            while i < len(cheesesRemaining):
                if bt.cheesesPath[order[lastIndex]][cheesesRemaining[i]][0] < bestWeight:
                    bestIndex = i
                    bestWeight = bt.cheesesPath[order[lastIndex]
                                                ][cheesesRemaining[i]][0]
                i += 1
            p = bt.cheesesPath[order[lastIndex]
                               ][cheesesRemaining[bestIndex]][1]
            index = order.index(cheesesRemaining[bestIndex])
            path.extend(p)
        elif index >= len(order):
            path.extend(bt.greedIsFeed(playerLocation,
                                       originalCheese, [originalCheese.index(x) for x in piecesOfCheese if x in originalCheese])[1])
        else:
            path.extend(bt.cheesesPath[order[lastIndex]
                                       ][order[index]][1])
    return dj.getDirection(path.pop(), playerLocation)
