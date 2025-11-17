from conexionBD import *
from tkinter import messagebox
class ventas:
    @staticmethod
    def buscar(campo,valor=None):
        cambio = {"ID":"id_venta","Fecha":"fecha_venta","Total":"total"}
        cursor, conexion = conectarBD()
        if cursor == None:
                messagebox.showinfo("Aviso", "Error al conectarse a la base de datos")
        if campo=="*":
            cursor.execute("select id_venta,fecha_venta,total from ventas")
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
                    cursor.execute(f"select * from ventas where {cambio[campo]} = '{valor}'")
        return cursor.fetchall()