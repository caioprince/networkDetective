import socket
import sys
import concurrent.futures

def check_port(ip, port):
    socketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketObj.settimeout(1)  # Tempo limite de 1 segundo para a conexão

    try:
        res = socketObj.connect_ex((ip, port))
        if res == 0:
            print(f"Porta {port} Aberta")
    except Exception as e:
        print(f"Erro na porta {port}: {e}")
    finally:
        socketObj.close()

def main():
    # Verificar se há argumentos suficientes
    if len(sys.argv) < 2:
        print("Uso: python main.py <IP> OU <URL>")
        sys.exit(1)

    ipURl = sys.argv[1]

    # Usar ThreadPoolExecutor para verificar as portas com no máximo 4 threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(check_port, [ipURl] * 65535, range(1, 65536))

if __name__ == '__main__':
    main()
