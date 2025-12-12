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

class Dashboard(Frame):
    def __init__(self, master, controlador):
        super().__init__(master) 
        self.controlador = controlador 
        global admin
        admin = False

        # --- Configuración de Colores ---
        COLOR_FONDO_APP    = "#B01E2D"
        COLOR_BLANCO       = "#FFFFFF"
        COLOR_HEADER_ROJO  = "#F82A3E"
        COLOR_BOTON_AZUL   = "#669BBC"
        COLOR_BOTON_ROJO   = "#D32F2F"
        COLOR_TEXTO_BLANCO = "#FFFFFF"
        COLOR_TEXTO_NEGRO  = "#000000"

        self.configure(bg=COLOR_FONDO_APP)

        self.master.update_idletasks()
        ancho_ventana = self.master.winfo_width()
        alto_ventana = self.master.winfo_height()

        ALTURA_BASE = 720.0 
        self.escala = alto_ventana / ALTURA_BASE 

        def s(valor):
            return int(valor * self.escala)

        f_welcome_t   = ("Arial", s(12))
        f_welcome_n   = ("Arial", s(20), "bold")
        f_btn_nav     = ("Arial", s(13))
        f_label_chart = ("Arial", s(15), "bold")

        w_logo, h_logo   = s(70), s(70)
        w_chart, h_chart = s(480), s(300)

        p_card_x = s(40)
        p_card_y = s(30)
        p_gap    = s(10)
        btn_ipad_y = s(8) 

        card = Frame(self, bg=COLOR_BLANCO)
        card.place(relx=0.5, rely=0.5, relwidth=0.92, relheight=0.92, anchor=CENTER)

        card.columnconfigure(0, weight=30) 
        card.columnconfigure(1, weight=70) 
        card.rowconfigure(0, weight=1)

        # ==========================================
        # MENU IZQUIERDO
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
        self.lbl_nombre = Label(frame_textos, text="[username]", bg=COLOR_HEADER_ROJO, fg=COLOR_TEXTO_BLANCO, font=f_welcome_n, anchor="w")
        self.lbl_nombre.pack(fill=X)

        frame_nav_top = Frame(frame_left, bg=COLOR_BLANCO)
        frame_nav_top.pack(side=TOP, fill=X)

        btn_ventas = Button(frame_nav_top, text="View Sales", 
                     bg=COLOR_BOTON_AZUL, fg=COLOR_TEXTO_BLANCO,
                     font=f_btn_nav, relief="flat", cursor="hand2",
                     command=lambda: self.controlador.mostrar_pantalla("mainventas"))
        btn_ventas.pack(fill=X, pady=s(12), ipady=btn_ipad_y)

        btn_productos = Button(frame_nav_top, text="View Ingredients", 
                     bg=COLOR_BOTON_AZUL, fg=COLOR_TEXTO_BLANCO,
                     font=f_btn_nav, relief="flat", cursor="hand2",
                     command=lambda: self.controlador.mostrar_pantalla("productos_main"))
        btn_productos.pack(fill=X, pady=s(12), ipady=btn_ipad_y)

        btn_prov = Button(frame_nav_top, text="View Suppliers", 
                     bg=COLOR_BOTON_AZUL, fg=COLOR_TEXTO_BLANCO,
                     font=f_btn_nav, relief="flat", cursor="hand2",
                     command=lambda: self.controlador.mostrar_pantalla("proveedores_main"))
        btn_prov.pack(fill=X, pady=s(12), ipady=btn_ipad_y)

        self.btn_usuarios = Button(frame_nav_top, text="View Users", 
            bg=COLOR_BOTON_AZUL, fg=COLOR_TEXTO_BLANCO,
            font=f_btn_nav, relief="flat", cursor="hand2",
            command=lambda: self.controlador.mostrar_pantalla("usuarios_main")) 
        
        btn_logout = Button(frame_left, text="Log Out", 
                            bg=COLOR_BOTON_ROJO, fg=COLOR_TEXTO_BLANCO,
                            font=f_btn_nav, relief="flat", cursor="hand2",
                            command=lambda: self.controlador.mostrar_pantalla("Login"))
        btn_logout.pack(side=BOTTOM, fill=X, ipady=btn_ipad_y)


        # ==========================================
        # DASHBOARD DERECHO
        # ==========================================
        frame_right = Frame(card, bg=COLOR_BLANCO)
        frame_right.grid(row=0, column=1, sticky="nsew", padx=(s(20), p_card_x), pady=p_card_y)

        area_grafico = Frame(frame_right, bg=COLOR_BLANCO)
        area_grafico.pack(fill=BOTH, expand=True)

        self.img_chart = obtener_imagen("grafico_ingresos_Weekly.png", w_chart, h_chart)

        contenedor_img = Frame(area_grafico, bg=COLOR_BLANCO)
        contenedor_img.pack(expand=True) 

        if self.img_chart:
            lbl_chart = Label(contenedor_img, image=self.img_chart, bg=COLOR_BLANCO)
            lbl_chart.pack(pady=(0, s(15)))
        else:
            Label(contenedor_img, text="[ Chart ]", bg="#eee", 
                  width=int(50*self.escala), height=int(15*self.escala)).pack()

        Label(contenedor_img, text="Weekly Sales", bg=COLOR_BLANCO, 
              fg=COLOR_TEXTO_NEGRO, font=f_label_chart).pack()


    def actualizar_info_usuario(self, nombre, rol):
        self.lbl_nombre.config(text=nombre)
        s = self.escala 
        btn_ipad_y = int(8 * s)

        if rol == "Admin":
            self.lbl_nombre.config(fg="#FFD700")  
            self.btn_usuarios.pack(fill=X, pady=int(12*s), ipady=btn_ipad_y)
        else:
            self.lbl_nombre.config(fg="#000000")
            self.btn_usuarios.pack_forget()


class App(Tk): 
    def __init__(self):
        super().__init__()
        self.title("Inventory and Sales System")
        self.state('zoomed')
        self.geometry("1024x720")

        self.rol_actual = None 
        self.pantallas = {} 

        self.pantallas["Login"] = Login(self, self)
        self.pantallas["Dashboard"] = Dashboard(self, self)
        self.pantallas["plantilla"] = Plantilla(self,self)
        self.pantallas["usuarios_main"] = UsuariosMain(self, self)
        self.pantallas["usuarios_insertar"] = UsuariosInsertar(self, self)

        self.pantallas["productos_main"] = ProductosMain(self, self)
        self.pantallas["productos_actualizar"] = ProductosActualizar(self, self)
        self.pantallas["productos_eliminar"] = ProductosEliminar(self, self)

        self.pantallas["proveedores_main"] = ProveedoresMain(self, self)
        self.pantallas["proveedores_insertar"] = ProveedoresInsertar(self, self)
        self.pantallas["proveedores_actualizar"] = ProveedoresActualizar(self, self)
        self.pantallas["proveedores_eliminar"] = ProveedoresEliminar(self, self)

        self.pantallas["menu_crud"] = ventanaMenu(self, self)

        self.crear_menu_atajos()
        self.mostrar_pantalla("Login")


    def mostrar_pantalla(self, nombre,parametro=None): 
        for pantalla in self.pantallas.values():
            pantalla.pack_forget()
        if nombre == "Login":
            self.config(menu=Menu(self))
        else:
            self.config(menu=self.menubar)

        match nombre:
            case "mainventas":
                self.pantallas["mainventas"] = mainVentas(self,self)
            case "insertarventas":
                self.pantallas["insertarventas"] = insertarVentas(self,self,"agregar")
            case "actualizarventas":
                self.pantallas["actualizarventas"] = insertarVentas(self,self,"actualizar",parametro)
            case "productos_insertar":
                self.pantallas["productos_insertar"] = ProductosInsertar(self, self)
        self.pantallas[nombre].pack(expand=True, fill="both")

    def ingresar(self, nombre_usuario, rol):
            self.rol_actual = rol
            self.crear_menu_atajos()  

            if "Dashboard" in self.pantallas:
                dashboard = self.pantallas["Dashboard"]
                dashboard.actualizar_info_usuario(nombre_usuario, rol)
                self.mostrar_pantalla("Dashboard")

    def crear_menu_atajos(self):
            COLOR_FONDO_MENU = "#F7F7F7"   
            COLOR_LETRA = "#000000"        
            COLOR_ACTIVO = "#B3B3B3"       
            FUENTE_MENU = ("Arial", 13) 

            config_menu = {
                "bg": COLOR_FONDO_MENU,
                "fg": COLOR_LETRA,
                "activebackground": COLOR_ACTIVO,
                "activeforeground": COLOR_LETRA,
                "font": FUENTE_MENU,
                "tearoff": 0,
                "bd": 0
            }

            self.menubar = Menu(self, bg=COLOR_FONDO_MENU, fg=COLOR_LETRA, font=FUENTE_MENU, bd=0)

            # 1. ATAJOS
            atajos_menu = Menu(self.menubar, **config_menu)
            self.menubar.add_cascade(label="  🏠 QUICK LINKS  ", menu=atajos_menu)
            
            atajos_menu.add_command(label="🏠 Go to Dashboard", command=lambda: self.mostrar_pantalla("Dashboard"))
            atajos_menu.add_separator()
            atajos_menu.add_command(label="🚪 Log Out", command=lambda: self.mostrar_pantalla("Login"))

            # 2. VENTAS
            ventas_menu = Menu(self.menubar, **config_menu)
            self.menubar.add_cascade(label="  💰 SALES  ", menu=ventas_menu)
            
            ventas_menu.add_command(label="📄 Manage Sales", command=lambda: self.mostrar_pantalla("mainventas"))
            ventas_menu.add_command(label="➕ New Sale", command=lambda: self.mostrar_pantalla("insertarventas"))
            ventas_menu.add_separator()
            ventas_menu.add_command(label="💲 Modify Prices", command=lambda: self.mostrar_pantalla("menu_crud"))

            # 3. PRODUCTOS
            prod_menu = Menu(self.menubar, **config_menu)
            self.menubar.add_cascade(label="  🍔 INGREDIENTS  ", menu=prod_menu)
            
            prod_menu.add_command(label="📦 View Inventory", command=lambda: self.mostrar_pantalla("productos_main"))
            prod_menu.add_command(label="➕ Add Ingredient", command=lambda: self.mostrar_pantalla("productos_insertar"))

            # 4. PROVEEDORES
            prov_menu = Menu(self.menubar, **config_menu)
            self.menubar.add_cascade(label="  🚚 SUPPLIERS  ", menu=prov_menu)
            
            prov_menu.add_command(label="📋 View Suppliers", command=lambda: self.mostrar_pantalla("proveedores_main"))
            prov_menu.add_command(label="➕ Add Supplier", command=lambda: self.mostrar_pantalla("proveedores_insertar"))

            # 5. USUARIOS
            if self.rol_actual == "Admin":
                user_menu = Menu(self.menubar, **config_menu)
                self.menubar.add_cascade(label="  👥 USERS  ", menu=user_menu)
                user_menu.add_command(label="🔑 Manage Users", command=lambda: self.mostrar_pantalla("usuarios_main"))
                user_menu.add_command(label="➕ Create New User", command=lambda: self.mostrar_pantalla("usuarios_insertar"))
            
            if self.master: 
                try:
                    self.config(menu=self.menubar)
                except:
                    pass


if __name__ == "__main__":
    app = App()
    app.mainloop()