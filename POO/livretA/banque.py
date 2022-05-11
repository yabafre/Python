class Banque :
    
    def __init__(self, nom):
        self.nom = nom
        self.livrets = []
        
    def ajout_client(self, nom_client):
        self.client =client