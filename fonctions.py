import time
import re
from getpass import *
import hashlib
import os

def menu(*titres):

#Gestion des titres des menus
	
	titres = list(titres)
	for i,titre in enumerate(titres):
		titres[i]=str(titre)
		n = str(i+1)
		chaine = n + "  - " + titres[i] + "\n"

		print(chaine)

		mode = ""
		taille_menu = len(titres)
		format_mode = r"^[1-9]$" #formatage de chaine

		# Restriction des erreurs de saisies
	while re.search(format_mode,mode) is None or int(mode) > taille_menu:

		mode = input("\nChoisissez un mode: ")	
		if re.search(format_mode,mode) is None:
			print("Ce n'est pas une valeur attendue")	
		elif int(mode) > taille_menu:
			print("Ce menu n'existe pas")

	return mode

def freq_debut():

#fréquence de debut de surveillance

	low_freq = ""
	format_low_freq = r"[0-9]?[0-9]?[0-9][0-9].?[0-9]?[0-9]?[M,m]" #formatage de chaine

	# Restriction des erreurs de saisies
	while re.search(format_low_freq,low_freq) is None or float(low_freq[0:len(low_freq)-1])<24 or float(low_freq[0:len(low_freq)-1])>1700:
	
		low_freq = input("Fréquence du début de surveillance (ex: 81.3M): ")
		if re.search(format_low_freq,low_freq) is None: 
			print("Mauvais formatage de la fréquence\n")
		elif float(low_freq[0:len(low_freq)-1])<24 or float(low_freq[0:len(low_freq)-1])>1700:
			print("valeur hors gamme (24M - 1700M pour la rtl-sdr)\n")

	return low_freq

def freq_fin(low_freq):

#fréquence de fin de surveillance

	high_freq = ""
	format_high_freq = r"[0-9]?[0-9]?[0-9][0-9].?[0-9]?[0-9]?[M,m]" #formatage de chaine
	
	# Restriction des erreurs de saisies
	while re.search(format_high_freq,high_freq) is None or float(high_freq[0:len(high_freq)-1])<24 or \
	float(high_freq[0:len(high_freq)-1])>1700 or float(high_freq[0:len(high_freq)-1]) < float(low_freq[0:len(low_freq)-1]):
	
		high_freq = input("Fréquence du fin de surveillance (ex: 81.3M): ")
		if re.search(format_high_freq,high_freq) is None: 
			print("Mauvais formatage de la fréquence\n")
		elif float(high_freq[0:len(high_freq)-1])<24 or float(high_freq[0:len(high_freq)-1])>1700:
			print("valeur hors gamme (24M - 1700M pour la rtl-sdr)\n")
		elif float(high_freq[0:len(high_freq)-1]) < float(low_freq[0:len(low_freq)-1]):
			print("La fréquence de fin de surveillance est inférieure à celle du début")

	return high_freq

def bin_size():

#Ecarts entre les points de mesures

	bin_size = ""
	format_bin_size = r"^[0-9]{1,}$" #formatage de chaine

		# Restriction des erreurs de saisies

	bin_size_ok=True			
	while bin_size_ok:
		try:
			bin_size = input("Entrer l'écart entre les points de mesures ( en Hz entre 1 et 2800000): ")
			if re.search(format_bin_size,bin_size) is None: 
				print("Mauvais formatage\n")
				bin_size_ok = True
			elif float(bin_size)<1 or float(bin_size)>2800000:
				print("valeur hors gamme (1Hz - 2800000Hz)\n")		
				bin_size_ok = True
			else:
				bin_size_ok = False
		except ValueError:
			print("Veillez à ne saisir que des chiffres")
			bin_size_ok = True

	return bin_size

def crop():

#Gestion du crop en pourcentage

	crop = ""
	format_crop = r"^[0-9][0-9]?$" #formatage de chaine

		# Restriction des erreurs de saisies

	crop_ok = True
	while crop_ok:
		try:
			crop = input("Entrer le pourcentage de crop (0 = no crop, crop compris entre 20 et 50%): ")
			if re.search(format_crop,crop) is None: 
				print("Mauvais formatage")
				crop_ok = True
			elif int(crop)<0 or int(crop) > 50:
				print("Valeur hors gamme (19 < crop < 51)")
				crop_ok = True
			else:
				crop_ok = False
		except ValueError:
			print("Veillez à ne saisir que des chiffres")
			crop_ok = True

		if crop != "0":
			string_crop = " -c {}%".format(crop)
		else:
			string_crop = ""

	return string_crop

def gain():

#Gestion du gain

	gain = ""
	format_gain = r"[0-9]?[0-9].?[0-9]?[0-9]?" #formatage de chaine

		# Restriction des erreurs de saisies
	gain_ok=True			
	while gain_ok:
		try:
			gain = input("Entrer le gain (de 1 à 50 max, 0 = auto): ")
			if re.search(format_gain,gain) is None: 
				print("Mauvais formatage\n")
				gain_ok = True
			elif float(gain)<0 or float(gain)>50:
				print("valeur hors gamme (0 - 50)\n")		
				gain_ok = True
			else:
				gain_ok = False
		except ValueError:
			print("Veillez à ne saisir que des chiffres")
			gain_ok = True

		if gain != "0":
			string_gain = " -g {}".format(gain)
		else:
			string_gain = ""

	return string_gain

def interval():

#Intervalle de temps entre les prises de mesures

	interval = ""
	format_interval = r"[0-9]?[0-9][s,m,h,S,M,H]" #formatage de chaine

		# Restriction des erreurs de saisies
	interval_ok = True	
	while interval_ok:
		try:
			interval = input("Entrer l'intervalle de temps entre les mesures (mini 1s, supporte s/m/h): ")
			unite = interval[len(interval)-1]

			if re.search(format_interval,interval) is None: 
				print("Mauvais formatage de l'intervalle\n")
				interval_ok = True
			elif float(interval[0:len(interval)-1])<1:
				print("Minimum 1s\n") 
				interval_ok = True
			elif unite == "s" and float(interval[0:len(interval)-1])>86400:
				print("Maximun 24h\n") 
				interval_ok = True
			elif unite == "m" and float(interval[0:len(interval)-1])>3600:
				print("Maximun 24h\n") 
				interval_ok = True
			elif unite == "h" and float(interval[0:len(interval)-1])>24:
				interval_ok = True						
			else:
				interval_ok = False
		except ValueError:
			print("Erreur")
			interval_ok = True

	return interval

def tps_surv():

#Durée de la surveillance

	tps_surv = ""
	format_tps_surv = r"[0-9]?[0-9][s,m,h,S,M,H]" #formatage de chaine

		# Restriction des erreurs de saisies
	tps_surv_ok = True	
	while tps_surv_ok:
		try:
			tps_surv = input("Entrer la durée de surveillance de temps entre les mesures (mini 1s, supporte s/m/h): ")
			unite_t = tps_surv[len(tps_surv)-1]

			if re.search(format_tps_surv,tps_surv) is None: 
				print("Mauvais formatage du temps de surveillance\n")
				tps_surv_ok = True
			elif float(tps_surv[0:len(tps_surv)-1])<1:
				print("Minimum 1s\n") 
				tps_surv_ok = True
			elif unite_t == "s" and float(tps_surv[0:len(tps_surv)-1])>86400:
				print("Maximun 24h\n") 
				tps_surv_ok = True
			elif unite_t == "m" and float(tps_surv[0:len(tps_surv)-1])>3600:
				print("Maximun 24h\n") 
				tps_surv_ok = True
			elif unite_t == "h" and float(tps_surv[0:len(tps_surv)-1])>24:
				tps_surv_ok = True						
			else:
				tps_surv_ok = False
		except ValueError:
			print("Erreur")
			tps_surv_ok = True

	return tps_surv

def file(low_freq,high_freq):

#Nom de fichier

	file = ""
	format_file = r"^[A-Za-z0-9]{1,}$" #formatage de chaine

		# Restriction des erreurs de saisies
	while re.search(format_file,file) is None:

		file = input("\nEntrez un nom de fichier: ")	
		if re.search(format_file,file) is None:
			print("Mauvais nom de fichier")	

	gdh=time.localtime()
	file_name="{}:{}__{}-{}-{}_{}:{}__{}".format(low_freq,high_freq,gdh.tm_mday,gdh.tm_mon,gdh.tm_year,gdh.tm_hour,gdh.tm_min,file)

	return file_name

def surveillance(low_freq,high_freq,bin_size,crop,gain,interval,tps_surv,file):

#Mise en forme de la commande bash de rtl_power
	#streaming dans un fichier à l'aide de '>>'
	commande_bash = "rtl_power -f {}:{}:{}{}{} -i {} -e {} >>survey_files/{}.csv".format(low_freq,high_freq,bin_size,crop,gain,interval,tps_surv,file)
	
	return commande_bash

def config(low_freq,high_freq,bin_size,crop,gain,interval,tps_surv):

#Mise en forme de la commande bash de rtl_power à conserver en fichier conf
	#streaming dans un fichier à l'aide de '>>'
	commande_conf = "rtl_power -f {}:{}:{}{}{} -i {} -e {} ".format(low_freq,high_freq,bin_size,crop,gain,interval,tps_surv)
	
	return commande_conf

def heatmap(file):

# réalise le heatmap du fichier de surveillance
	commande_heatmap = "python3 heatmap.py --palette charolastra 'survey_files/{}.csv' 'heatmap_files/{}.png'".format(file,file)

	return commande_heatmap

def gestion_mdp(mdp):
	
#Gestion et traitement des mots de passe
	mdp = mdp.encode()
	mot_de_passe_chiffre = hashlib.sha256(mdp).hexdigest()

	verrouille = True
	while verrouille:

		entre = getpass("Tapez votre mot de passe: ")

		entre = entre.encode()
		entre_chiffre =	hashlib.sha256(entre).hexdigest()
		if entre_chiffre == mot_de_passe_chiffre:
			verrouille = False
		else:
			print("Mot de passe incorrect")

	print("Mot de passe accepté...")

def visu_conf():       

#Visualisation du fichier conf
	if os.path.exists('save.conf'):
		with open('save.conf','r') as fichier_conf:
			for i,line in enumerate(fichier_conf):
				i+=1
				print(i,line)
		return i
	else:
		with open('save.conf','a') as fichier_conf:
			print("\nAucune configuration enregistrée")
			chaine = ""
		return(chaine)

def enr_conf(commande_config):

#Enregistrement du fichier conf
	commande_config += "\n"
	#print(commande_config)

	with open('save.conf','a') as fichier_conf:
		fichier_conf.write(commande_config)

	ok = "\n*** Configuration bien enregistrée. ***\n\n" 
	return ok

def choix(i):

#Permet de choisir une config
	choix = ""
	format_choix = r"^[1-9]$" #formatage de chaine

	# Restriction des erreurs de saisies
	while re.search(format_choix,choix) is None or int(choix) >i:

		choix = input("\nChoisissez une configuration: ")	
		if re.search(format_choix,choix) is None:
			print("Ce n'est pas une valeur attendue")
		elif int(choix) > i:	
			print("cette configuration n'existe pas")

	choix=int(choix)
	return choix


#-----------------------------------------------------------------------------------------------------------------------------------------------
