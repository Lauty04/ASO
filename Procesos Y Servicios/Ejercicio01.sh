#!/bin/bash



#comprovacion de permisos de root



echo #espacio de presentacion

echo '-[Comprovacion de permisos]'

echo



nombre=$(whoami)



if [ $nombre='root'  ]; then

	echo '*Si es root'

else 

	echo '*no es root'

fi

echo

#fin de comprovacion





#parametro de ip

echo '-[Comprovacion de parametro IP]'

echo

read -p 'Dame una ip : ' ip #pedimos la ip



if [ -z $ip  ]; then

	echo '*-----No me diste una ip'

	exit 1

	

else

	echo '*-----Gracias por tu ip' $ip



fi

echo

#fin de comprovacion de parametro



#Validacion de ip

echo '-[Validación de IP]'

echo

if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then

	echo '*-----Tu ip es valida'

else

	echo '*-----Tu ip no es valida'

fi

echo

#fin de validacion





#comprovando ping

echo '-[Comprovación de ping]'

echo

Error='NO HAY ERROR'

ping -c 1 $ip >> /dev/null || Error='SI HAY ERROR'

echo $Error

Ping=$Error

if [ "$Ping" = 'NO HAY ERROR'  ]; then

	echo 'Ping efectivo'

else

	echo 'El ping Fallo'

fi

echo



#fin de ping





#Servicios

echo '-[Servicios :]'

echo

nmap $ip