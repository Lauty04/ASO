#!/usr/bin/python3

import psutil
import subprocess
# Obtén una lista de todas las conexiones de red
conexiones = psutil.net_connections()

for conn in conexiones:
    if 'LISTEN' in conn :
        print(f"LADDR: {conn.laddr}, Status: {conn.status}"+'\n')
        puerto = str(conn.laddr.port)
        comando = f"sudo lsof -i :{puerto} | tail -n1 | cut -d / -f1"
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, executable='/bin/bash')
        print(resultado.stdout)
        entre = resultado.stdout.split()
        medio = entre[0]
        pripuerto = str(medio)
        print("El puerto: "+puerto+ f" esta: {conn.status} "+pripuerto+'\n')
        print('\n')

