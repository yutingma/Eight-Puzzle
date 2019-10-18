#
# searcher.py (Final Project)
#
# classes for objects that perform state-space search on Eight Puzzles
#
# name: Yuting Ma
# email: ytma@bu.edu
#
# If you worked with a partner, put his or her contact info below:
# partner's name:
# partner's email:
#

import random
from state import *

class Searcher:
    """ A class for objects that perform random state-space
        search on an Eight Puzzle.
        This will also be used as a superclass of classes for
        other state-space search algorithms.
    """
    ### Add your Searcher method definitions here. ###
    # 1.
    def __init__(self, init_state, depth_limit):
        """ initialize Searcher object
            Attributes:
            states: list of untested states
            (initialized to a list containing init_state)
            num_tested: keep track of how many states the Searcher tests
            (initialized to be 0)
            depth_limit: specifies how deep in the state-space search tree the
            Searcher will go (-1 indicates that Searcher does not use depth limit)
        """
        self.states = [init_state]
        self.num_tested = 0
        self.depth_limit = depth_limit
        


    def __repr__(self):
        """ returns a string representation of the Searcher object
            referred to by self.
        """
        # You should *NOT* change this method.
        s = str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        if self.depth_limit == -1:
            s += 'no depth limit'
        else:
            s += 'depth limit = ' + str(self.depth_limit)
        return s


### Add your other class definitions below. ###
    # 2.
    def should_add(self, state):
        """ takes a State object called state
            returns True if the called Searcher should add state to its list of
            untested states, and False otherwise
            (within the depth_limit and not cycle)
        """
        if self.depth_limit != -1 and state.num_moves > self.depth_limit:
            return False
        elif state.creates_cycle():
            return False
        else:
            return True


    # 3.
    def add_state(self, new_state):
        """ takes a single State object called new_state
            adds it to the Searcher' list of untested states
            (don't need to return value)
        """
        self.states += [new_state]

    # 4.
    def add_states(self, new_states):
        """ takes a list State objects called new_states
            processes the elements of new_states one at a time
            (if should be added: add
            if shouldn't be added: ignore
            not return value)
        """
        for i in range(len(new_states)):
            if self.should_add(new_states[i]):
                self.add_state(new_states[i])


    # 5.
    def next_state(self):
        """ chooses the next state to be tested from the list of
            untested states, removing it from the list and returning it
        """
        s = random.choice(self.states)
        self.states.remove(s)
        return s

    # 6.
    def find_solution(self):
        """ performs a full random state-space search
            stopping when the goal state is found or when the Searcher runs out
            of untested states
        """
        while len(self.states) > 0:
            s = self.next_state()
            self.num_tested += 1
            if s.is_goal():
                return s
            else:
                self.add_states(s.generate_successors())
        return None
    

    # Part IV:
class BFSearcher(Searcher):
    """ initialize BFSearcher with inheritance of class Searcher
    """
    def next_state(self):
        """ chooses the next state to be tested from the list of
            untested states, removing it from the list and returning it
            (in BFS, the first state in the states list)
        """
        s = self.states[0]
        self.states.remove(s)
        return s


class DFSearcher(Searcher):
    """ initialize DFSearcher with inheritance of class Searcher
    """
    def next_state(self):
        """ chooses the next state to be tested from the list of
            untested states, removing it from the list and returning it
            (in DFS, the last state in the states list)
        """
        s = self.states[-1]
        self.states.remove(s)
        return s
        

class GreedySearcher(Searcher):
    """ initialize GreedySearcher with inheritance of class Searcher
    """
    def priority(self, state):
        """ take a State object called state
            computes and returns the priority of that state
        """
        if self.heuristic == 1:
            priority = -1*state.board.num_misplaced() + state.score()
        elif self.heuristic == -1:
            num_misplaced_tiles = state.board.num_misplaced()
            priority = -1 * num_misplaced_tiles
        elif self.heuristic == 2:
            priority = -1*state.distance()
        return priority

    def __init__(self, init_state, heuristic, depth_limit):
        """ constructor for a GreedySearcher object inputs:
            * init_state - a State object for the initial state
            * heuristic - an integer specifying which heuristic
              function should be used when computing the priority
              of a state
            * depth_limit - the depth limit of the searcher
        """
        self.heuristic = heuristic
        self.states = [[self.priority(init_state), init_state]]
        self.num_tested = 0
        self.depth_limit = depth_limit

    def add_state(self, state):
        """ override the add_state method that is inherited from Searcher
            add a sublist that is a [priority, state] pair
        """
        if self.should_add(state):
            self.states += [[self.priority(state), state]]

    
    def next_state(self):
        """ chooses the next state to be tested from the list of
            untested states, removing it from the list and returning it
            (in GreedySearcher, the last state in the states list)
        """
        s = max(self.states)
        self.states.remove(s)
        return s[1]


class AStarSearcher(GreedySearcher):
    def priority(self, state):
        if self.heuristic == 1:
            priority = -1*(state.board.num_misplaced() + state.num_moves) + state.score()
        elif self.heuristic == -1:
            priority = -1*(state.board.num_misplaced() + state.num_moves)
        elif self.heuristic == 2:
            priority = -1*(state.distance() + state.num_moves)
        return priority
