from tkinter import *
from header import *
#Plantilla para realizar interfaces. Seguir la siguiente estructura para las clases principales

class Plantilla(Frame):
    def __init__(self, master, controlador):
        super().__init__(master)
        self.controlador = controlador
        head = header(self)
        head.titulo = "Nombre de su interfaz"
        head.pack(fill="x")

        #Widgets...