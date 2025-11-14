from tkinter import *
from tkinter import ttk
from view.header import *

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

        frameCRUD = Frame(body, bg="#c60000")
        frameCRUD.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        frameCRUD.pack_propagate(False)
        frameGRAPH = Frame(body, bg="#c60000")
        frameGRAPH.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        frameGRAPH.pack_propagate(False)

        #FRAME CRUD
        frame_filtrar = Frame(frameCRUD,bg="#c60000")
        frame_filtrar.pack(pady=20,)

        for i in range(4):
            frame_filtrar.columnconfigure(i, weight=0)
        frame_filtrar.rowconfigure(0, weight=0)
        
        lbl_filtrar = Label(frame_filtrar,text="Filtrar por:",font=("Arial", 22),bg="#c60000",fg="white")
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

        frame_botones = Frame(frameCRUD,bg="#c60000")
        frame_botones.pack_propagate(False)
        frame_botones.pack(padx=20,pady=10)

        btn_añadir = Button(frame_botones,text="Añadir",font=("Arial", 13, "bold"),width=15,fg="white",bg="#86B7D6",command=lambda: "")
        btn_añadir.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)

        btn_actualizar = Button(frame_botones,text="Actualizar",font=("Arial", 13, "bold"),width=15,fg="white",bg="#86B7D6",command=lambda: "")
        btn_actualizar.grid(row=0,column=1,sticky="nsew",padx=10,pady=10)

        btn_eliminar = Button(frame_botones,text="Eliminar",font=("Arial", 13, "bold"),width=15,fg="white",bg="#86B7D6",command=lambda: "")
        btn_eliminar.grid(row=0,column=2,sticky="nsew",padx=10,pady=10)

        #FRAME GRAPH

        self.graph1 = obtener_imagen("graph.png",600,270)
        lbl_msj1 = Label(frameGRAPH,text="Ultima semana",font=("Arial", 22),bg="#c60000",fg="white")
        lbl_msj1.pack()
        lbl_graph1 = Label(frameGRAPH,image=self.graph1,compound="top", height=270)
        lbl_graph1.pack()

        self.graph2 = obtener_imagen("graph.png",600,270)
        lbl_msj2 = Label(frameGRAPH,text="Ultimo mes",font=("Arial", 22),bg="#c60000",fg="white")
        lbl_msj2.pack()
        lbl_graph2 = Label(frameGRAPH,image=self.graph2,compound="top", height=270)
        lbl_graph2.pack()

class insertarVentas(Frame):
    def __init__(self, master, controlador):
        super().__init__(master)
        self.controlador = controlador

class actualizarVentas(Frame):
    def __init__(self, master, controlador):
        super().__init__(master)
        self.controlador = controlador

class eliminarVentas(Frame):
    def __init__(self, master, controlador):
        super().__init__(master)
        self.controlador = controlador