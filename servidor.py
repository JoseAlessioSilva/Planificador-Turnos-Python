import socket
import datetime

# Configuración del servidor
def iniciar_servidor():
    """
    Esta función inicia un servidor UDP que escucha mensajes de logs
    desde clientes y los guarda en un archivo de texto con una estampa de tiempo.
    """
    HOST = "localhost"
    PORT = 9999

    # Crear el socket (UDP)
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((HOST, PORT))

    print(f"Servidor de Logs escuchando en {HOST}:{PORT}...")

    # Bucle infinito para escuchar siempre
    while True:
        try:
            # 1. Recibimos el paquete
            data, addr = servidor.recvfrom(1024) # Buffer de 1024 bytes
            
            # 2. Decodificamos el mensaje
            mensaje = data.decode("utf-8")
            
            # 3. Agregamos estampa de tiempo
            hora = datetime.datetime.now()
            texto_log = f"{hora} - Cliente {addr}: {mensaje}\n"
            
            # 4. Guardamos en el archivo del servidor
            print(texto_log.strip()) # Mostrar en consola del servidor
            with open("registro_servidor.txt", "a") as f:
                f.write(texto_log)
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    iniciar_servidor()