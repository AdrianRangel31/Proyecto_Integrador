import os
from PIL import Image, ImageTk

def obtener_imagen(nombre, ancho, alto):
    RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
    ruta_imagen = os.path.join(RUTA_BASE, nombre)
    if os.path.exists(ruta_imagen):
        img = Image.open(ruta_imagen)
        img = img.resize((ancho, alto))
        return ImageTk.PhotoImage(img)