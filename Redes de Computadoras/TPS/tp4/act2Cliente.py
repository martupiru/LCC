#Actividad 2 Nahman Martina y Germani Emiliano
#CLIENTE
import socket
import threading

def recibir(sock):
    while True:
        try:
            #Lee continuamente desde el servidor. Si no hay datos o hay error, termina
            datos = sock.recv(1024)
            if not datos:
                break
            print(datos.decode())
        except:
            break

def cliente():
    #Pide la IP del servidor
    servidor_ip = input("Ingrese la IP del servidor: ")
    #Crea un socket TCP y lo conecta al servidor.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((servidor_ip, 60000))

    nombre = input("Ingrese su nombre de usuario: ")
    sock.sendall(nombre.encode())  # Enviamos el nombre al conectarse

    threading.Thread(target=recibir, args=(sock,), daemon=True).start()

    while True:
        texto = input()
        if texto.strip().lower() == "exit":
            sock.sendall(b"exit")
            break
        sock.sendall(texto.encode())

    sock.close()

if __name__ == "__main__":
    cliente()
