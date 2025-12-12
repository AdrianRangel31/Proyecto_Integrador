from tkinter import *
from tkinter import ttk, messagebox
import os
import sys

ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(ruta_raiz)

from model.usuariosCRUD import Usuarios
from controller.funciones import obtener_imagen
from view.header import header

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

class UsuariosMain(EstiloBase):
    def __init__(self, master, controlador):
        super().__init__(master, controlador, "User Management")
        
        frame_tabla = Frame(self, bg=COLOR_BLANCO)
        frame_tabla.pack(expand=True, fill="both", padx=40, pady=30)

        scroll = Scrollbar(frame_tabla)
        scroll.pack(side="right", fill="y")

        cols = ("ID", "Name", "Surname", "2nd Surname", "Email", "Role")
        self.tree = ttk.Treeview(frame_tabla, columns=cols, show="headings", yscrollcommand=scroll.set)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 14), rowheight=35, background="white", fieldbackground="white")
        style.configure("Treeview.Heading", background="#4A90E2", foreground="white",
                        font=("Arial", 16, "bold"), relief="flat")
        style.map("Treeview.Heading", background=[("active", "#357ABD")])

        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=0, stretch=NO) 
        
        self.tree.heading("Name", text="Name")
        self.tree.column("Name", width=120, anchor="center")
        
        self.tree.heading("Surname", text="Surname")
        self.tree.column("Surname", width=120, anchor="center")

        self.tree.heading("2nd Surname", text="Mat. Surname")
        self.tree.column("2nd Surname", width=120, anchor="center")
        
        self.tree.heading("Email", text="Email")
        self.tree.column("Email", width=180, anchor="center")
        
        self.tree.heading("Role", text="Role")
        self.tree.column("Role", width=100, anchor="center")
        
        self.tree.pack(expand=True, fill="both")
        scroll.config(command=self.tree.yview)

        self.tree.bind("<Double-1>", self.ir_a_actualizar)

        frame_botones = Frame(self, bg=COLOR_FONDO)
        frame_botones.pack(fill="x", pady=20, padx=40)
        
        container_btns = Frame(frame_botones, bg=COLOR_FONDO)
        container_btns.pack(anchor="center")

        btn_opts = {"fg": "white", "font": FONT_BTN, "width": 15, "bd": 0, "cursor": "hand2", "relief": "flat"}

        Button(container_btns, text="Add", bg=COLOR_BOTON_AZUL, 
               command=lambda: controlador.mostrar_pantalla("usuarios_insertar"), **btn_opts).pack(side="left", padx=10, ipady=5)
        
        Button(container_btns, text="Edit", bg="#2ECC71", 
               command=self.ir_a_actualizar, **btn_opts).pack(side="left", padx=10, ipady=5)
        
        Button(container_btns, text="Delete", bg=COLOR_BOTON_ROJO, 
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
            messagebox.showwarning("Selection", "Please select a user to edit.")

    def eliminar_usuario(self):
        seleccion = self.tree.focus()
        if not seleccion:
            messagebox.showwarning("Attention", "Select a user to delete.")
            return
        
        valores = self.tree.item(seleccion, "values")
        id_user = valores[0]
        nombre = valores[1]

        confirmar = messagebox.askyesno("Confirm", f"Are you sure you want to delete '{nombre}'?")
        if confirmar:
            if Usuarios.eliminar(id_user):
                messagebox.showinfo("Success", "User deleted.")
                self.cargar_datos()
            else:
                messagebox.showerror("Error", "Could not delete user.")

class UsuariosInsertar(EstiloBase):
    def __init__(self, master, controlador):
        super().__init__(master, controlador, "Register User")
        self.modo = "insertar"
        self.id_usuario_actual = None

        cuerpo = Frame(self, bg=COLOR_FONDO)
        cuerpo.pack(expand=True, fill="both", padx=30, pady=20)

        form_frame = Frame(cuerpo, bg=COLOR_FONDO)
        form_frame.place(relx=0.25, rely=0.05, relwidth=0.5, relheight=0.9)

        self.vars = {
            "nombre": StringVar(),
            "ap_paterno": StringVar(),
            "ap_materno": StringVar(),
            "correo": StringVar(),
            "password": StringVar(),
            "rol": StringVar()
        }

        campos = [
            ("Name", "nombre"),
            ("Paternal Surname", "ap_paterno"),
            ("Maternal Surname", "ap_materno"),
            ("Email", "correo"),
            ("Password", "password"),
            ("Role", "rol")
        ]

        for idx, (lbl_text, var_key) in enumerate(campos):
            Label(form_frame, text=lbl_text, bg=COLOR_FONDO, fg=COLOR_TEXTO_LBL, 
                  font=FONT_LABEL, anchor="w").pack(fill="x", pady=(10, 2))
            
            if var_key == "password":
                Entry(form_frame, textvariable=self.vars[var_key], width=30, 
                      font=FONT_INPUT, show="*").pack(fill="x", ipady=4)
            
            elif var_key == "rol":
                combo = ttk.Combobox(form_frame, textvariable=self.vars[var_key], 
                                     values=["Admin", "Colaborador"], 
                                     state="readonly", 
                                     font=FONT_INPUT)
                combo.pack(fill="x", ipady=4)
            
            else:
                Entry(form_frame, textvariable=self.vars[var_key], width=30, 
                      font=FONT_INPUT).pack(fill="x", ipady=4)

        self.lbl_aviso = Label(form_frame, text="* Leave password blank to keep current one", 
                               bg=COLOR_FONDO, fg="#FFCCCC", font=("Arial", 10))
        self.lbl_aviso.pack(pady=5)
        self.lbl_aviso.pack_forget()

        btn_frame = Frame(self, bg=COLOR_FONDO)
        btn_frame.pack(side="bottom", pady=30)
        
        btn_opts = {"fg": "white", "font": FONT_BTN, "width": 15, "bd": 0, "cursor": "hand2"}

        Button(btn_frame, text="SAVE", command=self.guardar, bg=COLOR_BOTON_AZUL, **btn_opts).pack(side="left", padx=15, ipady=5)
        Button(btn_frame, text="CANCEL", command=self.cancelar, bg="#7F8C8D", **btn_opts).pack(side="left", padx=15, ipady=5)

    def preparar_edicion(self, valores):
        self.modo = "actualizar"
        self.id_usuario_actual = valores[0]
        
        self.vars["nombre"].set(valores[1])
        self.vars["ap_paterno"].set(valores[2])
        self.vars["ap_materno"].set(valores[3])
        self.vars["correo"].set(valores[4].strip())
        self.vars["password"].set("")
        self.vars["rol"].set(valores[5])
        
        self.encabezado.titulo = "Edit User"
        self.lbl_aviso.pack()

    def limpiar(self):
        self.modo = "insertar"
        self.id_usuario_actual = None
        for key in self.vars:
            self.vars[key].set("")
        
        self.encabezado.titulo = "Register User"
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
            messagebox.showwarning("Incomplete Data", "Name, Paternal Surname, Email and Role are mandatory.")
            return

        if self.modo == "insertar":
            if not pwd:
                messagebox.showwarning("Error", "Password is mandatory for new users.")
                return
            if Usuarios.insertar(nom, pat, mat, mail, pwd, rol):
                messagebox.showinfo("Success", "User created successfully.")
                self.finalizar()
        
        elif self.modo == "actualizar":
            if Usuarios.actualizar(self.id_usuario_actual, nom, pat, mat, mail, pwd, rol):
                messagebox.showinfo("Success", "User updated successfully.")
                self.finalizar()

    def finalizar(self):
        self.limpiar()
        self.controlador.mostrar_pantalla("usuarios_main")
        self.controlador.pantallas["usuarios_main"].cargar_datos()