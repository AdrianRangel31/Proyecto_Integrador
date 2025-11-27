from tkinter import *
from tkinter import ttk
from model import ventasCRUD
COLOR_FRAME = "#c60000"

class ventanaMenu(Toplevel):
    def __init__(self,master,controlador):
        super().__init__(master)
        self.controlador = controlador
        self.title("Modificar menú")
        self.geometry("800x600")
        self.config(bg=COLOR_FRAME)
        # Esto impide interactuar con la ventana de Ventas hasta cerrar esta
        self.grab_set() 


        precios_result = ventasCRUD.menu.obtenerPrecios()
        self.precios = [fila[0] for fila in precios_result] if precios_result else []

        frame_prod = Frame(self,bg=COLOR_FRAME)
        frame_prod.pack()


        #frame prod
        lbl_prod = Label(frame_prod,text="Producto",font=("Arial", 24),fg="white",bg=COLOR_FRAME)
        lbl_prod.grid(row=0,column=0)

        lbl_cant = Label(frame_prod,text="Precio",font=("Arial", 24),fg="white",bg=COLOR_FRAME)
        lbl_cant.grid(row=0,column=1)

        productos_result = ventasCRUD.menu.obtenerProductos()
        self.opciones_prod = [fila[0] for fila in productos_result] if productos_result else []

        for i in range(len(self.opciones_prod)):
            lbl = Label(frame_prod,text=self.opciones_prod[i],font=("Arial", 20),fg="black",bg="white", highlightthickness=2,
                            highlightbackground="black",
                            highlightcolor="black")
            lbl.grid(row=i+1,column=0,sticky="nsew")

        precios_result = ventasCRUD.menu.obtenerPrecios()
        self.precios = [fila[0] for fila in precios_result] if precios_result else []

        self.entry_precios = []

        for i in range(len(self.opciones_prod)):
            entry = Entry(
                frame_prod,
                font=("Arial", 20),
                width=4,
                bg="white",
                fg="black",
                borderwidth=0,
                relief="flat",
                highlightthickness=2,
                highlightbackground="black",
                highlightcolor="black"
                
            )
            entry.grid(row=i+1, column=1, sticky="nsew")
            entry.insert(0,self.precios[i])
            self.entry_precios.append(entry)
            
        
        btn_guardar = Button(self, text="Guardar Cambios", bg="#4CAF50", fg="white")
        btn_guardar.pack(pady=20)
        
        btn_cerrar = Button(self, text="Cerrar", command=self.destroy)
        btn_cerrar.pack()
