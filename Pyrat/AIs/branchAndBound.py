###############################
# Please put your imports here
import AIs.backtracking as bt
import heapq
###############################
# Please put your global variables here

# upperBound to the constructing solution, we will use a greedy method to get it


def upperBound(constructingSolution, mazeMap, playerPos, piecesOfCheese, mazeWidth, mazeHeight):
    weight = bt.cheesesPath[-1][constructingSolution[0]][0]
    for i in range(len(constructingSolution) - 1):
        weight += bt.cheesesPath[constructingSolution[i]
                                 ][constructingSolution[i + 1]][0]
    finalPosition = constructingSolution[-1]
    cheeseTaken = [piecesOfCheese[x] for x in constructingSolution]
    cheeseRemaining = [c for c in piecesOfCheese if c not in cheeseTaken]
    w, p = bt.greedIsFeed(finalPosition, mazeMap,
                          cheeseRemaining, mazeWidth, mazeHeight)
    return weight + w


def branchAndBound(mazeMap, playerPos, piecesOfCheese, mazeWidth, mazeHeight):
    heap = []
    n = len(piecesOfCheese)
    bestScore, bestPath = bt.greedIsFeed(
        playerPos, mazeMap, piecesOfCheese, mazeWidth, mazeHeight)
    heapq.heappush(heap, (0, []))
    while heap != []:
        currentSolution = heapq.heappop(heap)
        # we get the sons of the current solution with this line :
        nextSolutions = [currentSolution+[x]
                         for x in range(n) if x not in currentSolution]
        if len(nextSolutions) >= 1:
            # we get the lower and upper bound of these solutions
            # if their lowerB is worse than bestScore we discard them
            # we put the rest in the heap with their respected priority

            lowerBounds = [bt.lowerBound(
                sol, mazeMap, playerPos, piecesOfCheese, mazeWidth, mazeHeight) for sol in nextSolutions]
            retainedSol = [(upperBound(nextSolutions[i], mazeMap, playerPos,
                                       piecesOfCheese, mazeWidth, mazeHeight), lowerBounds[i], nextSolutions[i]) for i in range(n) if lowerBounds[i] < bestScore]
            for sol in retainedSol:
                heapq.heappush(heap, sol)
        # if nextSolutions is empty or one cheese away to be over it means we are on a leaf then we check the score
        else:
            w, p = bt.getPath(
                nextSolutions[0], playerPos, mazeMap, piecesOfCheese, mazeWidth, mazeHeight)
            if w < bestScore:
                bestScore = w
                bestPath = p
                # when we found a better solution we do a cleanup of the heap:
                # we check again the lower bound and pop the ones not useful anymore
                for i in range(len(heap)):
                    upperB, lowerB, sol = heap[i]
                    if lowerB > bestScore:
                        heap.pop(i)

    return bestScore, bestPath


def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    return


def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    return
