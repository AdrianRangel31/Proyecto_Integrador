from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import sys
try:
    from view.header import header 
except ImportError:
    from tkinter import Frame as header 


ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(ruta_raiz)

from model.proveedoresCRUD import Proveedores
from controller.funciones import obtener_imagen

COLOR_HEADER = "#FF3333"
COLOR_FONDO = "#B71C1C"
COLOR_BOTON = "#5DADE2"
COLOR_TEXTO_LBL = "#5DADE2"
COLOR_BLANCO = "#FFFFFF"

FONT_TITLE = ("Arial", 28, "bold")       
FONT_LABEL = ("Arial", 14, "bold")       
FONT_INPUT = ("Arial", 14)               
FONT_BTN = ("Arial", 14, "bold")         
FONT_TABLE = ("Arial", 13)               

class EstiloBase(Frame):
    def __init__(self, master, controlador, titulo):
        super().__init__(master)
        self.controlador = controlador
        self.configure(bg=COLOR_FONDO)
        
        try:
            self.encabezado = header(self, controlador)
            self.encabezado.pack(side="top", fill="x")
            self.encabezado.titulo = titulo
        except Exception:
            Label(self, text=titulo, bg=COLOR_FONDO, fg="white", font=("Arial", 24)).pack(pady=10)

class ProveedoresMain(EstiloBase):
    def __init__(self, master, controlador):
        super().__init__(master, controlador, "SUPPLIERS MANAGEMENT")
        
        frame_tabla = Frame(self, bg="white")
        frame_tabla.pack(expand=True, fill="both", padx=30, pady=30)

        scroll = Scrollbar(frame_tabla)
        scroll.pack(side="right", fill="y")

        cols = ("ID", "Company", "Contact", "Phone", "Address")
        self.tree = ttk.Treeview(frame_tabla, columns=cols, show="headings", yscrollcommand=scroll.set)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Arial", 14), rowheight=35, background="white", fieldbackground="white")
        style.configure("Treeview.Heading", background="#4A90E2", foreground="white",
                        font=("Arial", 16, "bold"), relief="flat")
        style.map("Treeview.Heading", background=[("active", "#357ABD")])

        anchos = [60, 220, 160, 140, 280]
        for col, ancho in zip(cols, anchos):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho, anchor="center" if col == "ID" else "w")
        
        self.tree.pack(expand=True, fill="both")
        scroll.config(command=self.tree.yview)

        frame_botones = Frame(self, bg=COLOR_FONDO)
        frame_botones.pack(fill="x", pady=20, padx=40)

        btn_opts = {
            "bg": COLOR_BOTON, "fg": "white", 
            "font": FONT_BTN, "width": 18,      
            "bd": 0, "cursor": "hand2"
        }

        Button(frame_botones, text="Add", command=lambda: controlador.mostrar_pantalla("proveedores_insertar"), **btn_opts).pack(side="left", padx=15, ipady=10)
        Button(frame_botones, text="Update", command=self.ir_a_actualizar, **btn_opts).pack(side="left", padx=15, ipady=10)
        Button(frame_botones, text="Delete", command=self.ir_a_eliminar, **btn_opts).pack(side="left", padx=15, ipady=10)
        Button(frame_botones, text="Refresh", command=self.cargar_datos, **btn_opts).pack(side="right", padx=15, ipady=10)

        self.cargar_datos()

    def cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        datos = Proveedores.buscar()
        for fila in datos:
            self.tree.insert("", "end", values=fila)

    def ir_a_actualizar(self):
        seleccion = self.tree.focus()
        if seleccion:
            valores = self.tree.item(seleccion, "values")
            pantalla_act = self.controlador.pantallas["proveedores_actualizar"]
            pantalla_act.cargar_datos_formulario(valores)
            self.controlador.mostrar_pantalla("proveedores_actualizar")
        else:
            messagebox.showwarning("Notice", "Select a supplier to update")

    def ir_a_eliminar(self):
        seleccion = self.tree.focus()
        if seleccion:
            valores = self.tree.item(seleccion, "values")
            pantalla_eli = self.controlador.pantallas["proveedores_eliminar"]
            pantalla_eli.cargar_datos_vista(valores)
            self.controlador.mostrar_pantalla("proveedores_eliminar")
        else:
            messagebox.showwarning("Notice", "Select a supplier to delete")

class ProveedoresInsertar(EstiloBase):
    def __init__(self, master, controlador, modo="insertar"):
        titulo = "ADD SUPPLIER" if modo == "insertar" else "UPDATE SUPPLIER"
        super().__init__(master, controlador, titulo)
        self.modo = modo
        self.id_proveedor_actual = None 

        cuerpo = Frame(self, bg=COLOR_FONDO)
        cuerpo.pack(expand=True, fill="both", padx=30, pady=20)

        form_frame = Frame(cuerpo, bg=COLOR_FONDO)
        form_frame.place(relx=0.15, rely=0.05, relwidth=0.7, relheight=0.9)

        self.vars = {
            "nombre": StringVar(), 
            "contacto": StringVar(),
            "telefono": StringVar(), 
            "direccion": StringVar()
        }

        campos = [
            ("Company Name", "nombre"), 
            ("Contact Name", "contacto"),
            ("Phone", "telefono"),
            ("Address", "direccion")
        ]

        for idx, (lbl_text, var_key) in enumerate(campos):
            Label(form_frame, text=lbl_text, bg=COLOR_TEXTO_LBL, fg="black", 
                font=FONT_LABEL, width=40, anchor="w", padx=10).pack(pady=(10, 5), anchor="w")
            
            Entry(form_frame, textvariable=self.vars[var_key], width=45, font=FONT_INPUT).pack(pady=0, ipady=12, anchor="w", padx=5)

        btn_frame = Frame(self, bg=COLOR_FONDO)
        btn_frame.pack(side="bottom", pady=30)
        
        btn_opts = {"font": FONT_BTN, "width": 18, "bd": 0, "cursor": "hand2"}

        txt_confirmar = "SAVE" if modo == "insertar" else "UPDATE"
        Button(btn_frame, text=txt_confirmar, command=self.guardar, bg=COLOR_BOTON, fg="white", **btn_opts).pack(side="left", padx=15, ipady=10)
        Button(btn_frame, text="CLEAR", command=self.limpiar, bg="gray", fg="white", **btn_opts).pack(side="left", padx=15, ipady=10)
        Button(btn_frame, text="BACK", command=lambda: controlador.mostrar_pantalla("proveedores_main"), bg=COLOR_BOTON, fg="white", **btn_opts).pack(side="left", padx=15, ipady=10)

    def limpiar(self):
        for key in self.vars:
            self.vars[key].set("")

    def guardar(self):
        if not self.vars["nombre"].get():
            messagebox.showwarning("Error", "Company Name is required")
            return

        datos = [
            self.vars["nombre"].get(), 
            self.vars["contacto"].get(),
            self.vars["telefono"].get(),
            self.vars["direccion"].get()
        ]
        
        if self.modo == "insertar":
            if Proveedores.insertar(*datos):
                messagebox.showinfo("Success", "Supplier added successfully")
                self.limpiar()
                self.controlador.pantallas["proveedores_main"].cargar_datos()
        else:
            if Proveedores.actualizar(self.id_proveedor_actual, *datos):
                messagebox.showinfo("Success", "Supplier updated successfully")
                self.controlador.mostrar_pantalla("proveedores_main")
                self.controlador.pantallas["proveedores_main"].cargar_datos()


class ProveedoresActualizar(ProveedoresInsertar):
    def __init__(self, master, controlador):
        super().__init__(master, controlador, modo="actualizar")

    def cargar_datos_formulario(self, valores):
        self.id_proveedor_actual = valores[0]
        self.vars["nombre"].set(valores[1])
        self.vars["contacto"].set(valores[2])
        self.vars["telefono"].set(valores[3])
        self.vars["direccion"].set(valores[4])


class ProveedoresEliminar(EstiloBase):
    def __init__(self, master, controlador):
        super().__init__(master, controlador, "DELETE SUPPLIER")
        self.id_a_eliminar = None

        cuerpo = Frame(self, bg=COLOR_FONDO)
        cuerpo.pack(expand=True, fill="both", padx=50, pady=50)

        Label(cuerpo, text="Are you sure you want to delete this supplier?", 
            bg=COLOR_FONDO, fg="white", font=("Arial", 20, "bold")).pack(pady=30)

        self.lbl_info = Label(cuerpo, text="", bg="#900C0C", fg="white", font=("Arial", 18), padx=20, pady=20)
        self.lbl_info.pack(pady=10, fill="x")

        btn_frame = Frame(cuerpo, bg=COLOR_FONDO)
        btn_frame.pack(pady=40)

        btn_opts = {"font": FONT_BTN, "width": 20, "bd": 0, "cursor": "hand2"}

        Button(btn_frame, text="CONFIRM DELETION", bg="red", fg="white", 
            command=self.confirmar_eliminar, **btn_opts).pack(side="left", padx=20, ipady=10)
        
        Button(btn_frame, text="Cancel / Back", bg=COLOR_BOTON, fg="white", 
            command=lambda: controlador.mostrar_pantalla("proveedores_main"), **btn_opts).pack(side="left", padx=20, ipady=10)

    def cargar_datos_vista(self, valores):
        self.id_a_eliminar = valores[0]
        texto = f"ID: {valores[0]}\nCompany: {valores[1]}\nContact: {valores[2]}"
        self.lbl_info.config(text=texto)

    def confirmar_eliminar(self):
        if self.id_a_eliminar:
            if Proveedores.eliminar(self.id_a_eliminar):
                messagebox.showinfo("Deleted", "Supplier deleted successfully.")
                self.controlador.pantallas["proveedores_main"].cargar_datos()
                self.controlador.mostrar_pantalla("proveedores_main")