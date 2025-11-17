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

        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        frameVENTA = Frame(body, bg=COLOR_FRAME)
        frameVENTA.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        frameVENTA.pack_propagate(False)
        frameDETALLES = Frame(body, bg=COLOR_FRAME)
        frameDETALLES.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        frameDETALLES.pack_propagate(False)

        # FRAME FILTRAR
        frame_filtrar = Frame(frameVENTA, bg=COLOR_FRAME)
        frame_filtrar.pack(pady=20)

        for i in range(4):
            frame_filtrar.columnconfigure(i, weight=0)
        frame_filtrar.rowconfigure(0, weight=0)
        
        lbl_filtrar = Label(frame_filtrar, text="Filtrar por:", font=("Arial", 22),
                            bg=COLOR_FRAME, fg="white")
        lbl_filtrar.grid(row=0, column=0, sticky="w")

        columnas = ["ID", "Fecha", "Total"]

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
        combo_campo.grid(row=0, column=1, sticky="nsew")
        def campo_seleccionado(event):
            valor = combo_campo.get()
            match valor:
                case "ID":
                    combo_valor.config(values=[])
                case "Fecha":
                    combo_valor.config(values=filtros_fecha)
                case "Total":
                    combo_valor.config(values=filtros_precio)
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

        # --------------------------- TABLA --------------------------------
        chartframe = Frame(frameVENTA, bg="white", height=450)
        chartframe.pack_propagate(False)
        chartframe.pack(fill="x")

        table_container = Frame(chartframe, bg="white")
        table_container.pack(fill="both", expand=True)

        registros = ventasCRUD.ventas.buscar("*")

        tabla = ttk.Treeview(
            table_container,
            columns=columnas,
            show="headings",
            selectmode="browse",
            style="Custom.Treeview"
        )

        vsb = ttk.Scrollbar(table_container, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=vsb.set)

        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, anchor="center", width=100)

        for fila in registros:
            tabla.insert("", "end", values=fila)

        tabla.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        table_container.rowconfigure(0, weight=1)
        table_container.columnconfigure(0, weight=1)
        # -------------------------------------------------------------------

        frame_botones = Frame(frameVENTA, bg=COLOR_FRAME)
        frame_botones.pack_propagate(False)
        frame_botones.pack(padx=20, pady=10)

        btn_añadir = Button(frame_botones, text="Añadir",
                            font=("Arial", 13, "bold"), width=15,
                            fg="white", bg="#86B7D6",
                            command=lambda: self.controlador.mostrar_pantalla("insertarventas"))
        btn_añadir.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        btn_actualizar = Button(frame_botones, text="Actualizar",
                                font=("Arial", 13, "bold"), width=15,
                                fg="white", bg="#86B7D6",
                                command=lambda: self.controlador.mostrar_pantalla("actualizarventas"))
        btn_actualizar.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        btn_eliminar = Button(frame_botones, text="Eliminar",
                              font=("Arial", 13, "bold"), width=15,
                              fg="white", bg="#86B7D6",
                              command=lambda: self.eliminar_venta())
        btn_eliminar.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)



            

    def buscar_venta(self,campo,valor):
        registros = ventasCRUD.ventas.buscar(campo,valor)
        print(registros)

    def eliminar_venta(self):
        eliminar = messagebox.askyesno("ADVERTENCIA", 
                                       f"El ID seleccionado es: ##\n¿Está seguro de que desea eliminar este registro?")
        if eliminar:
            messagebox.showinfo("Exito", 
                                f"El registro con ID = ## se eliminó exitosamente")

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


        opciones = ["Hamburguesa sencilla","Hamburguesa doble","Hamburguesa especial","Hotdog"]
        for i in range(len(opciones)):
            lbl = Label(frame_prod,text=opciones[i],font=("Arial", 20),fg="black",bg="white",                            highlightthickness=2,
                            highlightbackground="black",
                            highlightcolor="black")
            lbl.grid(row=i+1,column=0,sticky="nsew")

        spinbox_prod = []
        for i in range(len(opciones)):
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
                            highlightcolor="black"
                        )
            spinbox_prod.append(spin)
            spinbox_prod[i].grid(row=i+1,column=1,sticky = "nsew")

        #Bebidas
        lbl_beb = Label(frame_prod,text="Bebidas",font=("Arial", 24),fg="white",bg=COLOR_FRAME)
        lbl_beb.grid(row=6,column=0)

        lbl_cant = Label(frame_prod,text="Cantidad",font=("Arial", 24),fg="white",bg=COLOR_FRAME)
        lbl_cant.grid(row=6,column=1)

        opciones = ["Refresco","Agua"]
        for i in range(len(opciones)):
            lbl = Label(frame_prod,text=opciones[i],font=("Arial", 20),fg="black",bg="white",                            highlightthickness=2,
                            highlightbackground="black",
                            highlightcolor="black")
            lbl.grid(row=i+7,column=0,sticky="nsew")



        spinbox_beb = []
        for i in range(len(opciones)):
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
                            highlightcolor="black"
                        )
            spinbox_beb.append(spin)
            spinbox_beb[i].grid(row=i+7,column=1,sticky = "nsew")

        #frame total

        frame_total.pack_propagate(False)
        lbl_total = Label(frame_total,text="Total",font=("Arial", 24),fg="white",bg=COLOR_FRAME)
        lbl_total.pack(pady=(50,5))

        txt_total = Label(frame_total,
                            font=("Arial", 25),
                            text="$_________",
                            bg="white",
                            fg="black",
                            borderwidth=0,
                            relief="flat",
                            highlightthickness=2,
                            highlightbackground="black",
                            highlightcolor="black")
        txt_total.pack(pady=5)

        btn_agregar = Button(frame_total,text="Agregar venta",width=20,font=("Arial",20),command=lambda:"",bg="#669BBC",fg="white")
        btn_agregar.pack(pady=5)

        btn_volver = Button(frame_total,text="Volver",width=20,font=("Arial",20),command=lambda:self.controlador.mostrar_pantalla("mainventas"),bg="#669BBC",fg="white")
        btn_volver.pack(pady=5)


class eliminarVentas(Frame):
    def __init__(self, master, controlador):
        super().__init__(master)
        self.controlador = controlador
