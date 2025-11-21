from tkinter import *
from PIL import Image, ImageTk
from view.plantilla.plantilla_interfaz import *
from view.usuarios.usuario import *
from controller.funciones import *
from view.ventas.ventas import *
from tkinter import messagebox
from view.Productos.productos import *
from view.Proveedores.proveedores_interfaz import *

class Dashboard(Frame):#Cada interfaz es un Frame. La clase hereda los atributos y metodos de la clase Frame()
    def __init__(self, master, controlador): #El master es el contenedor padre del widget o frame. En todas las interfaces sera la ventana App()
        super().__init__(master) #Se heredan los atributos que tenga la clase App. 
        self.controlador = controlador #El controlador hereda los metodos de la clase App. Se usara principalmente para la funcion mostrar pantalla. Ej. self.controlador.mostrar_pantalla("interfaz")

        # --- 1. Configuración de Colores ---
        COLOR_FONDO_APP    = "#B01E2D"
        COLOR_BLANCO       = "#FFFFFF"
        COLOR_HEADER_ROJO  = "#F82A3E"
        COLOR_BOTON_AZUL   = "#669BBC"
        COLOR_BOTON_ROJO   = "#D32F2F"
        COLOR_TEXTO_BLANCO = "#FFFFFF"
        COLOR_TEXTO_NEGRO  = "#000000"
        
        self.configure(bg=COLOR_FONDO_APP)
        
        # --- 2. Escalado Dinámico ---
        self.master.update_idletasks()
        ancho_ventana = self.master.winfo_width()
        alto_ventana = self.master.winfo_height()
        
        ALTURA_BASE = 720.0 
        self.escala = alto_ventana / ALTURA_BASE 

        def s(valor):
            return int(valor * self.escala)

        # Fuentes
        f_welcome_t   = ("Arial", s(12))
        f_welcome_n   = ("Arial", s(20), "bold")
        f_btn_nav     = ("Arial", s(13))
        f_label_chart = ("Arial", s(15), "bold")
        f_label_sc    = ("Arial", s(14))
        f_btn_sc      = ("Arial", s(12), "bold")
        
        # Tamaños
        w_logo, h_logo   = s(70), s(70)
        w_chart, h_chart = s(480), s(300)
        w_icon, h_icon   = s(24), s(24)
        
        # Espaciados
        p_card_x = s(40)
        p_card_y = s(30)
        p_gap    = s(10)
        
        # Relleno interno botones
        btn_ipad_y = s(8) 
        

        # --- 3. Estructura Visual ---
        
        card = Frame(self, bg=COLOR_BLANCO)
        card.place(relx=0.5, rely=0.5, relwidth=0.92, relheight=0.92, anchor=CENTER)
        
        card.columnconfigure(0, weight=30) 
        card.columnconfigure(1, weight=70) 
        card.rowconfigure(0, weight=1)

        # ==========================================
        # COLUMNA IZQUIERDA: MENÚ
        # ==========================================
        frame_left = Frame(card, bg=COLOR_BLANCO)
        frame_left.grid(row=0, column=0, sticky="nsew", padx=(p_card_x, s(20)), pady=p_card_y)
        
        header_frame = Frame(frame_left, bg=COLOR_HEADER_ROJO)
        header_frame.pack(fill=X, pady=(0, s(30)), ipady=p_gap) 
        
        header_content = Frame(header_frame, bg=COLOR_HEADER_ROJO)
        header_content.pack(expand=True)
        
        self.img_logo = obtener_imagen("logo.png", w_logo, h_logo)
        Label(header_content, image=self.img_logo, bg=COLOR_HEADER_ROJO).pack(side=LEFT, padx=(0, p_gap))
        
        frame_textos = Frame(header_content, bg=COLOR_HEADER_ROJO)
        frame_textos.pack(side=LEFT)
        Label(frame_textos, text="Welcome", bg=COLOR_HEADER_ROJO, fg=COLOR_TEXTO_BLANCO, font=f_welcome_t, anchor="w").pack(fill=X)
        Label(frame_textos, text="[nombre_usuario]", bg=COLOR_HEADER_ROJO, fg=COLOR_TEXTO_BLANCO, font=f_welcome_n, anchor="w").pack(fill=X)

        # Botones Navegación
        botones_nav = ["Ver ventas", "Ver productos", "Ver proveedores", "Ver usuarios"]
        
        frame_nav_top = Frame(frame_left, bg=COLOR_BLANCO)
        frame_nav_top.pack(side=TOP, fill=X)


        btn_ventas = Button(frame_nav_top, text="Ver ventas", 
                     bg=COLOR_BOTON_AZUL, fg=COLOR_TEXTO_BLANCO,
                     font=f_btn_nav, relief="flat", cursor="hand2",
                     command=lambda: self.controlador.mostrar_pantalla("mainventas"))
        btn_ventas.pack(fill=X, pady=s(12), ipady=btn_ipad_y)

        btn_productos = Button(frame_nav_top, text="Ver productos", 
                     bg=COLOR_BOTON_AZUL, fg=COLOR_TEXTO_BLANCO,
                     font=f_btn_nav, relief="flat", cursor="hand2",
                     command=lambda: self.controlador.mostrar_pantalla("productos_main"))
        btn_productos.pack(fill=X, pady=s(12), ipady=btn_ipad_y)

        btn_prov = Button(frame_nav_top, text="Ver proveedores", 
                     bg=COLOR_BOTON_AZUL, fg=COLOR_TEXTO_BLANCO,
                     font=f_btn_nav, relief="flat", cursor="hand2",
                     command=lambda: self.controlador.mostrar_pantalla("proveedores_main"))
        btn_prov.pack(fill=X, pady=s(12), ipady=btn_ipad_y)

        btn_usuarios = Button(frame_nav_top, text="Ver usuarios", 
                     bg=COLOR_BOTON_AZUL, fg=COLOR_TEXTO_BLANCO,
                     font=f_btn_nav, relief="flat", cursor="hand2",
                     command=lambda: "")
        btn_usuarios.pack(fill=X, pady=s(12), ipady=btn_ipad_y)

        # Botón Cerrar Sesión
        btn_logout = Button(frame_left, text="Cerrar sesión", 
                            bg=COLOR_BOTON_ROJO, fg=COLOR_TEXTO_BLANCO,
                            font=f_btn_nav, relief="flat", cursor="hand2",
                            command=lambda: self.controlador.mostrar_pantalla("Login"))
        btn_logout.pack(side=BOTTOM, fill=X, ipady=btn_ipad_y)


        # ==========================================
        # COLUMNA DERECHA: DASHBOARD
        # ==========================================
        frame_right = Frame(card, bg=COLOR_BLANCO)
        frame_right.grid(row=0, column=1, sticky="nsew", padx=(s(20), p_card_x), pady=p_card_y)
        
        area_grafico = Frame(frame_right, bg=COLOR_BLANCO)
        area_grafico.pack(fill=BOTH, expand=True)
        
        self.img_chart = obtener_imagen("graph.png", w_chart, h_chart)
        
        contenedor_img = Frame(area_grafico, bg=COLOR_BLANCO)
        contenedor_img.pack(expand=True) 
        
        if self.img_chart:
            lbl_chart = Label(contenedor_img, image=self.img_chart, bg=COLOR_BLANCO)
            lbl_chart.pack(pady=(0, s(15)))
        else:
            Label(contenedor_img, text="[ Gráfico ]", bg="#eee", 
                  width=int(50*self.escala), height=int(15*self.escala)).pack()
            
        Label(contenedor_img, text="Ventas semanales", bg=COLOR_BLANCO, 
              fg=COLOR_TEXTO_NEGRO, font=f_label_chart).pack()
        
        
        # --- SECCIÓN ATAJOS ---
        area_atajos = Frame(frame_right, bg=COLOR_BLANCO)
        area_atajos.pack(fill=X, pady=(s(20), 0))
        
        Label(area_atajos, text="Atajos", bg=COLOR_BLANCO, 
              fg=COLOR_TEXTO_NEGRO, font=f_label_sc).pack(pady=(0, s(10)))
        
        #self.icon_stats = obtener_imagen("icon_stats.png", w_icon, h_icon)
        #self.icon_refresh = obtener_imagen("icon_refresh.png", w_icon, h_icon)
        
        margen_interno_horizontal = s(20) # Espacio dentro del botón a los lados del texto

        btn_reg = Button(area_atajos, text="  Registrar ventas",
                         compound=LEFT, bg=COLOR_BOTON_AZUL, fg=COLOR_TEXTO_BLANCO,
                         font=f_btn_sc, relief="flat", cursor="hand2")
        
        btn_reg.pack(pady=s(8), ipady=btn_ipad_y, ipadx=margen_interno_horizontal) 

        btn_upd = Button(area_atajos, text="  Actualizar inventario",
                         compound=LEFT, bg=COLOR_BOTON_AZUL, fg=COLOR_TEXTO_BLANCO,
                         font=f_btn_sc, relief="flat", cursor="hand2")
                         
        btn_upd.pack(pady=s(8), ipady=btn_ipad_y, ipadx=margen_interno_horizontal)

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
        self.pantallas["Login"] = Login(self, self)
        self.pantallas["Dashboard"] = Dashboard(self, self)
        self.pantallas["plantilla"] = Plantilla(self,self) #Cada que hagan una interfaz deben agregarla al diccionario self.pantallas
        self.mostrar_pantalla("Login")
        
        #---------------------------------------------------------------
        #                       PANTALLAS PRODUCTOS
        #---------------------------------------------------------------
        self.pantallas["productos_main"] = ProductosMain(self, self)

        self.pantallas["productos_actualizar"] = ProductosActualizar(self, self)
        self.pantallas["productos_eliminar"] = ProductosEliminar(self, self)
        #self.mostrar_pantalla("mainventas")

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
            case "productos_insertar":
                self.pantallas["productos_insertar"] = ProductosInsertar(self, self)
        for pantalla in self.pantallas.values():
            pantalla.pack_forget()
        self.pantallas[nombre].pack(expand=True, fill="both")


if __name__ == "__main__":
    app = App()
    app.mainloop()
