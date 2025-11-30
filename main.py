from tkinter import *
from PIL import Image, ImageTk
from view.plantilla.plantilla_interfaz import *
from view.usuarios.usuario import *
from view.usuarios.usuarios_interfaz import UsuariosMain, UsuariosInsertar
from controller.funciones import *
from view.ventas.ventas import *
from tkinter import messagebox
from view.Productos.productos import *
from view.Proveedores.proveedores_interfaz import *
from view.ventas.menu import ventanaMenu

class Dashboard(Frame):#Cada interfaz es un Frame. La clase hereda los atributos y metodos de la clase Frame()
    def __init__(self, master, controlador): #El master es el contenedor padre del widget o frame. En todas las interfaces sera la ventana App()
        super().__init__(master) #Se heredan los atributos que tenga la clase App. 
        self.controlador = controlador #El controlador hereda los metodos de la clase App. Se usara principalmente para la funcion mostrar pantalla. Ej. self.controlador.mostrar_pantalla("interfaz")
        global su
        su = False

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
        frame_left = Frame(card, bg=COLOR_BLANCO,width=450)
        frame_left.grid(row=0, column=0, sticky="nsew", padx=(p_card_x, s(20)), pady=p_card_y)
        frame_left.pack_propagate(False)

        header_frame = Frame(frame_left, bg=COLOR_HEADER_ROJO)
        header_frame.pack(fill=X, pady=(0, s(30)), ipady=p_gap) 

        header_content = Frame(header_frame, bg=COLOR_HEADER_ROJO)
        header_content.pack(expand=True)

        self.img_logo = obtener_imagen("logo.png", w_logo, h_logo)
        Label(header_content, image=self.img_logo, bg=COLOR_HEADER_ROJO).pack(side=LEFT, padx=(0, p_gap))

        frame_textos = Frame(header_content, bg=COLOR_HEADER_ROJO)
        frame_textos.pack(side=LEFT)
        Label(frame_textos, text="Welcome", bg=COLOR_HEADER_ROJO, fg=COLOR_TEXTO_BLANCO, font=f_welcome_t, anchor="w").pack(fill=X)
        self.lbl_nombre = Label(frame_textos, text="[nombre_usuario]", bg=COLOR_HEADER_ROJO, fg=COLOR_TEXTO_BLANCO, font=f_welcome_n, anchor="w")
        self.lbl_nombre.pack(fill=X)

        frame_nav_top = Frame(frame_left, bg=COLOR_BLANCO)
        #frame_nav_top.grid_propagate(False)
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

        self.btn_usuarios = Button(frame_nav_top, text="Ver usuarios", 
            bg=COLOR_BOTON_AZUL, fg=COLOR_TEXTO_BLANCO,
            font=f_btn_nav, relief="flat", cursor="hand2",
            command=lambda: self.controlador.mostrar_pantalla("usuarios_main")) 
        #btn_usuarios.pack(fill=X, pady=s(12), ipady=btn_ipad_y)

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

        self.img_chart = obtener_imagen("grafico_ingresos_Semanal.png", w_chart, h_chart)

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
        area_atajos.pack(fill=X, pady=(s(10), 0))

        Label(area_atajos, text="Atajos", bg=COLOR_BLANCO, 
              fg=COLOR_TEXTO_NEGRO, font=f_label_sc).pack(pady=(0, s(2)))

        #self.icon_stats = obtener_imagen("icon_stats.png", w_icon, h_icon)
        #self.icon_refresh = obtener_imagen("icon_refresh.png", w_icon, h_icon)

        margen_interno_horizontal = s(20) # Espacio dentro del botón a los lados del texto

        btn_reg = Button(area_atajos, text="  Registrar ventas",
                         compound=LEFT, bg=COLOR_BOTON_AZUL, fg=COLOR_TEXTO_BLANCO,
                         font=f_btn_sc, relief="flat", cursor="hand2",
                         command=lambda: self.controlador.mostrar_pantalla("insertarventas"))

        btn_reg.pack(pady=s(8), ipady=btn_ipad_y, ipadx=margen_interno_horizontal) 
        """         
        btn_upd = Button(area_atajos, text="Ver informes de venta",
                         compound=LEFT, bg=COLOR_BOTON_AZUL, fg=COLOR_TEXTO_BLANCO,
                         font=f_btn_sc, relief="flat", cursor="hand2")

        btn_upd.pack(pady=s(8), ipady=btn_ipad_y, ipadx=margen_interno_horizontal)
        """
    def actualizar_info_usuario(self, nombre, rol):
        self.lbl_nombre.config(text=nombre)
        s = self.escala # Recuperamos la escala para mantener el padding correcto
        btn_ipad_y = int(8 * s)

        if rol == "Superadmin":
            self.lbl_nombre.config(fg="#FFD700")  # Dorado para SuperAdmin
            # Mostramos el botón
            self.btn_usuarios.pack(fill=X, pady=int(12*s), ipady=btn_ipad_y)
        else:
            self.lbl_nombre.config(fg="#000000")
            # Ocultamos el botón si no es Superadmin
            self.btn_usuarios.pack_forget()


class App(Tk): #Clase donde va la ventana principal del sistema
    def __init__(self):
        super().__init__()
        self.title("Sistema de inventario y ventas")
        self.state('zoomed')
        self.geometry("1024x720")

        self.rol_actual = None # Variable para almacenar el rol del usuario actual

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
        self.pantallas["usuarios_main"] = UsuariosMain(self, self)
        self.pantallas["usuarios_insertar"] = UsuariosInsertar(self, self)
        #---------------------------------------------------------------
        #                       PANTALLAS PRODUCTOS
        #---------------------------------------------------------------
        self.pantallas["productos_main"] = ProductosMain(self, self)

        self.pantallas["productos_actualizar"] = ProductosActualizar(self, self)
        self.pantallas["productos_eliminar"] = ProductosEliminar(self, self)


        #---------------------------------------------------------------
        #                       PANTALLAS PROVEEDORES
        #---------------------------------------------------------------
        self.pantallas["proveedores_main"] = ProveedoresMain(self, self)
        self.pantallas["proveedores_insertar"] = ProveedoresInsertar(self, self)
        self.pantallas["proveedores_actualizar"] = ProveedoresActualizar(self, self)
        self.pantallas["proveedores_eliminar"] = ProveedoresEliminar(self, self)

        self.pantallas["menu_crud"] = ventanaMenu(self, self)


        self.crear_menu_atajos()
        self.mostrar_pantalla("Login")


    def mostrar_pantalla(self, nombre,parametro=None): #Cambia completamente la interfaz. Incluye un "Borrar pantalla"
        for pantalla in self.pantallas.values():
            pantalla.pack_forget()
        if nombre == "Login":
            # Ocultar menú en el login pasando un menú vacío
            self.config(menu=Menu(self))
        else:
            # Mostrar menú en el resto de pantallas
            self.config(menu=self.menubar)

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
        self.pantallas[nombre].pack(expand=True, fill="both")

    def ingresar(self, nombre_usuario, rol):
        # 1. Obtener la referencia al frame del Dashboard
        # Asegúrate que la "key" ("Dashboard") sea exactamente como la definiste al crear los frames
            self.rol_actual = rol
            self.crear_menu_atajos()  # Actualiza el menú con el rol correcto   

            if "Dashboard" in self.pantallas:
                dashboard = self.pantallas["Dashboard"]
                # 2. Mandar el nombre al Dashboard
                dashboard.actualizar_info_usuario(nombre_usuario, rol)
                # 3. Cambiar de pantalla
                self.mostrar_pantalla("Dashboard")

    def crear_menu_atajos(self):
            # --- CONFIGURACIÓN DE ESTILO ---
            # Usamos los mismos colores que defines en tu Dashboard
            COLOR_FONDO_MENU = "#F7F7F7"   # Color del Header (Rojo Brillante)
            COLOR_LETRA = "#000000"        # Blanco
            COLOR_ACTIVO = "#B3B3B3"       # Color Fondo App (Rojo Oscuro) para selección
            FUENTE_MENU = ("Arial", 13) # Fuente más grande para el tamaño

            # Diccionario de configuración para reutilizar en todos los menús
            config_menu = {
                "bg": COLOR_FONDO_MENU,
                "fg": COLOR_LETRA,
                "activebackground": COLOR_ACTIVO,
                "activeforeground": COLOR_LETRA,
                "font": FUENTE_MENU,
                "tearoff": 0,   # Quita la línea punteada de separación
                "bd": 0
            }

            # --- BARRA PRINCIPAL ---
            self.menubar = Menu(self, bg=COLOR_FONDO_MENU, fg=COLOR_LETRA, font=FUENTE_MENU, bd=0)

            # 1. Menú ATAJOS (General)
            atajos_menu = Menu(self.menubar, **config_menu)
            self.menubar.add_cascade(label="  🏠 ATAJOS RÁPIDOS  ", menu=atajos_menu)
            
            atajos_menu.add_command(label="🏠 Ir al Dashboard", command=lambda: self.mostrar_pantalla("Dashboard"))
            atajos_menu.add_separator()
            atajos_menu.add_command(label="🚪 Cerrar Sesión", command=lambda: self.mostrar_pantalla("Login"))

            # 2. Menú VENTAS
            ventas_menu = Menu(self.menubar, **config_menu)
            self.menubar.add_cascade(label="  💰 VENTAS  ", menu=ventas_menu)
            
            ventas_menu.add_command(label="📄 Gestionar Ventas (Ver Tabla)", command=lambda: self.mostrar_pantalla("mainventas"))
            ventas_menu.add_command(label="➕ Nueva Venta", command=lambda: self.mostrar_pantalla("insertarventas"))
            ventas_menu.add_separator()
        
            ventas_menu.add_command(label="💲 Modificar Precios (Menú)", command=lambda: self.mostrar_pantalla("menu_crud"))

            # 3. Menú PRODUCTOS
            prod_menu = Menu(self.menubar, **config_menu)
            self.menubar.add_cascade(label="  🍔 INGREDIENTES  ", menu=prod_menu)
            
            prod_menu.add_command(label="📦 Ver Inventario", command=lambda: self.mostrar_pantalla("productos_main"))
            prod_menu.add_command(label="➕ Añadir Ingrediente", command=lambda: self.mostrar_pantalla("productos_insertar"))

            # 4. Menú PROVEEDORES
            prov_menu = Menu(self.menubar, **config_menu)
            self.menubar.add_cascade(label="  🚚 PROVEEDORES  ", menu=prov_menu)
            
            prov_menu.add_command(label="📋 Ver Proveedores", command=lambda: self.mostrar_pantalla("proveedores_main"))
            prov_menu.add_command(label="➕ Añadir Proveedor", command=lambda: self.mostrar_pantalla("proveedores_insertar"))

            # 5. Menú USUARIOS
            if self.rol_actual == "Superadmin":
                user_menu = Menu(self.menubar, **config_menu)
                self.menubar.add_cascade(label="  👥 USUARIOS  ", menu=user_menu)
                user_menu.add_command(label="🔑 Gestionar Usuarios", command=lambda: self.mostrar_pantalla("usuarios_main"))
                user_menu.add_command(label="➕ Crear Nuevo Usuario", command=lambda: self.mostrar_pantalla("usuarios_insertar"))
            
            # Si el usuario ya está logueado, forzamos la actualización del menú visualmente
            if self.master: 
                try:
                    self.config(menu=self.menubar)
                except:
                    pass


if __name__ == "__main__":
    app = App()
    app.mainloop()