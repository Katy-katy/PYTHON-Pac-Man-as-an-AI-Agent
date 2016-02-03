# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

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
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions() # ['West', 'Stop', 'East', 'North', 'South']


    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    #print "bestScore", bestScore
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
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPosition = successorGameState.getPacmanPosition()# (4,8)
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"


    #print "successorGameState", successorGameState
    #print "newPosition", newPosition # (5,8)
    #print "oldFood", oldFood.asList()
    #print "newGostState", type(newGhostStates) #list
    #print "newScaredTimes", newScaredTimes #[0]
  # print "successorGameState.getScore()", successorGameState.getScore()


    #idea: the Pat-man should not meet the Ghost and he wants to eat!

    result = successorGameState.getScore()
    # first of all - if the next state is win the pacman must do this action
    if successorGameState.isWin():
            return 50000

    # to create a list of all avalible food
    food = oldFood.asList()
    #to create a list of the food which will be avalible after action
    nextFood = successorGameState.getFood().asList()
    foodDistance = 0.0
    for f in food:
      foodDistance = foodDistance + float(manhattanDistance(newPosition, f))
    if len(nextFood) != 0:
      foodAv = foodDistance/float(len(nextFood))


    if len(nextFood) < len(food):
      result = result + 100 # it is good to have some food!
    else:
      result = result - foodAv# the Pat-man should go in the direction of food

    #to create a list of all possible positions of the ghost
    ghostPos = [ghost.getPosition() for ghost in newGhostStates]
    ghostDis = 0.0
    for g in ghostPos:
      ghostDis = ghostDis + float(manhattanDistance(newPosition, g))

  # I use only the distance form the pat-man to the ghost
    if ghostDis ==2:
      result = result - 2 # the pac-man should not go to this direction
    if ghostDis ==1:
      result = result - 5000 # the pac-man must not go to this direction

    return result





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
    self.treeDepth = int(depth)

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

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    # I used the idea from the page wich was provided during a lecture
    # It is a page with pseodo code for Alpha-Beta-Search, but I used it
    # for minmax agent, too. The main difference is that I do not use
    # alfa and beta for minMax agent.
    # But in the both cases (nimMaxAgent and AlphaBetaAgent I do the
    # terminate test inside maxValue and minValue functions

    # self.treeDepth == 0 means we has reached the bottom of the tree and now we are "going back"
    if self.treeDepth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

    value = float("-inf")# initially the value is the negative infinity

    #the list of legal action for Pat-man
    legalActions = gameState.getLegalActions(0)

    #remove the Directions.STOP
    legalActions.remove(Directions.STOP)

    action = Directions.STOP# the function will return STOP if leght of legal action is 0
                            # actually, I am not sure if it is possible to have len(legalAction) = 0
                            # but we need to initialize variable "action" anyway

    #we have to chose the best action
    for actions in legalActions:
            # for every action in Legal Actions we need to find the next state and use it to calculate min possible value
            state = gameState.generateSuccessor(0, actions)

            v = self.minValue(state, self.treeDepth, 1)
            if v > value:
                value = v
                action = actions
    return action


  # the function minValue calls the function maxValue to calculate the "next level"
  # we need agentIndex since the function can be used for Pat-man
  def minValue(self, gameState, depth, agentIndex):# we need agentIndex since the function can be used for P
        #depth == 0 means we has reached the bottom of the tree and now we are "going back"
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        v = float("inf")# initially v is the positive infinity
        legalActions = gameState.getLegalActions(agentIndex)

        successorStates = [gameState.generateSuccessor(agentIndex,action) for action in legalActions]
        for s in successorStates:
            if agentIndex == gameState.getNumAgents()-1:# it is Pac-Man
                v = min(v, self.maxValue(s, depth-1))# we are going on the next level of depth
            else:
                v = min(v, self.minValue(s, depth, agentIndex+1))# we can have some Ghosts.Thus we need
        return v                                                #to calculate v for each of them

  def maxValue(self, gameState, depth):
        #depth == 0 means we has reached the bottom of the tree and now we are "going back"
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        v = float("-inf")#initially v is the negative infinity
        legalActions = gameState.getLegalActions(0)# for Pat-man
        successorStates = [gameState.generateSuccessor(0,action) for action in legalActions]
        for s in successorStates:
            v = max(v, self.minValue(s, depth, 1))
        return v



class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"

    # actually, the function is almost the same as getAction form MinMaxAgent,
    # but I added alfa and betta here

    # self.treeDepth == 0 means we has reached the bottom of the tree and now we are "going back"
    if self.treeDepth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

    value = float("-inf")# initially the value is the negative infinity
    alfa = float("-inf")# initially alfa is the negative infinity
    betta = float("inf")# and betta is positive infinity

    #the list of legal action for Pat-man
    legalActions = gameState.getLegalActions(0)

    #remove the Directions.STOP
    legalActions.remove(Directions.STOP)

    action = Directions.STOP# the function will return STOP if leght of legal action is 0
                            # actually, I am not sure if it is possible to have len(legalAction) = 0
                            # but we need to initialize variable "action" anyway

    #we have to chose the best action
    for actions in legalActions:
            # for every action in Legal Actions we need to find the next state and use it to calculate min possible value
            state = gameState.generateSuccessor(0, actions)
            v = self.minValue(state, self.treeDepth, 1, alfa, betta)
            if alfa < v:
              alfa = v
            if v > value:
                value = v
                action = actions # we need max value here
    return action


  # the function minValue calls the function maxValue to calculate the "next level"
  # we need agentIndex since the function can be used for Pat-man
  def minValue(self, gameState, depth, agentIndex, alfa, betta):# we need agentIndex since the function can be used for P
        #depth == 0 means we has reached the bottom of the tree and now we are "going back"
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        v = float("inf")# initially v is the positive infinity
        legalActions = gameState.getLegalActions(agentIndex)

        successorStates = [gameState.generateSuccessor(agentIndex,action) for action in legalActions]
        for s in successorStates:
            if agentIndex == gameState.getNumAgents()-1:# it is Pac-Man
                v = min(v, self.maxValue(s, depth-1, alfa, betta))# we are going on the next level of depth
            else:
                v = min(v, self.minValue(s, depth, agentIndex+1, alfa, betta))# we can have some Ghosts.Thus we need
            if v < alfa:                                                         #to calculate v for each of them
              return v
            if betta < v:
              betta = v # we need the min value here

        return v


  def maxValue(self, gameState, depth, alfa, betta):# now we also need alfa and betta
        #depth == 0 means we has reached the bottom of the tree and now we are "going back"
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        v = float("-inf")#initially v is the negative infinity
        legalActions = gameState.getLegalActions(0)# for Pat-man
        successorStates = [gameState.generateSuccessor(0,action) for action in legalActions]
        for s in successorStates:
            v = max(v, self.minValue(s, depth, 1, alfa, betta))
            if v > betta:
              return v
            if v > alfa:
              alfa = v
        return v

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

    value = float("-inf")# initially the value is the negative infinity

    #the list of legal action for Pat-man
    legalActions = gameState.getLegalActions(0)

    #remove the Directions.STOP
    legalActions.remove(Directions.STOP)

    action = Directions.STOP# the function will return STOP if leght of legal action is 0
                            # actually, I am not sure if it is possible to have len(legalAction) = 0
                            # but we need to initialize variable "action" anyway

    #we have to chose the best action
    for actions in legalActions:
            # for every action in Legal Actions we need to find the next state and use it to calculate min possible value
            state = gameState.generateSuccessor(0, actions)

            v = self.expValue(state, 0, 1)# depth, agent
            if v > value:
                value = v
                action = actions
    return action

  def maxValue(self, state, depth, agentIndex):

            if depth == self.treeDepth:
                return self.evaluationFunction(state)# we reached the botton level
            else:
                legalActions = state.getLegalActions(agentIndex)
                if len(legalActions) != 0:# we have some actions to chose from
                    val = float('-inf')
                else:
                    val = self.evaluationFunction(state)
                for action in state.getLegalActions(agentIndex):
                    a = self.expValue(state.generateSuccessor(agentIndex, action), depth, agentIndex + 1)
                    if a > val:
                      val = a

                return val # return max value


  def expValue(self, state, depth, agentIndex):
            if depth == self.treeDepth:
                  return self.evaluationFunction(state)# we reached the botton level
            else:
                  val = 0;
                  legalActions = state.getLegalActions(agentIndex)
                  for action in legalActions:
                        if agentIndex == state.getNumAgents() - 1:
                            val = val + self.maxValue( state.generateSuccessor(agentIndex, action),depth+1, 0)
                        else:
                            val = val + self.expValue(state.generateSuccessor(agentIndex, action),depth, agentIndex + 1)
                  if len(legalActions) != 0:
                        val =  val / len(legalActions)# expected value
                  else:
                        val = self.evaluationFunction(state)

                  return val


def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"

  # I am going to use this information:
  newPosition = currentGameState.getPacmanPosition()# (4,8)
  food = currentGameState.getFood()
  newGhostStates = currentGameState.getGhostStates()

  #Actually, the idea is exactly same as for ReflexAgent:
  #the Pat-man should not meet the Ghost and he wants to eat!

  result = currentGameState.getScore()
  # first of all - if the next state is win the pacman must do this action
  if currentGameState.isWin():
            return 50000

  # to create a list of all avalible food
  foodList = food.asList()
  #to create a list of the food which will be avalible after action
  nextFood = currentGameState.getFood().asList()
  foodDistance = 0.0
  for f in foodList:
    foodDistance = foodDistance + float(manhattanDistance(newPosition, f))
  if len(nextFood) != 0:
    foodAv = foodDistance/float(len(nextFood))


  if len(nextFood) < len(foodList):
    result = result + 100 # it is good to have some food!
  else:
    result = result - foodAv# the Pat-man should go in the direction of food

  #to create a list of all possible positions of the ghost
  ghostPos = [ghost.getPosition() for ghost in newGhostStates]
  ghostDis = 0.0
  for g in ghostPos:
    ghostDis = ghostDis + float(manhattanDistance(newPosition, g))

  # I use only the distance form the pat-man to the ghost
  if ghostDis ==2:
    result = result - 2 # the pac-man should not go to this direction
  if ghostDis ==1:
    result = result - 5000 # the pac-man must not go to this direction

  return result


# Abbreviation
better = betterEvaluationFunction


class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()







