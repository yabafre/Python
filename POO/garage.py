import voiture


class Garage:
    def __init__(self):
        self.voitures= []
        nb_voiture = int(input("Cobien de voiture à créer?"))
        for i in range(nb_voiture):
            self.voitures.append(voiture.Voiture())


    def showRoom(self):
        for i in self.voitures:
            print(i)