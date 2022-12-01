# echo-client.py
import socket
import os

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


# Listar arquivos de um diretório
def list_files(path):
  try:
    s.send(("list " + path).encode('utf-8'))
  except:
    print("Não foi possível realizar a requisição.")
    return
  try:
    n_arquivos = int(s.recv(1024).decode('utf-8'))

    for arquivos in range(n_arquivos):
      file_name = s.recv(1024).decode('utf-8')
      file_size = int(s.recv(1024).decode('utf-8'))

      print("\t{} - {}b".format(file_name, file_size))
      s.send(bytes("1", "utf-8"))
  except:
    print("Não foi possível listar os arquivos")
    return


# Cria uma pasta
def mkdir(nome):
  try:
    s.send(("mkdir " + nome).encode('utf-8'))
  except:
    print("Não foi possível realizar a requisição.")
    return

  data = s.recv(1024)

  if data.decode('utf-8') == "1":
    print("Diretório criado com sucesso.")
  else:
    print("Não foi possível criar o diretório")
  return


# Remover diretório
def rmdir(nome):
  try:
    s.send(("rmdir " + nome).encode('utf-8'))
  except:
    print("Não foi possível realizar a requisição.")
    return

  data = s.recv(1024)

  if data.decode('utf-8') == "1":
    print("Diretório removido com sucesso.")
  else:
    print("Não foi possível remover o diretório")
  return


# Enviar arquivo
def upld(file_name):
  # Upload a file
  print("\nUploading file: {}...".format(file_name))
  try:
    # Check the file exists
    content = open(file_name, "rb")
  except:
    print("Couldn't open file. Make sure the file name was entered correctly.")
    return
  try:
    # Make upload request
    s.send(("upld " + file_name).encode('utf-8'))
  except:
    print(
      "Couldn't make server request. Make sure a connection has bene established."
    )
    return
  try:
    # Send file name size
    s.send((str((os.stat(file_name)).st_size)).encode('utf-8'))
  except:
    print("Error sending name size")
  try:
    # Send the file in chunks defined by BUFFER_SIZE
    # Doing it this way allows for unlimited potential file sizes to be sent
    l = content.read(1024)
    print("\nSending...")
    while l:
      s.send(l)
      l = content.read(1024)
    content.close()
  except:
    print("Error sending file")
    return
  return


def rmfil(file_path):
  print("Removendo arquivo: {}...".format(file_path))
  # s.send(("rmfil " + file_path).encode('utf_8'))
  # s.send(bytes("1", "utf-8"))
  # full_path = os.getcwd() + file_path

  # # Confere se o arquivo existe
  # if os.path.isfile(full_path):
  #   s.send(bytes("1", 'utf-8'))
  # else:
  #   s.send(bytes("-1", 'utf-8'))

  # # Confirma se deve deletar o arquivo
  # confirmar = conn.recv(1024)
  # if confirmar == "S":
  #   try:
  #     # Remove o arquivo
  #     os.remove(full_path)
  #     s.send(bytes("1", 'utf-8'))
  #   except:
  #     print("Erro ao tentar deletar {}".format(file_path))
  #     s.send(bytes("-1", 'utf-8'))
  # else:
  #   print("Operação cancelada.")
  return


def quit():
  s.send("QUIT")
  s.recv(1024)
  s.close()
  print("Conexão encerrada")
  return


print("\n\nUtilize uma das seguintes funções:\n")
print("LIST caminho_diretorio : lista os arquivos de um diretório\n")
print("UPLD caminho_arquivo caminho_diretorio : Realiza o upload do arquivo\n")
print("DWLD caminho_arquivo : Baixa o arquivo\n")
print("RMDIR caminho_diretorio : Remove uma pasta\n")
print("RMFIL caminho_arquivo : Remove um arquivo\n")
print("QUIT : Exit")


def main():
  while True:
    # Listen for a command
    comando = input("\nDigite o comando: ")
    if comando[:4].upper() == "LIST":  # FAZENDO
      path = comando[5:]
      list_files(path)
    elif comando[:4].upper() == "UPLD":  # FAZENDO
      file_path = comando[5:]
      upld(file_path)
    elif comando[:4].upper() == "DWLD":  # A FAZER
      file_path = comando[5:]
      mkdir(file_path)
    elif comando[:5].upper() == "MKDIR":
      dir_name = comando[6:]
      mkdir(dir_name)
    elif comando[:5].upper() == "RMDIR":
      dir_name = comando[6:]
      rmdir(dir_name)
    elif comando[:5].upper() == "RMFIL":  # A FAZER
      file_path = comando[6:]
      rmfil(file_path)
    elif comando[:4].upper() == "QUIT":
      quit()
      break
    else:
      print("Comando não reconhecido; tente novamente")


if __name__ == "__main__":
  main()
