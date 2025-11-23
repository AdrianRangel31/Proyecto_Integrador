from tkinter import *
from tkinter import ttk, messagebox
import os
import sys

# Rutas para importar modelos y controladores
ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(ruta_raiz)

from model.usuariosCRUD import Usuarios
from controller.funciones import obtener_imagen

# --- COLORES BASADOS EN LA IMAGEN ---
COLOR_ROJO_INTENSO = "#D32F2F"  # Fondo general
COLOR_ROJO_HEADER = "#FF3333"   # Header un poco más claro
COLOR_BOTON_AZUL = "#5DADE2"    # Botones inferiores
COLOR_BLANCO = "#FFFFFF"

# --- FUENTES ---
FONT_TITLE = ("Arial", 28, "bold")
FONT_TABLE_HEAD = ("Arial", 14, "bold")
FONT_TABLE_BODY = ("Arial", 12)
FONT_BTN = ("Arial", 14, "bold")

class EstiloUsuarios(Frame):
    def __init__(self, master, controlador, titulo):
        super().__init__(master)
        self.controlador = controlador
        self.configure(bg=COLOR_ROJO_INTENSO)
        
        # --- HEADER (IGUAL A LA IMAGEN) ---
        header = Frame(self, bg=COLOR_ROJO_HEADER, height=120)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Logo Izquierda
        self.img_logo = obtener_imagen("logo.png", 100, 100)
        if self.img_logo:
            Label(header, image=self.img_logo, bg=COLOR_ROJO_HEADER).pack(side="left", padx=20)
        
        # Icono Home (Casa)
        lbl_home = Label(header, text="🏠", font=("Arial", 30), bg=COLOR_ROJO_HEADER, fg="white", cursor="hand2")
        lbl_home.pack(side="left", padx=10)
        lbl_home.bind("<Button-1>", lambda e: controlador.mostrar_pantalla("Dashboard"))

        # Titulo Centrado
        Label(header, text=titulo, font=FONT_TITLE, bg=COLOR_ROJO_HEADER, fg="white").pack(side="right", padx=50, fill="y")
        # Nota: Usamos pack side right o expand para centrar visualmente según preferencia, 
        # en la imagen el titulo "Usuarios" está bastante centrado/derecha.

# ==========================================================
# PANTALLA PRINCIPAL: TABLA DE USUARIOS
# ==========================================================
class UsuariosMain(EstiloUsuarios):
    def __init__(self, master, controlador):
        super().__init__(master, controlador, "Usuarios")

        # Contenedor principal centrado
        main_frame = Frame(self, bg=COLOR_ROJO_INTENSO)
        main_frame.pack(expand=True, fill="both", padx=40, pady=20)

        # --- TABLA BLANCA ---
        # Simulamos el borde azulado de la imagen poniendo un frame
        border_frame = Frame(main_frame, bg="#4A90E2", bd=2)
        border_frame.pack(expand=True, fill="both", pady=(0, 20))

        scroll = Scrollbar(border_frame)
        scroll.pack(side="right", fill="y")

        # Columnas: ID oculto, Nombre, Apellidos, Correo, Contraseña (simulada)
        cols = ("ID", "Nombre", "Apellidos", "Correo", "Pass")
        self.tree = ttk.Treeview(border_frame, columns=cols, show="headings", yscrollcommand=scroll.set)

        # Estilo de la tabla
        style = ttk.Style()
        style.configure("Treeview", font=FONT_TABLE_BODY, rowheight=40)
        style.configure("Treeview.Heading", font=FONT_TABLE_HEAD, background="#B01E2D", foreground="black")

        # Configuración de columnas
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=0, stretch=NO) # Ocultamos ID
        
        self.tree.heading("Nombre", text="Nombre")
        self.tree.column("Nombre", width=150, anchor="center")
        
        self.tree.heading("Apellidos", text="Apellidos")
        self.tree.column("Apellidos", width=150, anchor="center")
        
        self.tree.heading("Correo", text="Correo")
        self.tree.column("Correo", width=200, anchor="center")
        
        self.tree.heading("Pass", text="Contraseña")
        self.tree.column("Pass", width=150, anchor="center")

        self.tree.pack(expand=True, fill="both")
        scroll.config(command=self.tree.yview)
        
        # Evento Doble Clic para Editar (Simula el lápiz)
        self.tree.bind("<Double-1>", self.ir_a_actualizar)

        # --- BOTONES INFERIORES (AZULES REDONDEADOS) ---
        btn_frame = Frame(main_frame, bg=COLOR_ROJO_INTENSO)
        btn_frame.pack(fill="x", pady=10)

        # Centrar botones
        btn_container = Frame(btn_frame, bg=COLOR_ROJO_INTENSO)
        btn_container.pack(anchor="center")

        btn_opts = {
            "bg": COLOR_BOTON_AZUL, "fg": "white", 
            "font": FONT_BTN, "width": 15, "bd": 0, 
            "cursor": "hand2", "relief": "flat"
        }

        # Botón Añadir
        btn_add = Button(btn_container, text="Añadir", command=lambda: controlador.mostrar_pantalla("usuarios_insertar"), **btn_opts)
        btn_add.pack(side="left", padx=20, ipady=5)

        # Botón Eliminar
        btn_del = Button(btn_container, text="Eliminar", command=self.eliminar_usuario, **btn_opts)
        btn_del.pack(side="left", padx=20, ipady=5)

        # Botón Refrescar (Opcional, pequeño)
        Button(btn_frame, text="↻", command=self.cargar_datos, bg=COLOR_ROJO_INTENSO, fg="white", font=("Arial", 12, "bold"), bd=0).place(x=0, y=0)

        self.cargar_datos()

    def cargar_datos(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener datos
        usuarios = Usuarios.buscar()
        for u in usuarios:
            # u = (id, nombre, apellido, correo, pass)
            # Mostramos asteriscos en la contraseña por seguridad
            fila_visual = (u[0], u[1], u[2], u[3], "********") 
            self.tree.insert("", "end", values=fila_visual)

    def ir_a_actualizar(self, event=None):
        seleccion = self.tree.focus()
        if seleccion:
            valores = self.tree.item(seleccion, "values")
            # Enviamos los datos a la pantalla de insertar/actualizar
            pantalla = self.controlador.pantallas["usuarios_insertar"]
            pantalla.preparar_actualizacion(valores)
            self.controlador.mostrar_pantalla("usuarios_insertar")

    def eliminar_usuario(self):
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un usuario de la lista para eliminar.")
            return
        
        valores = self.tree.item(seleccion, "values")
        id_user = valores[0]
        nombre = valores[1]

        confirmar = messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar al usuario '{nombre}'?")
        if confirmar:
            if Usuarios.eliminar(id_user):
                messagebox.showinfo("Éxito", "Usuario eliminado.")
                self.cargar_datos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario.")


# ==========================================================
# PANTALLA FORMULARIO (INSERTAR / ACTUALIZAR)
# ==========================================================
class UsuariosInsertar(EstiloUsuarios):
    def __init__(self, master, controlador):
        super().__init__(master, controlador, "Gestión Usuario")
        self.modo = "insertar"
        self.id_usuario_actual = None

        container = Frame(self, bg=COLOR_ROJO_INTENSO)
        container.pack(expand=True)

        # Variables
        self.nombre = StringVar()
        self.apellidos = StringVar()
        self.correo = StringVar()
        self.password = StringVar()

        # Diseño del formulario
        lbl_style = {"bg": COLOR_ROJO_INTENSO, "fg": "white", "font": ("Arial", 14, "bold"), "anchor": "w"}
        entry_style = {"font": ("Arial", 12), "width": 30}

        Label(container, text="Nombre:", **lbl_style).grid(row=0, column=0, pady=10, padx=10, sticky="w")
        Entry(container, textvariable=self.nombre, **entry_style).grid(row=0, column=1, pady=10, ipady=5)

        Label(container, text="Apellidos:", **lbl_style).grid(row=1, column=0, pady=10, padx=10, sticky="w")
        Entry(container, textvariable=self.apellidos, **entry_style).grid(row=1, column=1, pady=10, ipady=5)

        Label(container, text="Correo:", **lbl_style).grid(row=2, column=0, pady=10, padx=10, sticky="w")
        Entry(container, textvariable=self.correo, **entry_style).grid(row=2, column=1, pady=10, ipady=5)

        Label(container, text="Contraseña:", **lbl_style).grid(row=3, column=0, pady=10, padx=10, sticky="w")
        self.ent_pass = Entry(container, textvariable=self.password, show="*", **entry_style)
        self.ent_pass.grid(row=3, column=1, pady=10, ipady=5)
        
        self.lbl_aviso_pass = Label(container, text="(Dejar vacía para mantener la actual)", bg=COLOR_ROJO_INTENSO, fg="#FFDDDD", font=("Arial", 9))
        self.lbl_aviso_pass.grid(row=4, column=1, sticky="w")
        self.lbl_aviso_pass.grid_remove() # Se oculta por defecto

        # Botones
        btn_frame = Frame(self, bg=COLOR_ROJO_INTENSO)
        btn_frame.pack(pady=30)

        Button(btn_frame, text="Guardar", command=self.guardar, bg=COLOR_BOTON_AZUL, fg="white", font=FONT_BTN, width=15).pack(side="left", padx=10)
        Button(btn_frame, text="Cancelar", command=self.cancelar, bg="#555", fg="white", font=FONT_BTN, width=15).pack(side="left", padx=10)

    def preparar_actualizacion(self, valores):
        """Llama esto antes de mostrar la pantalla para modo editar"""
        self.modo = "actualizar"
        self.id_usuario_actual = valores[0]
        self.nombre.set(valores[1])
        self.apellidos.set(valores[2])
        self.correo.set(valores[3])
        self.password.set("") # Contraseña limpia
        self.lbl_aviso_pass.grid() # Mostrar aviso

    def cancelar(self):
        self.limpiar()
        self.controlador.mostrar_pantalla("usuarios_main")

    def limpiar(self):
        self.modo = "insertar"
        self.id_usuario_actual = None
        self.nombre.set("")
        self.apellidos.set("")
        self.correo.set("")
        self.password.set("")
        self.lbl_aviso_pass.grid_remove()

    def guardar(self):
        nom = self.nombre.get()
        ape = self.apellidos.get()
        mail = self.correo.get()
        pwd = self.password.get()

        if not nom or not ape or not mail:
            messagebox.showwarning("Datos incompletos", "Nombre, Apellidos y Correo son obligatorios.")
            return

        if self.modo == "insertar":
            if not pwd:
                messagebox.showwarning("Error", "La contraseña es obligatoria para nuevos usuarios.")
                return
            if Usuarios.insertar(nom, ape, mail, pwd):
                messagebox.showinfo("Éxito", "Usuario creado correctamente.")
                self.limpiar()
                self.controlador.pantallas["usuarios_main"].cargar_datos()
                self.controlador.mostrar_pantalla("usuarios_main")
        
        elif self.modo == "actualizar":
            # Si pwd esta vacio, el CRUD sabe que no debe actualizarla
            if Usuarios.actualizar(self.id_usuario_actual, nom, ape, mail, pwd):
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
                self.limpiar()
                self.controlador.pantallas["usuarios_main"].cargar_datos()
                self.controlador.mostrar_pantalla("usuarios_main")