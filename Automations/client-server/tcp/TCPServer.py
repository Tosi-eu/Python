import socket
import jwt
import os
import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

load_dotenv()

SERVER_HOST = '0.0.0.0'
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

def log_audit_event(event_type, username, token, public_key, private_key):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        query = sql.SQL("""
            INSERT INTO audit (event_type, username, token, rsa_public_key, rsa_private_key)
            VALUES (%s, %s, %s, %s, %s)
        """)
        cursor.execute(query, (event_type, username, token, public_key, private_key))
        conn.commit()
        cursor.close()
        conn.close()

def log_user_message(username, message, encrypted_message):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        query = sql.SQL("""
            INSERT INTO user_messages (username, message, encrypted_message)
            VALUES (%s, %s, %s)
        """)
        cursor.execute(query, (username, message, encrypted_message))
        conn.commit()
        cursor.close()
        conn.close()

def generate_rsa_keys():
    return rsa.newkeys(2048)

def decrypt_message(ciphertext, iv, aes_key):
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted_message = unpadder.update(decrypted_padded) + unpadder.finalize()

    return decrypted_message.decode('utf-8')

def encrypt_message(message, aes_key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    padded_message = padder.update(message.encode('utf-8')) + padder.finalize()

    encrypted = encryptor.update(padded_message) + encryptor.finalize()
    return iv + encrypted

def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded['user']
    except jwt.ExpiredSignatureError:
        return "Error: Token expired"
    except jwt.InvalidTokenError:
        return "Error: Invalid token"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print("Server is listening...")

public_key, private_key = generate_rsa_keys()

aes_keys = {}

while True:
    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    request = conn.recv(1024)
    if request == b'REQUEST_PUBLIC_KEY':
        conn.send(public_key.save_pkcs1())
        encrypted_aes_key = conn.recv(1024)
        aes_key = rsa.decrypt(encrypted_aes_key, private_key)
        aes_keys[addr] = aes_key
        print(f"AES Key received from {addr}")

    token = conn.recv(1024).decode('utf-8')
    username = verify_token(token)
    if "Error" in username:
        conn.send(username.encode('utf-8'))
        conn.close()
        continue

    log_audit_event(
        event_type='AUTHENTICATION',
        username=username,
        token=token,
        public_key=public_key.save_pkcs1().decode('utf-8'),
        private_key=private_key.save_pkcs1().decode('utf-8')
    )

    conn.send("Authenticated successfully!".encode('utf-8'))
    print(f"{username} authenticated from {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        iv, encrypted_data = data[:16], data[16:]
        decrypted_message = decrypt_message(encrypted_data, iv, aes_keys[addr])
        print(f"Received from {username}: {decrypted_message}")
        log_user_message(username, decrypted_message, encrypted_data)
        response_message = f"Echo: {decrypted_message}"
        encrypted_response = encrypt_message(response_message, aes_keys[addr])
        conn.send(encrypted_response)

    conn.close()
    print(f"Connection with {addr} closed.")