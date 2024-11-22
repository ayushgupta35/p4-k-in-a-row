'''
ayushg35_KInARow.py
Authors: Gupta, Ayush; Epstein, Benjamin

An agent for playing "K-in-a-Row with Forbidden Squares" and related games.
CSE 473, University of Washington

THIS IS A TEMPLATE WITH STUBS FOR THE REQUIRED FUNCTIONS.
YOU CAN ADD WHATEVER ADDITIONAL FUNCTIONS YOU NEED IN ORDER
TO PROVIDE A GOOD STRUCTURE FOR YOUR IMPLEMENTATION.

'''

from agent_base import KAgent
from game_types import State, Game_Type
from winTesterForK import winTesterForK

AUTHORS = 'Ayush Gupta and Benjamin Epstein'

import time # You'll probably need this to avoid losing a
 # game due to exceeding a time limit.

# Create your own type of agent by subclassing KAgent:

class OurAgent(KAgent):  # Keep the class name "OurAgent" so a game master
    # knows how to instantiate your agent class.

    def __init__(self, twin=False):
        self.twin = twin
        self.nickname = 'Houdini'
        if twin:
            self.nickname += '2'
        self.long_name = 'Lamar Jackson'
        if twin:
            self.long_name += ' 2.0'
        self.persona = 'Dual Threat'
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
        self.playing = "X"

    def introduce(self):
        intro = f'''
        Yo, I am {self.nickname}, better known as {self.long_name}.
        Built to compete, built to win. That’s it, that’s the mindset.
        Credit to Ayush Gupta and Benjamin Epstein for putting me together, but now it’s all me.
        '''
        if self.twin:
            intro += "Oh, and there’s two of us. Twice as much heat coming your way."
        intro += "\nLet’s see if you can keep up."
        return intro

    # Receive and acknowledge information about the game from
    # the game master:
    def prepare(
        self,
        game_type,
        what_side_to_play,
        opponent_nickname,
        expected_time_per_move = 0.1, # Time limits can be
                                      # changed mid-game by the game master.
        utterances_matter=True):      # If False, just return 'OK' for each utterance.

        # Write code to save the relevant information in variables
        # local to this instance of the agent.
        # Game-type info can be in global variables.
        self.game_type = game_type
        self.side = what_side_to_play
        self.opponent_nickname = opponent_nickname
        self.time_per_move = expected_time_per_move
        return "OK"
   
    # The core of your agent's ability should be implemented here:             
    def makeMove(self, currentState, currentRemark, timeLimit=10000):
        best_move, _ = self.minimax(currentState, depthRemaining=3, pruning=True, alpha=float('-inf'), beta=float('inf'))
        if best_move is None or not isinstance(best_move, (tuple, list)) or len(best_move) != 2:
            print(f"Invalid best_move returned by minimax: {best_move}")
            return None, "No valid moves available. Passing the turn."

        newState = self.applyMove(currentState, best_move)
        newRemark = "Your turn!"
        return [[best_move, newState], newRemark]

    # The main adversarial search function:
    def minimax(self,
            state,
            depthRemaining,
            pruning=False,
            alpha=None,
            beta=None,
            zHashing=None):
        if depthRemaining == 0 or self.isTerminal(state):
            eval_value = self.staticEval(state)
            print(f"Terminal state or depth 0 reached. Eval: {eval_value}")
            return eval_value, None  # Always return eval and None for move.

        best_move = None
        if state.whose_move == "X":  # Maximizing player
            max_eval = float('-inf')
            for move, newState in self.getSuccessors(state):
                eval, _ = self.minimax(newState, depthRemaining - 1, pruning, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                if pruning:
                    alpha = max(alpha, eval)
                    if beta is not None and alpha >= beta:
                        break
            print(f"Maximizing move selected: {best_move} with eval: {max_eval}")
            return max_eval, best_move
        else:  # Minimizing player
            min_eval = float('inf')
            for move, newState in self.getSuccessors(state):
                eval, _ = self.minimax(newState, depthRemaining - 1, pruning, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                if pruning:
                    beta = min(beta, eval)
                    if alpha is not None and alpha >= beta:
                        break
            print(f"Minimizing move selected: {best_move} with eval: {min_eval}")
            return min_eval, best_move
        # Only the score is required here but other stuff can be returned
        # in the list, after the score, in case you want to pass info
        # back from recursive calls that might be used in your utterances,
        # etc. 
 
    def staticEval(self, state):
        x_count = sum(row.count('X') for row in state.board)
        o_count = sum(row.count('O') for row in state.board)
        return x_count - o_count

    def isTerminal(self, state):
        for row in range(len(state.board)):
            for col in range(len(state.board[0])):
                if state.board[row][col] != ' ':
                    if winTesterForK(state, [row, col], self.game_type.k) != "No win":
                        return True
        if all(cell != ' ' for row in state.board for cell in row):
            return True
        return False

    def getSuccessors(self, state):
        successors = []
        for i in range(len(state.board)):
            for j in range(len(state.board[0])):
                if state.board[i][j] == ' ':
                    newState = State(old=state)
                    newState.board[i][j] = state.whose_move
                    newState.change_turn()
                    successors.append(((i, j), newState))
        if not successors:
            print("No successors generated. State:")
            print(state)
        return successors

    def applyMove(self, state, move):
        if not isinstance(move, (tuple, list)) or len(move) != 2:
            raise ValueError(f"Invalid move format: {move}")
        row, col = move
        newState = State(old=state)
        newState.board[row][col] = state.whose_move
        newState.change_turn()
        return newState
 
# OPTIONAL THINGS TO KEEP TRACK OF:

#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances

