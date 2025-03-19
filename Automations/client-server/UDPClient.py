from socket import *

serverName = "localhost"
serverPort = 11991

clientSocket = socket(AF_INET, SOCK_DGRAM)

a_for_client = input("Variable A: ")
b_for_client = input("Variable B: ")

clientSocket.sendto(a_for_client.encode('utf-8'), (serverName, serverPort))
clientSocket.sendto(b_for_client.encode('utf-8'), (serverName, serverPort))

modifiedMessage, _ = clientSocket.recvfrom(2048)

print("From UDP Server:", modifiedMessage.decode('utf-8'))

clientSocket.close()
