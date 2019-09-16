# Template file to create an AI for the game PyRat
# http://formations.telecom-bretagne.eu/pyrat


###############################
# Please put your imports here
import random

###############################
# When the player is performing a move, it actually sends a character to the main program
# The four possibilities are defined here
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'


###############################
# Please put your global variables here
visitedArray = []
lastPlaceVisited = (0, 0)
directions = {(0, 1): MOVE_UP, (0, -1): MOVE_DOWN,
              (1, 0): MOVE_RIGHT, (-1, 0): MOVE_LEFT}

###############################
# Preprocessing function
# The preprocessing function is called at the start of a game
# It can be used to perform intensive computations that can be
# used later to move the player in the maze.
###############################
# Arguments are:
# mazeMap : dict(pair(int, int), dict(pair(int, int), int))
# mazeWidth : int
# mazeHeight : int
# playerLocation : pair(int, int)
# opponentLocation : pair(int,int)
# piecesOfCheese : list(pair(int, int))
# timeAllowed : float
###############################
# This function is not expected to return anything


def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    pass
    ###############################
    # Turn function
    # The turn function is called each time the game is waiting
    # for the player to make a decision (a move).
    ###############################
    # Arguments are:
    # mazeMap : dict(pair(int, int), dict(pair(int, int), int))
    # mazeWidth : int
    # mazeHeight : int
    # playerLocation : pair(int, int)
    # opponentLocation : pair(int, int)
    # playerScore : float
    # opponentScore : float
    # piecesOfCheese : list(pair(int, int))
    # timeAllowed : float
    ###############################
    # This function is expected to return a move


def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    choices = []
    # for each neighboor available check if it was visited if not add it to the list choices
    for dir in mazeMap[playerLocation].keys():
        if dir not in visitedArray:
            choices.append(getDirection(dir, playerLocation))
    # if choices is empty then we just choose a possible move randomly
    if choices == []:
        for place in mazeMap[playerLocation].keys():
            choices.append(getDirection(place, playerLocation))
    visitedArray.append(playerLocation)
    return random.choice(choices)

# allows to get the move needed to go from position to direction


def getDirection(direction, position):
    (fstA, sndA) = direction
    (fstB, sndB) = position
    fst = fstA - fstB
    snd = sndA-sndB
    return directions[(fst, snd)]
