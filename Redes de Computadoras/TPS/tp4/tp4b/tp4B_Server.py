#TP4B Germani y Nahman
#SERVIDOR

import socket
import os

HOST = '0.0.0.0'
PORT = 60000

def servidor():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)
    print(f"[+] Servidor escuchando en {HOST}:{PORT}")

    conn, addr = sock.accept()
    print(f"[+] Conexión establecida desde {addr}")

    # Pedir al usuario del servidor el nombre del archivo
    nombre_archivo = input("Ingrese la ruta del archivo a enviar: ")

    # Verificar si el archivo existe
    if not os.path.exists(nombre_archivo):
        print("[!] El archivo no existe. Cerrando conexión.")
        sock.close()
        conn.sendall(b"ERROR: Archivo no encontrado.")
        conn.close()
        return

    # Enviar nombre del archivo y tamaño
    tamaño = os.path.getsize(nombre_archivo)
    conn.sendall(f"{os.path.basename(nombre_archivo)}|{tamaño}".encode())

    # Esperar confirmación
    confirmacion = conn.recv(1024).decode()
    if confirmacion != "OK":
        print("[!] Cliente no listo para recibir el archivo.")
        conn.close()
        return

    # Enviar archivo en bloques
    with open(nombre_archivo, "rb") as f:
        while True:
            bloque = f.read(1024)
            if not bloque:
                break
            conn.sendall(bloque)

    print(f"[+] Archivo '{nombre_archivo}' enviado con éxito.")
    conn.close()
    sock.close()

if __name__ == "__main__":
    servidor()
