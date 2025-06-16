#Martina Nahman 
#Emiliano Germani

#Funcion que elimina el correspondiente 7D
def delete7D(cadena,pos):
    #Verifica si los 2 valores que tiene atras es un 7D
    if cadena[pos-2]=="D" and cadena[pos-3]=="7":
        #Vuelve a entrar a la funcion delete pero en la posicion "D"
        cadena=delete7D(cadena,pos-2)
    else:
        #Elimina el ultimo 7D encontrado
        cadena=cadena[:pos-1] + cadena[pos+1:]
    #retorna la cadena sin el 7D
    return cadena

#Funcion que verifica si hay 7D
def verificate7D(cadena,pos):
    #Verifica si los 2 valores que tiene atras es un 7D
    if cadena[pos-2]=="D" and cadena[pos-3]=="7":
        #Retorna True en caso afirmativo
        return True
    else:
        #Retorna False en caso que no se encuentre
        return False

#Funcion que verifica si la Longitud de la Trama es correcta
def long_correcta(trama):
    #Guardo la Longitud de la trama
    longitud = len(trama)
    if longitud <8:
        #trama demasiado corta
        return False 
    #buscamos el valor de la longitud a verificar
    subcadena = trama[2:6] 
    #longitud de la trama sin incluir los campos bandera, longitud y checksum.
    long_trama = trama[6:(longitud-2)]
    #paso a decimal mi subcadena
    subcadena_decimal = int(subcadena,16)
    if (len(long_trama) == subcadena_decimal*2):
        return True
    else:
        return False

def check_sum(trama):
    longitud = len(trama)
    #todos los bytes sin incluir el bit bandera, el campo longitud y el checksum
    subcadena = trama[6:(longitud-2)]
    #convertimos la subcadena a bytes para poder sumarlos
    subcadena_bytes = bytes.fromhex(subcadena)
    #sumamos todos los bytes de la subcadena
    suma_bytes = sum(subcadena_bytes)
    #calculamos el checksum con la fórmula: 0xFF - (suma de bytes & 0xFF)
    checksum_calculado = 0xFF - (suma_bytes & 0xFF)

    #checksum a validar, ultimos 2 byte
    checksum = trama[(longitud-2):]
    #paso a decimal mi checksum 
    checksum_decimal = int(checksum,16)

    #verificamos si coinciden
    if checksum_calculado == checksum_decimal:
        return True
    else:
        return False



archivo = open(r"C:\Users\Usuario\Documents\MARTI\FING\2025\Redes\TPS\tp1\Tramas_802-15-4.log", "r", encoding="utf-8")

#Guardo todo el texto del archivo en "contenido" como String
contenido=archivo.read()
cont=0
#Guardo la posicion del primer 7E que existe
position=contenido.find("7E")+1
#string.find(value, start, end)
#Guardo en la subcadena "cadena1" todo el contenido del archivo
cadena1 = contenido
tramasTotales=0
tramasLongCorrecta=0
tramasLongIncorrecta=0
tramasLongChecksumCorrecto=0
tramasLongChecksumIncorrecto=0
tramasSecEscape=0
lista_secuenciaEscape=[]
lista_LongIncorrecto=[]
lista_CheckSumIncorrecto=[]
secEsc=False
i=0 #Numero de Trama
#Repito el proceso hasta que no hayaAn mas "7E"
while (cadena1.find("7E")!=-1):
    #Guarda la posicion del siguiente 7E
    pos1=cadena1.find("7E",1)+1
    #Realiza un bucle hasta encontrar el proximo 7E que no contenga 7D atras
    while verificate7D(cadena1,pos1):
        #Booleano que uso para poder guardar en una lista la trama que tiene secuencia de escape
        secEsc=True
        #En caso de encontrar 7D suma 1 a la secuencia de escape
        tramasSecEscape=tramasSecEscape+1
        #Elimina el 7D correspondiente
        cadena1=delete7D(cadena1,pos1)
        #Busca el siguiente 7E
        pos1=cadena1.find("7E",pos1)+1
    #Guardo la trama con secuencia de escape en su respectiva lista
    if secEsc==True:
        lista_secuenciaEscape.append(str(i) + ": " + cadena1[:pos1-1])
        secEsc=False
    """print ("Trama ",i, ": ", cadena1[:pos1-1])"""
    
    #Sumo 1 a las tramas totales
    tramasTotales=tramasTotales+1
    #Verifico si la trama encontrada tiene la Longitud correcta
    longC=long_correcta(cadena1[:pos1-1])
    #Verifico si la trama encontrada tiene el CheckSum correcto
    sumC=check_sum(cadena1[:pos1-1])
    
    
    if longC==True:
        #Sumo 1 a trama con Longitud correcta
        tramasLongCorrecta=tramasLongCorrecta+1
        if sumC==True:
            #Sumo 1 a trama con Longitud correcta y checksum correcto
            tramasLongChecksumCorrecto=tramasLongChecksumCorrecto+1
        else:
            #Sumo 1 a trama con Longitud correcta y checksum incorrecto
            tramasLongChecksumIncorrecto=tramasLongChecksumIncorrecto+1
    else:
        #Guardo la trama con longitud incorrecta en su respectiva lista
        lista_LongIncorrecto.append(str(i) + ": " + cadena1[:pos1-1])
        #Sumo 1 a trama con Longitud incorrecta
        tramasLongIncorrecta=tramasLongIncorrecta+1
    if sumC==False:
        #Guardo la trama con CheckSum incorrecto en su respectiva lista
        lista_CheckSumIncorrecto.append(str(i) + ": " + cadena1[:pos1-1])
    #cadena1 comienza a partir del ultimo 7E encontrado
    cadena1=cadena1[pos1-1:len(contenido)]
    #Sumo 1 a la siguiente Trama
    i=i+1
print("Tramas Totales: ",tramasTotales)
print("Tramas con longitud correcta: ", tramasLongCorrecta)
print("Tramas con longitud incorrecta: ", tramasLongIncorrecta)
print("Tramas con longitud correcta y checksum correcto: ", tramasLongChecksumCorrecto)
print("Tramas con longitud correcta checksum incorrecto: ", tramasLongChecksumIncorrecto)
print ("Tramas con secuencia de escape: ",tramasSecEscape)
print("")
print("Tramas con Secuencia de escape:")
for trama in lista_secuenciaEscape:
    print (trama)
print("")

print("Tramas con Longitud incorrecta:")
for trama in lista_LongIncorrecto:
    print (trama)
print("")

print("Tramas con CheckSum Incorrecto:")
for trama in lista_CheckSumIncorrecto:
    print (trama)
print("")