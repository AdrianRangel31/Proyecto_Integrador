from conexionBD import *
from tkinter import messagebox
import hashlib

class Usuarios():
    @staticmethod
    def iniciar_sesion(email,password):
        cursor, conexion = conectarBD()
        try:
            password=hashlib.sha256(password.encode()).hexdigest()
            cursor.execute(
                    "select * from usuarios where correo=%s and password=%s",
                    (email,password)
                    )
            usuario=cursor.fetchone()
            if usuario:
                return usuario
            else:
                return None      
        except Exception as e:
            print(f"🔴 Error en BD al iniciar sesión: {e}")
            return None