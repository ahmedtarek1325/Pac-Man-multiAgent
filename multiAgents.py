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
from math import inf 
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
        #### ####### EVALUATION FUNCTION OF FOOD #############
        ############### to be adujsted by a search algorithm ##########
        temp_minimum_dist=100;
        _distance= 0;
        for i in newFood.asList():
            if(newFood[i[0]][i[1]]==True):
                Food_dsitance=manhattanDistance(newPos,i);
                if(Food_dsitance<temp_minimum_dist):
                    temp_minimum_dist=Food_dsitance;
        food_min_distance=temp_minimum_dist;
        
        #print("minimal distance expectation: ",food_min_distance)
        
        ############################################################
        ############################################################
        #####################  ghost contribution in the  evaluation####
        min_ghost_location=50;
        for i in newGhostStates:
            temp_ghost_loc=manhattanDistance(newPos, i.getPosition());
            if(temp_ghost_loc<min_ghost_location):
                min_ghost_location=temp_ghost_loc;
        #################################################################
        ########################## Capsules case ########################        

        return (successorGameState.getScore()+1/food_min_distance*10 - 1/(min_ghost_location+1)*15);
      

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
        # Collect legal moves and successor states
        
        def max_value(gameState,Depth = 0,agentIndex = 0):
            if agentIndex==0:
                Pac_Moves = gameState.getLegalActions(agentIndex)
                if len(Pac_Moves) == 0 or Depth==self.depth:
                    return self.evaluationFunction(gameState)
                maxi = -float('inf')
                for action in Pac_Moves:
                    ####### always communicarte with the firt agent 
                    maxi = max(maxi, min_value(gameState.generateSuccessor(0, action),Depth,1))
                return maxi                

        def min_value(gameState,Depth = 0,agentIndex = 1):
            ## ghost 1 [N,W]  ghost 2 =[E,W,S]
            Ghost_Moves = gameState.getLegalActions(agentIndex)
            if(Depth == self.depth or len(Ghost_Moves) == 0):
                return self.evaluationFunction(gameState)
            ghostMoves= gameState.getLegalActions(agentIndex)
            mini= float('inf')
            for action in ghostMoves:
                if (agentIndex== gameState.getNumAgents()-1):
                    mini=min(mini,max_value(gameState.generateSuccessor(agentIndex,action),Depth + 1,0))
                else: 
                    mini = min(mini, min_value(gameState.generateSuccessor(agentIndex, action),Depth,agentIndex+1))
            return mini

        best_value = -float('inf')
        Pac_Moves = gameState.getLegalActions(0)
        depth=self.depth
        for action in Pac_Moves:
            action_value =min_value(gameState.generateSuccessor(0, action))
            if  action_value is not None and best_value < action_value:
                best_value = action_value
                best_action = action
        
        return best_action

        util.raiseNotDefined()
        # Choose one of the best actions

        
        
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        #best_value = -float('inf')
        #Pac_Moves = gameState.getLegalActions(0)
        #alpha = -(float("inf"))
        #beta = float("inf")
        #for action in Pac_Moves:
        #    action_value =min_value(gameState.generateSuccessor(0, action),alpha,beta)
        #    if  action_value is not None and best_value < action_value:
        #        best_value = action_value
        #        best_action = action
        "*** YOUR CODE HERE ***"
    
        def max_value(gameState,alpha,beta,Depth = 0,agentIndex = 0):
            if agentIndex==0:
                best_value = -float('inf')
                Pac_Moves = gameState.getLegalActions(agentIndex)
                if len(Pac_Moves) == 0 or Depth==self.depth:
                    return [self.evaluationFunction(gameState),]
                maxi = -float('inf')
                for action in Pac_Moves:
                    ####### always communicarte with the firt agent 
                    maxi = max(maxi, min_value(gameState.generateSuccessor(0, action),alpha,beta,Depth,1))
                    if  maxi is not None and best_value < maxi:
                        best_value = maxi
                        best_action = action
                    
                    if maxi >= beta:
                        return [maxi,best_action]
                alpha = max(alpha, maxi)
            return [maxi,best_action]               

        def min_value(gameState,alpha,beta,Depth = 0,agentIndex = 1):
            ## ghost 1 [N,W]  ghost 2 =[E,W,S]
            Ghost_Moves = gameState.getLegalActions(agentIndex)
            if(Depth == self.depth or len(Ghost_Moves) == 0):
                return self.evaluationFunction(gameState)
            ghostMoves= gameState.getLegalActions(agentIndex)
            mini= float('inf')
            for action in ghostMoves:
                if (agentIndex== gameState.getNumAgents()-1):
                    mini=min(mini,max_value(gameState.generateSuccessor(agentIndex,action),alpha,beta,Depth+1,0)[0])
                    if mini <= alpha:
                        return mini
                    beta = min(beta, mini)
                else: 
                    mini = min(mini, min_value(gameState.generateSuccessor(agentIndex, action),alpha,beta,Depth,agentIndex+1))
                    if mini <= alpha:
                        return mini
                beta = min(beta, mini)
            return mini

       
        return max_value(gameState,-float('inf'),float('inf'))[1]


        
        
        
        
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
        def max_value(gameState,Depth = 0,agentIndex = 0):
                
                Pac_Moves = gameState.getLegalActions(agentIndex)
                if len(Pac_Moves) == 0 or Depth==self.depth:
                    return self.evaluationFunction(gameState)
                maxi = -float('inf')
                for action in Pac_Moves:
                    ####### always communicarte with the firt agent 
                    maxi = max(maxi, min_value(gameState.generateSuccessor(0, action),Depth,1))
                
                return maxi           

        def min_value(gameState,Depth = 0,agentIndex = 1):
            ## ghost 1 [N,W]  ghost 2 =[E,W,S]
            sum=0;
            c=0
            Ghost_Moves = gameState.getLegalActions(agentIndex)
            if(Depth == self.depth or len(Ghost_Moves) == 0):
                return self.evaluationFunction(gameState)
            ghostMoves= gameState.getLegalActions(agentIndex)
            mini= float('inf')
            for action in ghostMoves:
                if (agentIndex== gameState.getNumAgents()-1):
                    if (mini== float('inf')):
                        counter=1;
                        mini=min(mini,max_value(gameState.generateSuccessor(agentIndex,action),Depth + 1,0))
                    else :
                        mini=mini*counter;
                        mini= mini+max_value(gameState.generateSuccessor(agentIndex,action),Depth + 1,0);
                        counter=counter+1 ;
                        mini=mini/counter;
                else: 
                    mini= float('inf')
                    mini = min(mini, min_value(gameState.generateSuccessor(agentIndex, action),Depth,agentIndex+1))
                    sum=sum+mini;
                    c=c+1;
                    
            if(c!=0):
                mini=sum/c;
            
            return mini

        best_value = -float('inf')
        Pac_Moves = gameState.getLegalActions(0)
        depth=self.depth
        for action in Pac_Moves:
            action_value =min_value(gameState.generateSuccessor(0, action))
            if  action_value is not None and best_value < action_value:
                best_value = action_value
                best_action = action
        
        return best_action
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    

     # Useful information you can extract from a GameState (pacman.py)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    Food_distance=0;
    food_counter=0;
    for i in newFood.asList():
            if(newFood[i[0]][i[1]]==True):
                Food_distance+=manhattanDistance(newPos,i);
                food_counter+=1;
    ###########################################################
    ghostDistance=0;
    x=0;
    penalty=0;
    for j in newGhostStates:
        x=manhattanDistance(newPos, j.getPosition());
        if(x<3):
            penalty-=20;
        elif (x<6):
            penalty-=10;
        else:
            penalty-=1/x*10;

    eval= penalty + 1/(Food_distance+1)*10;
    return eval
    

    

    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
