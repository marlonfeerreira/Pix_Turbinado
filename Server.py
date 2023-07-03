import socket
import sqlite3
import threading

# Configurações do servidor PIX simulado
SERVER_HOST = 'localhost' 
SERVER_PORT = 5000 

# Função para inicializar o banco de dados
def inicializar_banco_dados():
    conn = sqlite3.connect('pix.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                 (username TEXT, password TEXT)''')

    conn.commit()
    conn.close()

# Função para cadastrar um novo usuário
def cadastrar_usuario(username, password):
    conn = sqlite3.connect('pix.db')
    c = conn.cursor()

    c.execute("SELECT * FROM usuarios WHERE username=?", (username,))
    if c.fetchone():
        return False, "Usuário já cadastrado."

    # Insere o novo usuário na tabela 'usuarios'
    c.execute("INSERT INTO usuarios VALUES (?, ?)", (username, password))

    conn.commit()
    conn.close()

    return True, "Usuário cadastrado com sucesso."

user1 = '14251'
passwordUser1 = '154924'

cadastrar_usuario(user1,passwordUser1)

# Função para autenticar o usuário
def autenticar_usuario(username, password):
    conn = sqlite3.connect('pix.db')
    c = conn.cursor()

    # Verifica se o usuário e senha estão corretos
    c.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (username, password))
    if c.fetchone():
        return True

    return False

# Função para processar a transação do cliente
def processar_transacao(client_socket, origem, destino, valor, username, password):
    # Conexão com o banco de dados
    conn = sqlite3.connect('pix.db')
    c = conn.cursor()

    # Inicia a região crítica (lock)
    lock.acquire()

    try:
        if not autenticar_usuario(username, password):
            resposta = "Usuário não autenticado."
        else:
            c.execute("INSERT INTO transacoes VALUES (?, ?, ?)", (origem, destino, valor))

            conn.commit()

            resposta = f'Transação PIX simulada de {origem} para {destino}, no valor de R${valor}, realizada com sucesso.'

    except Exception as e:
        resposta = f'Falha na transação: {str(e)}'

    finally:
        # Libera a região crítica (unlock)
        lock.release()

    # Envia a resposta simulada ao cliente
    client_socket.sendall(resposta.encode())

    client_socket.close()

# Função para lidar com as conexões dos clientes
def handle_client(client_socket):
    data = client_socket.recv(1024).decode()
    origem, destino, valor, username, password = data.split(';')

    # Processa a transação em uma thread separada
    thread = threading.Thread(target=processar_transacao, args=(client_socket, origem, destino, valor, username, password))
    thread.start()

inicializar_banco_dados()

# Criação do socket do servidor
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((SERVER_HOST, SERVER_PORT))
sock.listen(1)

# Inicializa o lock
lock = threading.Lock()

print('Servidor PIX Simulado iniciado.')

while True:
    client_socket, addr = sock.accept()
    print('Cliente conectado:', addr)

    # Lida com a conexão do cliente em uma thread separada
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()

