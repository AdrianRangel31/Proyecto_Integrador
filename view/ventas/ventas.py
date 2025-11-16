from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from view.header import *

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

        frameCRUD = Frame(body, bg=COLOR_FRAME)
        frameCRUD.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        frameCRUD.pack_propagate(False)
        frameGRAPH = Frame(body, bg=COLOR_FRAME)
        frameGRAPH.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        frameGRAPH.pack_propagate(False)

        #FRAME CRUD
        frame_filtrar = Frame(frameCRUD,bg=COLOR_FRAME)
        frame_filtrar.pack(pady=20,)

        for i in range(4):
            frame_filtrar.columnconfigure(i, weight=0)
        frame_filtrar.rowconfigure(0, weight=0)
        
        lbl_filtrar = Label(frame_filtrar,text="Filtrar por:",font=("Arial", 22),bg=COLOR_FRAME,fg="white")
        lbl_filtrar.grid(row=0,column=0,sticky="w")
 
        lista = ["Opciones","campo1","campo2"]
        combo = ttk.Combobox(frame_filtrar, values=lista,state="readonly",show="ola")
        combo.grid(row=0,column=1,sticky="nsew")

        entrybuscar = Entry(frame_filtrar)
        entrybuscar.grid(row=0,column=2,sticky="nsew")
        
        btn_buscar = Button(frame_filtrar,text="Buscar",font=("Arial", 13, "bold"),command=lambda: "")
        btn_buscar.grid(row=0,column=3,sticky="nsew")

        chartframe = Frame(frameCRUD,bg="white",height=450)
        chartframe.pack_propagate(False)
        chartframe.pack(fill="x")
        
        columnas = ["ID","Fecha","Productos","Total"]
        # contenedor para la tabla y sus scrollbars
        table_container = Frame(chartframe, bg="white")
        table_container.pack(fill="both", expand=True)

        tabla = ttk.Treeview(table_container, columns=columnas, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(table_container, orient="vertical", command=tabla.yview)
        hsb = ttk.Scrollbar(table_container, orient="horizontal", command=tabla.xview)
        tabla.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Layout usando grid para que los scrollbars funcionen correctamente
        tabla.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_container.rowconfigure(0, weight=1)
        table_container.columnconfigure(0, weight=1)

        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, anchor="center", width=120)

        registros = [(1,"2-2-2020","Hamburguesa",123)]
        for i in range(30):
            registros.append((i,"2-2-2020","Hamburguesa",123))
        for fila in registros:
            tabla.insert("", "end", values=fila)

        frame_botones = Frame(frameCRUD,bg=COLOR_FRAME)
        frame_botones.pack_propagate(False)
        frame_botones.pack(padx=20,pady=10)

        btn_añadir = Button(frame_botones,text="Añadir",font=("Arial", 13, "bold"),width=15,fg="white",bg="#86B7D6",command=lambda: self.controlador.mostrar_pantalla("insertarventas"))
        btn_añadir.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)

        btn_actualizar = Button(frame_botones,text="Actualizar",font=("Arial", 13, "bold"),width=15,fg="white",bg="#86B7D6",command=lambda: self.controlador.mostrar_pantalla("actualizarventas"))
        btn_actualizar.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)

        btn_eliminar = Button(frame_botones,text="Eliminar",font=("Arial", 13, "bold"),width=15,fg="white",bg="#86B7D6",command=lambda: self.eliminar_cliente())
        btn_eliminar.grid(row=0,column=2,sticky="nsew",padx=10,pady=10)

        #FRAME GRAPH

        self.graph1 = obtener_imagen("graph.png",600,270)
        lbl_msj1 = Label(frameGRAPH,text="Ultima semana",font=("Arial", 22),bg=COLOR_FRAME,fg="white")
        lbl_msj1.pack()
        lbl_graph1 = Label(frameGRAPH,image=self.graph1,compound="top", height=270)
        lbl_graph1.pack()

        self.graph2 = obtener_imagen("graph.png",600,270)
        lbl_msj2 = Label(frameGRAPH,text="Ultimo mes",font=("Arial", 22),bg=COLOR_FRAME,fg="white")
        lbl_msj2.pack()
        lbl_graph2 = Label(frameGRAPH,image=self.graph2,compound="top", height=270)
        lbl_graph2.pack()
    
    def eliminar_cliente(self):
        eliminar = messagebox.askyesno("ADVERTENCIA",f"El ID seleccionado es: ##\n¿Está seguro de que desea eliminar este registro?")
        if eliminar:
            messagebox.showinfo("Exito",f"El registro con ID = ## se eliminó exitosamente")

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
