from conexionBD import *
from tkinter import messagebox
class ventas:
    @staticmethod
    def buscar(campo,valor=None):
        cambio = {"ID":"id_venta","Fecha":"fecha_venta","Total":"total"}
        cursor, conexion = conectarBD()
        if cursor == None:
                messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
        if campo=="Todo":
            cursor.execute("select id_venta,fecha_venta,total from ventas")
        else:
            match valor:
                case "Más recientes":
                    cursor.execute(f"select id_venta,fecha_venta,total from ventas order by fecha_venta desc")
                case "Más antiguos":
                    cursor.execute(f"select id_venta,fecha_venta,total from ventas order by fecha_venta asc")
                case "Más bajo":
                    cursor.execute(f"select id_venta,fecha_venta,total from ventas order by total asc")  
                case "Más alto":
                    cursor.execute(f"select id_venta,fecha_venta,total from ventas order by total desc")       
                case _:
                    cursor.execute(f"select id_venta,fecha_venta,total from ventas where {cambio[campo]} = '{valor}'")
        return cursor.fetchall()

    @staticmethod
    def insertar(total):
        cursor, conexion = conectarBD()
        if cursor == None:
                messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
                return False,0
        cursor.execute(f"insert into ventas values(NULL,1,NOW(),{total})")
        conexion.commit()
        return True, cursor.lastrowid

    def eliminar(id):
        cursor, conexion = conectarBD()
        if cursor == None:
                messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
                return False
        cursor.execute(f"delete from ventas where id_venta = {id}")
        conexion.commit()
        return True

class detalleVenta:
    @staticmethod
    def buscar(id):
        cursor, conexion = conectarBD()
        if cursor == None:
                messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
        cursor.execute("""
            SELECT dv.id_detalle,dv.id_venta, m.nombre, dv.cantidad, dv.subtotal
            FROM detalle_venta dv
            JOIN menu m ON dv.id_producto = m.id_menu
            WHERE dv.id_venta = %s
        """, (id,))
        return cursor.fetchall()
    
    def insertar(id_venta,producto,cantidad):
        cursor, conexion = conectarBD()
        if cursor == None:
                messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
        cursor.execute(f"select id_menu,precio from menu where nombre = '{producto}'")
        registros = cursor.fetchall()
        id_producto = registros[0][0]
        precio = registros[0][1]
        cursor.execute(f"insert into detalle_venta values(NULL,{id_venta},{id_producto},{cantidad},{precio*cantidad})")    
        conexion.commit()
        return True

class menu:
    @staticmethod
    def obtenerPrecios():
        cursor, conexion = conectarBD()
        if cursor == None:
                messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
        cursor.execute("select precio from menu")
        return cursor.fetchall()

    @staticmethod
    def obtenerProductos():
        cursor, conexion = conectarBD()
        if cursor == None:
                messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
        cursor.execute("select nombre from menu")
        return cursor.fetchall()