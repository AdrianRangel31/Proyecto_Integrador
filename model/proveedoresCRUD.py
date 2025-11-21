from conexionBD import *
from tkinter import messagebox

class Proveedores:
    
    @staticmethod
    def buscar(campo="Todo", valor=None):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "No se pudo conectar con la base de datos")
            return []

        # --- CORRECCIÓN: Columnas exactas según tu diagrama ---
        cols = "id_proveedor, nombre, contacto, telefono, direccion"
        sql = f"SELECT {cols} FROM proveedores"
        
        if campo != "Todo":
            match valor:
                case "Nombre A-Z":
                    sql += " ORDER BY nombre ASC"
                case "Nombre Z-A":
                    sql += " ORDER BY nombre DESC"
                case _:
                    # Filtros actualizados a tus columnas reales
                    filtros = {
                        "ID": "id_proveedor",
                        "Nombre": "nombre",
                        "Contacto": "contacto",
                        "Telefono": "telefono", 
                        "Direccion": "direccion"
                    }
                    if campo in filtros:
                        sql += f" WHERE {filtros[campo]} LIKE '%{valor}%'"

        try:
            cursor.execute(sql)
            resultado = cursor.fetchall()
            desconectarBD(conexion)
            return resultado
        except Exception as e:
            messagebox.showerror("Error SQL", str(e))
            return []

    @staticmethod
    def insertar(nombre, contacto, telefono, direccion):
        cursor, conexion = conectarBD()
        if cursor == None: return False
        try:
            # Insertamos en las 4 columnas de datos (sin correo)
            sql = """INSERT INTO proveedores 
                    (nombre, contacto, telefono, direccion) 
                    VALUES (%s, %s, %s, %s)"""
            val = (nombre, contacto, telefono, direccion)
            cursor.execute(sql, val)
            conexion.commit()
            desconectarBD(conexion)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")
            return False

    @staticmethod
    def actualizar(id_prov, nombre, contacto, telefono, direccion):
        cursor, conexion = conectarBD()
        if cursor == None: return False
        try:
            # Actualizamos las 4 columnas (sin correo)
            sql = """UPDATE proveedores SET 
                    nombre=%s, contacto=%s, telefono=%s, direccion=%s 
                    WHERE id_proveedor=%s"""
            val = (nombre, contacto, telefono, direccion, id_prov)
            cursor.execute(sql, val)
            conexion.commit()
            desconectarBD(conexion)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")
            return False

    @staticmethod
    def eliminar(id_prov):
        cursor, conexion = conectarBD()
        if cursor == None: return False
        try:
            cursor.execute(f"DELETE FROM proveedores WHERE id_proveedor = {id_prov}")
            conexion.commit()
            desconectarBD(conexion)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se puede eliminar: {e}")
            return False