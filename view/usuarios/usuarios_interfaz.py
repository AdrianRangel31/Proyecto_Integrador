from tkinter import *
from tkinter import ttk, messagebox
import os
import sys

# --- IMPORTS DE RUTAS ---
ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(ruta_raiz)

from model.usuariosCRUD import Usuarios
from controller.funciones import obtener_imagen
from view.header import header

# --- CONSTANTES DE ESTILO ---
COLOR_FONDO = "#B71C1C"      
COLOR_BLANCO = "#FFFFFF"
COLOR_BOTON_AZUL = "#5DADE2" 
COLOR_BOTON_ROJO = "#D32F2F" 
COLOR_TEXTO_LBL = "#5DADE2"  

FONT_TITLE = ("Arial", 24, "bold")       
FONT_LABEL = ("Arial", 12, "bold")       
FONT_INPUT = ("Arial", 12)               
FONT_BTN = ("Arial", 12, "bold")        
FONT_TABLE = ("Arial", 11)

class EstiloBase(Frame):
    def __init__(self, master, controlador, titulo):
        super().__init__(master)
        self.controlador = controlador
        self.configure(bg=COLOR_FONDO)
        
        self.encabezado = header(self, controlador)
        self.encabezado.pack(side="top", fill="x")
        self.encabezado.titulo = titulo

# ==========================================================
# PANTALLA 1: MAIN (TABLA DE USUARIOS)
# ==========================================================
class UsuariosMain(EstiloBase):
    def __init__(self, master, controlador):
        super().__init__(master, controlador, "Gestión de Usuarios")
        
        frame_tabla = Frame(self, bg=COLOR_BLANCO)
        frame_tabla.pack(expand=True, fill="both", padx=40, pady=30)

        scroll = Scrollbar(frame_tabla)
        scroll.pack(side="right", fill="y")

        # --- AHORA SON MÁS COLUMNAS ---
        cols = ("ID", "Nombre", "Ap_Paterno", "Ap_Materno", "Correo", "Rol")
        self.tree = ttk.Treeview(frame_tabla, columns=cols, show="headings", yscrollcommand=scroll.set)
        
        style = ttk.Style()
        style.configure("Treeview", font=FONT_TABLE, rowheight=35)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

        # Configuración de columnas
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=0, stretch=NO) 
        
        self.tree.heading("Nombre", text="Nombre")
        self.tree.column("Nombre", width=120, anchor="center")
        
        self.tree.heading("Ap_Paterno", text="Apellido Paterno")
        self.tree.column("Ap_Paterno", width=120, anchor="center")

        self.tree.heading("Ap_Materno", text="Apellido Materno")
        self.tree.column("Ap_Materno", width=120, anchor="center")
        
        self.tree.heading("Correo", text="Correo")
        self.tree.column("Correo", width=180, anchor="center")
        
        self.tree.heading("Rol", text="Rol")
        self.tree.column("Rol", width=100, anchor="center")
        
        self.tree.pack(expand=True, fill="both")
        scroll.config(command=self.tree.yview)

        self.tree.bind("<Double-1>", self.ir_a_actualizar)

        # BOTONES
        frame_botones = Frame(self, bg=COLOR_FONDO)
        frame_botones.pack(fill="x", pady=20, padx=40)
        
        container_btns = Frame(frame_botones, bg=COLOR_FONDO)
        container_btns.pack(anchor="center")

        btn_opts = {"fg": "white", "font": FONT_BTN, "width": 15, "bd": 0, "cursor": "hand2", "relief": "flat"}

        Button(container_btns, text="Añadir", bg=COLOR_BOTON_AZUL, 
               command=lambda: controlador.mostrar_pantalla("usuarios_insertar"), **btn_opts).pack(side="left", padx=10, ipady=5)
        
        Button(container_btns, text="Editar", bg="#2ECC71", 
               command=self.ir_a_actualizar, **btn_opts).pack(side="left", padx=10, ipady=5)
        
        Button(container_btns, text="Eliminar", bg=COLOR_BOTON_ROJO, 
               command=self.eliminar_usuario, **btn_opts).pack(side="left", padx=10, ipady=5)

        self.cargar_datos()
        self.bind("<Map>", self.evento_actualizar_tabla)

    def evento_actualizar_tabla(self, event):
        self.cargar_datos()

    def cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        usuarios = Usuarios.buscar()
        for u in usuarios:
            # u = (id, nombre, pat, mat, correo, rol)
            fila_visual = (u[0], u[1], u[2], u[3], u[4], u[7])
            self.tree.insert("", "end", values=fila_visual)

    def ir_a_actualizar(self, event=None):
        seleccion = self.tree.focus()
        if seleccion:
            valores = self.tree.item(seleccion, "values")
            pantalla = self.controlador.pantallas["usuarios_insertar"]
            pantalla.preparar_edicion(valores)
            self.controlador.mostrar_pantalla("usuarios_insertar")
        else:
            messagebox.showwarning("Selección", "Por favor, selecciona un usuario para editar.")

    def eliminar_usuario(self):
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un usuario para eliminar.")
            return
        
        valores = self.tree.item(seleccion, "values")
        id_user = valores[0]
        nombre = valores[1]

        confirmar = messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar a '{nombre}'?")
        if confirmar:
            if Usuarios.eliminar(id_user):
                messagebox.showinfo("Éxito", "Usuario eliminado.")
                self.cargar_datos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar.")


# ==========================================================
# PANTALLA 2: FORMULARIO (AÑADIR / EDITAR)
# ==========================================================
class UsuariosInsertar(EstiloBase):
    def __init__(self, master, controlador):
        super().__init__(master, controlador, "Registrar Usuario")
        self.modo = "insertar"
        self.id_usuario_actual = None

        cuerpo = Frame(self, bg=COLOR_FONDO)
        cuerpo.pack(expand=True, fill="both", padx=30, pady=20)

        form_frame = Frame(cuerpo, bg=COLOR_FONDO)
        form_frame.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.9)

        # Variables separadas
        self.vars = {
            "nombre": StringVar(),
            "ap_paterno": StringVar(),
            "ap_materno": StringVar(),
            "correo": StringVar(),
            "password": StringVar(),
            "rol": StringVar()
        }

        campos = [
            ("Nombre", "nombre"),
            ("Apellido Paterno", "ap_paterno"),
            ("Apellido Materno", "ap_materno"),
            ("Correo Electrónico", "correo"),
            ("Contraseña", "password"),
            ("Rol", "rol")
        ]

        for idx, (lbl_text, var_key) in enumerate(campos):
            Label(form_frame, text=lbl_text, bg=COLOR_FONDO, fg=COLOR_TEXTO_LBL, 
                  font=FONT_LABEL, anchor="w").pack(fill="x", pady=(10, 2))
            
            # Caso 1: Campo de contraseña (oculto)
            if var_key == "password":
                Entry(form_frame, textvariable=self.vars[var_key], width=30, 
                      font=FONT_INPUT, show="*").pack(fill="x", ipady=4)
            
            # Caso 2: Campo de Rol (AHORA ES UN COMBOBOX)
            elif var_key == "rol":
                combo = ttk.Combobox(form_frame, textvariable=self.vars[var_key], 
                                     values=["Admin", "Colaborador"], # Opciones solicitadas
                                     state="readonly", # Evita que escriban otra cosa
                                     font=FONT_INPUT)
                combo.pack(fill="x", ipady=4)
            
            # Caso 3: Resto de campos (texto normal)
            else:
                Entry(form_frame, textvariable=self.vars[var_key], width=30, 
                      font=FONT_INPUT).pack(fill="x", ipady=4)

        self.lbl_aviso = Label(form_frame, text="* Deja la contraseña vacía para no cambiarla", 
                               bg=COLOR_FONDO, fg="#FFCCCC", font=("Arial", 10))
        self.lbl_aviso.pack(pady=5)
        self.lbl_aviso.pack_forget()

        # BOTONES
        btn_frame = Frame(self, bg=COLOR_FONDO)
        btn_frame.pack(side="bottom", pady=30)
        
        btn_opts = {"fg": "white", "font": FONT_BTN, "width": 15, "bd": 0, "cursor": "hand2"}

        Button(btn_frame, text="GUARDAR", command=self.guardar, bg=COLOR_BOTON_AZUL, **btn_opts).pack(side="left", padx=15, ipady=5)
        Button(btn_frame, text="CANCELAR", command=self.cancelar, bg="#7F8C8D", **btn_opts).pack(side="left", padx=15, ipady=5)

    def preparar_edicion(self, valores):
        # valores = (ID, Nombre, Paterno, Materno, Correo, Rol)
        self.modo = "actualizar"
        self.id_usuario_actual = valores[0]
        
        self.vars["nombre"].set(valores[1])
        self.vars["ap_paterno"].set(valores[2])
        self.vars["ap_materno"].set(valores[3])
        self.vars["correo"].set(valores[4].strip())
        self.vars["password"].set("")
        self.vars["rol"].set(valores[5])
        
        self.encabezado.titulo = "Editar Usuario"
        self.lbl_aviso.pack()

    def limpiar(self):
        self.modo = "insertar"
        self.id_usuario_actual = None
        for key in self.vars:
            self.vars[key].set("")
        
        self.encabezado.titulo = "Registrar Usuario"
        self.lbl_aviso.pack_forget()

    def cancelar(self):
        self.limpiar()
        self.controlador.mostrar_pantalla("usuarios_main")

    def guardar(self):
        nom = self.vars["nombre"].get()
        pat = self.vars["ap_paterno"].get()
        mat = self.vars["ap_materno"].get()
        mail = self.vars["correo"].get()
        pwd = self.vars["password"].get()
        rol = self.vars["rol"].get()

        if not nom or not pat or not mail or not rol:
            messagebox.showwarning("Datos incompletos", "Nombre, Apellido Paterno, Correo y Rol son obligatorios.")
            return

        if self.modo == "insertar":
            if not pwd:
                messagebox.showwarning("Error", "La contraseña es obligatoria para nuevos usuarios.")
                return
            if Usuarios.insertar(nom, pat, mat, mail, pwd, rol):
                messagebox.showinfo("Éxito", "Usuario creado correctamente.")
                self.finalizar()
        
        elif self.modo == "actualizar":
            if Usuarios.actualizar(self.id_usuario_actual, nom, pat, mat, mail, pwd, rol):
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
                self.finalizar()

    def finalizar(self):
        self.limpiar()
        self.controlador.mostrar_pantalla("usuarios_main")
        self.controlador.pantallas["usuarios_main"].cargar_datos()