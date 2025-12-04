from conexionBD import *
from tkinter import messagebox

class Proveedores:
    
    @staticmethod
    def buscar(campo="Todo", valor=None):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "No se pudo conectar con la base de datos")
            return []

        # --- ACTUALIZADO: Columnas correctas según tu BD ---
        cols = "id_proveedor, nombre_empresa, nombre_contacto, telefono, direccion"
        sql = f"SELECT {cols} FROM proveedores"
        
        if campo != "Todo":
            match valor:
                case "Empresa A-Z": 
                    sql += " ORDER BY nombre_empresa ASC"
                case "Empresa Z-A":
                    sql += " ORDER BY nombre_empresa DESC"
                case _:
                    filtros = {
                        "ID": "id_proveedor",
                        "Empresa": "nombre_empresa",    
                        "Contacto": "nombre_contacto", 
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
    def insertar(nombre_empresa, nombre_contacto, telefono, direccion):
        cursor, conexion = conectarBD()
        if cursor == None: return False
        try:
            # Insertamos usando nombre_empresa y nombre_contacto
            sql = """INSERT INTO proveedores 
                    (nombre_empresa, nombre_contacto, telefono, direccion) 
                    VALUES (%s, %s, %s, %s)"""
            val = (nombre_empresa, nombre_contacto, telefono, direccion)
            cursor.execute(sql, val)
            conexion.commit()
            desconectarBD(conexion)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")
            return False

    @staticmethod
    def actualizar(id_prov, nombre_empresa, nombre_contacto, telefono, direccion):
        cursor, conexion = conectarBD()
        if cursor == None: return False
        try:
            # Actualizamos usando los nombres nuevos
            sql = """UPDATE proveedores SET 
                    nombre_empresa=%s, nombre_contacto=%s, telefono=%s, direccion=%s 
                    WHERE id_proveedor=%s"""
            val = (nombre_empresa, nombre_contacto, telefono, direccion, id_prov)
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
            # 1. VERIFICACIÓN DE SEGURIDAD:
           
            check_sql = "SELECT COUNT(*) FROM ingredientes WHERE id_proveedor = %s"
            cursor.execute(check_sql, (id_prov,))
            cantidad_productos = cursor.fetchone()[0]

            if cantidad_productos > 0:
                messagebox.showwarning(
                    "No se puede eliminar", 
                    f"Este proveedor tiene {cantidad_productos} ingrediente(s) registrados.\n\n"
                    "Para eliminarlo, primero debes eliminar o reasignar sus productos en el menú de Ingredientes."
                )
                desconectarBD(conexion)
                return False

            sql = "DELETE FROM proveedores WHERE id_proveedor = %s"
            cursor.execute(sql, (id_prov,))
            conexion.commit()
            desconectarBD(conexion)
            return True

        except Exception as e:
            messagebox.showerror("Error", f"No se puede eliminar: {e}")
            if conexion: desconectarBD(conexion)
            return False