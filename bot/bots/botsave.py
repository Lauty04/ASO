#!/usr/bin/env python
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
    comandos = info+'\n'+host+'\n'+ip+'\n'+ping+'\n'+start+'\n'+error_log+'\n'+service_is_running+'\n'+service_start+'\n'+service_stop+'\n'+ports_in_use+'\n'
    await update.message.reply_text(comandos)


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    info_text = "¡Hola! Soy un bot de ejemplo creado en ASO. Mi función es servirte."
    await update.message.reply_text(info_text)

async def host(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    info = platform.platform()
    await update.message.reply_text(info)


async def ip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip=(s.getsockname()[0])
    await update.message.reply_text(ip)


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
    await update.message.reply_text(salida)





async def error_log(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:



    host=update.message.text
    leer = ''
    logs = '/var/log/syslog'
    if host.endswith('/error_log'):
            uso = "[USAGE]: Debes indicarme el numero de errores que quieres leer."
            leer=uso
    else:
        destino = '/var/log/logsbot'
        n = int(context.args[0])


        with open(logs, 'r') as archivo_origen:
            lineas = archivo_origen.readlines()
        if n >= len(lineas):
            leer = lineas
        else:
            leer = lineas[-n:]


        with open(destino, 'w') as archivo_destino:
            for linea in leer:
                if 'error' in linea.lower():
                    archivo_destino.write('\n' + 'linea ' + linea + '\n')

        await update.message.reply_text(''.join(leer))
        os.remove(destino)





async def service_is_running(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

    await update.message.reply_text(ifis)






async def service_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    entrada = update.message.text

    if entrada.endswith('/service_start'):
        ifis='[USAGE] : Debes ejecutar el comando y darme el nombre de un servicio existente en el servidor'
    else:
        servicio = context.args[0]
        arranque = subprocess.run(['sudo', 'service', servicio, 'start'], capture_output=True, text=True)
        ejecuto = arranque.stdout
        arrancado = 'El servicio fue inicializado'


    await update.message.reply_text(arrancado)








async def service_stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    entrada = update.message.text

    if entrada.endswith('/service_stop'):
        ifis='[USAGE] : Debes ejecutar el comando y darme el nombre de un servicio existente en el servidor'
    else:
        servicio = context.args[0]
        arranque = subprocess.run(['sudo', 'service', servicio, 'stop'], capture_output=True, text=True)
        ejecuto = arranque.stdout
        arrancado = 'El servicio fue detenido'


    await update.message.reply_text(arrancado)




async def ports_in_use(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

    await update.message.reply_text(salidacon)


















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



    # on non command i.e message - echo the message on Telegram

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
