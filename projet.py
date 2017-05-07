# Programme de surveillance de spectre par SDR
# Nik0 _31-03-2017_

# --- Début du programme ---

from fonctions import *
import pickle
import time
import os
import re
import linecache

mdp = "*pluton35"
#gestion_mdp(mdp)

# mise en place de la gestion du mot de passe
os.system("clear")
print("     --------------------------")
print("     --------BIENVENUE---------")
print("     --------------------------\n\n")


# --- CHOIX DU MODE ---
print("----MODES----\n-------------\n")
nomenu = menu("SURVEILLANCE","EDITION CONFIG","RAPPEL CONFIG","EXIT")
#menu = menu("SURVEILLANCE","CONFIGURATION","RAPPEL CONFIG")

while nomenu != "4":
	if nomenu == "1":

	# --- MODE SURVEILLANCE-------------------------------------------------------------------------------------------------------------------------

		os.system("clear")
		print("\n----SURVEILLANCE----\n--------------------\n")	
		print("Paramètrage de la surveillance de bande.\n")

		debut = freq_debut()
		fin = freq_fin(debut)
		resolution = bin_size()
		croping = crop()
		gain_val = gain()
		intervalle = interval()
		temps_surv = tps_surv()
		fichier = file(debut,fin)


		commande_bash = surveillance(debut,fin,resolution,croping,gain_val,intervalle,temps_surv,fichier)
		print(commande_bash)   #décommenté permet de voir la commande envoyée
		os.system(commande_bash)

		commande_heatmap = heatmap(fichier)
		os.system(commande_heatmap)

		os.system("rm survey_files/{}.csv".format(fichier)) 
		print("supp OK\n")
		os.system("clear")


		print("----MODES----\n-------------\n")
		nomenu = menu("SURVEILLANCE","EDITION CONFIG","RAPPEL CONFIG","EXIT")

	elif nomenu == "2":

	# --- MODE EDITION CONFIG ----------------------------------------------------------------------------------------------------------------------

		os.system("clear")
		print("\n----EDITION CONFIG----\n----------------------\n")
		print("Création de configuration de surveillance\n")

		visu = ""
		format_visu = r"^[O,o,N,n]{1,}$" #formatage de chaine

			# Restriction des erreurs de saisies
		while re.search(format_visu,visu) is None:

			visu = input("\nSouhaitez vous voir les config déja enregistrées?: (O/N)")	
			if re.search(format_visu,visu) is None:
				print("Je n'ai pas compris votre réponse")

		visu = visu.lower()
		if visu == "o":
			print("\n")
			visu_conf()

			enr = ""
			format_enr = r"^[O,o,N,n]{1,}$" #formatage de chaine

				# Restriction des erreurs de saisies
			while re.search(format_enr,enr) is None:

				enr = input("Voulez-vous en creer une? (O/N): ")	
				if re.search(format_enr,enr) is None:
					print("Je n'ai pas compris votre réponse")

			enr = enr.lower()
			if enr == "o":
				debut = freq_debut()
				fin = freq_fin(debut)
				resolution = bin_size()
				croping = crop()
				gain_val = gain()
				intervalle = interval()
				temps_surv = tps_surv()


				commande_config = config(debut,fin,resolution,croping,gain_val,intervalle,temps_surv)

				os.system("clear")
				ok=enr_conf(commande_config)
				print(ok)
				
				print("----MODES----\n-------------\n")
				nomenu = menu("SURVEILLANCE","EDITION CONFIG","RAPPEL CONFIG","EXIT")

			else:

				print("Dommage, retour au menu principal\n")
				os.system("clear")
				print("----MODES----\n-------------\n")
				nomenu = menu("SURVEILLANCE","EDITION CONFIG","RAPPEL CONFIG","EXIT")	

		else:

			enr = ""
			format_enr = r"^[O,o,N,n]{1,}$" #formatage de chaine

				# Restriction des erreurs de saisies
			while re.search(format_enr,enr) is None:

				enr = input("\nVoulez-vous en creer une? (O/N): ")	
				if re.search(format_enr,enr) is None:
					print("Je n'ai pas compris votre réponse")

			enr = enr.lower()
			os.system("clear")
			if enr == "o":
				debut = freq_debut()
				fin = freq_fin(debut)
				resolution = bin_size()
				croping = crop()
				gain_val = gain()
				intervalle = interval()
				temps_surv = tps_surv()

				commande_config = config(debut,fin,resolution,croping,gain_val,intervalle,temps_surv)

				os.system("clear")
				ok=enr_conf(commande_config)
				print(ok)
				


				print("----MODES----\n-------------\n")
				nomenu = menu("SURVEILLANCE","EDITION CONFIG","RAPPEL CONFIG","EXIT")

			else:

				os.system("clear")
				print("Dommage, retour au menu principal\n")

				print("----MODES----\n-------------\n")
				nomenu = menu("SURVEILLANCE","EDITION CONFIG","RAPPEL CONFIG","EXIT")


	# --- MODE RAPPEL CONFIG -----------------------------------------------------------------------------------------------------------------------

	elif nomenu == "3":
		os.system("clear")
		print("\n----RAPPEL CONFIG----\n---------------------\n")
		print("Utilisation d'une configuration existante\n")

		i = visu_conf()

		choice = choix(i)
		conf_voulue=linecache.getline('save.conf',choice)
		config_voulue= conf_voulue[0:len(conf_voulue)-1]
		print(config_voulue)

		conf_voulue=conf_voulue[13:]
		freq_surv = conf_voulue.split(":")
		low_freq=freq_surv[0]
		high_freq=freq_surv[1]

		#Saisie du nom de fichier
		fichier = file(low_freq,high_freq)
		rappel = "{} > survey_files/{}.csv".format(config_voulue,fichier)   #décommenté permet de voir la commande envoyée
		os.system(rappel)

		commande_heatmap = heatmap(fichier)
		os.system(commande_heatmap)

		os.system("rm survey_files/{}.csv".format(fichier)) 
		linecache.clearcache()
		print("supp OK\n")
		os.system("clear")

		print("----MODES----\n-------------\n")
		nomenu = menu("SURVEILLANCE","EDITION CONFIG","RAPPEL CONFIG","EXIT")

	else:
		print("Je n'ai pas compris votre choix")
