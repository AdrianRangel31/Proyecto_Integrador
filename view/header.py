from tkinter import *
from controller.funciones import *
class header(Frame):
    def __init__(self, master,controlador):
        super().__init__(master)
        self.controlador = controlador
        self.config(bg="#F82A3E", height=230)
        self.__titulo = Label(self, text="Plantilla", font=("Arial", 32), bg="#F82A3E", fg="white")
        self.logo_img = obtener_imagen("logo.png", 230, 230)
        lbl_logo = Label(self, image=self.logo_img, compound="top", height=230, bg="#F82A3E")
        lbl_logo.grid(row=0, column=0)
        self.home_img = obtener_imagen("home.png", 140, 140)
        lbl_home = Button(self, image=self.home_img, height=230, bg="#F82A3E", relief="flat"
                          ,activebackground="#F82A3E")
        lbl_home.grid(row=0, column=1)
        self.__titulo.grid(row=0, column=2, padx=350)

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, nuevo):
        self.__titulo.config(text=nuevo)
    
