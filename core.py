#TODO add point counting
import random
from random import shuffle
from collections import defaultdict
from itertools import combinations_with_replacement,combinations,permutations

def none():
    return None

possiblestones = combinations_with_replacement(range(0,6),3)

def shiftToLowest(a):
    """Shifts a list to it's lowest possible representation: [3,1,2] -> [1,2,3]"""
    shifts = [a[i:] + a[:i] for i in range(len(a))]
    shifts.sort()
    return shifts[0]

def allStones():
    """Generates all unique stones.
       Stones are identical, if they can be shifted to each other"""
    stones = [shiftToLowest(stone) for stone in possiblestones]
    #Remove duplicates
    stones = set([tuple(stone) for stone in stones])
    return list(stones)

class Game():
    """The game class stores and controls the state of the game"""
    def __init__(self,players):
        self.valuefield = defaultdict(none)
        self.positionfield = []
        self.edges = []
        self.players = players            
        self.stones = allStones()
        shuffle(self.stones)
        self.player_index = 0
        for player in players:
            for i in range(5):
                player.stones.append(self.stones.pop())
            player.stones.append([0,1,2])
        self.set([0,1,2],[(0,0),(0,1),(1,0)])

    def set(self,stone,poss):
        """Place a stone onto the field,
           Fit always has to be run to check if a move is valid"""
        #Sort tuple to exclude possible duplicates
        #must be tuple to be hashable
        self.valuefield[poss[0]] = stone[0]
        self.valuefield[poss[1]] = stone[1]
        self.valuefield[poss[2]] = stone[2]  
        self.positionfield += [poss]
        self.edges += combinations(poss,2)
        return True
        
    def player(self):
        """Returns the current player"""
        return self.players[self.player_index]

    def next(self):
        """Selects the next player"""
        self.player_index += 1
        if self.player_index >= len(self.players):
            self.player_index = 0

    #TODO still buggy, calculate score
    #Bug is probably due to order of the list
    def fits(self,stone,poss):
        """If more than one point has a value
           If at least one edge is in use
           If not a stone on the same position
           Pointreward: One edge all points 
                        Two edges all points
                        Three edges"""
        if poss in self.positionfield:
            return False
        posvals = zip(poss,stone)
        print posvals
        values = [self.valuefield[posval[0]] for posval in posvals if (self.valuefield[posval[0]] != None) and (self.valuefield[posval[0]] == posval[1])]
        print values
        edges_count = len([edge for edge in list(combinations(poss,2)) if edge in self.edges])
        if edges_count <= 0:
            return False
        if len(values) >= 2: 
            return True        
        return False

    def gameloop(self):
        """A game loop: Not used in opengl version, because events handle that"""
        for player in self.players:
            player.move(self)
            self.gameloop()

    def move(self,position):
        """The active player tries to set the active stone (stored in player object) to the given position"""
        if self.player().move(self,position):
            self.next()
        
class Player(object):
    """A human controllable player class"""
    def __init__(self):
        self.stones = []
        self.stone_index = 0
    def next(self):
        self.stone_index += 1
        if self.stone_index >= len(self.stones):
            self.stone_index = 0
    def stone(self):
        return self.stones[self.stone_index]
    def setStone(self,s):
        self.stones[self.stone_index] = s
    def rotate(self):
        stone = self.stone()
        self.stones[self.stone_index] = stone[1:] + stone[0:1]
    #TODO: Add points
    def move(self,game,position):
        valid = game.fits(self.stone(),position)
        if valid: 
            game.set(self.stone(),position)
            self.stones.pop(self.stone_index)
            self.stone_index -= 1
            if self.stones == []:
               self.stones.append(game.stones.pop())
        return valid

if __name__ == "__main__":
    p = Player()
    g = Game([p])

