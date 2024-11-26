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

AUTHORS = 'Jane Smith and Laura Lee' 

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
        self.ids = "ayushg35 and bre4"
        self.authors = "Ayush Gupta and Benjamin Epstein"
        self.persona = 'Dual Threat'
        self.voice_info = {'Chrome': 10, 'Firefox': 2, 'other': 0}
        self.playing = "X"

    def introduce(self):
        intro = f'''
        Yo, I am {self.nickname}, better known as {self.long_name}.
        Built to compete, built to win. That’s it, that’s the mindset.
        Credit to {self.authors} ({self.ids}) for putting me together, but now it’s all me.
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
        start_time = time.time()
        best_move = None
        best_value = float('-inf') if self.side == 'X' else float('inf')
        
        depth = 1
        while time.time() - start_time < timeLimit:
            try:
                move, value = self.minimax(currentState, depth, pruning=True, alpha=float('-inf'), beta=float('inf'))
                if (self.side == 'X' and value > best_value) or (self.side == 'O' and value < best_value):
                    best_move, best_value = move, value
                depth += 1
            except TimeoutError:
                break

        new_state = self.perform_move(currentState, best_move)
        remark = "Let’s see how you handle this!"
        
        return [[best_move, new_state], remark]

    # The main adversarial search function:
    def minimax(self,
            state,
            depthRemaining,
            pruning=False,
            alpha=None,
            beta=None,
            zHashing=None):
        if depthRemaining == 0 or state.finished:
            return None, self.staticEval(state)

        possible_moves = self.get_possible_moves(state)
        if state.whose_move == 'X':
            max_eval = float('-inf')
            best_move = None
            for move in possible_moves:
                next_state = self.perform_move(state, move)
                _, eval = self.minimax(next_state, depthRemaining - 1, pruning, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                if pruning:
                    alpha = max(alpha, eval)
                    if beta is not None and beta <= alpha:
                        break
            return best_move, max_eval
        else:
            min_eval = float('inf')
            best_move = None
            for move in possible_moves:
                next_state = self.perform_move(state, move)
                _, eval = self.minimax(next_state, depthRemaining - 1, pruning, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                if pruning:
                    beta = min(beta, eval)
                    if beta is not None and beta <= alpha:
                        break
            return best_move, min_eval
        # Only the score is required here but other stuff can be returned
        # in the list, after the score, in case you want to pass info
        # back from recursive calls that might be used in your utterances,
        # etc. 
 
    def staticEval(self, state):
        board = state.board
        k = self.game_type.k
        maximizing_player = 'X'
        minimizing_player = 'O'

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        score = 0

        def evaluate_line(line):
            """Evaluate a line segment."""
            x_count = line.count(maximizing_player)
            o_count = line.count(minimizing_player)
            spaces = line.count(' ')
            
            # Strongly favor lines with high potential for winning
            if x_count == k:
                return float('inf')  # Winning line
            if o_count == k:
                return float('-inf')  # Opponent wins
            
            # Reward near-complete lines
            if x_count > 0 and o_count == 0:
                return 10 ** x_count  # Favor own lines
            if o_count > 0 and x_count == 0:
                return -(10 ** o_count)  # Block opponent
            
            return 0

        def get_line_segments(i, j, di, dj):
            # Get all possible line segments including (i, j) in the given direction.
            line = []
            for step in range(-k + 1, k):
                ni, nj = i + step * di, j + step * dj
                if 0 <= ni < len(board) and 0 <= nj < len(board[0]):
                    line.append(board[ni][nj])
            return line

        for i in range(len(board)):
            for j in range(len(board[0])):
                for di, dj in directions:
                    line = get_line_segments(i, j, di, dj)
                    if len(line) >= k:
                        score += evaluate_line(line)
        return score
    
    def get_possible_moves(self, state):
        moves = []
        for i in range(len(state.board)):
            for j in range(len(state.board[0])):
                if state.board[i][j] == ' ':
                    moves.append((i, j))
        return moves

    def perform_move(self, state, move):
        new_state = State(old=state)
        i, j = move
        new_state.board[i][j] = state.whose_move
        new_state.change_turn()
        return new_state
 
# OPTIONAL THINGS TO KEEP TRACK OF:

#  WHO_MY_OPPONENT_PLAYS = other(WHO_I_PLAY)
#  MY_PAST_UTTERANCES = []
#  OPPONENT_PAST_UTTERANCES = []
#  UTTERANCE_COUNT = 0
#  REPEAT_COUNT = 0 or a table of these if you are reusing different utterances

