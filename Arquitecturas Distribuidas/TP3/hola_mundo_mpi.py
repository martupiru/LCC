from mpi4py import MPI
import socket

def obtener_ip():
    """
    Obtiene la IP local usada para salir a Internet (no localhost)
    creando un socket hacia un servidor público.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Nos conectamos sin enviar datos, solo para saber qué IP usaría el sistema
        s.connect(("8.8.8.8", 80))  # Servidor DNS de Google
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "IP desconocida"

# Inicializamos el comunicador MPI
comm = MPI.COMM_WORLD
size = comm.Get_size()  # Total de procesos
rank = comm.Get_rank()  # ID del proceso actual
nombre_maquina = MPI.Get_processor_name()  # Nombre del host
ip = obtener_ip()  # Dirección IP del nodo

# Imprimimos la información solicitada
print(f"Hola Mundo! soy el proceso {rank} de {size} corriendo en la máquina {nombre_maquina} IP={ip}")
