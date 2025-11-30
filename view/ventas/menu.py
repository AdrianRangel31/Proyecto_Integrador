import tkinter as tk
from tkinter import ttk
from model import ventasCRUD
from tkinter import messagebox
from view.header import header
COLOR_FRAME = "#c60000"

class ventanaMenu(tk.Frame):
    def __init__(self,master,controlador):
        super().__init__(master)
        self.controlador = controlador
        self.config(bg=COLOR_FRAME)

        head = header(self, controlador)
        head.pack(fill="x")
        head.titulo = "Modificar precios"

        self.producto_var = tk.StringVar()
        self.precio_var = tk.IntVar()

        # Frame formulario
        form_frame = tk.Frame(self,bg=COLOR_FRAME)
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Producto",font=("Arial", 20),fg="white",bg=COLOR_FRAME).grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.producto_var,width=30,font=("Arial",20)).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Precio",font=("Arial", 20),fg="white",bg=COLOR_FRAME).grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.precio_var,width=30,font=("Arial",20)).grid(row=1, column=1, padx=5, pady=5)

        # Botones
        btn_frame = tk.Frame(self,bg=COLOR_FRAME)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Agregar", command=self.agregar_producto,width=15,font=("Arial",16),bg="#669BBC",fg="white").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Modificar", command=self.modificar_producto,width=15,font=("Arial",16),bg="#669BBC",fg="white").grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar_producto,width=15,font=("Arial",16),bg="#669BBC",fg="white").grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Limpiar", command=self.limpiar_campos,width=15,font=("Arial",16),bg="#669BBC",fg="white").grid(row=0, column=3, padx=5)

        # Tabla
        chartframe = tk.Frame(self,width=800,height=400)
        chartframe.pack(padx=100)
        self.tree = ttk.Treeview(chartframe, columns=("ID", "Producto", "Precio"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Precio", text="Precio")
        self.tree.pack()
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
