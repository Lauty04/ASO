#!/usr/bin/python3


import sys
import os
import subprocess
import urllib.request
import requests
from termcolor import colored, cprint


##URL ULTIMO ITACA
urlitaca ='http://lliurex.net/focal/pool/main/i/itaca/itaca_1.0.8_amd64.deb'
nombre = urlitaca.split("/")[8] ## CORTAMOS EL NOMBRE PARA 
#print(nombre)                   ## LA RUTA DE DESCARGA


if len(sys.argv) < 2 : ##COMPROVAMOS QUE ESTE BIEN EJECUTADO
    cprint('Necesito un argumento de entrada','red')
    cprint('USAGE: [ sudo ./comprovador-instalador.py {programa} ] ','red')
    sys.exit(1)


print('\n')
cprint("*Welcom to the Itaca Installer"+'\n','blue')

id = os.getuid() ##VEMOS QUE SEA SUPERUSUARIO
if id == 0 :
    cprint('-Eres válido'+'\n','green')
else:
    cprint('-Debes ser superusuario,lo siento :('+'\n','red')
    sys.exit(1)



programa=sys.argv[1] ##PROGRAMA QUE VAMOS A VERIFICAR
#print(itaca)

dpkg = subprocess.check_output(["dpkg", "-l"], text=True) ##LISTAMOS LOS PROGRAMAS EN DPKG PARA VER SI ESTA NUESTRO PROGRAMA

if programa in dpkg:
    cprint('-El paquete esta instalado'+'\n','green')
    print('--Desea continuar? [y/n]')
    sigue = input()
    #print (sigue)

    if sigue == 'y' or 'yes' or 's' or 'si':
        print('-Continuamos con la verificacion --->'+'\n')
    else:
        print('-Bye Bye ***') ##LLUEGO DE LA VERIFICACION
        sys.exit(1)
   
else:
    cprint('-El paquete no esta instalado','yellow')
    print('--Deseas instalarlo? [y/n]') ##PREGUNTAMOS SI DESEA INSTALARLO
    insta = input()
    
    print('--Cual es tu home?')
    home = input()
    home = '/home/'+home+'/'

    print('--En que ruta deseas instalarlo?[ Descargas/ | Escritorio/ | /tmp/ ]')
    directorio = input() #PREGUNTAMOS EN QUE RUTA DESEA
    ruta = home+directorio
    

    descarga = ruta + nombre ##RUTA FINAL DE DESCARGA
    print(descarga)

            #COMPROVAMOS LA EJECUCION

    if directorio not in ['Descargas/', 'Escritorio/', '/tmp/']:
        cprint('-Debe ser una de las opciones [ Descargas/ | Escritorio/ | /tmp/ ]','red')
        sys.exit(1)
    
        ##VERIFICAMOS SI DESEA INSTALARLO
    if insta == 'y' or 'yes' or 's' or 'si':
        print(urlitaca, descarga)
        urllib.request.urlretrieve(urlitaca , descarga) ## Lo descargamos
        comando="sudo dpkg -i "+descarga
        subprocess.run(comando , shell=True)
    else: 
        print('-Perfecto, hasta luego!!')
        sys.exit1



##MOSTRAMOS LOS PAQUETES INSTALADOS REFERIDOS AL PROGRAMA QUE VERIFICAMOS
dpkg = subprocess.check_output(["dpkg", "-l"], text=True)
lineas = dpkg.splitlines()
print('**Los paquetes instalados de '+programa+' son:')

for linea in lineas:
    if programa in linea: 
        cprint(linea+'\n','blue')


sys.exit(0)
