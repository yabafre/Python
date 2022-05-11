from ion import keydown
from kandinsky import *
from random import randint
from time import sleep

v = "1.20"  # 18/04/2020 (v1.1=28/02/2020)


def wait(buttons=range(53)):  # Attends qu'une des touches précisées soit pressée
    while True:
        for i in buttons:
            if keydown(i):
                while keydown(i): True  # Fonction anti-rebond
                return i


def omega():  # Vérificateur d'OS
    try:
        get_keys()
        return True
    except:
        return False


def menu(titre, action, *para):
    n, g, f = (0, 0, 0), (96, 96, 96), (255, 183, 52)  # couleurs : réglages, optionsn focus
    if omega():
        f = (192, 53, 53)
    set = [1 for i in para]  # Valeurs par défaut
    curs = 0  # Initialisation sur l'action
    draw_string(titre, int(160 - 5 * len(titre)), 8, (42, 120, 224))
    draw_string(action, int(160 - 5 * len(action)), 36, f)

    def menu_option(i, col, cursor):
        draw_string(" " * 13, 150, 64 + i * 25, col)
        txt = str(para[i][set[i]])
        if txt.find("$") != -1:
            txt2 = txt[txt.find("$") + 1:]
            txt = txt[:txt.find("$")]
            draw_string(" " * 32, 0, 64 + (i + 1) * 25)
            draw_string(str(txt2), int(150 + (150 - 10 * len(str(txt2))) / 2), 64 + (i + 1) * 25, col)
        draw_string(" " * 17, 140, 64 + (i) * 25)
        draw_string(str(txt), int(150 + (150 - 10 * len(str(txt))) / 2), 64 + i * 25, col)
        draw_string("<" * cursor, 140, 64 + i * 25, g)
        draw_string(">" * cursor, 300, 64 + i * 25, g)

    for i in range(len(para)):
        draw_string(para[i][0], 10, 64 + i * 25, n)
        menu_option(i, g, False)

    while True:
        r = wait((0, 1, 2, 3, 4, 52))
        if r in (4, 52):  # Lance l'application
            return [para[i][set[i]] for i in range(len(para))]
        elif r in (1, 2):
            if curs == 0:
                draw_string(action, int(160 - 5 * len(action)), 36, n)
            else:
                menu_option(curs - 1, g, False)
            curs = (curs - 1 * (r == 1) + 1 * (r == 2)) % (len(para) + 1)
            if curs == 0:
                draw_string(action, int(160 - 5 * len(action)), 36, f)
            else:
                menu_option(curs - 1, f, True)
        elif r in (0, 3) and curs != 0:
            set[curs - 1] = set[curs - 1] + 1 * (r == 3) - 1 * (r == 0)
            if set[curs - 1] == 0:
                set[curs - 1] = len(para[curs - 1]) - 1
            if set[curs - 1] == len(para[curs - 1]):
                set[curs - 1] = 1
            menu_option(curs - 1, f, True)


# couleurs
f, h, n = 255, 127, 0
c = ((f, f, f), (45, 125, 210), (151, 204, 4), (238, 185, 2), (244, 93, 1), (215, 65, 167), (n, n, n), (n, n, n),
     (n, n, n), (h, h, h), (192, 192, 192), (96, 96, 96), (253, 236, 185))

mines, triche, graphisme, safe = 19, 0, 0, 0
m, p = [], []
# initialisation
x0, y0, x1, y1 = 4, 2, 4, 2


def deminage():
    global mines, safe
    draw_string(str(safe), 12, 2, c[2])
    if safe + mines >= 150:
        draw_string("Gagné ! ", 120, 2)
        sleep(2)
        wait()
        start()


def decouvre(x, y):
    i = 1
    while i > 0:
        chiffre(x, y)
        for p in range(max(0, x - 1), min(15, x + 2)):
            for q in range(max(0, y - 1), min(10, y + 2)):
                if m[p][q] >= 100:
                    chiffre(p, q)
                elif m[p][q] == 0:
                    m[p][q] += 1
        i = 0
        for p in range(15):
            for q in range(10):
                if m[p][q] % 100 == 1:
                    i, x, y, p, q = 1, p, q, 14, 9


def terrain():
    fill_rect(8, 21, 300, 200, c[9])
    for y in range(21, 243, 20):
        for x in range(8, 309):
            set_pixel(x, y, c[10])
    for x in range(8, 320, 20):
        for y in range(21, 222):
            set_pixel(x, y, c[10])


def chiffre(x, y):
    global safe
    fill_rect(20 * x + 9, 20 * y + 22, 19, 19, c[0])
    safe += (m[x][y] % 100 != 42)
    v = m[x][y] // 100
    m[x][y] = 100 * v + 42
    if v: draw_string(str(v), 20 * (x) + 13, 20 * (y) + 23, c[v], c[0])
    deminage()


# On place les mines et génère la matrice
def minage(b):
    global safe
    safe = 0
    fill_rect(0, 0, 320, 240, c[0])
    terrain()
    m.clear()
    for x in range(15): m.append([0 for y in range(10)])
    i = b
    while i > 0:
        x, y = randint(0, 14), randint(0, 9)
        if m[x][y] != 999:
            m[x][y] = 999
            i -= 1
            for p in range(max(0, x - 1), min(15, x + 2)):
                for q in range(max(0, y - 1), min(10, y + 2)):
                    if m[p][q] != 999: m[p][q] += 100
    draw_string("/" + str(150 - b), 42, 2, c[1])
    draw_string("Demineur", 120, 2)
    draw_string("mines:" + str(b), 220, 2, c[5])
    deminage()

# Vous êtes mort !
def explose():
    draw_string("perdu ! ", 120, 2)
    for x in range(15):
        for y in range(10):
            if m[x][y] == 999:
                mine(x, y)
    sleep(2)
    wait()
    start()


def marche(x, y):
    if m[x][y] >= 999:
        explose()
    elif m[x][y] >= 100:
        chiffre(x, y)
    else:
        decouvre(x, y)


def survol():
    global x0, y0, x1, y1
    if x1 != x0 or y1 != y0:
        gps(x0, y0, 10)
    gps(x1, y1)
    x0, y0 = x1, y1


def gps(x, y, i=6):
    fill_rect(8 + 20 * x, 21 + 20 * y, 21, 1, c[i])
    fill_rect(28 + 20 * x, 21 + 20 * y, 1, 21, c[i])
    fill_rect(8 + 20 * x, 21 + 20 * y, 1, 21, c[i])
    fill_rect(8 + 20 * x, 41 + 20 * y, 21, 1, c[i])

# On se promène sans déclencher les mines
def drone():
    global mines, triche, x0, y0, x1, y1
    while not keydown(5):
        if keydown(0) or keydown(3) or keydown(1) or keydown(2):
            x1 = min(max(x0 - keydown(0) + keydown(3), 0), 14)
            y1 = min(max(y0 - keydown(1) + keydown(2), 0), 9)
            survol()
            sleep(0.120)
        if keydown(4) or keydown(52):
            marche(x0, y0)
        if keydown(17) or keydown(16):
            drapeau(x0, y0)
        if keydown(12) and triche > 0:
            cheat()
        if keydown(6):
            return start()

# Mode de triche codé par satan
def cheat():
    for i in range(666):
        x, y = randint(0, 14), randint(0, 9)
        if m[x][y] == 0:
            decouvre(x, y)
            break


def drapeau(x, y):
    global graphisme
    if graphisme == 0:
        fill_rect(20 * x + 9, 20 * y + 22, 19, 19, c[0])
        fill_rect(20 * x + 9, 20 * y + 22, 19, 19, c[3])
    else:
        fill_rect(20 * x + 20, 20 * y + 31, 2, 6, c[7])
        fill_rect(20 * x + 16, 20 * y + 37, 8, 2, c[7])
        fill_rect(20 * x + 16, 20 * y + 27, 6, 4, c[4])


def mine(x, y):
    global graphisme
    fill_rect(20 * x + 9, 20 * y + 22, 19, 19, c[0])
    if graphisme == 0:
        fill_rect(20 * x + 9, 20 * y + 22, 19, 19, c[4])
    else:
        fill_rect(20 * x + 14, 20 * y + 27, 9, 9, c[6])
        fill_rect(20 * x + 12, 20 * y + 31, 13, 1, c[6])
        fill_rect(20 * x + 18, 20 * y + 25, 1, 13, c[6])
        fill_rect(20 * x + 16, 20 * y + 29, 2, 2, (255, 255, 255))
        for p in [[9, 2], [10, 3], [10, 9], [9, 10], [3, 10], [2, 9], [2, 3], [3, 2]]:
            set_pixel(20 * x + p[0] + 12, 20 * y + p[1] + 25, c[4])


def start():
    fill_rect(0, 0, 320, 240, c[0])
    global mines, triche, graphisme
    try:
        mines, triche, graphisme, com, cre = menu("Démineur", "Lancer la partie [OK]",
                                                  ["Mines", 16, 19, 22, 25, 28, 31, 33, 36, 39, 42, 7, 10, 13],
                                                  ["Mode Triche", "1 fois", "non", "oui"],
                                                  ["Graphisme", "sobre", "classique"],
                                                  ["Commandes", "Nav: Flèches", "Déminer: OK", "Drapeau: Retour",
                                                   "Rejouer: Maison", "Triche: shift"],
                                                  ["Crédits", "Site web$nsi.xyz/demine", "Auteur$Vincent Robert",
                                                   "Contributeur$Bisam tiplanet.org",
                                                   "Contributeur$Critor tiplanet.org", "Contributeur$Arthur Jacquin"])
        triche = 0 * (triche == "non") + 1 * (triche == "1 fois") + 42 * (triche == "oui")
        graphisme = 0 * (graphisme == "sobre") + 1 * (graphisme == "classique")
    except:
        mines, triche, graphisme = 19, 0, 0
    fill_rect(0, 0, 320, 240, c[0])
    minage(mines)
    if triche > 0:
        triche -= 1
        cheat()
    survol()
    drone()


start()