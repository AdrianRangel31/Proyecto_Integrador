from conexionBD import *
from tkinter import messagebox

class ventas:
    @staticmethod
    def buscar(campo,valor=None):
        # Mapeo de UI en Inglés a columnas BD
        cambio = {"ID":"id_venta","Date":"fecha_venta","Total":"total_venta","Time":"hora_venta"}
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Notice", "Error connecting to database")
            return []
        try:
            if campo=="All":
                cursor.execute("select * from ventas")
            elif campo=="Time":
                cursor.execute(f"select * from ventas where hora_venta like '%{valor}%'")
            else:
                match valor:
                    case "Newest":
                        cursor.execute(f"select * from ventas order by fecha_venta desc, hora_venta desc")
                    case "Oldest":
                        cursor.execute(f"select * from ventas order by fecha_venta asc, hora_venta asc")
                    case "Lowest":
                        cursor.execute(f"select * from ventas order by total_venta asc")  
                    case "Highest":
                        cursor.execute(f"select * from ventas order by total_venta desc")       
                    case _:
                        cursor.execute(f"select * from ventas where {cambio[campo]} = %s", (valor,))
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error searching sales: {e}")
            return []

    @staticmethod
    def insertar(total,fecha,hora):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Notice", "Error connecting to database")
            return False,0
        try:
            cursor.execute(f"insert into ventas values(NULL,'{fecha}','{hora}',{total})")
            conexion.commit()
            return True, cursor.lastrowid
        except Exception as e:
            messagebox.showerror("Error", f"Could not insert sale: {e}")
            return False,0

    @staticmethod
    def eliminar(id):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Notice", "Error connecting to database")
            return False
        try:
            cursor.execute(f"delete from ventas where id_venta = %s", (id,))
            conexion.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete sale: {e}")
            return False

    @staticmethod
    def actualizar_total(id_venta, total,fecha,hora):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Notice", "Error connecting to database")
            return False
        try:
            cursor.execute("update ventas set total_venta = %s,fecha_venta = %s, hora_venta = %s where id_venta = %s", (total,fecha,hora, id_venta))
            conexion.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not update sale total: {e}")
            return False
        
    @staticmethod
    def obtener_hora(id):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Notice", "Error connecting to database")
            return []
        try:
            cursor.execute(f"select fecha_venta,hora_venta from ventas where id_venta = {id}")
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error searching sales: {e}")
            return []

class detalleVenta:
    @staticmethod
    def insertar(id_venta,producto,cantidad):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Notice", "Error connecting to database")
            return False
        try:
            cursor.execute("select id_menu,precio from productos where nombre = %s", (producto,))
            registros = cursor.fetchall()
            if not registros:
                messagebox.showerror("Error", f"Product '{producto}' does not exist in menu.")
                return False
            id_producto = registros[0][0]
            precio = registros[0][1]
            cursor.execute("insert into detalle_venta values(NULL,%s,%s,%s,%s)", (id_venta, id_producto, cantidad, float(precio)*int(cantidad)))
            conexion.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not insert sale detail: {e}")
            return False
    
    @staticmethod
    def buscar(id):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Notice", "Error connecting to database")
            return []
        try:
            cursor.execute("""
                SELECT dv.id_detalle, dv.id_venta, m.nombre, dv.cantidad, dv.subtotal
                FROM detalle_venta dv
                JOIN productos m ON dv.id_menu = m.id_menu
                WHERE dv.id_venta = %s
            """, (id,))
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Could not get details: {e}")
            return []

    @staticmethod
    def actualizar(id_detalle,valor,producto):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Notice", "Error connecting to database")
            return False
        try:
            cursor.execute("select precio from productos where nombre = %s", (producto,))
            registros = cursor.fetchall()
            if not registros:
                messagebox.showerror("Error", f"Product '{producto}' does not exist in menu.")
                return False
            precio = registros[0][0]
            cursor.execute("update detalle_venta set cantidad = %s, subtotal = %s where id_detalle = %s", (valor, float(valor)*float(precio), id_detalle))
            conexion.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not update detail: {e}")
            return False
    
    @staticmethod
    def eliminar(id_detalle):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Notice", "Error connecting to database")
            return False
        try:
            cursor.execute("delete from detalle_venta where id_detalle = %s", (id_detalle,))
            conexion.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete detail: {e}")
            return False

    @staticmethod
    def eliminar_por_venta(id_venta):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Notice", "Error connecting to database")
            return False
        try:
            cursor.execute("delete from detalle_venta where id_venta = %s", (id_venta,))
            conexion.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete sale details: {e}")
            return False

    @staticmethod
    def obtener_cantidades(id_venta):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Notice", "Error connecting to database")
            return []
        try:
            cursor.execute("""
                SELECT m.id_menu, COALESCE(dv.cantidad, 0) as cantidad
                FROM productos m
                LEFT JOIN detalle_venta dv ON dv.id_menu = m.id_menu AND dv.id_venta = %s
                ORDER BY m.id_menu
            """, (id_venta,))
            filas = cursor.fetchall()
            cantidades = [int(f[1]) for f in filas]
            return cantidades
        except Exception as e:
            messagebox.showerror("Error", f"Could not get quantities: {e}")
            return []

    @staticmethod
    def obtener_id_detalle(id_venta,id_producto):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Notice", "Error connecting to database")
            return None
        try:
            cursor.execute("select id_detalle from detalle_venta where id_venta = %s and id_menu = %s", (id_venta, id_producto))
            res = cursor.fetchone()
            if not res:
                return None
            return int(res[0])
        except Exception as e:
            messagebox.showerror("Error", f"Could not get id_detalle: {e}")
            return None


class menu:
    @staticmethod
    def obtenerPrecios():
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Notice", "Error connecting to database")
            return []
        try:
            cursor.execute("select precio from productos order by id_menu")
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Could not get prices: {e}")
            return []

    @staticmethod
    def obtenerProductos():
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Notice", "Error connecting to database")
            return []
        try:
            cursor.execute("select nombre from productos order by id_menu")
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Could not get products: {e}")
            return []

    @staticmethod
    def obtener_todo():
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Notice", "Error connecting to database")
            return []
        cursor.execute("SELECT * FROM productos")
        return cursor.fetchall()
    
    @staticmethod
    def insertar(nombre, precio):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Notice", "Error connecting to database")
            return False
        try:
            cursor.execute("INSERT INTO productos (nombre, precio) VALUES (%s, %s)",
                                (nombre, precio))
            conexion.commit()
            return True
        except:
            return False
    @staticmethod
    def actualizar(id, nombre, precio):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Notice", "Error connecting to database")
            return False
        try:       
            cursor.execute("UPDATE productos SET nombre=%s, precio=%s WHERE id_menu=%s",
                                (nombre, precio, id))
            conexion.commit()
            return True
        except:    
            return False
    @staticmethod
    def eliminar(id):
        cursor, conexion = conectarBD()
        if cursor == None:
            messagebox.showinfo("Notice", "Error connecting to database")
            return False
        try:
            cursor.execute("DELETE FROM productos WHERE id_menu=%s", (id,))
            conexion.commit()
            return True
        except:
            return False

class reportes:
    @staticmethod
    def obtener_datos_grafico(periodo):
        cursor, conexion = conectarBD()
        if cursor == None:
            return []
        
        intervalo = ""
        # Traducimos de la UI en Inglés a SQL
        match periodo:
            case "Weekly":
                intervalo = "INTERVAL 1 WEEK"
            case "Monthly":
                intervalo = "INTERVAL 1 MONTH"
            case "Quarterly":
                intervalo = "INTERVAL 3 MONTH"
            case _:
                intervalo = "INTERVAL 1 WEEK"

        query = f"""
            SELECT m.nombre, SUM(dv.cantidad) as total_cantidad, SUM(dv.subtotal) as total_dinero
            FROM detalle_venta dv
            JOIN ventas v ON dv.id_venta = v.id_venta
            JOIN productos m ON dv.id_menu = m.id_menu
            WHERE v.fecha_venta >= DATE_SUB(CURDATE(), {intervalo})
            GROUP BY m.nombre
            ORDER BY total_cantidad DESC
        """
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Report error: {e}")
            return []

    @staticmethod
    def obtener_ingresos_grafico(periodo):
        cursor, conexion = conectarBD()
        if cursor == None:
            return []
        
        intervalo = ""
        match periodo:
            case "Weekly":
                intervalo = "INTERVAL 1 WEEK"
            case "Monthly":
                intervalo = "INTERVAL 1 MONTH"
            case "Quarterly":
                intervalo = "INTERVAL 3 MONTH"
            case _:
                intervalo = "INTERVAL 1 WEEK"

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
            print(f"Income report error: {e}")
            return []