#!/usr/bin/python3
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import sys
import os
import logging
import platform
import nmap
import re
import socket
import sys
import psutil
import subprocess
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Consulat con el comando /comandos")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    hola = "Devolvemos el mensaje : "+update.message.text
    await update.message.reply_text(hola)





async def comandos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    start = "/start = saluda al usuario que envia el mensaje"  
    info = "/info = información del bot"
    host = "/host = información del sistema operativo del host"
    ip = "/ip = Obtendremos la ip del host"
    ping = "/ping = Obtendremos la información sobre el ping a una ip"
    error_log = "/error_log Información sobre los errores en /var/log/syslog" 
    service_is_running = "/service_is_running  Devuelve el estado del servicio, si no existe que diga que no esiste el servicio."
    service_start = '/service_start Enciende el servicio, si no existe que lo diga'
    service_stop = '/service_stop Detiene el servicio, si no existe que lo diga'
    ports_in_use = '/ports_in_use Devuelve el listado de puertos y programas que los están usando.'
    counter = '/counter Devuelve en formato resultados de la encuesta el porcentaje de uso de cada uno de los comandos del bot, reiniciando los contadores cuando se pida el informe.'
    nmap = "/nmap Lista las IPs accesibles desde esa red y si podéis el nombre del equipo."
    comandos = info+'\n'+host+'\n'+ip+'\n'+ping+'\n'+start+'\n'+error_log+'\n'+service_is_running+'\n'+service_start+'\n'+service_stop+'\n'+ports_in_use+'\n'+counter+'\n'+nmap+'\n'
    await update.message.reply_text(comandos)






contador_info = 0
contador_host = 0
contador_ip = 0
contador_ping = 0
contador_error = 0
contador_is_running = 0
contador_start = 0
contador_stop = 0
contador_ports = 0
contador_mapeado = 0


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global contador_info
    info_text = "¡Hola! Soy un bot de ejemplo creado en ASO. Mi función es servirte."
    contador_info = contador_info +1
    await update.message.reply_text(info_text)

async def host(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global contador_host
    info = platform.platform()
    contador_host = contador_host +1

    await update.message.reply_text(info)


async def ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global contador_ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip=(s.getsockname()[0])


    contador_ip = contador_ip +1

    await update.message.reply_text(ip)


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global contador_ping
    host=update.message.text
    parametros = host.split()
    parametro = " ".join(parametros[1:])
    resultado = subprocess.run(["ping", "-c", "2", parametro], stdout=subprocess.PIPE, text=True)
    salida = resultado.stdout
    if '2 received' in salida:
        salida = ('EL ping fue efectivo: '+'\n'+'\n'+resultado.stdout)	
    else: 
        salida=('Lo siento no pude realizar el ping a : '+parametro+'\n'+resultado.stdout)
        if host.endswith('/ping'):
            uso = "[USAGE]: Debes ejecutar el /ping mas la ip o el nombre de dominio al que quieres ejecutar el ping, por ejemplo : /ping google.com || /ping 192.168.5.4"
            salida = uso
    
    contador_ping = contador_ping +1

    await update.message.reply_text(salida)





async def error_log(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global contador_error
    host = update.message.text
    nums=context.args[0]
    if host.endswith('/error_log'):
            uso = "[USAGE]: Debes indicarme el numero de errores que quieres leer."
            leer=uso
    else:
        este = "error_log "+ nums
        errores = subprocess.check_output(este, shell=True, text=True)
        ##ejecucion = comado.stdout
        await update.message.reply_text(errores)





async def service_is_running(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global contador_is_running
    entrada = update.message.text

    if entrada.endswith('/service_is_running'):
        ifis='[USAGE] : Debes ejecutar el comando y darme el nombre de un servicio existente en el servidor'
    else:
        servicio = context.args[0]
        comando = subprocess.run(['service', servicio, 'status'], capture_output=True, text=True)
        resultado = comando.stdout
        resultado = resultado.split()
        ifis = '' 
        if '(running)' in resultado:
            ifis = 'El servicio ' + servicio + ' está activo.'
        elif '(dead)' in resultado:
            ifis = 'El servicio ' + servicio + ' está inactivo.'
        else:
            ifis = 'El servicio ' + servicio + ' no existe.'

    contador_is_running = contador_is_running + 1
    await update.message.reply_text(ifis)






async def service_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global contador_start
    entrada = update.message.text
    servicio = context.args[0]
    if entrada.endswith('/service_start'):
        resultado='[USAGE] : Debes ejecutar el comando y darme el nombre de un servicio existente en el servidor'
    else:
        resultado = subprocess.run(["start_service", servicio])
        resultado = 'El servicio fue inicializado con exito ' + str(resultado) 
    contador_start = contador_start +1
    await update.message.reply_text(resultado)








async def service_stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global contador_stop
    entrada = update.message.text
    servicio = context.args[0]
    if entrada.endswith('/service_stop'):
        resultado='[USAGE] : Debes ejecutar el comando y darme el nombre de un servicio existente en el servidor'
    else:
        resultado = subprocess.run(["stop_service", servicio])
        resultado = 'El servicio fue detenido con exito ' + str(resultado)
    
    contador_stop = contador_stop +1

    await update.message.reply_text(resultado)
    




async def ports_in_use(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global contador_ports
    conexiones = psutil.net_connections()
    salidacon = ""  # Inicializar salidacon como una cadena vacía antes del bucle

    for conn in conexiones:
        if 'LISTEN' in conn:
            puerto = str(conn.laddr.port)
            comando = f"sudo lsof -i :{puerto} | tail -n1 | cut -d / -f1"
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True, executable='/bin/bash')
            entre = resultado.stdout.split()
            medio = entre[0]
            pripuerto = str(medio)
            vueltas = "El puerto: " + puerto + f" esta: {conn.status} usado por el programa: " + pripuerto + "\n"
            salidacon += vueltas  # Concatenar cada iteración
    contador_ports = contador_ports +1
    await update.message.reply_text(salidacon)




async def counter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global contador_info
    global contador_host
    global contador_ip
    global contador_ping
    global contador_error
    global contador_is_running
    global contador_start
    global contador_stop
    global contador_ports
    global contador_mapeado
    
    contador_global = contador_info +contador_host+contador_ip+contador_ping+contador_error+contador_is_running+contador_start+contador_stop+contador_ports
    
    vuelta = (
        "El porcentaje de uso del comando /info es de " "%" + str(contador_info/contador_global*100) + "\n" +
        "El porcentaje de uso del comando /host es de " "%" + str(contador_host/contador_global*100) + "\n" +
        "El porcentaje de uso del comando /ip es de " "%" + str(contador_ip/contador_global*100) + "\n" +
        "El porcentaje de uso del comando /ping es de " "%" + str(contador_ping/contador_global*100) + "\n" +
        "El porcentaje de uso del comando /error_log es de " "%" + str(contador_error/contador_global*100) + "\n" +
        "El porcentaje de uso del comando /service_is_running es de " "%" + str(contador_is_running/contador_global*100) + "\n" +
        "El porcentaje de uso del comando /service_start es de " "%" + str(contador_start/contador_global*100) + "\n" +
        "El porcentaje de uso del comando /service_stop es de " "%" + str(contador_stop/contador_global*100) + "\n" +
        "El porcentaje de uso del comando /ports_in_use es de " "%" + str(contador_ports/contador_global*100) + "\n" +
        "El porcentaje de uso del comando /mapeado es de " "%" + str(contador_mapeado/contador_global*100) + "\n" 
)
    contador_info = 0
    contador_host = 0
    contador_ip = 0
    contador_ping = 0
    contador_error = 0
    contador_is_running = 0
    contador_start = 0 
    contador_stop = 0
    contador_ports = 0
    contador_mapeado = 0
    await update.message.reply_text(vuelta)








async def mapeado(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    global contador_mapeado
    variable=''
    ips=0
    ip = context.args[0] 
    valida = r'^(\d{1,3}\.){3}\d{1,3}(\/\d{1,2})?$'
    
    nm = nmap.PortScanner()
    if re.match(valida, ip):
        try:
            
            hola = nm.scan(hosts=ip, arguments='-n -sP -PE -PA21,23,80,3389', timeout=60)
            if hola:
                hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
                for host, status in hosts_list:
                    variable += "-------·-------\n IP: " +  host  +": " + status + "\n"
                    ips += 1
            respuesta = "* IP's UP * \n \n" + variable + "\n Cantidad de ip en la red: " + str(ips)
                    
        except:
            variable = "* [Error] no se encontro nada en la ip: " + ip 
            
    else:
        
        variable  = "La ip " + host + " no es correcta"
    contador_mapeado = contador_mapeado +1
    await update.message.reply_text(respuesta)












def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6633158712:AAFwlYdHmbCH6nQv3uQvYYsmOustwFjWP_M").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start)) 
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info)) 
    application.add_handler(CommandHandler("host", host))
    application.add_handler(CommandHandler("ip", ip))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CommandHandler("comandos", comandos))
    application.add_handler(CommandHandler("error_log", error_log))  
    application.add_handler(CommandHandler("service_is_running",service_is_running))
    application.add_handler(CommandHandler("service_start",service_start))
    application.add_handler(CommandHandler("service_stop",service_stop))
    application.add_handler(CommandHandler("ports_in_use",ports_in_use))
    application.add_handler(CommandHandler("counter",counter))
    application.add_handler(CommandHandler("nmap",mapeado))

    # on non command i.e message - echo the message on Telegram

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
