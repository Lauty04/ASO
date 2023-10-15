#!/usr/bin/python3


import sys
import os
import subprocess
import wget
from termcolor import colored, cprint
import subprocess
import urllib.request




cprint("*Welcom to the Itaca Installer"+'\n','blue')

id = os.getuid() ##VEMOS QUE SEA SUPERUSUARIO
if id == 0 :
    cprint('-Eres válido'+'\n','green')
else:
    cprint('[ERROR]-Debes ser superusuario,lo siento :('+'\n','red')
    sys.exit(1)



programa='itaca'
ubi = '/home/principal2do/Descargas/itaca_1.0.8_amd64.deb'
urlitaca = 'http://lliurex.net/focal/pool/main/i/itaca/itaca_1.0.8_amd64.deb'
comando = "sudo dpkg -i "+ ubi
borrar = "sudo dpkg -P itaca"
dpkg = subprocess.check_output(["dpkg", "-l"], text=True) ##LISTAMOS LOS PROGRAMAS EN DPKG PARA VER SI ESTA NUESTRO PROGRAMA

if programa in dpkg:
    cprint('-El paquete esta instalado'+'\n','green')
    print('--Desea reinstalarlo? [y/n]')
    sigue1 = input()
    #print (sigue)
    subprocess.run(borrar, shell=True, check=True)
    if os.path.exists(ubi):
        os.remove(ubi)
    if sigue1 == 'y' or sigue1 == 'yes' or sigue1 == 's' or sigue1 == 'si' : 
        urllib.request.urlretrieve(urlitaca , ubi) ## Lo descargamos
        subprocess.run(comando , shell=True)
    else:
        print('Bye Bye :)')
        sys.exit(1)

else:
    cprint('-El paquete no esta instalado'+'\n','red')
    print('--Desea instalarlo? [y/n]')
    sigue = input()
    if sigue == 'y' or sigue == 'yes' or sigue == 's' or sigue == 'si' :
        urllib.request.urlretrieve(urlitaca , ubi) ## Lo descargamos
        subprocess.run(comando , shell=True)

    else :
        print('Bye Bye :) 2')
        sys.exit(1)

































sys.exit(0)
