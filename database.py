import mysql.connector
from mysql.connector import Error

def conectar():
    """Cria e retorna uma conexão com o banco de dados MySQL."""
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="educaprova"
        )
        if conexao.is_connected():
            print("✅ Conectado ao banco de dados MySQL.")
        return conexao
    except Error as e:
        print("❌ Erro ao conectar ao MySQL:", e)
        return None
