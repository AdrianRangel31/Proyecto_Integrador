from conexionBD import *
from tkinter import messagebox

class ventas:
    @staticmethod
    def buscar(campo,valor=None):
        cambio = {"ID":"id_venta","Fecha":"fecha_venta","Total":"total_venta"}
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
            return []
        try:
            if campo=="Todo":
                cursor.execute("select * from ventas")
            else:
                match valor:
                    case "Más recientes":
                        cursor.execute(f"select * from ventas order by fecha_venta desc, hora_venta desc")
                    case "Más antiguos":
                        cursor.execute(f"select * from ventas order by fecha_venta asc, hora_venta asc")
                    case "Más bajo":
                        cursor.execute(f"select * from ventas order by total_venta asc")  
                    case "Más alto":
                        cursor.execute(f"select * from ventas order by total_venta desc")       
                    case _:
                        cursor.execute(f"select * from ventas where {cambio[campo]} = %s", (valor,))
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar ventas: {e}")
            return []

    @staticmethod
    def insertar(total,fecha,hora):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
            return False,0
        try:
            cursor.execute(f"insert into ventas values(NULL,'{fecha}','{hora}',{total})")
            conexion.commit()
            return True, cursor.lastrowid
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo insertar la venta: {e}")
            return False,0

    @staticmethod
    def eliminar(id):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
            return False
        try:
            cursor.execute(f"delete from ventas where id_venta = %s", (id,))
            conexion.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la venta: {e}")
            return False

    @staticmethod
    def actualizar_total(id_venta, total,fecha,hora):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
            return False
        try:
            cursor.execute("update ventas set total_venta = %s,fecha_venta = %s, hora_venta = %s where id_venta = %s", (total,fecha,hora, id_venta))
            conexion.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el total de la venta: {e}")
            return False
        
    @staticmethod
    def obtener_hora(id):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
            return []
        try:
            cursor.execute(f"select fecha_venta,hora_venta from ventas where id_venta = {id}")
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar ventas: {e}")
            return []

class detalleVenta:
    @staticmethod
    def insertar(id_venta,producto,cantidad):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
            return False
        try:
            cursor.execute("select id_menu,precio from menu where nombre = %s", (producto,))
            registros = cursor.fetchall()
            if not registros:
                messagebox.showerror("Error", f"No existe el producto '{producto}' en el menú.")
                return False
            id_producto = registros[0][0]
            precio = registros[0][1]
            cursor.execute("insert into detalle_venta values(NULL,%s,%s,%s,%s)", (id_venta, id_producto, cantidad, float(precio)*int(cantidad)))
            conexion.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo insertar detalle de venta: {e}")
            return False
    
    @staticmethod
    def buscar(id):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
            return []
        try:
            cursor.execute("""
                SELECT dv.id_detalle, dv.id_venta, m.nombre, dv.cantidad, dv.subtotal
                FROM detalle_venta dv
                JOIN menu m ON dv.id_menu = m.id_menu
                WHERE dv.id_venta = %s
            """, (id,))
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener detalles: {e}")
            return []

    @staticmethod
    def actualizar(id_detalle,valor,producto):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
            return False
        try:
            cursor.execute("select precio from menu where nombre = %s", (producto,))
            registros = cursor.fetchall()
            if not registros:
                messagebox.showerror("Error", f"No existe el producto '{producto}' en el menú.")
                return False
            precio = registros[0][0]
            cursor.execute("update detalle_venta set cantidad = %s, subtotal = %s where id_detalle = %s", (valor, float(valor)*float(precio), id_detalle))
            conexion.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar detalle: {e}")
            return False
    
    @staticmethod
    def eliminar(id_detalle):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
            return False
        try:
            cursor.execute("delete from detalle_venta where id_detalle = %s", (id_detalle,))
            conexion.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar detalle: {e}")
            return False

    @staticmethod
    def eliminar_por_venta(id_venta):
        """Elimina todos los detalles de una venta (usado cuando todos los spinbox = 0)."""
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
            return False
        try:
            cursor.execute("delete from detalle_venta where id_venta = %s", (id_venta,))
            conexion.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron eliminar los detalles de la venta: {e}")
            return False

    @staticmethod
    def obtener_cantidades(id_venta):
        """
        Devuelve una lista de cantidades (int) en el orden de los productos del menú.
        Si un producto no está presente en detalle_venta para esa venta, su cantidad será 0.
        """
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
            return []
        try:
            cursor.execute("""
                SELECT m.id_menu, COALESCE(dv.cantidad, 0) as cantidad
                FROM menu m
                LEFT JOIN detalle_venta dv ON dv.id_menu = m.id_menu AND dv.id_venta = %s
                ORDER BY m.id_menu
            """, (id_venta,))
            filas = cursor.fetchall()
            # filas será lista de tuplas (id_menu, cantidad)
            cantidades = [int(f[1]) for f in filas]
            return cantidades
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener cantidades: {e}")
            return []

    @staticmethod
    def obtener_id_detalle(id_venta,id_producto):
        """
        Devuelve el id_detalle (int) para una pareja (id_venta,id_menu) o None si no existe.
        id_producto se espera como id_menu (entero).
        """
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
            return None
        try:
            cursor.execute("select id_detalle from detalle_venta where id_venta = %s and id_menu = %s", (id_venta, id_producto))
            res = cursor.fetchone()
            if not res:
                return None
            return int(res[0])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener id_detalle: {e}")
            return None


class menu:
    @staticmethod
    def obtenerPrecios():
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
            return []
        try:
            cursor.execute("select precio from menu order by id_menu")
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener precios: {e}")
            return []

    @staticmethod
    def obtenerProductos():
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
            return []
        try:
            cursor.execute("select nombre from menu order by id_menu")
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener productos: {e}")
            return []

# --- CLASE PARA REPORTES ---
class reportes:
    @staticmethod
    def obtener_datos_grafico(periodo):
        cursor, conexion = conectarBD()
        if cursor == None:
            return []
        
        # Definir el intervalo de tiempo en SQL
        intervalo = ""
        match periodo:
            case "Semanal":
                intervalo = "INTERVAL 1 WEEK"
            case "Mensual":
                intervalo = "INTERVAL 1 MONTH"
            case "Trimestral":
                intervalo = "INTERVAL 3 MONTH"
            case _:
                intervalo = "INTERVAL 1 WEEK" # Default

        # Consulta: Unimos ventas con detalle_venta y menu para obtener nombres y sumas
        query = f"""
            SELECT m.nombre, SUM(dv.cantidad) as total_cantidad, SUM(dv.subtotal) as total_dinero
            FROM detalle_venta dv
            JOIN ventas v ON dv.id_venta = v.id_venta
            JOIN menu m ON dv.id_menu = m.id_menu
            WHERE v.fecha_venta >= DATE_SUB(CURDATE(), {intervalo})
            GROUP BY m.nombre
            ORDER BY total_cantidad DESC
        """
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en reporte: {e}")
            return []

    @staticmethod
    def obtener_ingresos_grafico(periodo):
        cursor, conexion = conectarBD()
        if cursor == None:
            return []
        
        intervalo = ""
        match periodo:
            case "Semanal":
                intervalo = "INTERVAL 1 WEEK"
            case "Mensual":
                intervalo = "INTERVAL 1 MONTH"
            case "Trimestral":
                intervalo = "INTERVAL 3 MONTH"
            case _:
                intervalo = "INTERVAL 1 WEEK" # Default

        # Consulta para ingresos (ventas totales agrupadas por fecha)
        query = f"""
            SELECT fecha_venta, SUM(total_venta) as total_dia
            FROM ventas
            WHERE fecha_venta >= DATE_SUB(CURDATE(), {intervalo})
            GROUP BY fecha_venta
            ORDER BY fecha_venta ASC
        """
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error en reporte ingresos: {e}")
            return []