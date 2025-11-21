from conexionBD import *
from tkinter import messagebox

class ventas:
    @staticmethod
    def buscar(campo,valor=None):
        cambio = {"ID":"id_venta","Fecha":"fecha_venta","Total":"total"}
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
                        cursor.execute(f"select * from ventas order by fecha_venta desc")
                    case "Más antiguos":
                        cursor.execute(f"select * from ventas order by fecha_venta asc")
                    case "Más bajo":
                        cursor.execute(f"select * from ventas order by total asc")  
                    case "Más alto":
                        cursor.execute(f"select * from ventas order by total desc")       
                    case _:
                        cursor.execute(f"select * from ventas where {cambio[campo]} = %s", (valor,))
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar ventas: {e}")
            return []

    @staticmethod
    def insertar(total):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
            return False,0
        try:
            cursor.execute(f"insert into ventas values(NULL,NOW(),%s)", (total,))
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
    def actualizar_total(id_venta, total):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
            return False
        try:
            cursor.execute("update ventas set total = %s where id_venta = %s", (total, id_venta))
            conexion.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el total de la venta: {e}")
            return False

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
