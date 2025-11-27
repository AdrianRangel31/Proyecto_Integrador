from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from datetime import datetime
import os

# Ajusta esta ruta si es necesario para encontrar tu logo
def obtener_ruta_logo():
    ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(ruta_base, "images", "logo.png")

class GeneradorPDF:
    def __init__(self, nombre_archivo, titulo_reporte):
        self.nombre_archivo = nombre_archivo
        self.titulo = titulo_reporte
        # Tamaño carta
        self.c = canvas.Canvas(nombre_archivo, pagesize=letter)
        self.ancho, self.alto = letter

    def generar_encabezado(self):
        # Logo
        ruta_logo = obtener_ruta_logo()
        if os.path.exists(ruta_logo):
            self.c.drawImage(ruta_logo, 30, 700, width=80, height=80, mask='auto')
        
        # Títulos
        self.c.setFont("Helvetica-Bold", 20)
        self.c.setFillColor(HexColor("#B71C1C")) # Rojo Chivata's
        self.c.drawString(130, 750, "CHIVATA'S BURGER - INVENTARIO")
        
        self.c.setFont("Helvetica-Bold", 14)
        self.c.setFillColor(HexColor("#000000"))
        self.c.drawString(130, 730, self.titulo)
        
        # Fecha
        fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.c.setFont("Helvetica", 10)
        self.c.drawString(450, 750, f"Fecha: {fecha_hoy}")
        
        # Línea divisoria
        self.c.setStrokeColor(HexColor("#B71C1C"))
        self.c.line(30, 700, 580, 700)

    def generar_tabla(self, datos):
        # datos es una lista de tuplas: [(id, nombre, desc, cant, unidad, precio, cad, prov), ...]
        
        y = 670 # Posición vertical inicial
        encabezados = ["ID", "Producto", "Stock", "Unidad", "Precio", "Caducidad"]
        posiciones_x = [30, 70, 220, 280, 350, 430] # Dónde empieza cada columna

        # Dibujar Encabezados de Tabla
        self.c.setFont("Helvetica-Bold", 10)
        self.c.setFillColor(HexColor("#FFFFFF"))
        
        # Fondo rojo para encabezados
        self.c.setFillColor(HexColor("#B71C1C"))
        self.c.rect(30, y-5, 550, 15, fill=1, stroke=0)
        
        self.c.setFillColor(HexColor("#FFFFFF")) # Texto blanco
        for i, enc in enumerate(encabezados):
            self.c.drawString(posiciones_x[i], y, enc)
        
        y -= 20 # Bajar renglón
        
        # Dibujar Filas
        self.c.setFont("Helvetica", 9)
        self.c.setFillColor(HexColor("#000000"))
        
        total_inventario = 0

        for fila in datos:
            # fila: (0:id, 1:nombre, 2:desc, 3:cant, 4:unidad, 5:precio, 6:cad, 7:prov)
            # Imprimimos solo lo relevante
            self.c.drawString(posiciones_x[0], y, str(fila[0])) # ID
            self.c.drawString(posiciones_x[1], y, str(fila[1])[:25]) # Nombre (recortado si es muy largo)
            self.c.drawString(posiciones_x[2], y, str(fila[3])) # Cantidad
            self.c.drawString(posiciones_x[3], y, str(fila[4])) # Unidad
            self.c.drawString(posiciones_x[4], y, f"${fila[5]}") # Precio
            self.c.drawString(posiciones_x[5], y, str(fila[6])) # Caducidad
            
            # Calculo de valor total (Precio * Cantidad)
            try:
                total_inventario += float(fila[3]) * float(fila[5])
            except:
                pass

            y -= 15 # Bajar para el siguiente producto
            
            # Si se acaba la hoja, crear nueva (simple)
            if y < 50:
                self.c.showPage()
                self.generar_encabezado()
                y = 670

        # Pie de página con totales
        self.c.setStrokeColor(HexColor("#B71C1C"))
        self.c.line(30, y+5, 580, y+5)
        y -= 20
        self.c.setFont("Helvetica-Bold", 12)
        self.c.drawString(350, y, f"Valor Total Inventario: ${total_inventario:.2f}")

    def guardar(self):
        self.c.save()