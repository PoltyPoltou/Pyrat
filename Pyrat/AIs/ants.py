import random as rd
import AIs.metagraph as mg
import AIs.backtracking as bt
import AIs.dijkstra as dj
import time


def antColonyHeuristic(numberOfAnts, metaGraph, maxTime):
    antColony = [Ant(3, 1, 0.9) for x in range(numberOfAnts)]
    pheromonesTable = [[0]*(len(metaGraph)-1) for x in range(len(metaGraph)-1)]
    decayRate = 0.1
    begin = time.time()
    best = float('inf')
    bestPath = []
    while time.time() - begin < maxTime:
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
    order = antColonyHeuristic(20, bt.cheesesPath, 1)[1]
    path.extend(bt.cheesesPath[-1][order[index]][1])
    return


def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    global index
    global path
    global order
    if path == []:
        lastIndex = index
        index += 1
        while index < len(order) and originalCheese[order[index]] not in piecesOfCheese:
            index += 1
        if index == len(order):
            p = dj.targetNextCheese(
                playerLocation, mazeMap, piecesOfCheese, mazeWidth, mazeHeight)[1]
        else:
            p = bt.cheesesPath[order[lastIndex]][order[index]][1]
        path.extend(p)
    if not dj.isNextCheeseStillHere(path, piecesOfCheese):
        lastIndex = index
        index += 1
        while index < len(order) and originalCheese[order[index]] not in piecesOfCheese:
            index += 1
        if index == len(order):
            path = dj.targetNextCheese(
                playerLocation, mazeMap, piecesOfCheese, mazeWidth, mazeHeight)[1]
        else:
            path = dj.targetPoint(
                playerLocation, mazeMap, originalCheese[order[index]], mazeWidth, mazeHeight)
    return dj.getDirection(path.pop(), playerLocation)
