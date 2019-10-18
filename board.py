#
# board.py (Final Project)
#
# A Board class for the Eight Puzzle
#
# name: Yuting Ma
# email: ytma@bu.edu
#
# If you worked with a partner, put his or her contact info below:
# partner's name:
# partner's email:
#

class Board:
    """ A class for objects that represent an Eight Puzzle board.
    """
    def __init__(self, digitstr):
        """ a constructor for a Board object whose configuration
            is specified by the input digitstr
            input: digitstr is a permutation of the digits 0-9
        """
        # check that digitstr is 9-character string
        # containing all digits from 0-9
        assert(len(digitstr) == 9)
        for x in range(9):
            assert(str(x) in digitstr)

        self.tiles = [[0] * 3 for x in range(3)]
        self.blank_r = -1
        self.blank_c = -1


        # Put your code for the rest of __init__ below.
        # Do *NOT* remove our code above.
        # update tile, blank_r, and blank_c
        for r in range(3):
            for c in range(3):
                self.tiles[r][c] = int(digitstr[3*r+c])
                if self.tiles[r][c] == 0:
                    self.blank_r = r
                    self.blank_c = c

            
    ### Add your other method definitions below. ###

    # 2. __repr__
    def __repr__(self):
        """ return a string representation of a Board object
        """
        s = ''
        for r in range(3):
            for c in range(3):
                if self.tiles[r][c] == 0:
                    s += '_'
                else:
                    s += str(self.tiles[r][c])
            s += '\n'
        return s


    # 3. move_blank
    def move_blank(self, direction):
        """ take as input a string direction that specifies the direction in
            which the blank should move and that attempts to modify the contents
            of the called Board object accordingly
        """
        if direction == 'left':
            new_r = self.blank_r
            new_c = self.blank_c - 1
        elif direction == 'right':
            new_r = self.blank_r
            new_c = self.blank_c + 1
        elif direction == 'up':
            new_r = self.blank_r - 1
            new_c = self.blank_c
        elif direction == 'down':
            new_r = self.blank_r + 1
            new_c = self.blank_c
        else:
            print('unknown direction:', direction)
            return False

        if 0 <= new_r <= 2 and 0 <= new_c <= 2:
            self.tiles[self.blank_r][self.blank_c] = self.tiles[new_r][new_c]
            self.tiles[new_r][new_c] = 0
            self.blank_r = new_r
            self.blank_c = new_c
            return True
        else:
            return False


    # 4. digit_string
    def digit_string(self):
        """ create and return a string of digits that correspongds to the current
            contents of the called Board object's tiles attribute
        """
        s = ''
        for r in range(3):
            for c in range(3):
                s += str(self.tiles[r][c])
        return s


    # 5. copy
    def copy(self):
        """ return a newly-constructed Board object that is a deep copy of the
            called object
        """
        b = Board(self.digit_string())
        return b


    # 6. num_misplaced
    def num_misplaced(self):
        """ counts and returns the number of tiles in the called Board object that
            are not where they should be in the goal state
        """
        goal = '012345678'
        s = self.digit_string()
        count = 0
        for i in range(9):
            if s[i] != '0' and s[i] != goal[i]:
                count += 1
        return count

    # 7. __eq__
    def __eq__(self, other):
        """ overload the == operator
            return True if the called object(self) and the argument(other) have
            the same values for the tiles attribute, False otherwise
        """
        s_self = self.digit_string()
        s_other = other.digit_string()
        return s_self == s_other

