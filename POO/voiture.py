class Voiture:
    def __init__(self, moteur = None):
        self.moteur = moteur

    def __str__(self):

        if self.moteur == None:
            return "Je suis une voiture à pédale"
        return f"Je suis une voiture avec " + str(self.moteur)

    def demarrer(self):
        print("La voiture démarre")
        self.moteur.brule_essence()

if __name__ == "__main__":
    ma_voiture= Voiture()
    print(ma_voiture)