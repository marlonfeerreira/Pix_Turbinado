import socket
import sqlite3

# Configurações do servidor PIX simulado
SERVER_HOST = 'localhost'  
SERVER_PORT = 5000 

# Função para realizar a transação PIX
def realizar_transacao(origem, destino, valor, username, password):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))

    # Envio dos dados da transação e informações de login
    mensagem = f'{origem};{destino};{valor};{username};{password}'
    sock.sendall(mensagem.encode())

    # Recebimento da resposta do servidor PIX simulado
    resposta = sock.recv(1024).decode()
    print('Resposta do servidor PIX simulado:', resposta)

    
    sock.close()

# Dados da transação simulada
origem = 'conta_origem'  
destino = 'conta_destino'  
valor = '100.00'  
username = 'usuario'  
password = 'senha'  

realizar_transacao(origem, destino, valor, username, password)
