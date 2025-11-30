from conexionBD import *
from tkinter import messagebox
import hashlib

class Usuarios:
    
    @staticmethod
    def iniciar_sesion(email, password):
        cursor, conexion = conectarBD()
        try:
            password = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute(
                "SELECT * FROM usuarios WHERE correo=%s AND password=%s",
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

    @staticmethod
    def buscar():
        cursor, conexion = conectarBD()
        if cursor is None: return []
        try:
            # Seleccionamos AMBOS apellidos
            sql = "SELECT * FROM usuarios"
            cursor.execute(sql)
            datos = cursor.fetchall()
            desconectarBD(conexion)
            return datos
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar usuarios: {e}")
            return []

    @staticmethod
    def insertar(nombre, ap_paterno, ap_materno, correo, password, rol):
        cursor, conexion = conectarBD()
        if cursor is None: return False
        try:
            pass_encrypt = hashlib.sha256(password.encode()).hexdigest()
            
            # Insertamos ambos apellidos
            if not ap_materno:
                ap_materno = ""
                sql = "INSERT INTO usuarios (nombre, apellido_paterno, apellido_materno, correo, password, Rol) VALUES (%s, %s, '', %s, %s, %s)"
                val = (nombre, ap_paterno, correo, pass_encrypt, rol)
            else:
                sql = "INSERT INTO usuarios (nombre, apellido_paterno, apellido_materno, correo, password, Rol) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (nombre, ap_paterno, ap_materno, correo, pass_encrypt, rol)
            
            cursor.execute(sql, val)
            conexion.commit()
            desconectarBD(conexion)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el usuario: {e}")
            return False

    @staticmethod
    def actualizar(id_usuario, nombre, ap_paterno, ap_materno, correo, password, rol):
        cursor, conexion = conectarBD()
        if cursor is None: return False
        try:
            if not password:
                # Actualizar SIN contraseña
                sql = "UPDATE usuarios SET nombre=%s, apellido_paterno=%s, apellido_materno=%s, correo=%s, Rol=%s WHERE id_usuario=%s"
                val = (nombre, ap_paterno, ap_materno, correo, rol, id_usuario)
            else:
                # Actualizar CON contraseña
                pass_encrypt = hashlib.sha256(password.encode()).hexdigest()
                sql = "UPDATE usuarios SET nombre=%s, apellido_paterno=%s, apellido_materno=%s, correo=%s, password=%s, Rol=%s WHERE id_usuario=%s"
                val = (nombre, ap_paterno, ap_materno, correo, pass_encrypt, rol, id_usuario)

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
            sql = "DELETE FROM usuarios WHERE id_usuario = %s"
            cursor.execute(sql, (id_usuario,))
            conexion.commit()
            desconectarBD(conexion)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se puede eliminar: {e}")
            return False