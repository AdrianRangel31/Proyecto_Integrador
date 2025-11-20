from conexionBD import *
from tkinter import messagebox

class Productos:
    
    @staticmethod
    def buscar(campo="Todo", valor=None):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "no se pudo conectarse con la base de datos")
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
                    filtros = {
                        "ID": "id_producto",
                        "Nombre": "nombre",
                        "Proveedor": "id_proveedor"
                    }
                    if campo in filtros:
                        sql = f"SELECT * FROM productos WHERE {filtros[campo]} LIKE '%{valor}%'"

        cursor.execute(sql)
        resultado = cursor.fetchall()
        desconectarBD(conexion)
        return resultado

    @staticmethod
    def insertar(nombre, descripcion, cantidad, unidad, precio, fecha_cad, proveedor):
        cursor, conexion = conectarBD()
        if cursor == None: return False
        try:
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
        if cursor == None: return False
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
        if cursor == None: return False
        try:
            cursor.execute(f"DELETE FROM productos WHERE id_producto = {id_prod}")
            conexion.commit()
            desconectarBD(conexion)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se puede eliminar: {e}")
            return False

    # --- NUEVO MÉTODO PARA LA TABLA DE AYUDA ---
    @staticmethod
    def obtener_lista_proveedores():
        """Retorna ID y Nombre de los proveedores para mostrar en la tabla de ayuda"""
        cursor, conexion = conectarBD()
        if cursor == None: return []
        # Asegúrate de que tu tabla proveedores tenga columnas 'id_proveedor' y 'nombre'
        try:
            cursor.execute("SELECT id_proveedor, nombre FROM proveedores")
            datos = cursor.fetchall()
            desconectarBD(conexion)
            return datos
        except:
            return []