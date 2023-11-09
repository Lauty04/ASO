#!/usr/bin/python3
import subprocess
import sys
servicio = sys.argv[1]
print(servicio)
comando = subprocess.run(['service', servicio, 'status'], capture_output=True, text=True)
resultado = comando.stdout

resultado = resultado.split()
ifis = ''
if '(running)' in resultado:
    ifis = 'El servicio ' + servicio + ' está activo.'
elif '(dead)' in resultado:
    ifis = 'El servicio ' + servicio + ' está inactivo.'
else:
    ifis = 'El servicio ' + servicio + 'no existe.'
print(ifis)
