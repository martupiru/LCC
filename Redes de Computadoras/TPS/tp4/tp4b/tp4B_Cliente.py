#TP4B Germani y Nahman
#CLIENTE

import socket

def cliente():
    servidor_ip = input("Ingrese la IP del servidor: ")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((servidor_ip, 60000))
    print("[+] Conectado al servidor.")

    # Recibir nombre y tamaño del archivo
    encabezado = sock.recv(1024).decode()
    if encabezado.startswith("ERROR"):
        print("[!] Error del servidor:", encabezado)
        sock.close()
        return

    nombre_archivo, tamaño_str = encabezado.split("|")
    tamaño_total = int(tamaño_str)

    # Confirmar que estamos listos
    sock.sendall(b"OK")

    # Recibir archivo y guardarlo
    recibido = 0
    with open("recibido_" + nombre_archivo, "wb") as f:
        while recibido < tamaño_total:
            datos = sock.recv(1024)
            if not datos:
                break
            f.write(datos)
            recibido += len(datos)

    print(f"[+] Archivo recibido y guardado como: recibido_{nombre_archivo}")
    sock.close()

if __name__ == "__main__":
    cliente()
