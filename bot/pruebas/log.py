#!/usr/bin/python3


logs = '/var/log/syslog'
destino = '/var/log/logsbot'


with open(logs, 'r') as archivo_origen, open(destino, 'w') as archivo_destino:
    for linea in archivo_origen:
        if 'error' in linea or 'ERROR' in linea:
            archivo_destino.write('linea' + linea+'\n')
