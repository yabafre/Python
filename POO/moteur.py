class Moteur:
    def __init__(self, type = "Essence"):
        self.type = type

    def __str__(self):
        return f"Je suis un moteur {self.type}"

    def brule_essence(self):
        print(f"Le moteur brule de {self.type}")

if __name__ == "__main__":
    moteur = Moteur()
    print(moteur)
    moteur.type = "Diesel"
    print(moteur)

    moteur_elec = Moteur("Electrique")
    print(moteur_elec)