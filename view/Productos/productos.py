from tkinter import *
from tkinter import ttk, messagebox
import os
import sys

# --- IMPORTS DE RUTAS ---
ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(ruta_raiz)

from model.productosCRUD import Productos
from controller.funciones import obtener_imagen

# --- IMPORTAR EL HEADER DE TU AMIGO ---
try:
    from view.header import header 
except ImportError:
    print("⚠️ Error importando header. Asegúrate de que view.plantilla.header exista.")
    from tkinter import Frame as header 

# --- CONSTANTES DE ESTILO ---
COLOR_FONDO = "#B71C1C"
COLOR_BOTON = "#5DADE2"
COLOR_TEXTO_LBL = "#5DADE2"
COLOR_BLANCO = "#FFFFFF"

# Fuentes
FONT_LABEL = ("Arial", 12, "bold")
FONT_INPUT = ("Arial", 12)
FONT_BTN = ("Arial", 12, "bold")
FONT_TABLE = ("Arial", 12)

class EstiloBase(Frame):
    """
    Clase padre modificada para usar el Header compartido del equipo.
    """
    def __init__(self, master, controlador, titulo):
        super().__init__(master)
        self.controlador = controlador
        self.configure(bg=COLOR_FONDO)
        
        self.encabezado = header(self, controlador)
        self.encabezado.pack(side="top", fill="x")
        self.encabezado.titulo = titulo


# ==========================================================
# PANTALLA 1: MAIN (TABLA DE PRODUCTOS)
# ==========================================================
class ProductosMain(EstiloBase):
    def __init__(self, master, controlador):
        super().__init__(master, controlador, "GESTION DE PRODUCTOS")
        
        frame_tabla = Frame(self, bg="white")
        frame_tabla.pack(expand=True, fill="both", padx=30, pady=30)

        scroll = Scrollbar(frame_tabla)
        scroll.pack(side="right", fill="y")

        cols = ("ID", "Nombre", "Desc.", "Cant.", "Unidad", "Precio", "Caducidad", "Prov.")
        self.tree = ttk.Treeview(frame_tabla, columns=cols, show="headings", yscrollcommand=scroll.set)
        
        style = ttk.Style()
        style.configure("Treeview", font=FONT_TABLE, rowheight=35)
        style.configure("Treeview.Heading", font=("Arial", 13, "bold"))

        anchos = [50, 200, 200, 80, 80, 100, 120, 80]
        for col, ancho in zip(cols, anchos):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho, anchor="center")
        
        self.tree.pack(expand=True, fill="both")
        scroll.config(command=self.tree.yview)

        frame_botones = Frame(self, bg=COLOR_FONDO)
        frame_botones.pack(fill="x", pady=20, padx=40)

        btn_opts = {"bg": COLOR_BOTON, "fg": "white", "font": FONT_BTN, "width": 15, "bd": 0, "cursor": "hand2"}

        Button(frame_botones, text="Añadir", command=lambda: controlador.mostrar_pantalla("productos_insertar"), **btn_opts).pack(side="left", padx=10)
        Button(frame_botones, text="Actualizar", command=self.ir_a_actualizar, **btn_opts).pack(side="left", padx=10)
        Button(frame_botones, text="Eliminar", command=self.ir_a_eliminar, **btn_opts).pack(side="left", padx=10)
        Button(frame_botones, text="Refrescar", command=self.cargar_datos, **btn_opts).pack(side="right", padx=10)

        # Cargar datos iniciales
        self.cargar_datos()

        # --- EVENTO MÁGICO PARA ACTUALIZAR ---
        # El evento <Map> se dispara cuando el widget se hace visible (pack)
        self.bind("<Map>", self.evento_actualizar_tabla)

    def evento_actualizar_tabla(self, event):
        """Método que se ejecuta automáticamente al entrar a esta pantalla"""
        self.cargar_datos()

    def cargar_datos(self):
        # Limpiar y recargar
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
# PANTALLA 2: INSERTAR (CON TABLA DE PROVEEDORES)
# ==========================================================
class ProductosInsertar(EstiloBase):
    def __init__(self, master, controlador, modo="insertar"):
        titulo = "AÑADIR PRODUCTO" if modo == "insertar" else "ACTUALIZAR PRODUCTO"
        super().__init__(master, controlador, titulo)
        self.modo = modo
        self.id_producto_actual = None 

        cuerpo = Frame(self, bg=COLOR_FONDO)
        cuerpo.pack(expand=True, fill="both", padx=30, pady=20)

        # --- IZQUIERDA: FORMULARIO ---
        form_frame = Frame(cuerpo, bg=COLOR_FONDO)
        form_frame.place(relx=0.0, rely=0.0, relwidth=0.55, relheight=1.0)

        self.vars = {
            "nombre": StringVar(), "cantidad": DoubleVar(), "unidad": StringVar(),
            "precio": DoubleVar(), "desc": StringVar(), "prov": StringVar(), "caducidad": StringVar()
        }

        campos = [
            ("Nombre del Producto", "nombre"), ("Cantidad", "cantidad"),
            ("Unidad", "unidad"), ("Precio", "precio"),
            ("Descripcion", "desc"), ("Fecha Caducidad (YYYY-MM-DD)", "caducidad"),
            ("ID Proveedor (Selecciona de la tabla ➜)", "prov")
        ]

        for idx, (lbl_text, var_key) in enumerate(campos):
            Label(form_frame, text=lbl_text, bg=COLOR_TEXTO_LBL, fg="black", 
                  font=FONT_LABEL, width=35, anchor="w", padx=10).grid(row=idx*2, column=0, sticky="w", pady=(10, 0))
            
            if var_key == "unidad":
                ent = ttk.Combobox(form_frame, textvariable=self.vars[var_key], values=["kg", "litros", "piezas", "caja"], width=38, font=FONT_INPUT)
            else:
                ent = Entry(form_frame, textvariable=self.vars[var_key], width=40, font=FONT_INPUT)
            ent.grid(row=idx*2+1, column=0, sticky="w", pady=(2, 5), ipady=4, padx=5)


        # --- DERECHA: TABLA DE PROVEEDORES (AYUDA) ---
        ayuda_frame = Frame(cuerpo, bg="white", bd=2, relief="ridge")
        ayuda_frame.place(relx=0.58, rely=0.02, relwidth=0.40, relheight=0.75)

        Label(ayuda_frame, text="LISTA DE PROVEEDORES", bg="#E0E0E0", font=("Arial", 12, "bold")).pack(fill="x")
        Label(ayuda_frame, text="(Haz doble clic para seleccionar)", bg="white", font=("Arial", 9), fg="gray").pack(fill="x")

        # Treeview de Proveedores
        cols_prov = ("ID", "Empresa")
        self.tree_prov = ttk.Treeview(ayuda_frame, columns=cols_prov, show="headings", height=10)
        self.tree_prov.heading("ID", text="ID")
        self.tree_prov.column("ID", width=50, anchor="center")
        self.tree_prov.heading("Empresa", text="Nombre Empresa")
        self.tree_prov.column("Empresa", width=200, anchor="w")
        
        scroll_prov = Scrollbar(ayuda_frame, command=self.tree_prov.yview)
        self.tree_prov.configure(yscrollcommand=scroll_prov.set)
        scroll_prov.pack(side="right", fill="y")
        self.tree_prov.pack(expand=True, fill="both")

        self.tree_prov.bind("<<TreeviewSelect>>", self.seleccionar_proveedor)
        self.cargar_lista_proveedores()

        # --- BOTONES ---
        btn_frame = Frame(self, bg=COLOR_FONDO)
        btn_frame.pack(side="bottom", pady=20)
        
        txt_confirmar = "GUARDAR" if modo == "insertar" else "ACTUALIZAR"
        Button(btn_frame, text=txt_confirmar, command=self.guardar, bg=COLOR_BOTON, fg="white", font=FONT_BTN, width=15).pack(side="left", padx=15)
        Button(btn_frame, text="LIMPIAR", command=self.limpiar, bg="gray", fg="white", font=FONT_BTN, width=15).pack(side="left", padx=15)
        Button(btn_frame, text="VOLVER", command=lambda: controlador.mostrar_pantalla("productos_main"), bg=COLOR_BOTON, fg="white", font=FONT_BTN, width=15).pack(side="left", padx=15)

        # --- EVENTO MÁGICO PARA ACTUALIZAR PROVEEDORES ---
        # Esto soluciona tu problema: recarga los proveedores cada vez que la pantalla se muestra
        self.bind("<Map>", self.evento_actualizar_proveedores)

    def evento_actualizar_proveedores(self, event):
        """Se ejecuta al mostrar la pantalla de insertar/actualizar"""
        self.cargar_lista_proveedores()

    def cargar_lista_proveedores(self):
        for item in self.tree_prov.get_children():
            self.tree_prov.delete(item)
        datos = Productos.obtener_lista_proveedores()
        for row in datos:
            self.tree_prov.insert("", "end", values=row)

    def seleccionar_proveedor(self, event):
        seleccion = self.tree_prov.focus()
        if seleccion:
            valores = self.tree_prov.item(seleccion, "values")
            self.vars["prov"].set(valores[0])

    def limpiar(self):
        for key in self.vars:
            if key in ["cantidad", "precio"]: self.vars[key].set(0.0)
            else: self.vars[key].set("")

    def guardar(self):
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
# PANTALLA 3: ACTUALIZAR
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
        self.cargar_lista_proveedores()


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
              bg=COLOR_FONDO, fg="white", font=("Arial", 18)).pack(pady=20)

        self.lbl_info = Label(cuerpo, text="", bg="#900C0C", fg="white", font=("Arial", 16), padx=20, pady=20)
        self.lbl_info.pack(pady=10, fill="x")

        btn_frame = Frame(cuerpo, bg=COLOR_FONDO)
        btn_frame.pack(pady=40)

        Button(btn_frame, text="CONFIRMAR ELIMINACIÓN", bg="red", fg="white", font=FONT_BTN,
               command=self.confirmar_eliminar, cursor="hand2").pack(side="left", padx=20)
        
        Button(btn_frame, text="Cancelar / Volver", bg=COLOR_BOTON, fg="white", font=FONT_BTN,
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