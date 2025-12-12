from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from datetime import datetime
import os

def obtener_ruta_logo():
    ruta_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(ruta_base, "images", "logo.png")

class GeneradorPDF:
    def __init__(self, nombre_archivo, titulo_reporte):
        self.nombre_archivo = nombre_archivo
        self.titulo = titulo_reporte
        self.c = canvas.Canvas(nombre_archivo, pagesize=letter)
        self.ancho, self.alto = letter

    def generar_encabezado(self):
        ruta_logo = obtener_ruta_logo()
        if os.path.exists(ruta_logo):
            self.c.drawImage(ruta_logo, 30, 700, width=80, height=80, mask='auto')
        
        self.c.setFont("Helvetica-Bold", 20)
        self.c.setFillColor(HexColor("#B71C1C")) 
        self.c.drawString(130, 750, "CHIVATA'S BURGER - INVENTORY")
        
        self.c.setFont("Helvetica-Bold", 14)
        self.c.setFillColor(HexColor("#000000"))
        self.c.drawString(130, 730, self.titulo)
        
        fecha_hoy = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.c.setFont("Helvetica", 10)
        self.c.drawString(450, 750, f"Date: {fecha_hoy}")
        
        self.c.setStrokeColor(HexColor("#B71C1C"))
        self.c.line(30, 700, 580, 700)

    def generar_tabla(self, datos):
        y = 670 
        # Encabezados en inglés
        encabezados = ["ID", "Product", "Stock", "Unit", "Price", "Expiration"]
        posiciones_x = [30, 70, 220, 280, 350, 430] 

        self.c.setFont("Helvetica-Bold", 10)
        self.c.setFillColor(HexColor("#FFFFFF"))
        
        self.c.setFillColor(HexColor("#B71C1C"))
        self.c.rect(30, y-5, 550, 15, fill=1, stroke=0)
        
        self.c.setFillColor(HexColor("#FFFFFF")) 
        for i, enc in enumerate(encabezados):
            self.c.drawString(posiciones_x[i], y, enc)
        
        y -= 20 
        
        self.c.setFont("Helvetica", 9)
        self.c.setFillColor(HexColor("#000000"))
        
        total_inventario = 0

        for fila in datos:
            self.c.drawString(posiciones_x[0], y, str(fila[0])) # ID
            self.c.drawString(posiciones_x[1], y, str(fila[1])[:25]) # Nombre
            self.c.drawString(posiciones_x[2], y, str(fila[3])) # Cantidad
            self.c.drawString(posiciones_x[3], y, str(fila[4])) # Unidad
            self.c.drawString(posiciones_x[4], y, f"${fila[5]}") # Precio
            self.c.drawString(posiciones_x[5], y, str(fila[6])) # Caducidad
            
            try:
                total_inventario += float(fila[3]) * float(fila[5])
            except:
                pass

            y -= 15 
            
            if y < 50:
                self.c.showPage()
                self.generar_encabezado()
                y = 670

        self.c.setStrokeColor(HexColor("#B71C1C"))
        self.c.line(30, y+5, 580, y+5)
        y -= 20
        self.c.setFont("Helvetica-Bold", 12)
        self.c.drawString(350, y, f"Total Inventory Value: ${total_inventario:.2f}")

    def guardar(self):
        self.c.save()