import random










def create_grille(height, width, nb_mine):
    grille = []
    for i in range(height):
        ligne = []
        for j in range(width):
            ligne.append(0)
        grille.append(ligne)
    k = 0
    while k != nb_mine:
        place_bombe = random.randrange(height * width)
        ligne_bombe = place_bombe // height
        colonne_bombe = place_bombe % height

        if grille[ligne_bombe][colonne_bombe] != -1:
            grille[ligne_bombe][colonne_bombe] = -1
            k +=1
        else:
            continue

        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= ligne_bombe + i < height and 0 <= colonne_bombe + j < width and not (i == 0 and j == 0):
                    if grille[ligne_bombe + i][colonne_bombe + j] != -1:
                        grille[ligne_bombe + i][colonne_bombe + j] += 1

    return grille


def afficher_grille(grille):
    grille_hide = []
    for i in range(len(grille)):
        ligne = []
        for j in range(len(grille[i])):
            ligne.append(9)
        grille_hide.append(ligne)

    for i in range(len(grille)):
        print(grille_hide[i])

    for i in range(len(grille)):
        print(grille[i])


afficher_grille(create_grille(5, 5, 5))