# echo-server.py

import socket
import os

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()


#Função de criar diretório
def mkdir(dirName):
  currentDir = os.getcwd()
  if not os.path.exists(currentDir + '/' + dirName):
    os.makedirs(currentDir + '/' + dirName)
    conn.send(bytes("1", 'utf-8'))
  else:
    conn.send(bytes("-1", 'utf-8'))


#Função de remover diretório
def rmdir(dirName):
  currentDir = os.getcwd()
  if os.path.exists(currentDir + '/' + dirName):
    os.removedirs(currentDir + '/' + dirName)
    conn.send(bytes("1", 'utf-8'))
  else:
    conn.send(bytes("-1", 'utf-8'))


#Função de listagem de arquivos
def list_files(path):
  full_path = os.getcwd() + path;
  arquivos = os.listdir()
  conn.send(bytes(str(len(arquivos)), 'utf-8'))

  for arquivo in arquivos:
    # Nome do arquivo
    conn.send(bytes(arquivo, 'utf-8'))
    # Tamanho do arquivo
    conn.send(
      bytes(str(os.path.getsize(os.getcwd() + path + "/" + arquivo)), 'utf-8'))
    conn.recv(1024)
  print("Listagem feita com sucesso")
  return


#Função de downloas de arquivo
def dwld(path):
  print('')


#Função de enviar arquivo
def upld(file_name):
  output_file = open(file_name, "wb")
  # This keeps track of how many bytes we have recieved,      so we know when to stop the loop
  file_size = conn.recv(1024)
  bytes_recieved = 0
  print("\nRecieving...")
  while bytes_recieved < file_size:
    l = conn.recv(1024)
    output_file.write(l)
    bytes_recieved += 1024
  output_file.close()


# Funçao para excluir um arquivo
def rmfil(file_path):
  conn.send(bytes("1", "utf-8"))
  full_path = os.getcwd() + file_path

  # Confere se o arquivo existe
  if os.path.isfile(full_path):
    conn.send(bytes("1", 'utf-8'))
  else:
    conn.send(bytes("-1", 'utf-8'))

  # Confirma se deve deletar o arquivo
  confirmar = conn.recv(1024)
  if confirmar == "S":
    try:
      # Remove o arquivo
      os.remove(full_path)
      conn.send(bytes("1", 'utf-8'))
    except:
      print("Erro ao tentar deletar {}".format(file_path))
      conn.send(bytes("-1", 'utf-8'))
  else:
    print("Operação cancelada.")
    return


# Função para fechar conexão
def quit():
  # Enviar confirmação
  conn.send("1")
  # Fecha a conexão e reinicia o servidor
  conn.close()
  s.close()
  os.execl(sys.executable, sys.executable, *sys.argv)


def main():
  while True:
    data = conn.recv(1024)

    if data[:4].decode('utf-8').upper() == "LIST":  # FAZENDO
      path = data[5:].decode('utf-8')
      list_files(path)
    elif data[:4].decode('utf-8').upper() == "UPLD":
      file_name = data[5:].decode('utf-8')
      upld(file_name)
    elif data[:4].decode('utf-8').upper() == "DWLD":  # A FAZER
      nome_pasta = data[5:].decode('utf-8')
      mkdir(nome_pasta)
    elif data[:5].decode('utf-8').upper() == "MKDIR":
      dirName = data[6:].decode('utf-8')
      mkdir(dirName)
    elif data[:5].decode('utf-8').upper() == "RMDIR":
      dirName = data[6:].decode('utf-8')
      rmdir(dirName)
    elif data[:5].decode('utf-8').upper() == "RMFIL":  # A FAZER
      caminho = data[6:]
      rmfil(caminho)
    elif data[:4].decode('utf-8').upper() == "QUIT":
      quit()
      break


if __name__ == "__main__":
  main()
