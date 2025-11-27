from conexionBD import *
from tkinter import messagebox
import hashlib

class Usuarios:
    
    @staticmethod
    def iniciar_sesion(email, password):
        cursor, conexion = conectarBD()
        try:
            # Encriptamos la contraseña para comparar
            password = hashlib.sha256(password.encode()).hexdigest()
            # Usamos backticks en apellido paterno por tener espacio en el nombre de la columna
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
            # CORRECCIÓN: La BD tiene `apellido paterno` y `apellido_materno`.
            # La interfaz solo pide "Apellidos", así que unimos ambos o traemos el paterno.
            # Nota el uso de ` ` (backticks) para 'apellido paterno' porque tiene un espacio.
            sql = "SELECT id_usuario, nombre, `apellido paterno`, correo, password FROM usuarios"
            cursor.execute(sql)
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
            pass_encrypt = hashlib.sha256(password.encode()).hexdigest()
            
            # CORRECCIÓN: Insertamos el valor del formulario en `apellido paterno`.
            # Enviamos una cadena vacía "" a `apellido_materno` para cumplir con el NOT NULL de la BD.
            sql = "INSERT INTO usuarios (nombre, `apellido paterno`, apellido_materno, correo, password, Rol) VALUES (%s, %s, '', %s, %s, '')"
            
            # Nota: También agregué 'Rol' como vacío para evitar error si no tiene default.
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
            if not password:
                # Actualizar sin tocar la contraseña
                sql = "UPDATE usuarios SET nombre=%s, `apellido paterno`=%s, correo=%s WHERE id_usuario=%s"
                val = (nombre, apellidos, correo, id_usuario)
            else:
                # Actualizar con nueva contraseña
                pass_encrypt = hashlib.sha256(password.encode()).hexdigest()
                sql = "UPDATE usuarios SET nombre=%s, `apellido paterno`=%s, correo=%s, password=%s WHERE id_usuario=%s"
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
            # Usamos parámetros para evitar inyección SQL básica y errores de formato
            sql = "DELETE FROM usuarios WHERE id_usuario = %s"
            cursor.execute(sql, (id_usuario,))
            conexion.commit()
            desconectarBD(conexion)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se puede eliminar: {e}")
            return False