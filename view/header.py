from tkinter import *
from controller.funciones import *
class header(Frame):
    def __init__(self, master,controlador):
        super().__init__(master)
        self.controlador = controlador
        self.config(bg="#F82A3E", height=150)
        self.__titulo = Label(self, text="Plantilla", font=("Arial", 38), bg="#F82A3E", fg="white")
        self.logo_img = obtener_imagen("logo.png", 150, 150)
        btn_home = Button(self, image=self.logo_img, height=150, bg="#F82A3E", relief="flat"
                          ,activebackground="#F82A3E",
                          command=lambda: self.controlador.mostrar_pantalla("Dashboard"))
        btn_home.grid(row=0, column=0)
        self.__titulo.grid(row=0, column=1, padx=20)

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, nuevo):
        self.__titulo.config(text=nuevo)
    
