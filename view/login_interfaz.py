from tkinter import *
from view.header import *
#Plantilla para realizar interfaces. Seguir la siguiente estructura para las clases principales

class iniciar_sesion(Frame):
    def __init__(self, master, controlador):
        super().__init__(master)
        self.controlador = controlador
        titulo = "Iniciar sesion"
        label = Label(self,text="hola amigo")
        label.pack()

    def interfaz_login(frame):
        frame_login = Frame(width=300, height=180, bg="#F82A3E", relief=SUNKEN)
        frame_login.pack_propagate(False)
        frame_login(pady=300)