
import moteur
import voiture
import garage

un_moteur = moteur.Moteur()
ma_voiture = voiture.Voiture(un_moteur)
print(ma_voiture)

mon_autre_voiture = voiture.Voiture(moteur.Moteur("Electrique"))
print(mon_autre_voiture)
ma_troiseme_voiture = voiture.Voiture(moteur.Moteur())
print(ma_troiseme_voiture)

autre_moteur = moteur.Moteur("Diesel")

ma_voiture.moteur = autre_moteur
print(ma_voiture)


ma_voiture.demarrer()
mon_autre_voiture.demarrer()

mon_garage = garage.Garage()
mon_garage.showRoom()