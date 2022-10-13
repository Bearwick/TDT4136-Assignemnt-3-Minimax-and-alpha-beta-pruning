# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
import math

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        #Returns the best move (search restricted by depth)
        def Minimax_Search(depth, gamestate):
            value, move = Max_Value(depth, gamestate)
            return move

        def Max_Value(depth, gameState): #Returns a (utility, move) pair
            #Checks if game is in terminal state, or if it has reached the depth of the tree. 
            if gameState.isWin() or (gameState.isLose()) or (depth == 0):
                return scoreEvaluationFunction(gameState), gameState

            v = float(-math.inf) #Initial v value

            #Checks the scoreEvaluation, of the moves, from min-agent for max-agent´s legal actions, i.e., possible moves.
            # Then chooses the max (best move) of min-agent´s max-outcome.
            for validMove in gameState.getLegalActions(0):
                v2, a2 = Min_Value(self, gameState.generateSuccessor(self.index, validMove), gameState.getNumAgents()-1, 1,validMove, depth-1)
                if v2 > v:
                    v, move = v2, validMove
            return v, move
        
        def Min_Value(self, gameState, numOfGhosts, ghostCounter, move, depth): #Returns a (utility, move) pair
            #Checks if game is in terminal state
            if gameState.isWin() or (gameState.isLose()):
                return scoreEvaluationFunction(gameState), move

            v = float(math.inf) #Initial v value

            #Does the same as Max_value, but also calls on itself for the number of ghosts present. e.g., 2 ghosts will make it call on itself one time
            # Then chooses the max (best move, which is the min) of max-agent´s max-outcome.
            for validMove in gameState.getLegalActions(ghostCounter):
                #Makes sure that Max is only called when every agent has made an action.
                if (numOfGhosts == ghostCounter):
                    v2, a2 = Max_Value(depth, gameState.generateSuccessor(ghostCounter, validMove))
                else:
                    v2, a2 = Min_Value(self, gameState.generateSuccessor(ghostCounter, validMove), numOfGhosts, ghostCounter+1, validMove, depth)
                if v2 < v:
                    v, move = v2, validMove
            return v, move

        #Returns the best move
        return Minimax_Search(self.depth, gameState)
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent): #Code here
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        #Returns the best move (search restricted by depth)
        def Minimax_Search(depth, gamestate): #Returns an action
            value, move = Max_Value(depth, gamestate, float(-math.inf), float(math.inf))
            return move

        def Max_Value(depth, gameState, alfa, beta): #Returns a (utility, move) pair
            #Checks if game is in terminal state, or if it has reached the depth of the tree. 
            if gameState.isWin() or (gameState.isLose()) or (depth == 0):
                return scoreEvaluationFunction(gameState), gameState

            v = float(-math.inf) #Initial v value

            #Checks the scoreEvaluation, of the moves, from min-agent for max-agent´s legal actions, i.e., possible moves.
            # Then chooses the max (best move) of min-agent´s max-outcome.
            for validMove in gameState.getLegalActions(0):
                v2, a2 = Min_Value(self, gameState.generateSuccessor(self.index, validMove), gameState.getNumAgents()-1, 1,validMove, depth-1, alfa, beta)
                
                #Alpha-beta pruning
                #Returns only the (utility, move) pair that is better than beta. I.e., the new utility score must be better that the last, but also greater than what Min_value (beta) has as its best.
                if v2 > v:
                    v, move = v2, validMove
                    alfa = max(alfa, v)
                if v > beta:
                    return v, move
            return v, move
        
        def Min_Value(self, gameState, numOfGhosts, ghostCounter, move, depth, alfa, beta): #Returns a (utility, move) pair
             #Checks if game is in terminal state
            if gameState.isWin() or (gameState.isLose()):
                return scoreEvaluationFunction(gameState), move

            v = float(math.inf) #Initial v value

            #Does the same as Max_value, but also calls on itself for the number of ghosts present. e.g., 2 ghosts will make it call on itself one time
            # Then chooses the max (best move, which is the min) of max-agent´s max-outcome.
            for validMove in gameState.getLegalActions(ghostCounter):
                #Makes sure that Max is only called when every agent has made an action.
                if (numOfGhosts == ghostCounter):
                    v2, a2 = Max_Value(depth, gameState.generateSuccessor(ghostCounter, validMove), alfa, beta)
                else:
                    v2, a2 = Min_Value(self, gameState.generateSuccessor(ghostCounter, validMove), numOfGhosts, ghostCounter+1, validMove, depth, alfa, beta)
                
                #Alpha-beta pruning
                #Returns only the (utility, move) pair that is better than alfa. I.e., the new utility score must be better than the previous, but also less than what Max_value (alfa) has as its best.
                if v2 < v:
                    v, move = v2, validMove
                    beta = min(beta, v)
                if v < alfa:
                    return v, move
            return v, move

        return Minimax_Search(self.depth, gameState)
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
