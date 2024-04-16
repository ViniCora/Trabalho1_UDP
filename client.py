import socket
import hashlib

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 6789
REQUEST_TYPE = "GET"
CAMINHO_PROTOCOLO = "arquivo"
CAMINHO_PROTOCOLO_ERRO = "arquivoErro"
CAMINHO_ARQUIVO = "D:/Faculdade/Redes/Bruno Carvalho Ferreira - Ficha.pdf"
CAMINHO_ARQUIVO_RECEBER = "D:/Faculdade/Redes/Teste_Recebido/Bruno Carvalho Ferreira - Ficha.pdf"
PARAR_PERGUNTA = False

def calculate_checksum(data):
    checksum = hashlib.md5()
    checksum.update(data)
    return checksum.hexdigest()

filename = CAMINHO_ARQUIVO
    #input("Digite o nome do arquivo que deseja receber: ")

request = {'type': REQUEST_TYPE, 'caminho_protocolo': CAMINHO_PROTOCOLO, 'caminho_aqruivo': CAMINHO_ARQUIVO}
    #f"{REQUEST_TYPE}{CAMINHO_PROTOCOLO}@{filename}"

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.sendto(str(request).encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))
i = 0
vetor = None
while True:
    packet, _ = clientSock.recvfrom(65536)  # 1024 bytes de dados + 16 bytes do checksum
    packet = eval(packet.decode())
    if i == 0:
        vetor = [None] * packet['totalPacotes']
    checksum = calculate_checksum(packet['data'])
    #print(packet['data'])
    packet_Check = packet['checksum']
    #print(f'{checksum} : {packet_Check}')

    if checksum == packet['checksum']:
        if PARAR_PERGUNTA == False:
            continuar = input("Digite 'N' para simular uma perda de pacote e 'S' para parar de perguntar: ")
            if continuar == 'N':
                continue
            else:
                if continuar == 'S':
                    PARAR_PERGUNTA = True

        id = packet['id']
        print(f"Id atual {id}")
        #if i == packet['id']:
        #    print(f"Id atual{i} do pacote {id}")
        #else:
        vetor[id] = packet['data']
        #with open(CAMINHO_ARQUIVO_RECEBER, 'ab') as file:
        #   file.write(packet['data'])
        i += 1
    else:
        print("Checksum inválido. Dados corrompidos.")
    if len(packet['data']) < 16384:
        break  # Se o último pacote tiver menos de 1 KB, todos os dados foram recebidos
print("Arquivo recebido com sucesso.")
i = 0
for elemento in vetor:
    # Faz algo com o elemento
    if elemento == None:
        packet = {'id': i, 'type': REQUEST_TYPE, 'caminho_protocolo': CAMINHO_PROTOCOLO_ERRO, 'caminho_aqruivo': CAMINHO_ARQUIVO }
        clientSock.sendto(str(packet).encode(), (UDP_IP_ADDRESS, UDP_PORT_NO))
        packet, _ = clientSock.recvfrom(65536)
        packet = eval(packet.decode())
        vetor[i] = packet['data']
    i += 1

for elemento in vetor:
    with open(CAMINHO_ARQUIVO_RECEBER, 'ab') as file:
        file.write(elemento)

# Fecha o socket
clientSock.close()
