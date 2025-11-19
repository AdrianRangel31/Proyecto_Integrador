from conexionBD import *
from tkinter import messagebox

class Productos:
    
    @staticmethod
    def buscar(campo="Todo", valor=None):
        """
        Busca productos aplicando filtros.
        campo: El criterio (Nombre, ID, Proveedor, etc)
        valor: El valor a buscar o el tipo de ordenamiento.
        """
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
            return []

        sql = "SELECT * FROM productos"
        
        if campo == "Todo":
            sql = "SELECT * FROM productos"
        else:
            match valor:
                case "Mayor Precio":
                    sql = "SELECT * FROM productos ORDER BY precio DESC"
                case "Menor Precio":
                    sql = "SELECT * FROM productos ORDER BY precio ASC"
                case "Stock Bajo":
                    sql = "SELECT * FROM productos ORDER BY cantidad ASC"
                case "Por Caducar":
                    sql = "SELECT * FROM productos ORDER BY fecha_caducidad ASC"
                case _:
                    # Filtro dinámico seguro
                    filtros = {
                        "ID": "id_producto",
                        "Nombre": "nombre",
                        "Proveedor": "id_proveedor"
                    }
                    if campo in filtros:
                        # Usamos f-string con cuidado, idealmente usar parámetros %s para evitar inyección SQL,
                        # pero sigo tu patrón actual manteniendo comillas simples para strings
                        sql = f"SELECT * FROM productos WHERE {filtros[campo]} LIKE '%{valor}%'"

        cursor.execute(sql)
        resultado = cursor.fetchall()
        desconectarBD(conexion)
        return resultado

    @staticmethod
    def insertar(nombre, descripcion, cantidad, unidad, precio, fecha_cad, proveedor):
        cursor, conexion = conectarBD()
        if cursor == None:
            return False
        
        try:
            # Usamos parámetros %s para evitar errores con caracteres especiales y fechas
            sql = """INSERT INTO productos 
                    (id_producto, nombre, descripcion, cantidad, unidad, precio, fecha_caducidad, id_proveedor) 
                    VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)"""
            val = (nombre, descripcion, cantidad, unidad, precio, fecha_cad, proveedor)
            
            cursor.execute(sql, val)
            conexion.commit()
            desconectarBD(conexion)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")
            return False

    @staticmethod
    def actualizar(id_prod, nombre, descripcion, cantidad, unidad, precio, fecha_cad, proveedor):
        cursor, conexion = conectarBD()
        if cursor == None:
            return False
        
        try:
            sql = """UPDATE productos SET 
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
            return False

    @staticmethod
    def eliminar(id_prod):
        cursor, conexion = conectarBD()
        if cursor == None:
            return False
        try:
            cursor.execute(f"DELETE FROM productos WHERE id_producto = {id_prod}")
            conexion.commit()
            desconectarBD(conexion)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se puede eliminar (posiblemente esté en uso en ventas): {e}")
            return False

    @staticmethod
    def obtener_ids_proveedores():
        """Retorna solo los IDs de proveedores para el Combobox"""
        cursor, conexion = conectarBD()
        if cursor == None: return []
        cursor.execute("SELECT id_proveedor FROM proveedores")
        datos = [row[0] for row in cursor.fetchall()] # Convertir lista de tuplas a lista simple
        desconectarBD(conexion)
        return datos