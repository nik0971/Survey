from getpass import *
import hashlib


chaine_mot_de_passe = b"azerty"
mot_de_passe_chiffre = hashlib.sha256(chaine_mot_de_passe).hexdigest()

verrouille = True
while verrouille:

	entre = getpass("Tapez votre mot de passe: ")

	entre = entre.encode()

	entre_chiffre =	hashlib.sha256(entre).hexdigest()
	print(entre_chiffre)
	if entre_chiffre == mot_de_passe_chiffre:
		verrouille = False
	else:
		print("Mot de passe incorrect")

print("Mot de passe accepté...")
