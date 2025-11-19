from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from view.header import *
from model import ventasCRUD

COLOR_FRAME = "#c60000"

class mainVentas(Frame):
    def __init__(self, master, controlador):
        super().__init__(master)
        self.controlador = controlador
        head = header(self, controlador)
        head.pack(fill="x")
        head.titulo = "Ventas"
        body = Frame(self, bg="#ffffff")
        body.pack(fill="both", expand=True)
        self.id_seleccionado = 0
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        frameVENTA = Frame(body, bg=COLOR_FRAME)
        frameVENTA.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        frameVENTA.pack_propagate(False)
        frameDETALLES = Frame(body, bg=COLOR_FRAME)
        frameDETALLES.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        frameDETALLES.pack_propagate(False)

        #FRAME VENTA
        # FRAME FILTRAR
        frame_filtrar = Frame(frameVENTA, bg=COLOR_FRAME)
        frame_filtrar.pack(pady=20)

        for i in range(4):
            frame_filtrar.columnconfigure(i, weight=0)
        frame_filtrar.rowconfigure(0, weight=0)
        
        lbl_filtrar = Label(frame_filtrar, text="Filtrar por:", font=("Arial", 22),
                            bg=COLOR_FRAME, fg="white")
        lbl_filtrar.grid(row=0, column=0, sticky="w")

        columnas = ["Todo","ID", "Fecha", "Total"]

        # ---------------------------- ESTILOS -------------------------------
        style = ttk.Style()
        style.theme_use("clam")

        # Estilo personalizado SOLO para Treeview
        style.configure("Custom.Treeview",
                        font=("Arial", 16),
                        rowheight=35)
        
        style.configure("Custom.Treeview.Heading",
                        background="#4A90E2",
                        foreground="white",
                        font=("Arial", 18, "bold"),
                        relief="flat")
        
        style.map("Custom.Treeview.Heading",
                  background=[("active", "#357ABD")])

        # Estilo para ComboBox
        style.configure("Custom.TCombobox",
                        fieldbackground="#4A90E2",
                        background="#4A90E2",
                        foreground="black",
                        bordercolor="#4A90E2",
                        lightcolor="#4A90E2",
                        arrowcolor="white",
                        font=("Arial", 22))

        style.map("Custom.TCombobox",
                  fieldbackground=[("readonly", "#4A90E2")],
                  foreground=[("readonly", "white")],
                  selectbackground=[("readonly", "#4A90E2")],
                  selectforeground=[("readonly", "white")])
        # -------------------------------------------------------------------

        # COMBOBOX con estilo aplicado
        combo_campo = ttk.Combobox(frame_filtrar,
                             values=columnas,
                             state="readonly",
                             style="Custom.TCombobox")
        combo_campo.configure(font=("Arial", 22),width=10)
        combo_campo.current(0)
        combo_campo.grid(row=0, column=1, sticky="nsew")
        def campo_seleccionado(event):
            valor = combo_campo.get()
            match valor:
                case "Fecha":
                    combo_valor.config(values=filtros_fecha)
                case "Total":
                    combo_valor.config(values=filtros_precio)
                case _:
                    combo_valor.config(values=[])
            combo_valor.set("")
        combo_campo.bind("<<ComboboxSelected>>", campo_seleccionado)


        filtros_fecha = ["Más recientes","Más antiguos"]
        filtros_precio = ["Más alto","Más bajo"]
        combo_valor = ttk.Combobox(frame_filtrar,
                             values=[],
                             style="Custom.TCombobox")
        combo_valor.configure(font=("Arial", 22),width=10)
        combo_valor.grid(row=0, column=2, sticky="nsew")
        
        btn_buscar = Button(frame_filtrar, text="Buscar",
                            font=("Arial", 13, "bold"),
                            command=lambda: self.buscar_venta(combo_campo.get(),combo_valor.get()))
        btn_buscar.grid(row=0, column=3, sticky="nsew")

        # --------------------------- TABLA VENTAS --------------------------------
        chartframe = Frame(frameVENTA, bg="white", height=450)
        chartframe.pack_propagate(False)
        chartframe.pack(fill="x")

        table_container = Frame(chartframe, bg="white")
        table_container.pack(fill="both", expand=True)


        columnas.remove("Todo")
        self.tabla = ttk.Treeview(
            table_container,
            columns=columnas,
            show="headings",
            selectmode="browse",
            style="Custom.Treeview"
        )

        vsb = ttk.Scrollbar(table_container, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=vsb.set)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=100)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        table_container.rowconfigure(0, weight=1)
        table_container.columnconfigure(0, weight=1)

        def seleccionar_fila(event):
            fila = self.tabla.selection()  # Obtiene ID(s) de las filas seleccionadas
            if fila:
                valores = self.tabla.item(fila[0], "values")
                self.id_seleccionado = valores[0]
            self.ver_detalles()
        self.tabla.bind("<<TreeviewSelect>>", seleccionar_fila)
        # -------------------------------------------------------------------

        frame_botones = Frame(frameVENTA, bg=COLOR_FRAME)
        frame_botones.pack_propagate(False)
        frame_botones.pack(padx=20, pady=10)

        btn_añadir = Button(frame_botones, text="Añadir",
                            font=("Arial", 16, "bold"), width=15,
                            fg="white", bg="#86B7D6",
                            command=lambda: self.controlador.mostrar_pantalla("insertarventas"))
        btn_añadir.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        btn_actualizar = Button(frame_botones, text="Actualizar",
                                font=("Arial", 16, "bold"), width=15,
                                fg="white", bg="#86B7D6",
                                command=lambda: self.controlador.mostrar_pantalla("actualizarventas"))
        btn_actualizar.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        btn_eliminar = Button(frame_botones, text="Eliminar",
                              font=("Arial", 16, "bold"), width=15,
                              fg="white", bg="#86B7D6",
                              command=lambda: self.eliminar_venta())
        btn_eliminar.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        self.buscar_venta("Todo","")






        #FRAME DETALLES
        lbl_titulo = Label(frameDETALLES,text="Detalles de venta",font=("Arial", 22),
                            bg=COLOR_FRAME, fg="white")
        lbl_titulo.pack(pady=20)

        # --------------------------- TABLA  DETALLES--------------------------------
        chartframe2 = Frame(frameDETALLES, bg="white", height=450)
        chartframe2.pack_propagate(False)
        chartframe2.pack(fill="x")

        table_container2 = Frame(chartframe2, bg="white")
        table_container2.pack(fill="both", expand=True)

        columnas2 = ["ID","ID_Venta","Producto","Cantidad","Subtotal"]
        self.tabla2 = ttk.Treeview(
            table_container2,
            columns=columnas2,
            show="headings",
            selectmode="browse",
            style="Custom.Treeview"
        )

        vsb = ttk.Scrollbar(table_container2, orient="vertical", command=self.tabla2.yview)
        self.tabla2.configure(yscrollcommand=vsb.set)

        for col in columnas2:
            self.tabla2.heading(col, text=col)
            self.tabla2.column(col, anchor="center", width=60)

        self.tabla2.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        table_container2.rowconfigure(0, weight=1)
        table_container2.columnconfigure(0, weight=1)

        """
        def seleccionar_fila(event):
            fila = self.tabla2.selection()  # Obtiene ID(s) de las filas seleccionadas
            if fila:
                valores = self.tabla2.item(fila[0], "values")
                self.id_seleccionado = valores[0]
            print(self.id_seleccionado)
        self.tabla2.bind("<<TreeviewSelect>>", seleccionar_fila) 
        """
        # -------------------------------------------------------------------

            

    def buscar_venta(self,campo,valor):
        registros = ventasCRUD.ventas.buscar(campo,valor)
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        for fila in registros:
            self.tabla.insert("", "end", values=fila)

    def eliminar_venta(self):
        confirmar = messagebox.askyesno("ADVERTENCIA", 
                                       f"El ID seleccionado es: {self.id_seleccionado}\n¿Está seguro de que desea eliminar este registro?")
        if confirmar:
            eliminar = ventasCRUD.ventas.eliminar(self.id_seleccionado)
            if eliminar:
                messagebox.showinfo("Exito", 
                                f"El registro con ID = {self.id_seleccionado} se eliminó exitosamente")
                self.buscar_venta("Todo","")
            else: 
                messagebox.showinfo("Error", 
                                    "No se pudo eliminar el registro")      

    def ver_detalles(self):
        if self.id_seleccionado == 0:
            messagebox.showinfo("Aviso", "Seleccione un registro para continuar.")
            return
        registros = ventasCRUD.detalleVenta.buscar(self.id_seleccionado)
        for row in self.tabla2.get_children():
            self.tabla2.delete(row)
        for fila in registros:
            self.tabla2.insert("", "end", values=fila)
        

class insertarVentas(Frame):
    def __init__(self, master, controlador,accion):
        super().__init__(master)
        self.controlador = controlador
        head = header(self, controlador)
        head.pack(fill="x")
        body = Frame(self, bg=COLOR_FRAME)
        body.pack(fill="both", expand=True,padx=30,pady=30)
        
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self.precios = [fila[0] for fila in ventasCRUD.menu.obtenerPrecios()]

        frame_prod = Frame(body,bg=COLOR_FRAME)
        frame_total = Frame(body,bg=COLOR_FRAME)
        match accion:
            case "agregar":
                head.titulo = "Registrar venta"
                frame_prod.grid(row=0,column=0,sticky="nsew",padx=40,pady=50)
                frame_total.grid(row=0,column=1,sticky="nsew",pady=50,padx=20)
                frame_prod.grid_propagate(False)
            case "actualizar":
                head.titulo = "Actualizar venta"
                frame_prod.grid(row=1,column=0,sticky="nsew",padx=40,pady=50)
                frame_total.grid(row=1,column=1,sticky="nsew",pady=50,padx=20)
                body.rowconfigure(1, weight=1)

                chartframe = Frame(body,bg="white")
                chartframe.pack_propagate(False)
                chartframe.grid(row=0,column=0,sticky="nsew",pady=(50,0),padx=10,columnspan=2)
                columnas = ["ID","Fecha","Productos","Total"]
                table_container = Frame(chartframe, bg="white")
                table_container.pack(fill="both", expand=True)
                tabla = ttk.Treeview(table_container, columns=columnas, show="headings", selectmode="browse")
                tabla.grid(row=0, column=0, sticky="nsew")

                table_container.rowconfigure(0, weight=1)
                table_container.columnconfigure(0, weight=1)

                for col in columnas:
                    tabla.heading(col, text=col)
                    tabla.column(col, anchor="center", width=120)

                registros = [(1,"2-2-2020","Hamburguesa",123)]
                for fila in registros:
                    tabla.insert("", "end", values=fila)





        #frame prod
        #Comida
        lbl_prod = Label(frame_prod,text="Producto",font=("Arial", 24),fg="white",bg=COLOR_FRAME)
        lbl_prod.grid(row=0,column=0)

        lbl_cant = Label(frame_prod,text="Cantidad",font=("Arial", 24),fg="white",bg=COLOR_FRAME)
        lbl_cant.grid(row=0,column=1)


        #self.opciones_prod = ["Hamburguesa doble","Hamburguesa especial","Hamburguesa especial","Hotdog","Ingrediente extra","Refresco","Agua"]
        self.opciones_prod = [fila[0] for fila in ventasCRUD.menu.obtenerProductos()]

        for i in range(len(self.opciones_prod)):
            lbl = Label(frame_prod,text=self.opciones_prod[i],font=("Arial", 20),fg="black",bg="white", highlightthickness=2,
                            highlightbackground="black",
                            highlightcolor="black")
            lbl.grid(row=i+1,column=0,sticky="nsew")
        
        self.spinbox_prod = []

        for i in range(len(self.opciones_prod)):
            vcmd = (self.register(lambda val, idx=i: self.validar_spin(val, idx)), "%P")
            spin = Spinbox(
                frame_prod,
                from_=0, to=100,
                font=("Arial", 20),
                width=4,
                bg="white",
                fg="black",
                borderwidth=0,
                relief="flat",
                highlightthickness=2,
                highlightbackground="black",
                highlightcolor="black",
                command=lambda idx=i: self.spin_cambio(idx, self.spinbox_prod[idx].get()),
                validate="key",
                validatecommand=lambda:vcmd
            )

            self.spinbox_prod.append(spin)
            spin.grid(row=i+1, column=1, sticky="nsew")


        #frame total

        frame_total.pack_propagate(False)
        lbl_msj = Label(frame_total,text="Total",font=("Arial", 24),fg="white",bg=COLOR_FRAME)
        lbl_msj.pack(pady=(50,5))

        self.lbl_total = Label(frame_total,
                            font=("Arial", 25),
                            text="$_________",
                            bg="white",
                            fg="black",
                            borderwidth=0,
                            relief="flat",
                            highlightthickness=2,
                            highlightbackground="black",
                            highlightcolor="black")
        self.lbl_total.pack(pady=5)

        btn_agregar = Button(frame_total,text="Agregar venta",width=20,font=("Arial",20),command=lambda:self.crearVenta(),bg="#669BBC",fg="white")
        btn_agregar.pack(pady=5)
        self.total_venta = 0
        btn_volver = Button(frame_total,text="Volver",width=20,font=("Arial",20),command=lambda:self.controlador.mostrar_pantalla("mainventas"),bg="#669BBC",fg="white")
        btn_volver.pack(pady=5)

    def spin_cambio(self, index, valor):
        cant_prod = []
        for i in range(len(self.spinbox_prod)):
            cant_prod.append(self.spinbox_prod[i].get())
        total = 0
        for i in range(len(self.opciones_prod)):
            total += float(cant_prod[i]) * float(self.precios[i])
        self.lbl_total.config(text=f"$ {total}")
        self.total_venta = total

    def validar_spin(self, nuevo_valor, index):
        if nuevo_valor.isdigit() or nuevo_valor == "":
            self.spin_cambio(index, nuevo_valor)
            return True
        return False

    def crearVenta(self):
        insertar,id = ventasCRUD.ventas.insertar(self.total_venta)
        for i in range(len(self.spinbox_prod)):
            cantidad = int(self.spinbox_prod[i].get())
            if cantidad > 0:
                insertar_detalle = ventasCRUD.detalleVenta.insertar(id,self.opciones_prod[i],cantidad)
        if insertar and insertar_detalle:
            messagebox.showinfo("Exito", "La venta se guardó exitosamente.")




