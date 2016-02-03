## Pac-Man as an AI Agent

![Mockup for feature A](https://github.com/Katy-katy/PYTHON-Pac-Man-as-an-AI-Agent/blob/master/Screen_shot.png)

It is an assignment for "CMPS140: Artificial Intelligence" - Winter 2016 class at University of California Santa Cruz.
My goal was to implement some search functions in multiAgents.py

# evaluationFunction(self, currentGameState, action) in the ReflexAgent(Agent) classs 
This function helps to Pac-Man to behave "rationally." The main idea is that the Pat-Man should not meet the Ghost and he wants to eat!
Thus, from the set of available action Pat-Man choses the action which leads to having some food and where hi will not meet the Ghost.
 My main innovation here is that we do not worry about distance between Pat-Man and Ghost when the distance is bigger than 2.
 
 To run this function:
 python pacman.py --frameTime 0 -p ReflexAgent -k 1
 
#Function getAction(self, gameState) in the MinimaxAgent(MultiAgentSearchAgent) class

This function implements an adversarial search (minimax search).
Now Pat-Man thinks that Ghosts are "rational" agents. Pat-Man is trying to increase his benefits and thinks that Ghosts are trying to decrease his benefits. 
Pat-man evaluates the situation for some next steps. To run this function with evaluating next 4 steps, type:
python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4
The game is running to slow since we expand to much nodes - we will fix it in the next function.

#Function getAction(self, gameState) in the AlphaBetaAgent(MultiAgentSearchAgent) class

Now we are using alpha-beta pruning to more efficiently explore the minimax tree (we expands less nodes).
You can run it:
python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic

#Function getAction(self, gameState) in the ExpectimaxAgent(MultiAgentSearchAgent)

Actually, the ghosts act randomly and are of not optimal minimax agents.
Thus, now Pat-man will "understand" that  he should think about a "chance" and act according Expect Max algorithm. To run:
python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 
