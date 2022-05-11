
import random
import re

# permet de créer un objet de plateau pour représenter le jeu de dragueur de mines
# c’est pour que nous puissions simplement dire « créer un nouvel objet de tableau », ou
# « creuser ici », ou « rendre ce jeu pour cet objet »
class Board:
    def __init__(self, taille, nb_bomb):
        self.taille = taille
        self.nb_bomb = nb_bomb

        # let's create the board
        self.board = self.make_new_board() # plant the bombs
        self.assign_values_to_board()

        # initialize a set to keep track of which locations we've uncovered
        # we'll save (row,col) tuples into this set 
        self.dug = set() # if we dig at 0, 0, then self.dug = {(0,0)}

    def make_new_board(self):
        # construct a new board based on the dim size and num bombs
        # we should construct the list of lists here (or whatever representation you prefer,
        # but since we have a 2-D board, list of lists is most natural)

        # generate a new board
        board = [[None for _ in range(self.taille)] for _ in range(self.taille)]
        # this creates an array like this:
        # [[None, None, ..., None],
        #  [None, None, ..., None],
        #  [...                  ],
        #  [None, None, ..., None]]
        # we can see how this represents a board!

        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.nb_bomb:
            loc = random.randint(0, self.taille**2 - 1) # return a random integer N such that a <= N <= b
            row = loc // self.taille  # we want the number of times taille goes into loc to tell us what row to look at
            col = loc % self.taille  # we want the remainder to tell us what index in that row to look at

            if board[row][col] == '*':
                # this means we've actually planted a bomb there already so keep going
                continue

            board[row][col] = '*' # plant the bomb
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        # now that we have the bombs planted, let's assign a number 0-8 for all the empty spaces, which
        # represents how many neighboring bombs there are. we can precompute these and it'll save us some
        # effort checking what's around the board later on :)
        for r in range(self.taille):
            for c in range(self.taille):
                if self.board[r][c] == '*':
                    # if this is already a bomb, we don't want to calculate anything
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):

        # top left: (row-1, col-1)
        # top middle: (row-1, col)
        # top right: (row-1, col+1)
        # left: (row, col-1)
        # right: (row, col+1)
        # bottom left: (row+1, col-1)
        # bottom middle: (row+1, col)
        # bottom right: (row+1, col+1)

        # make sure to not go out of bounds!

        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.taille-1, row+1)+1):
            for c in range(max(0, col-1), min(self.taille-1, col+1)+1):
                if r == row and c == col:
                    # our original location, don't check
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):
    
        self.dug.add((row, col)) # keep track that we dug here

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        # self.board[row][col] == 0
        for r in range(max(0, row-1), min(self.taille-1, row+1)+1):
            for c in range(max(0, col-1), min(self.taille-1, col+1)+1):
                if (r, c) in self.dug:
                    continue # don't dig where you've already dug
                self.dig(r, c)

        # si notre fouille initiale n’a pas touché une bombe, nous *ne devrions pas* frapper une bombe ici
        return True

    def __str__(self):
    

        # nouvelle grille qui représente ce que l’utilisateur verrait
        visible_board = [[None for _ in range(self.taille)] for _ in range(self.taille)]
        for row in range(self.taille):
            for col in range(self.taille):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        # put this together in a string
        string_rep = ''
        # get largeurs de colonne maximales pour affichage
        widths = []
        for idx in range(self.taille):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print grille
        indices = [i for i in range(self.taille)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.taille)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

def menu():
        global taille, nb_bomb
        niveau = str(input("Quel niveaux choisis-tu ?\n"
                           "1:Simple\n"
                           "2:Medium\n"
                           "3:Difficile\n"))
        if niveau == "1":
            # Step 1: create the board and plant the bombs
            taille = 10
            nb_bomb = 10
            print("Vous avez choisi le mode Simple ! Le jeux vas commencer")
        elif niveau == "2":
            taille = 11
            nb_bomb = 25
            print("Vous avez choisi le mode Medium ! Le jeux vas commencer")
        elif niveau == "3":
            taille = 11
            nb_bomb = 40
            print("Vous avez choisi le mode Difficile ! Le jeux vas commencer")
        else:
            print("\nVous n'avez choisi aucun mode ! Veuillez choisir le mode 1, 2, ou 3 !\n")
            return menu()

menu()
# play the game
def play(taille, nb_bomb):
    # Step 1: create the board and plant the bombs
    board = Board(taille, nb_bomb)

    # Step 2: show the user the board and ask for where they want to dig
    # Step 3a: if location is a bomb, show game over message
    # Step 3b: if location is not a bomb, dig recursively until each square is at least
    #          next to a bomb
    # Step 4: repeat steps 2 and 3a/b until there are no more places to dig -> VICTORY!
    safe = True 

    while len(board.dug) < board.taille ** 2 - nb_bomb:
        print(board)
        # 0,0 or 0, 0 or 0,    0
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))  # '0, 3'
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.taille or col < 0 or col >= taille:
            print("Invalid location. Try again.")
            continue

        # if it's valid, we dig
        safe = board.dig(row, col)
        if not safe:
            # dug a bomb ahhhhhhh
            break # (game over rip)

    # 2 ways to end loop, lets check which one
    if safe:
        print("CONGRATULATIONS!!!")
    else:
        print("SORRY GAME OVER :(")
        # let's reveal the whole board!
        board.dug = [(r,c) for r in range(board.taille) for c in range(board.taille)]
        print(board)

      
if __name__ == '__main__': # good practice :)
    play(taille,nb_bomb)
