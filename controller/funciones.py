import os
from PIL import Image, ImageTk
from model.usuariosCRUD import *

def obtener_imagen(nombre, ancho, alto):
    # Busca la carpeta 'images' desde la raíz del proyecto
    RUTA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RUTA_IMAGENES = os.path.join(RUTA_BASE, "images")
    ruta_imagen = os.path.join(RUTA_IMAGENES, nombre)

    if os.path.exists(ruta_imagen):
        img = Image.open(ruta_imagen)
        img = img.resize((ancho, alto))
        return ImageTk.PhotoImage(img)
    else:
        return None
