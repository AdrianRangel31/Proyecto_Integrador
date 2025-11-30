from tkinter import *
from view.header import *
from model.usuariosCRUD import *
#Plantilla para realizar interfaces. Seguir la siguiente estructura para las clases principales

class Login(Frame):
    def __init__(self, master, controlador):
        super().__init__(master)
        self.controlador = controlador

        # 1. Forzamos a Tkinter a procesar la geometría de la ventana
        self.master.update_idletasks()

        ancho_ventana = self.master.winfo_width()
        alto_ventana = self.master.winfo_height()

        # Definimos nuestra altura de diseño base
        ALTURA_BASE = 720.0 
        
        # Calculamos el factor de escala
        escala = alto_ventana / ALTURA_BASE 
        
        # --- 2. Aplicar Escala a todos los Tamaños ---
        
        # Tamaños de Frames
        frame_w = int(680 * escala)
        frame_h = int(350 * escala)
        
        # Tamaños de Imagen
        logo_w = int(300 * escala)
        logo_h = int(300 * escala)
        
        # Tamaños de Fuentes
        font_titulo = ("Arial", int(18 * escala), "bold")
        font_label = ("Arial", int(10 * escala)) # Fuente para "Correo:", "Contraseña:"
        font_entry = ("Arial", int(12 * escala))
        font_boton = ("Arial", int(12 * escala), "bold")

        # Tamaños de Padding (espaciado)
        p_frame = int(20 * escala)      # Padding del marco login
        p_logo_x = int(10 * escala)     # Padding X del logo
        p_titulo_y_top = int(20 * escala)
        p_titulo_y_bot = int(15 * escala)
        p_label_y = int(10 * escala)
        p_entry_y = int(5 * escala)
        p_entry_x = int(10 * escala)
        p_boton_y = int(20 * escala)

        self.imagen_fondo = obtener_imagen("fondo.jpg", ancho_ventana, alto_ventana) 
        fondo_label = Label(self, image=self.imagen_fondo)
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Capa 2: Marco de Login
        frame_login = Frame(self, width=frame_w, height=frame_h, bg="#F82A3E") 
        frame_login.pack_propagate(False)
        frame_login.place(relx=0.5, rely=0.5, anchor='center')

        # Capa 3: Contenido de 'frame_login'
        frame_izquierda = Frame(frame_login, bg="#F82A3E")
        frame_izquierda.pack(side=LEFT, fill="y", padx=p_frame, pady=p_frame)

        frame_derecha = Frame(frame_login, bg="#F82A3E")
        frame_derecha.pack(side=LEFT, fill="both", expand=True, padx=p_frame, pady=p_frame)

        # Rellenar Frame Izquierda (Logo)
        self.imagen_logo = obtener_imagen("logo.png", logo_w, logo_h) 
        label_logo = Label(frame_izquierda, image=self.imagen_logo, bg="#F82A3E")
        label_logo.pack(padx=p_logo_x) 

        # Rellenar Frame Derecha (Formulario)
        label_titulo = Label(frame_derecha, text="Iniciar sesión", bg="#F82A3E", 
                             fg="white", font=font_titulo)
        label_titulo.pack(pady=(p_titulo_y_top, p_titulo_y_bot)) 

        label_correo = Label(frame_derecha, text="Correo:", bg="#F82A3E", 
                             fg="white", font=font_label)
        label_correo.pack(pady=(p_label_y, 0), anchor="w") 
        
        self.email = StringVar()
        self.entry_correo = Entry(frame_derecha, textvariable=self.email , width=30, font=font_entry)
        self.entry_correo.pack(pady=p_entry_y, padx=p_entry_x, fill="x") 

        label_pass = Label(frame_derecha, text="Contraseña:", bg="#F82A3E", 
                           fg="white", font=font_label)
        label_pass.pack(pady=(p_label_y, 0), anchor="w")
        
        self.password = StringVar()
        self.entry_pass = Entry(frame_derecha, textvariable=self.password , width=30, font=font_entry, show="*")
        self.entry_pass.pack(pady=p_entry_y, padx=p_entry_x, fill="x")

        boton_iniciar = Button(frame_derecha, text="Iniciar sesión", 
                               font=font_boton, bg="#333", fg="white", command= self.validar_campos) 
        boton_iniciar.pack(pady=p_boton_y, fill="x", padx=p_entry_x)

    def validar_campos(self):
        
        correo = self.entry_correo.get()
        password = self.entry_pass.get()

        if not correo or not password:
            messagebox.showwarning(title="Advertencia", icon="warning", message="Por favor llene todos los campos")
            return
        
        self.verificar(correo,password)

    def verificar(self,correo,password):
        registro = Usuarios.iniciar_sesion(correo,password)
        if registro:
            username = registro[1]
            rol = registro[7]
            print("Rol del usuario:", rol)

            self.entry_correo.delete(0, END)
            self.entry_pass.delete(0, END)

            self.controlador.ingresar(username,rol)
        else:
            messagebox.showerror("Error","Usuario o contraseña incorrectos")
