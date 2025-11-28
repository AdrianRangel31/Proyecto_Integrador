import tkinter as tk
from tkinter import ttk
from model import ventasCRUD
from tkinter import messagebox
COLOR_FRAME = "#c60000"

class ventanaMenu(tk.Toplevel):
    def __init__(self,master,controlador):
        super().__init__(master)
        self.controlador = controlador
        self.title("Modificar menú")
        self.geometry("800x600")
        self.config(bg=COLOR_FRAME)
        # Esto impide interactuar con la ventana de Ventas hasta cerrar esta
        self.grab_set() 

        self.producto_var = tk.StringVar()
        self.precio_var = tk.IntVar()

        # Frame formulario
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Producto").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.producto_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Precio").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.precio_var).grid(row=1, column=1, padx=5, pady=5)

        # Botones
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Agregar", command=self.agregar_producto).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Modificar", command=self.modificar_producto).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar_producto).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Limpiar", command=self.limpiar_campos).grid(row=0, column=3, padx=5)

        # Tabla
        self.tree = ttk.Treeview(self, columns=("ID", "Producto", "Precio"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Precio", text="Precio")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_producto)

        self.mostrar_productos()
        
    def mostrar_productos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in ventasCRUD.menu.obtener_todo():
            self.tree.insert("", tk.END, values=row)

    def agregar_producto(self):
        if self.producto_var.get() and self.precio_var.get():
            ventasCRUD.menu.insertar(self.producto_var.get(), self.precio_var.get())
            self.mostrar_productos()
            self.limpiar_campos()
        else:
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.")

    def modificar_producto(self):
        selected = self.tree.focus()
        if selected:
            valores = self.tree.item(selected, "values")
            id_menu = valores[0]
            ventasCRUD.menu.actualizar(id_menu, self.producto_var.get(), self.precio_var.get())
            self.mostrar_productos()
            self.limpiar_campos()
        else:
            messagebox.showwarning("Atención", "Selecciona una película para modificar.")

    def eliminar_producto(self):
        selected = self.tree.focus()
        if selected:
            valores = self.tree.item(selected, "values")
            id_menu = valores[0]
            ventasCRUD.menu.eliminar(id_menu)
            self.mostrar_productos()
            self.limpiar_campos()
        else:
            messagebox.showwarning("Atención", "Selecciona una película para eliminar.")

    def seleccionar_producto(self, event):
        selected = self.tree.focus()
        if selected:
            valores = self.tree.item(selected, "values")
            self.producto_var.set(valores[1])
            self.precio_var.set(valores[2])

    def limpiar_campos(self):
        self.producto_var.set("")
        self.precio_var.set("")
