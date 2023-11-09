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
