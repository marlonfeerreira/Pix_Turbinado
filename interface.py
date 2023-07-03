import tkinter as tk
import socket

# Configurações do servidor PIX simulado
SERVER_HOST = 'localhost'  
SERVER_PORT = 5000  

# Função para realizar a transação PIX
def realizar_transacao():
    # Obter os valores dos campos de entrada
    origem = origem_entry.get()
    destino = destino_entry.get()
    valor = valor_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    # Criação do socket do cliente
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))

    # Envio dos dados da transação e informações de login
    mensagem = f'{origem};{destino};{valor};{username};{password}'
    sock.sendall(mensagem.encode())

    # Recebimento da resposta do servidor PIX simulado
    resposta = sock.recv(1024).decode()
    resultado_label.config(text=resposta)

    sock.close()

# Criação da janela principal
window = tk.Tk()
window.title('Sistema PIX')
window.geometry('400x300')

# Rótulos e campos de entrada
tk.Label(window, text='Conta de Origem:').pack()
origem_entry = tk.Entry(window)
origem_entry.pack()

tk.Label(window, text='Conta de Destino:').pack()
destino_entry = tk.Entry(window)
destino_entry.pack()

tk.Label(window, text='Valor:').pack()
valor_entry = tk.Entry(window)
valor_entry.pack()

tk.Label(window, text='Usuário:').pack()
username_entry = tk.Entry(window)
username_entry.pack()

tk.Label(window, text='Senha:').pack()
password_entry = tk.Entry(window, show='*')
password_entry.pack()

transacao_button = tk.Button(window, text='Realizar Transação', command=realizar_transacao)
transacao_button.pack()

# Rótulo para exibir o resultado da transação
resultado_label = tk.Label(window, text='')
resultado_label.pack()

# Execução da janela principal
window.mainloop()
