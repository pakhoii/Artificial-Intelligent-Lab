# CLASS DESCRIPTION FOR CONSTRAINT SATISFACTION PROBLEM (CSP)

from util import *

class csp:
    # INITIALIZING THE CSP
    def __init__(self, domain=digits, grid=""):
        """
        Unitlist consists of the 27 lists of peers
        Units is a dictionary consisting of the keys and the corresponding lists of peers
        Peers is a dictionary consisting of the 81 keys and the corresponding set of 27 peers
        Constraints denote the various all-different constraints between the variables
        """
        "***YOUR CODE HERE ***"
        self.domain = domain
        self.variables = squares
        self.values = self.getDict(grid.strip())
        
        # Unitlist: 9 rows, 9 columns, 9 boxes of 3x3
        self.unitlist = (
            [cross(rows, c) for c in cols] + 
            [cross(r, cols) for r in rows] + 
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
        )
        
        # Units: current key's rows, columns, and box
        self.units = dict((s, [u for u in self.unitlist if s in u]) for s in self.variables)
        
        # Peers: all the squares that share a unit with the current key
        # sum(self.units[s],[]) flattens the list of lists into a single list of peers
        # set() removes duplicates
        self.peers = dict((s, set(sum(self.units[s],[]))-set([s])) for s in self.variables)
        
        self.constraints = [] 
        for s in self.variables:
            for peer in self.peers[s]:
                self.constraints.append((s, peer))


    def getDict(self, grid=""):
        """
        Getting the string as input and returning the corresponding dictionary
        """
        i = 0
        values = dict()
        for cell in self.variables:
            if grid[i] != '0':
                values[cell] = grid[i]
            else:
                values[cell] = digits
            i = i + 1
        return values