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
        head.titulo = "Modify Prices"

        self.producto_var = tk.StringVar()
        self.precio_var = tk.IntVar()

        form_frame = tk.Frame(self,bg=COLOR_FRAME)
        form_frame.pack(pady=10)
        
        tk.Label(form_frame, text="Product",font=("Arial", 20),fg="white",bg=COLOR_FRAME).grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.producto_var,width=30,font=("Arial",20)).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Price",font=("Arial", 20),fg="white",bg=COLOR_FRAME).grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(form_frame, textvariable=self.precio_var,width=30,font=("Arial",20)).grid(row=1, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self,bg=COLOR_FRAME)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Add", command=self.agregar_producto,width=15,font=("Arial",16),bg="#669BBC",fg="white").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Modify", command=self.modificar_producto,width=15,font=("Arial",16),bg="#669BBC",fg="white").grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", command=self.eliminar_producto,width=15,font=("Arial",16),bg="#669BBC",fg="white").grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Clear", command=self.limpiar_campos,width=15,font=("Arial",16),bg="#669BBC",fg="white").grid(row=0, column=3, padx=5)

        chartframe = tk.Frame(self,width=800,height=400)
        chartframe.pack(padx=100)
        self.tree = ttk.Treeview(chartframe, columns=("ID", "Product", "Price"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Product", text="Product")
        self.tree.heading("Price", text="Price")
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
            insertar = ventasCRUD.menu.insertar(self.producto_var.get(), self.precio_var.get())
            if insertar:
                messagebox.showinfo("Success","Registered successfully")
                self.mostrar_productos()
                self.limpiar_campos()
            else: 
                messagebox.showinfo("Error","An error occurred while registering")
        else:
            messagebox.showwarning("Attention", "All fields are required.")

    def modificar_producto(self):
        selected = self.tree.focus()
        if selected:
            valores = self.tree.item(selected, "values")
            id_menu = valores[0]
            actualizar = ventasCRUD.menu.actualizar(id_menu, self.producto_var.get(), self.precio_var.get())
            if actualizar:
                messagebox.showinfo("Success","Updated successfully")
                self.mostrar_productos()
                self.limpiar_campos()
            else:
                messagebox.showinfo("Error","An error occurred while updating")
        else:
            messagebox.showwarning("Attention", "Select a record to modify.")

    def eliminar_producto(self):
        selected = self.tree.focus()
        if selected:
            valores = self.tree.item(selected, "values")
            id_menu = valores[0]
            eliminar = messagebox.askyesno("Warning",f"Are you sure you want to delete this record?\nID: {id_menu}")
            if eliminar:
                eliminar = ventasCRUD.menu.eliminar(id_menu)
                if eliminar:
                    messagebox.showinfo("Success","Deleted successfully")
                    self.mostrar_productos()
                    self.limpiar_campos()
                else:
                    messagebox.showinfo("Error","An error occurred while deleting\nIt is not possible to delete a record if there are related records in sales details.")
        else:
            messagebox.showwarning("Attention", "Select a record to delete.")

    def seleccionar_producto(self, event):
        selected = self.tree.focus()
        if selected:
            valores = self.tree.item(selected, "values")
            self.producto_var.set(valores[1])
            self.precio_var.set(valores[2])

    def limpiar_campos(self):
        self.producto_var.set("")
        self.precio_var.set("")