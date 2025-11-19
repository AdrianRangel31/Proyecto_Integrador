from tkinter import *
from PIL import Image, ImageTk
from view.plantilla.plantilla_interfaz import *
from view import login_interfaz
from controller.funciones import *
from view.ventas.ventas import *
from tkinter import messagebox

class login(Frame):#Cada interfaz es un Frame. La clase hereda los atributos y metodos de la clase Frame()
    def __init__(self, master, controlador): #El master es el contenedor padre del widget o frame. En todas las interfaces sera la ventana App()
        super().__init__(master) #Se heredan los atributos que tenga la clase App. 
        self.controlador = controlador #El controlador hereda los metodos de la clase App. Se usara principalmente para la funcion mostrar pantalla. Ej. self.controlador.mostrar_pantalla("interfaz")

class App(Tk): #Clase donde va la ventana principal del sistema
    def __init__(self):
        super().__init__()
        self.title("Ventas")
        self.state('zoomed')
        self.geometry("1024x720")
        self.pantallas = {} #Diccionario que contiene cada interfaz
        """
        Al crear una nueva interfaz, debe importarse y añadirse al diccionario de pantallas.
        self.pantallas["nombre de la interfaz"] = paquete.interfaz(self,self) 
        Es importante añadir el (self,self) pues hereda los metodos y atributos de la ventana principal para su correcto funcionamiento y conexion.
        """
        #self.pantallas["plantilla"] = Plantilla(self,self)
        self.pantallas["Login"] = login_interfaz.iniciar_sesion(self, self)
        self.pantallas["plantilla"] = Plantilla(self,self)#Cada que hagan una interfaz deben agregarla al diccionario self.pantallas
        self.mostrar_pantalla("mainventas")

    def mostrar_pantalla(self, nombre,parametro=None): #Cambia completamente la interfaz. Incluye un "Borrar pantalla"
        match nombre:
            case "mainventas":
                self.pantallas["mainventas"] = mainVentas(self,self)
            case "insertarventas":
                self.pantallas["insertarventas"] = insertarVentas(self,self,"agregar")
            case "actualizarventas":
                if parametro == 0:
                    messagebox.showwarning("Advertencia","Seleccione un registro para continuar")
                    return
                self.pantallas["actualizarventas"] = insertarVentas(self,self,"actualizar",parametro)

        for pantalla in self.pantallas.values():
            pantalla.pack_forget()
        self.pantallas[nombre].pack(expand=True, fill="both")


if __name__ == "__main__":
    app = App()
    app.mainloop()
