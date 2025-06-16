#Actividad 1 Nahman Martina y Germani Emiliano
import socket
import threading


# --- CONFIGURACIÓN --
PORT = 60000
BROADCAST_IP = '255.255.255.255'

#CREAMOS Y CONFIGURAMOS EL SOCKETE
sock= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) 
sock.bind(("0.0.0.0", 60000)) 

#PEDIMOS NOMBRE DE USUARIO
username=input(str("Ingrese su nombre de usuario: "))

def recibir_mensajes(sock):
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            mensaje = data.decode("utf-8")
            usuario, texto = mensaje.split(":", 1)

            if texto == "exit":
                print(f"El usuario {usuario} ({addr[0]}) ha abandonado la conversación")
            elif texto == "nuevo":
                print(f"El usuario {usuario} se ha unido a la conversación")
            else:
                print(f"{usuario} ({addr[0]}) dice: {texto}")
        except:
            break

def enviar_mensajes(sock, username):
    # Al iniciar, se anuncia como nuevo
    sock.sendto(f"{username}:nuevo".encode("utf-8"), (BROADCAST_IP, PORT))
    while True:
        texto = input()
        mensaje = f"{username}:{texto}"
        sock.sendto(mensaje.encode("utf-8"), (BROADCAST_IP, PORT))
        if texto == "exit":
            break

# --- CREAR Y EJECUTAR LOS HILOS ---
hilo_receptor = threading.Thread(target=recibir_mensajes, args=(sock,), daemon=True)
hilo_receptor.start()

enviar_mensajes(sock, username)

# --- CERRAR SOCKET AL SALIR ---
sock.close()
