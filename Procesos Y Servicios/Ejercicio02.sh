#!/bin/bash



if [ $(id -u) -ne 0 ]; then



	exit 1

fi





ides=$(docker ps -q)



echo "| Nombre del Contenedor | IP de Red |"





for id in $ides; do

  nombre=$(sudo docker inspect --format '{{.Name}}' "$id" | cut -d '/' -f2)

  ip=$(sudo docker inspect  "$id" | grep 'IPAddres' | tail -n1 | cut -d ':' -f2)

echo "| $nombre               | $ip"

done

