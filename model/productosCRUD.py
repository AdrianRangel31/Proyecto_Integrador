from conexionBD import *
from tkinter import messagebox

class Productos:
    @staticmethod
    def buscar(campo="Todo", valor=None):
        """
        Busca items en la tabla INGREDIENTES.
        Maneja lógica diferenciada para Reportes y Búsqueda General.
        """
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Notice", "Error connecting to database")
            return []

        # SQL por defecto (Trae todo)
        sql = "SELECT * FROM ingredientes"

        # --- CASO 1: REPORTES ESPECÍFICOS (Llamados desde el botón Reportes) ---
        if campo == "Stock Bajo":
            sql = "SELECT * FROM ingredientes WHERE cantidad < 10 ORDER BY cantidad ASC"
        
        elif campo == "Por Caducar":
            sql = """SELECT * FROM ingredientes 
                    WHERE fecha_caducidad BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY) 
                    ORDER BY fecha_caducidad ASC"""

        # --- CASO 2: BÚSQUEDA GENERAL (Desde la tabla principal) ---
        elif campo == "Todo":
            sql = "SELECT * FROM ingredientes"
            if valor == "Mayor Precio":
                sql += " ORDER BY precio DESC"
            elif valor == "Menor Precio":
                sql += " ORDER BY precio ASC"
            elif valor == "Stock Bajo": 
                sql += " ORDER BY cantidad ASC"
            elif valor == "Por Caducar":
                sql += " ORDER BY fecha_caducidad ASC"
        
        # --- CASO 3: BÚSQUEDA POR COLUMNA ESPECÍFICA ---
        else:
            filtros = {
                "ID": "id_producto",
                "Nombre": "nombre",
                "Proveedor": "id_proveedor"
            }
            if campo in filtros and valor:
                sql = f"SELECT * FROM ingredientes WHERE {filtros[campo]} LIKE '%{valor}%'"

        try:
            cursor.execute(sql)
            resultado = cursor.fetchall()
            desconectarBD(conexion)
            return resultado
        except Exception as e:
            messagebox.showerror("SQL Error", f"Error searching ingredients: {e}")
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
            messagebox.showerror("Error", f"Could not save ingredient: {e}")
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
            messagebox.showerror("Error", f"Could not update: {e}")
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
            messagebox.showerror("Error", f"Could not delete: {e}")
            if conexion: desconectarBD(conexion)
            return False

    @staticmethod
    def obtener_lista_proveedores():
        cursor, conexion = conectarBD()
        if cursor == None: return []
        try:
            cursor.execute("SELECT id_proveedor, nombre_empresa FROM proveedores")
            datos = cursor.fetchall()
            desconectarBD(conexion)
            return datos
        except Exception as e:
            messagebox.showerror("Error Proveedores", f"No se pudieron cargar los proveedores.\nError: {e}")
            if conexion: desconectarBD(conexion)
            return []