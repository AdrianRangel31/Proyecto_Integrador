from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import sys

# --- IMPORTS DE RUTAS (Para que encuentre model y controller) ---
# Esto asegura que Python encuentre las carpetas hermanas 'model' y 'controller'
ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(ruta_raiz)

from model.productosCRUD import Productos
from controller.funciones import obtener_imagen

# --- CONSTANTES DE ESTILO ---
COLOR_HEADER = "#FF3333"
COLOR_FONDO = "#B71C1C"
COLOR_BOTON = "#5DADE2"
COLOR_TEXTO_LBL = "#5DADE2"
COLOR_BLANCO = "#FFFFFF"
FONT_TITLE = ("Arial", 20, "bold")

class EstiloBase(Frame):
    """Clase padre para compartir el diseño del encabezado y fondo"""
    def __init__(self, master, controlador, titulo):
        super().__init__(master)
        self.controlador = controlador
        self.configure(bg=COLOR_FONDO)
        
        # --- ENCABEZADO ---
        header = Frame(self, bg=COLOR_HEADER, height=100)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # 1. LOGO (Izquierda)
        self.img_logo_small = obtener_imagen("logo.png", 80, 80)
        if self.img_logo_small:
            lbl_logo = Label(header, image=self.img_logo_small, bg=COLOR_HEADER)
            lbl_logo.pack(side="left", padx=10, pady=5)
        
        # 2. BOTÓN HOME (Icono de casita)
        btn_home = Button(header, text="🏠", font=("Arial", 20), bg=COLOR_HEADER, fg="white", 
                        bd=0, activebackground=COLOR_HEADER, cursor="hand2",
                        command=lambda: controlador.mostrar_pantalla("plantilla")) 
        btn_home.pack(side="left", padx=10)

        # 3. TÍTULO
        Label(header, text=titulo, font=FONT_TITLE, bg=COLOR_HEADER, fg="white").pack(side="left", padx=20)


# ==========================================================
# PANTALLA 1: MAIN (TABLA DE PRODUCTOS)
# ==========================================================
class ProductosMain(EstiloBase):
    def __init__(self, master, controlador):
        super().__init__(master, controlador, "GESTION DE PRODUCTOS")
        
        # --- CONTENEDOR DE LA TABLA ---
        frame_tabla = Frame(self, bg="white")
        frame_tabla.pack(expand=True, fill="both", padx=40, pady=40)

        # Scrollbar
        scroll = Scrollbar(frame_tabla)
        scroll.pack(side="right", fill="y")

        # Treeview
        cols = ("ID", "Nombre", "Desc.", "Cant.", "Unidad", "Precio", "Caducidad", "Prov.")
        self.tree = ttk.Treeview(frame_tabla, columns=cols, show="headings", yscrollcommand=scroll.set)
        
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

        anchos = [40, 150, 150, 60, 60, 80, 90, 60]
        for col, ancho in zip(cols, anchos):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho, anchor="center")
        
        self.tree.pack(expand=True, fill="both")
        scroll.config(command=self.tree.yview)

        # --- BOTONES INFERIORES ---
        frame_botones = Frame(self, bg=COLOR_FONDO)
        frame_botones.pack(fill="x", pady=20, padx=40)

        btn_opts = {"bg": COLOR_BOTON, "fg": "white", "font": ("Arial", 11, "bold"), "width": 15, "bd": 0, "cursor": "hand2"}

        Button(frame_botones, text="Añadir", command=lambda: controlador.mostrar_pantalla("productos_insertar"), **btn_opts).pack(side="left", padx=10)
        Button(frame_botones, text="Actualizar", command=self.ir_a_actualizar, **btn_opts).pack(side="left", padx=10)
        Button(frame_botones, text="Eliminar", command=self.ir_a_eliminar, **btn_opts).pack(side="left", padx=10)
        Button(frame_botones, text="Refrescar", command=self.cargar_datos, **btn_opts).pack(side="right", padx=10)

        self.cargar_datos()

    def cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        datos = Productos.buscar()
        for fila in datos:
            self.tree.insert("", "end", values=fila)

    def ir_a_actualizar(self):
        seleccion = self.tree.focus()
        if seleccion:
            valores = self.tree.item(seleccion, "values")
            pantalla_act = self.controlador.pantallas["productos_actualizar"]
            pantalla_act.cargar_datos_formulario(valores)
            self.controlador.mostrar_pantalla("productos_actualizar")
        else:
            messagebox.showwarning("Atención", "Seleccione un producto para actualizar")

    def ir_a_eliminar(self):
        seleccion = self.tree.focus()
        if seleccion:
            valores = self.tree.item(seleccion, "values")
            pantalla_eli = self.controlador.pantallas["productos_eliminar"]
            pantalla_eli.cargar_datos_vista(valores)
            self.controlador.mostrar_pantalla("productos_eliminar")
        else:
            messagebox.showwarning("Atención", "Seleccione un producto para eliminar")


# ==========================================================
# PANTALLA 2: INSERTAR
# ==========================================================
class ProductosInsertar(EstiloBase):
    def __init__(self, master, controlador, modo="insertar"):
        titulo = "AÑADIR PRODUCTO" if modo == "insertar" else "ACTUALIZAR PRODUCTO"
        super().__init__(master, controlador, titulo)
        self.modo = modo
        self.id_producto_actual = None 

        cuerpo = Frame(self, bg=COLOR_FONDO)
        cuerpo.pack(expand=True, fill="both", padx=40, pady=20)

        # --- FORMULARIO (Izquierda) ---
        form_frame = Frame(cuerpo, bg=COLOR_FONDO)
        form_frame.place(relx=0.05, rely=0.05, relwidth=0.55, relheight=0.9)

        self.vars = {
            "nombre": StringVar(), "cantidad": DoubleVar(), "unidad": StringVar(),
            "precio": DoubleVar(), "desc": StringVar(), "prov": StringVar(), "caducidad": StringVar()
        }

        campos = [
            ("Nombre del Producto", "nombre"), ("Cantidad", "cantidad"),
            ("Unidad", "unidad"), ("Precio", "precio"),
            ("Descripcion", "desc"), ("Fecha Caducidad (YYYY-MM-DD)", "caducidad"),
            ("ID Proveedor (Opcional)", "prov")
        ]

        for idx, (lbl_text, var_key) in enumerate(campos):
            Label(form_frame, text=lbl_text, bg=COLOR_TEXTO_LBL, fg="black", 
                font=("Arial", 9, "bold"), width=25, anchor="w", padx=5).grid(row=idx*2, column=0, sticky="w", pady=(5, 0))
            
            if var_key == "unidad":
                ent = ttk.Combobox(form_frame, textvariable=self.vars[var_key], values=["kg", "litros", "piezas", "caja"], width=40)
            else:
                ent = Entry(form_frame, textvariable=self.vars[var_key], width=45)
            ent.grid(row=idx*2+1, column=0, sticky="w", pady=(2, 5), ipady=3)

        # --- IMAGEN GRANDE (Derecha) ---
        img_frame = Frame(cuerpo, bg=COLOR_FONDO) # Fondo igual al resto
        img_frame.place(relx=0.65, rely=0.15, relwidth=0.3, relheight=0.5)
        
        # Cargamos el logo en grande para decorar
        self.img_logo_big = obtener_imagen("logo.png", 250, 250)
        if self.img_logo_big:
            Label(img_frame, image=self.img_logo_big, bg=COLOR_FONDO).pack()
        else:
            # Fallback si no carga la imagen
            Label(img_frame, text="LOGO\nCHIVATA'S", bg="white", fg="red", font=("Arial", 20)).pack(expand=True, fill="both")

        # --- BOTONES ---
        btn_frame = Frame(self, bg=COLOR_FONDO)
        btn_frame.pack(side="bottom", pady=30)
        estilo_btn = {"bg": COLOR_BOTON, "fg": "white", "font": ("Arial", 11, "bold"), "width": 15, "cursor": "hand2"}
        
        txt_confirmar = "Guardar" if modo == "insertar" else "Actualizar"
        Button(btn_frame, text=txt_confirmar, command=self.guardar, **estilo_btn).pack(side="left", padx=20)
        Button(btn_frame, text="Cancelar", command=self.limpiar, **estilo_btn).pack(side="left", padx=20)
        Button(btn_frame, text="Volver", command=lambda: controlador.mostrar_pantalla("productos_main"), **estilo_btn).pack(side="left", padx=20)

    def limpiar(self):
        for key in self.vars:
            if key in ["cantidad", "precio"]: self.vars[key].set(0.0)
            else: self.vars[key].set("")

    def guardar(self):
        # Convertir vacíos a 0 para evitar errores numéricos
        cant = self.vars["cantidad"].get() if str(self.vars["cantidad"].get()) else 0.0
        prec = self.vars["precio"].get() if str(self.vars["precio"].get()) else 0.0
        
        datos = [self.vars["nombre"].get(), self.vars["desc"].get(), cant,
                self.vars["unidad"].get(), prec, self.vars["caducidad"].get(), self.vars["prov"].get()]
        
        if self.modo == "insertar":
            if Productos.insertar(*datos):
                messagebox.showinfo("Éxito", "Producto agregado")
                self.limpiar()
                self.controlador.pantallas["productos_main"].cargar_datos()
        else:
            if Productos.actualizar(self.id_producto_actual, *datos):
                messagebox.showinfo("Éxito", "Producto actualizado")
                self.controlador.mostrar_pantalla("productos_main")
                self.controlador.pantallas["productos_main"].cargar_datos()


# ==========================================================
# PANTALLA 3: ACTUALIZAR (Hereda de Insertar)
# ==========================================================
class ProductosActualizar(ProductosInsertar):
    def __init__(self, master, controlador):
        super().__init__(master, controlador, modo="actualizar")

    def cargar_datos_formulario(self, valores):
        self.id_producto_actual = valores[0]
        self.vars["nombre"].set(valores[1])
        self.vars["desc"].set(valores[2])
        self.vars["cantidad"].set(valores[3])
        self.vars["unidad"].set(valores[4])
        self.vars["precio"].set(valores[5])
        self.vars["caducidad"].set(valores[6])
        self.vars["prov"].set(valores[7])


# ==========================================================
# PANTALLA 4: ELIMINAR
# ==========================================================
class ProductosEliminar(EstiloBase):
    def __init__(self, master, controlador):
        super().__init__(master, controlador, "ELIMINAR PRODUCTO")
        self.id_a_eliminar = None

        cuerpo = Frame(self, bg=COLOR_FONDO)
        cuerpo.pack(expand=True, fill="both", padx=50, pady=50)

        Label(cuerpo, text="¿Estás seguro que deseas eliminar este producto?", 
            bg=COLOR_FONDO, fg="white", font=("Arial", 16)).pack(pady=20)

        self.lbl_info = Label(cuerpo, text="", bg="#900C0C", fg="white", font=("Arial", 14), padx=20, pady=20)
        self.lbl_info.pack(pady=10, fill="x")

        btn_frame = Frame(cuerpo, bg=COLOR_FONDO)
        btn_frame.pack(pady=40)

        Button(btn_frame, text="CONFIRMAR ELIMINACIÓN", bg="red", fg="white", font=("Arial", 12, "bold"),
            command=self.confirmar_eliminar, cursor="hand2").pack(side="left", padx=20)
        
        Button(btn_frame, text="Cancelar / Volver", bg=COLOR_BOTON, fg="white", font=("Arial", 12, "bold"),
            command=lambda: controlador.mostrar_pantalla("productos_main"), cursor="hand2").pack(side="left", padx=20)

    def cargar_datos_vista(self, valores):
        self.id_a_eliminar = valores[0]
        texto = f"ID: {valores[0]}\nProducto: {valores[1]}\nDescripción: {valores[2]}\nStock: {valores[3]} {valores[4]}"
        self.lbl_info.config(text=texto)

    def confirmar_eliminar(self):
        if self.id_a_eliminar:
            if Productos.eliminar(self.id_a_eliminar):
                messagebox.showinfo("Eliminado", "El producto ha sido eliminado.")
                self.controlador.pantallas["productos_main"].cargar_datos()
                self.controlador.mostrar_pantalla("productos_main")