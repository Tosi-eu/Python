from socket import *

serverPort = 11991
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('0.0.0.0', serverPort))

print("The server is ready to receive")

while True:
    a_from_client, clientAddress = serverSocket.recvfrom(2048)
    b_from_client, _ = serverSocket.recvfrom(2048)

    a = int(a_from_client.decode('utf-8'))
    b = int(b_from_client.decode('utf-8'))

    sum_values = a + b

    print(f"Received A: {a}, B: {b}, Sum: {sum_values} FROM {clientAddress}")

    serverSocket.sendto(str(sum_values).encode('utf-8'), clientAddress)
