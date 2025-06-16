# Actividad 2 Nahman Martina y Germani Emiliano
# SERVIDOR CON CIERRE CONTROLADO
import socket
import threading

HOST = '0.0.0.0'
PORT = 60000

clientes = {}  # socket: (nombre, dirección IP)
lock = threading.Lock()
servidor_activo = True  # Variable para controlar el estado del servidor

def manejar_cliente(conn, addr):
    global clientes
    try:
        nombre = conn.recv(1024).decode()
        with lock:
            clientes[conn] = (nombre, addr[0])

        print(f"[+] {nombre} ({addr[0]}) se ha conectado.")
        broadcast(f"El usuario {nombre} se ha unido a la conversación", conn)

        while True:
            datos = conn.recv(1024)
            if not datos:
                break
            mensaje = datos.decode()
            if mensaje.strip().lower() == "exit":
                print(f"[+] {nombre} ({addr[0]}) se ha desconectado.")
                break
            broadcast(f"{nombre} ({addr[0]}) dice: {mensaje}", conn)

    except Exception as e:
        print(f"[!] Error con cliente {addr}: {e}")
    finally:

            if conn in clientes:
                nombre, ip = clientes.pop(conn)
                print(clientes)
                broadcast(f"El usuario {nombre} ({ip}) ha abandonado la conversación", conn)
                print(f"[-] {nombre} ({ip}) se ha desconectado.")
                conn.close()
        


def broadcast(mensaje, origen=None):
    with lock:
        for client in list(clientes):  # usamos list() para evitar error si se elimina cliente en medio
            if client != origen:
                try:
                    client.sendall(mensaje.encode())
                except:
                    pass


def entrada_servidor():
    global servidor_activo
    while True:
        
        comando = input()
        if comando.lower() == "exit":
                if clientes:
                    print("No es posible cerrar el servidor. Hay clientes conectados.")
                else:
                    print("Servidor cerrado.")
                    servidor_activo = False
                    break


def servidor():
    global servidor_activo
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen()
    print(f"[+] Servidor escuchando en {HOST}:{PORT}")

    # Lanzamos hilo para leer entrada del servidor
    threading.Thread(target=entrada_servidor, daemon=True).start()

    while servidor_activo:
        try:
            conn, addr = sock.accept()
            #sock.settimeout(1.0)  # Permite salir del accept() cada 1s para verificar servidor_activo
            if (servidor_activo == True): 
                threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True).start()
        except socket.timeout:
            continue
        except Exception as e:
            print(f"[!] Error en el servidor: {e}")
            break

    sock.close()

if __name__ == "__main__":
    servidor()
