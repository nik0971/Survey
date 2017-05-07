import re
from fonctions import *
import os
import linecache


def zob():
	if os.path.exists('save.conf'):
		with open('save.conf','r') as fichier_conf:
			for i,line in enumerate(fichier_conf):
				i+=1
				print(i,line)
	return i

zob()
i=zob()
print (i)

conf_voulue=linecache.getline('save.conf',2)
config_voulue= conf_voulue[0:len(conf_voulue)-1]
print(config_voulue)