#!/usr/bin/python3

import sys
import os
import re
from termcolor import colored, cprint

# Some useful values
DATE_FORMAT="\'YYYY-MM-DD\'"
THIS_VERSION="20231006-v5"

# Some sanity checks

cprint(" * Script version "+THIS_VERSION,'green')

if len(sys.argv) < 4:
    cprint(" USAGE : oraclize.py ORIG.sql DEST.sql TABLESPACE",'red',attrs=['underline'])
    sys.exit(1)


orig = open(sys.argv[1],'r')
if os.path.exists(sys.argv[2]):
    cprint(" * Old file present...removing it!",'green')
    os.remove(sys.argv[2])
    
destinosql = open(sys.argv[2],'x')

elultimoinsertbueno = ""

for line in orig:
    auxp = line 

    if auxp.startswith("SET"):
        auxp= auxp.replace(auxp,'--'+auxp)
    if auxp.startswith("START"):
        auxp= auxp.replace(auxp,'--'+auxp)


    # Tipos de datos
    if auxp.startswith(") ENGINE"):
        auxp = ") TABLESPACE "+sys.argv[3]+";\n"


    #if re.match('varchar', auxp, re.IGNORECASE):
    #    print("Aquitoca"+ auxp)
    
    if "VARCHAR" in auxp:
        auxp = auxp.replace("VARCHAR","VARCHAR2")

    if "varchar" in auxp:
        auxp = auxp.replace("varchar","VARCHAR2")


    if "FLOAT" in auxp:
        auxp = auxp.replace("FLOAT","NUMBER")

    if "float" in auxp:
        auxp = auxp.replace("float","NUMBER")
    
    if " INT " in auxp:
        auxp = auxp.replace(" INT "," NUMBER ")

    if " int(" in auxp:
        auxp = auxp.replace(" int("," NUMBER(")
    
    if auxp.startswith("INSERT INTO") and auxp.endswith("VALUES\n"):
        # Me la guardo
        elultimoinsertbueno = auxp
        auxp = ""

    if auxp.endswith(",\n") and auxp.startswith("("):
        
        auxp = auxp.replace(",\n",";\n")
   
        if "`" in auxp:
            auxp = auxp.replace("`","'")

    
    tablas = line
    tablas = tablas.split()
    #tablas = str(tablas)

    if 'ALTER TABLE' in line:
        tabla = tablas[2]
        tabla = tabla.replace("`","")
        tabla = str(tabla)
        auxp = auxp.replace(auxp,"")
        #print(tabla)


    if 'ADD PRIMARY KEY' in line:
        primary = 'PK_'+tabla
        #print(primary)
        auxp = auxp.replace(" ADD PRIMARY KEY ","  ALTER TABLE "+tabla+"\n"+"  ADD CONSTRAINT "+primary+ " PRIMARY KEY")

    if  auxp.startswith("  ADD KEY"):
        origin = line.split()
        index = origin[2]
        campo = origin[3]
        index = index.replace("`","")
        campo = campo.replace("`","")
        campo = campo.replace(",",";")
        #print (campo)
        #print(index)
        auxp = auxp.replace(auxp ,"  CREATE INDEX "+index +" ON "+tabla+campo+'\n')

    if auxp.startswith("  ADD UNIQUE KEY"):
        unix = line.split()
        uni = unix[3]
        uni = uni.replace("`","")
        camps = unix[4]
        camps = camps.replace("`","")
        #print(camps)

        auxp = auxp.replace(auxp,"  CREATE UNIQUE INDEX "+uni+" ON "+tabla+camps+"\n")
        
    
    if 'FOREIGN KEY' in line:
        auxp = auxp.replace(auxp,'ALTER TABLE '+tabla+'\n'+auxp)



    if auxp.endswith("),\n"):
        auxp = auxp.replace(",\n",";\n")




#Si no queremos comentarios descomentamos estas lineas:

    #if '/*!' in line:
       # auxp = auxp.replace(auxp,"")
    #if auxp.startswith("--"):
     #   auxp = auxp.replace(auxp,"")


    if auxp.startswith("("):
        pattern="\d{4}-\d{2}-\d{2}"

        fechasencontradas = re.findall(pattern,auxp)
        
        if len(fechasencontradas) > 0:
            for fecha in fechasencontradas:
               auxp = auxp.replace('\''+fecha+'\'','TO_DATE(\''+fecha+'\','+DATE_FORMAT+')')
               #print(auxp)

        auxp = elultimoinsertbueno.strip()+auxp
        
        #print(auxp)

    # THE MOTHER OF THE LAMB

    auxp= auxp.replace("`","")


    destinosql.write(auxp+'\n')

destinosql.close()






sys.exit(0)

