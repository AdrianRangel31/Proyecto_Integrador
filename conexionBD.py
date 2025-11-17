import mysql.connector
from mysql.connector import Error

def conectarBD():
    try:
        conexion1=mysql.connector.connect(host="localhost",
                             user="root", 
                             passwd="",
                             database="bd_hamburguesas")
        cursor1=conexion1.cursor()
        return cursor1, conexion1
    except Error as e:
        return None,e

def desconectarBD(conexion):
    conexion.close() 
