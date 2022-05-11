
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
	        # initialiser un ensemble pour garder une trace des endroits que nous avons découverts
        # we'll save (row,col) tuples into this set 
	        # nous enregistrerons des lignes (ligne, col) dans cet ensemble
        self.dug = set() # if we dig at 0, 0, then self.dug = {(0,0)}

    def make_new_board(self):
        # construct a new board based on the dim size and num bombs
		    # nous devrions construire la liste des listes ici (ou quelle que soit la représentation que vous préférez,
        # we should construct the list of lists here (or whatever representation you prefer,
		    # mais comme nous avons un tableau 2D, la liste des listes est la plus naturelle)
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
                                                            # retourne un entier aléatoire N tel qu'un <= N <= b
            row = loc // self.taille  # we want the number of times taille goes into loc to tell us what row to look at
                                        # nous voulons que le nombre de fois que la taille va dans loc pour nous dire quelle ligne regarder
            col = loc % self.taille  # we want the remainder to tell us what index in that row to look at
                                        # nous voulons que le reste nous dise quel index de cette rangée regarder

            if board[row][col] == '*':
                # this means we've actually planted a bomb there already so keep going
                    # cela signifie que nous avons déjà planté une bombe là-bas, alors continuez
                continue

            board[row][col] = '*' # plant the bomb
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
# now that we have the bombs planted, let's assign a number 0-8 for all the empty spaces, which	
	# maintenant que nous avons les bombes plantées, attribuons un numéro 0-8 pour tous les espaces vides, qui
# represents how many neighboring bombs there are. we can precompute these and it'll save us some
	# représente le nombre de bombes voisines qu'il y a. nous pouvons les précalculer et cela nous en sauvera
# effort checking what's around the board later on :)
	# effort pour vérifier ce qu'il y a autour du tableau plus tard :)
        for r in range(self.taille):
            for c in range(self.taille):
                if self.board[r][c] == '*':
                    # if this is already a bomb, we don't want to calculate anything
                        # si c'est déjà une bombe, nous ne voulons rien calculer
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
            # assurez-vous de ne pas sortir des limites !

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
        # dig at that location!
	# creuse à cet endroit !
# return True if successful dig, False if bomb dug
	# return True en cas de fouille réussie, False en cas de bombe creusée
# a few scenarios:
	# quelques scénarios :
# hit a bomb -> game over
	# a frappé une bombe -> jeu terminé
# dig at location with neighboring bombs -> finish dig
	# creuser sur place avec les bombes voisines -> terminer creuser
# dig at location with no neighboring bombs -> recursively dig neighbors!
	# creusez sur place sans bombes voisines -> creusez récursivement les voisins !
    
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

        # if our initial dig didn't hit a bomb, we *shouldn't* hit a bomb here
            # si notre fouille initiale n'a pas heurté une bombe, nous *ne devrions pas* frapper une bombe ici
        return True

    def __str__(self):
    
        # this is a magic function where if you call print on this object,
            # il s'agit d'une fonction magique où si vous appelez print sur cet objet,
        # it'll print out what this function returns!
            # il affichera ce que cette fonction retourne !
        # return a string that shows the board to the player
            # retourne une chaîne qui montre le plateau au joueur

        # first let's create a new array that represents what the user would see
            # créons d'abord un nouveau tableau qui représente ce que l'utilisateur verra 
        visible_board = [[None for _ in range(self.taille)] for _ in range(self.taille)]
        for row in range(self.taille):
            for col in range(self.taille):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        # put this together in a string
            # mettre ca dans une chaîne
        string_rep = ''
        # get largeurs de colonne maximales pour affichage
            # obtenir des largeurs de colonne maximales pour l'affichage
        widths = []
        for idx in range(self.taille):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
            # afficher les chaînes csv
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
    # jouer au jeu
def play(taille, nb_bomb):
    # Step 1: create the board and plant the bombs
        # Étape 1 : créer le plateau et planter les bombes
    board = Board(taille, nb_bomb)

    # Step 2: show the user the board and ask for where they want to dig
	    # Étape 2 : montrez à l'utilisateur le tableau et demandez-lui où il veut creuser
    # Step 3a: if location is a bomb, show game over message
	    # Étape 3a : si l'emplacement est une bombe, afficher le message jeu fini
    # Step 3b: if location is not a bomb, dig recursively until each square is at least
	    # Étape 3b : si l'emplacement n'est pas une bombe, creusez récursivement jusqu'à ce que chaque carré soit au moins à côté d'une bombe
    # Step 4: repeat steps 2 and 3a/b until there are no more places to dig -> VICTORY!
	    # Étape 4 : répétez les étapes 2 et 3a/b jusqu'à ce qu'il n'y ait plus d'endroits pour creuser -> VICTOIRE !
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
            # si c'est valide, nous creusons
        safe = board.dig(row, col)
        if not safe:
            # dug a bomb ahhhhhhh
                # toucher une bombe ahhhhhhh
            break # (game over rip)
        # 2 ways to end loop, lets check which one
            # 2 façons de mettre fin à la boucle, permet de vérifier laquelle
    if safe:
        print("CONGRATULATIONS!!!")
    else:
        print("SORRY GAME OVER :(")
        # let's reveal the whole board!
            # révélons toute la planche !
        board.dug = [(r,c) for r in range(board.taille) for c in range(board.taille)]
        print(board)

      
if __name__ == '__main__': # good practice :)
    play(taille,nb_bomb)