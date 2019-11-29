
import socket
import threading
import struct

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 5003

def threadPool (conexao, cliente):

  solicitacao = conexao.recv(1024)
  funcao = solicitacao.split(":")[0]
  valores = solicitacao.split(":")[1]

  # Carrega a biblioteca dinamicamente
  dynamic_module = __import__("myFunctions")

  # Carrega a classe dinamicamente
  dynamic_class = getattr(dynamic_module, funcao)

  # Carrega a funcao solicitada pelo cliente dinamicamente
  dynamic_function = getattr(dynamic_class(), "compute")

  # Executa a funcao
  resultado = dynamic_function(valores)

  # Envia o resultado para o middleware
  try:
  	conexao.send(str(resultado))
  except:
        pass
  # Encerra a conexao com o middleware
  conexao.close()

if __name__ == "__main__":


  s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s_socket.bind((SERVER_ADDRESS, SERVER_PORT))
  s_socket.listen(5)

  while True:
    threading.Thread(target=threadPool, args=(s_socket.accept())).start() 


