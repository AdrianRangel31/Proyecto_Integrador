from conexionBD import *
from tkinter import messagebox
import hashlib

class Usuarios:
    
    @staticmethod
    def iniciar_sesion(email, password):
        cursor, conexion = conectarBD()
        try:
            # Encriptamos la contraseña ingresada para compararla con la BD
            password = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute(
                    "select * from usuarios where correo=%s and password=%s",
                    (email, password)
                    )
            usuario = cursor.fetchone()
            desconectarBD(conexion)
            if usuario:
                return usuario
            else:
                return None      
        except Exception as e:
            print(f"🔴 Error en BD al iniciar sesión: {e}")
            return None

    # --- NUEVOS MÉTODOS CRUD ---

    @staticmethod
    def buscar():
        cursor, conexion = conectarBD()
        if cursor is None: return []
        try:
            # Seleccionamos id, nombre, apellidos, correo, password (hash)
            cursor.execute("SELECT id_usuario, nombre, apellidos, correo, password FROM usuarios")
            datos = cursor.fetchall()
            desconectarBD(conexion)
            return datos
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar usuarios: {e}")
            return []

    @staticmethod
    def insertar(nombre, apellidos, correo, password):
        cursor, conexion = conectarBD()
        if cursor is None: return False
        try:
            # Encriptamos la contraseña antes de guardarla
            pass_encrypt = hashlib.sha256(password.encode()).hexdigest()
            
            sql = "INSERT INTO usuarios (nombre, apellidos, correo, password) VALUES (%s, %s, %s, %s)"
            val = (nombre, apellidos, correo, pass_encrypt)
            
            cursor.execute(sql, val)
            conexion.commit()
            desconectarBD(conexion)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el usuario: {e}")
            return False

    @staticmethod
    def actualizar(id_usuario, nombre, apellidos, correo, password):
        cursor, conexion = conectarBD()
        if cursor is None: return False
        try:
            # Si la contraseña está vacía, actualizamos todo MENOS la contraseña
            if not password:
                sql = "UPDATE usuarios SET nombre=%s, apellidos=%s, correo=%s WHERE id_usuario=%s"
                val = (nombre, apellidos, correo, id_usuario)
            else:
                # Si hay contraseña nueva, la encriptamos y actualizamos todo
                pass_encrypt = hashlib.sha256(password.encode()).hexdigest()
                sql = "UPDATE usuarios SET nombre=%s, apellidos=%s, correo=%s, password=%s WHERE id_usuario=%s"
                val = (nombre, apellidos, correo, pass_encrypt, id_usuario)

            cursor.execute(sql, val)
            conexion.commit()
            desconectarBD(conexion)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")
            return False

    @staticmethod
    def eliminar(id_usuario):
        cursor, conexion = conectarBD()
        if cursor is None: return False
        try:
            cursor.execute(f"DELETE FROM usuarios WHERE id_usuario = {id_usuario}")
            conexion.commit()
            desconectarBD(conexion)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se puede eliminar: {e}")
            return False