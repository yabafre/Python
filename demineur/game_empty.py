
import random
import re

# Creating a grille object to represent the minesweeper grille
# This is so that when we code up the game, we can just say "create a new grille object"
# and dig on that grille, etc.
class grille:
    def __init__(self, taille, NB_Bomb):
        # keep track of these parameters because we might find them helpful later on
        self.taille = taille
        self.NB_Bomb = NB_Bomb

        # get the grille
        self.grille = self.make_new_grille()
        self.assign_values_to_grille()

        # initialize a set to keep track of which locations we've uncovered
        # we will put (row,col) tuples into these sets 
        self.dug = set()

    def make_new_grille(self):
        # construct a new grille based on the dim size and num bombs
        # we should construct the list of lists here (or whatever representation you prefer,
        # but since we have a 2-D grille, list of lists is most natural)
        return [] # change this

    def assign_values_to_grille(self):
        # now that we have the bombs planted, let's assign a number 0-8 for all the empty spaces, which
        # represents how many neighboring bombs there are. we can precompute these and it'll save us some
        # effort checking what's around the grille later on :)
        pass

    def get_num_neighboring_bombs(self, row, col):
        # let's iterate through each of the neighboring positions and sum number of bombs
        # top left: (row-1, col-1)
        # top middle: (row-1, col)
        # top right: (row-1, col+1)
        # left: (row, col-1)
        # right: (row, col+1)
        # bottom left: (row+1, col-1)
        # bottom middle: (row+1, col)
        # bottom right: (row+1, col+1)

        # ps we need to make sure we don't go out of bounds!!
        pass

    def dig(self, row, col):
        # dig at that location!
        # return True if successful dig, False if bomb dug

        # a couple of scenarios to consider:
        # hit a bomb -> game over
        # dig at a location with neighboring bombs -> finish dig
        # dig at a location with no neighboring bombs -> recursively dig neighbors!
        pass

    def __str__(self):
        # return a string that shows the grille to the player
        # note: this part is kinda hard to get the formatting right, you don't have to do it the same way
        # i did
        # you can also just copy and paste from the implementation
        # this part is not that important to understanding the logic of the code :)
        return ''

def play(taille=10, NB_Bomb=10):
    # Step 1: create the grille and plant the bombs
    # Step 2: show the user the grille and ask for where they want to dig
    # Step 3a: if the location is a bomb, then show game over message
    # Step 3b: if the location is not a bomb, dig recursively until one of the squares is next to a bomb
    # Step 4: repeat steps 2 and 3a/b until there are no more places to dig, then show victory
    pass

if __name__=='__main__':
    play()
    
