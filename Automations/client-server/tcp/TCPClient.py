import socket
import jwt
import os
import time
import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from dotenv import load_dotenv 
import psycopg2
from psycopg2 import sql    

load_dotenv()

SERVER_HOST = 'localhost'
SERVER_PORT = int(os.getenv('SERVER_PORT'))
SECRET_KEY = os.getenv('SECRET_KEY')

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def log_client_event(event_type, username=None, token=None, aes_key=None, message=None, encrypted_message=None):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        query = sql.SQL("""
            INSERT INTO client_audit (event_type, username, token, aes_key, message, encrypted_message)
            VALUES (%s, %s, %s, %s, %s, %s)
        """)
        cursor.execute(query, (event_type, username, token, aes_key, message, encrypted_message))
        conn.commit()
        cursor.close()
        conn.close()

def generate_token(username):
    payload = {'user': username, 'exp': time.time() + 3600}
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def encrypt_message(message, aes_key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    padded_message = padder.update(message.encode('utf-8')) + padder.finalize()

    encrypted = encryptor.update(padded_message) + encryptor.finalize()
    return iv + encrypted

def decrypt_message(ciphertext, iv, aes_key):
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted_message = unpadder.update(decrypted_padded) + unpadder.finalize()

    return decrypted_message.decode('utf-8')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

client_socket.send(b'REQUEST_PUBLIC_KEY')
public_key_data = client_socket.recv(1024)
server_public_key = rsa.PublicKey.load_pkcs1(public_key_data)

aes_key = os.urandom(32)
encrypted_aes_key = rsa.encrypt(aes_key, server_public_key)
client_socket.send(encrypted_aes_key)

log_client_event(event_type='AES_KEY_SENT', aes_key=aes_key)

username = input("Enter your username: ")
token = generate_token(username)
client_socket.send(token.encode('utf-8'))

auth_response = client_socket.recv(1024).decode('utf-8')
if "Error" in auth_response:
    print(auth_response)
    client_socket.close()
    exit()

print("Authenticated successfully!")

while True:
    message = input("You: ")
    if message.lower() == 'exit':
        break
    encrypted_message = encrypt_message(message, aes_key)
    client_socket.send(encrypted_message)

    log_client_event(event_type='MESSAGE_SENT', username=username, message=message, encrypted_message=encrypted_message)

    response = client_socket.recv(1024)
    iv, encrypted_response = response[:16], response[16:]
    decrypted_response = decrypt_message(encrypted_response, iv, aes_key)
    print("Server:", decrypted_response)
    log_client_event(event_type='SERVER_RESPONSE', username=username, message=decrypted_response, encrypted_message=encrypted_response)

client_socket.close()
