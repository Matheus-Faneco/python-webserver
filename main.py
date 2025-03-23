import socket

#Definindo Host e Porta do socket
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

#Criando socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print("na porta %s ..." % SERVER_PORT)

while True:
    #Esperando por conexões do cliente
    client_connection, client_adress = server_socket.accept()

    #Pegar requisição do cliente
    request = client_connection.recv(1024).decode()
    print(request)

    #Parcionar headers HTTP
    headers = request.split('\n')
    filename = headers[0].split()[1]

    #Pegar conteúdo do arquivo
    if filename == '/':
        filename = 'index.html'
    else:
        filename = filename.lstrip('/')

    try:
        fin = open(filename)
        content = fin.read()
        fin.close()

        response = 'HTTP/1.0 200 OK\n\n' + content
    except FileNotFoundError:
        response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'

    #Enviar resposta HTTP
    client_connection.sendall(response.encode())
    client_connection.close()

#Fechar socket
server_socket.close()