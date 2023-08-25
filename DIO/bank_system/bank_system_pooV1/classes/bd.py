import mysql.connector

class DatabaseConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("@@@ Conectado ao banco de dados do AGIOBANK @@@")

        except mysql.connector.Error as err:
            print(f"Algo deu errado => Eis o problema: {err}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("@@@ Desconectando-se da base de dados! @@@")

    def execute_query(self, query, params=None):
        if not self.connection:
            print("@@@ Conexão não estabelecida no momento @@@")
            return

        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            print("@@@ Query realizada com sucesso @@@")

        except mysql.connector.Error as err:
            print(f"Algo deu errado => Eis o problema: {err}")
            self.connection.rollback()

        finally:
            if cursor:
                cursor.close()

db_connector = DatabaseConnector(host="", user="", password="", database="") #host=localhost ou 127.0.0.1, user=root, senha só você sabe e databse=bd
db_connector.connect()

"""
query = "INSERT INTO users (username, email) VALUES (%s, %s)"
params = ("john_doe", "john@example.com")
db_connector.execute_query(query, params)

# Desconectando do banco de dados
db_connector.disconnect()
"""
