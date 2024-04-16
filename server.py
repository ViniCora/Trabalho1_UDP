import socket
import hashlib
import os
import time
import math

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789

def calculate_checksum(data):
    checksum = hashlib.md5()
    checksum.update(data)
    return checksum.hexdigest()

def envia_arquivo(filename, addr):
    file_size = os.path.getsize(filename)
    packages = math.ceil(file_size/16384)
    i = 0
    try:
        with open(filename, 'rb') as file:
            while True:
                data = file.read(16384)  # Lê 1 KB de dados
                if not data:
                    break  # Se não houver mais dados para enviar, sai do loop
                #print(f'Lidos {i*2048} de {file_size}')
                #print(data)
                checksum = calculate_checksum(data)
                packet = {'id': i, 'checksum': checksum, 'data': data, 'totalPacotes': packages}
                i += 1
                serverSock.sendto(str(packet).encode(), addr)
                time.sleep(0.05)
    except FileNotFoundError:
        error_message = "Arquivo não encontrado"
        print(error_message)


def envia_arquivo_erro(filename, addr, id):
    file_size = os.path.getsize(filename)
    seek = id * 16384
    try:
        with open(filename, 'rb') as file:
            file.seek(seek)
            data = file.read(16384)  # Lê 1 KB de dados
            #print(f'Lidos {i*2048} de {file_size}')
            #print(data)
            checksum = calculate_checksum(data)
            packet = {'checksum': checksum, 'data': data}
            serverSock.sendto(str(packet).encode(), addr)
    except FileNotFoundError:
        error_message = "Arquivo não encontrado"
        print(error_message)

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
## One difference is that we will have to bind our declared IP address
## and port number to our newly declared serverSock
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

while True:
    data, addr = serverSock.recvfrom(2048)
    message = eval(data.decode())
    PROTOCOL = message['type']
    SERVICE = message['caminho_protocolo']
    CAMINHO = message['caminho_aqruivo']

    if PROTOCOL == "GET":
        if SERVICE == "arquivo":
            envia_arquivo(CAMINHO, addr)
        if SERVICE == "arquivoErro":
            id = message['id']
            envia_arquivo_erro(CAMINHO, addr, id)


  #  print(f"protocol: {PROTOCOL} Service:{SERVICE} caminho: {CAMINHO} from {addr}")