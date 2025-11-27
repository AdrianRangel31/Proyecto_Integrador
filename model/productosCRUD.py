from conexionBD import *
from tkinter import messagebox

class Productos:
    
    @staticmethod
    def buscar(campo="Todo", valor=None):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
            return []

        sql = "SELECT * FROM ingredientes"
        
        if campo == "Todo":
            sql = "SELECT * FROM ingredientes"
        else:
            match valor:
                case "Mayor Precio":
                    sql = "SELECT * FROM ingredientes ORDER BY precio DESC"
                case "Menor Precio":
                    sql = "SELECT * FROM ingredientes ORDER BY precio ASC"
                case "Stock Bajo":
                    sql = "SELECT * FROM ingredientes ORDER BY cantidad ASC"
                case "Por Caducar":
                    sql = "SELECT * FROM ingredientes ORDER BY fecha_caducidad ASC"
                case _:
                    filtros = {
                        "ID": "id_producto",
                        "Nombre": "nombre",
                        "Proveedor": "id_proveedor"
                    }
                    if campo in filtros:
                        sql = f"SELECT * FROM ingredientes WHERE {filtros[campo]} LIKE '%{valor}%'"

        try:
            cursor.execute(sql)
            resultado = cursor.fetchall()
            desconectarBD(conexion)
            return resultado
        except Exception as e:
            messagebox.showerror("Error SQL", f"Error al buscar en ingredientes: {e}")
            if conexion: desconectarBD(conexion)
            return []

    @staticmethod
    def insertar(nombre, descripcion, cantidad, unidad, precio, fecha_cad, proveedor):
        cursor, conexion = conectarBD()
        if cursor == None: return False
        try:
            sql = """INSERT INTO ingredientes 
                        (id_producto, nombre, descripcion, cantidad, unidad, precio, fecha_caducidad, id_proveedor) 
                        VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)"""
            val = (nombre, descripcion, cantidad, unidad, precio, fecha_cad, proveedor)
            cursor.execute(sql, val)
            conexion.commit()
            desconectarBD(conexion)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar en ingredientes: {e}")
            if conexion: desconectarBD(conexion)
            return False

    @staticmethod
    def actualizar(id_prod, nombre, descripcion, cantidad, unidad, precio, fecha_cad, proveedor):
        cursor, conexion = conectarBD()
        if cursor == None: return False
        try:
            sql = """UPDATE ingredientes SET 
                        nombre=%s, descripcion=%s, cantidad=%s, unidad=%s, precio=%s, 
                        fecha_caducidad=%s, id_proveedor=%s 
                        WHERE id_producto=%s"""
            val = (nombre, descripcion, cantidad, unidad, precio, fecha_cad, proveedor, id_prod)
            cursor.execute(sql, val)
            conexion.commit()
            desconectarBD(conexion)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")
            if conexion: desconectarBD(conexion)
            return False

    @staticmethod
    def eliminar(id_prod):
        cursor, conexion = conectarBD()
        if cursor == None: return False
        try:
            cursor.execute(f"DELETE FROM ingredientes WHERE id_producto = {id_prod}")
            conexion.commit()
            desconectarBD(conexion)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se puede eliminar: {e}")
            if conexion: desconectarBD(conexion)
            return False

    @staticmethod
    def obtener_lista_proveedores():
        cursor, conexion = conectarBD()
        if cursor == None: 
            return []
        
        try:
            cursor.execute("SELECT id_proveedor, nombre_empresa FROM proveedores")
            datos = cursor.fetchall()
            desconectarBD(conexion)
            return datos
        except Exception as e:
            messagebox.showerror("Error Proveedores", f"No se pudieron cargar los proveedores.\nError técnico: {e}")
            if conexion: desconectarBD(conexion)
            return []