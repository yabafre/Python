import random


a = random.randrange(50)
b = random.randrange(60)
calcul = int( b/a )
print(b, "/",a,"  =")
user = int( input ( " entrez la reponse "))
if user == calcul :
    print("bravo")
else:    
    print("dommage")
