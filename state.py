#
# state.py (Final Project)
#
# A State class for the Eight Puzzle
#
# name: Yuting Ma
# email: ytma@bu.edu
#
# If you worked with a partner, put his or her contact info below:
# partner's name:
# partner's email:
#

from board import *

# a 2-D list that corresponds to the tiles in the goal state
GOAL_TILES = [[0, 1, 2],
              [3, 4, 5],
              [6, 7, 8]]

# the list of possible moves, each of which corresponds to
# moving the blank cell in the specified direction
MOVES = ['up', 'down', 'left', 'right']

class State:
    """ A class for objects that represent a state in the state-space 
        search tree of an Eight Puzzle.
    """
    ### Add your method definitions here. ###
    # 1. __init__
    def __init__(self, board, predecessor, move):
        """ construct a new State object by initializing four attributes:
            board: stores a reference to the Board object
            predecessor: a reference to the Stae object that comes before this state
            move: stores a string representing the move that was needed to
            trnsition from the predecessor state to this state
            num_moves: stores an integer representing the number of moves that
            were needed to get from the initial state to this state
        """
        self.board = board
        self.predecessor = predecessor
        self.move = move
        if predecessor == None:
            self.num_moves = 0
        else:
            self.num_moves = predecessor.num_moves + 1
        

    def __repr__(self):
        """ returns a string representation of the State object
            referred to by self.
        """
        # You should *NOT* change this method.
        s = self.board.digit_string() + '-'
        s += self.move + '-'
        s += str(self.num_moves)
        return s
    
    def creates_cycle(self):
        """ returns True if this State object (the one referred to
            by self) would create a cycle in the current sequence of moves,
            and False otherwise.
        """
        # You should *NOT* change this method.
        state = self.predecessor
        while state != None:
            if state.board == self.board:
               return True
            state = state.predecessor
        return False

    def __gt__(self, other):
        """ implements a > operator for State objects
            that always returns True. This will be needed to break
            ties when we use max() on a list of [priority, state] pairs.
            If we don't have a > operator for State objects,
            max() will fail with an error when it tries to compare
            two [priority, state] pairs with the same priority.
        """
        # You should *NOT* change this method.
        return True

    # 2. is_goal
    def is_goal(self):
        """ return True if self == goal
            return False otherwise
        """
        return GOAL_TILES == self.board.tiles

    # 3. generate_successors
    def generate_successors(self):
        """ create and return a list of State objects for all successor states of
            the called State object
        """
        successors = []
        for m in MOVES:
            b = State(self.board.copy(), self, m)
            if b.board.move_blank(m):
                successors += [b]
        return successors


    # Part III 7.
    def print_moves_to(self):
        """ print the sequence of moves from initial state to the called State
            object
        """
        if self.predecessor == None:
            print('initial state:')
            print(self.board)
        else:
            self.predecessor.print_moves_to()
            print('move the blank', self.move, ':')
            print(self.board)


    # Part V 4.
    # hueristic function 1
    def score(self):
        """ return a score of the called state object
            score = 1 if the number of misplaced tiles is less than its predecessor
            score = 0 if the number of misplaced tiles equals to its predecessor
            score = -1 if the number of misplaced tiles is larger than its predecessor
        """
        if self.predecessor != None:
            if self.board.num_misplaced() > self.predecessor.board.num_misplaced():
                return -1
            elif self.board.num_misplaced() < self.predecessor.board.num_misplaced():
                return 1
            
        return 0


    # hueristic function 2
    def distance(self):
        """ return the sum of row difference and column difference between self
            and goal tiles
        """
        distance = 0
        for r in range(3):
            for c in range(3):
                if self.board.tiles[r][c] != 0 and\
                   self.board.tiles[r][c] != GOAL_TILES[r][c]:
                    i = self.board.tiles[r][c]
                    diff = abs(i//3-r) + abs(i%3-c)
                    distance += diff
        return distance
