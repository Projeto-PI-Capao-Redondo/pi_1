"""
Connector mysql-connector-python

passo a passo:

1 - pip install mysql-connector-python
"""
import os
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

load_dotenv()

usuario = os.getenv('USUARIO')
senha = os.getenv('SENHA')
host = os.getenv('HOST')
porta = os.getenv('PORTA')
banco = os.getenv('NOME_BANCO')

def conecta_mysql():
    try:
        conectando = mysql.connector.connect(host=host, user=usuario, password=senha, database=banco, port=porta, connect_timeout=500)
        print('Conectado ao MySQL')
        return conectando
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Algo está errado com seu usuário ou senha')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Banco de dados não existe')
        else:
            print(err)