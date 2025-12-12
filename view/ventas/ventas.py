from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from view.header import *
from model import ventasCRUD
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from controller.funciones import obtener_imagen
from view.ventas.menu import *

COLOR_FRAME = "#c60000"

class mainVentas(Frame):
    def __init__(self, master, controlador):
        super().__init__(master)
        self.controlador = controlador
        head = header(self, controlador)
        head.pack(fill="x")
        head.titulo = "Sales"
        self.id_seleccionado = None
        
        container = Frame(self)
        container.pack(fill="both", expand=True)

        canvas = Canvas(container, bg="#ffffff", highlightthickness=0)
        vsb = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        body = Frame(canvas, bg="#ffffff")
        window_id = canvas.create_window((0, 0), window=body, anchor="nw")

        def _on_body_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        body.bind("<Configure>", _on_body_configure)

        def _on_canvas_configure(event):
            canvas.itemconfig(window_id, width=event.width)
            if event.height > 1:
                body.rowconfigure(0, minsize=event.height)

        canvas.bind("<Configure>", _on_canvas_configure)

        def _on_mousewheel(event):
            if event.delta:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _on_linux_scroll_up(event):
            canvas.yview_scroll(-1, "units")

        def _on_linux_scroll_down(event):
            canvas.yview_scroll(1, "units")

        def _bind_mouse(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            canvas.bind_all("<Button-4>", _on_linux_scroll_up)
            canvas.bind_all("<Button-5>", _on_linux_scroll_down)

        def _unbind_mouse(event):
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")

        container.bind("<Enter>", _bind_mouse)
        container.bind("<Leave>", _unbind_mouse)
        self.bind("<Destroy>", _unbind_mouse)
        
        body.columnconfigure(0, weight=1, uniform="cols")
        body.columnconfigure(1, weight=1, uniform="cols")

        self.frameVENTA = Frame(body, bg=COLOR_FRAME)
        self.frameVENTA.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        frameDETALLES = Frame(body, bg=COLOR_FRAME)
        frameDETALLES.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.frame_filtrar = Frame(self.frameVENTA, bg=COLOR_FRAME)
        self.frame_filtrar.pack(pady=20)

        for i in range(4):
            self.frame_filtrar.columnconfigure(i, weight=1)
        
        self.lbl_filtrar = Label(self.frame_filtrar, text="Filter by:", font=("Arial", 22),
                            bg=COLOR_FRAME, fg="white")
        self.lbl_filtrar.grid(row=0, column=0, sticky="w")

        columnas = ["All","ID", "Date","Time", "Total"]

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview", font=("Arial", 14), rowheight=35)
        style.configure("Custom.Treeview.Heading", background="#4A90E2", foreground="white",
                        font=("Arial", 16, "bold"), relief="flat")
        style.map("Custom.Treeview.Heading", background=[("active", "#357ABD")])
        style.configure("Custom.TCombobox", fieldbackground="#4A90E2", background="#4A90E2",
                        foreground="black", bordercolor="#4A90E2", lightcolor="#4A90E2",
                        arrowcolor="white", font=("Arial", 20))
        style.map("Custom.TCombobox", fieldbackground=[("readonly", "#4A90E2")],
                  foreground=[("readonly", "white")], selectbackground=[("readonly", "#4A90E2")],
                  selectforeground=[("readonly", "white")])

        self.combo_campo = ttk.Combobox(self.frame_filtrar, values=columnas, state="readonly", style="Custom.TCombobox")
        self.combo_campo.configure(font=("Arial", 22),width=10)
        self.combo_campo.current(0)
        self.combo_campo.grid(row=0, column=1, sticky="nsew", padx=5)
        
        def campo_seleccionado(event):
            valor = self.combo_campo.get()
            match valor:
                case "Date":
                    self.combo_valor.config(values=filtros_fecha)
                case "Total":
                    self.combo_valor.config(values=filtros_precio)
                case _:
                    self.combo_valor.config(values=[])
            self.combo_valor.set("")
        self.combo_campo.bind("<<ComboboxSelected>>", campo_seleccionado)

        filtros_fecha = ["Newest","Oldest"]
        filtros_precio = ["Highest","Lowest"]
        self.combo_valor = ttk.Combobox(self.frame_filtrar, values=[], style="Custom.TCombobox")
        self.combo_valor.configure(font=("Arial", 22),width=10)
        self.combo_valor.grid(row=0, column=2, sticky="nsew", padx=5)
        
        self.btn_buscar = Button(self.frame_filtrar, text="Search", font=("Arial", 13, "bold"),
                            command=lambda: self.buscar_venta(self.combo_campo.get(),self.combo_valor.get()))
        self.btn_buscar.grid(row=0, column=3, sticky="nsew", padx=5)

        columnas_ventas = ["ID", "Date","Time", "Total"]
        frame_tablaventas = Frame(self.frameVENTA,height=200)
        frame_tablaventas.pack(fill="x")
        self.tabla = tabla(
            frame_tablaventas,
            columnas_ventas,
            callback_seleccion=self.actualizar_id
        )

        self.tabla.bind("<Enter>", _unbind_mouse)
        self.tabla.bind("<Leave>", _bind_mouse)

        def seleccionar_fila(event):
            fila = self.tabla.selection()
            if fila:
                valores = self.tabla.item(fila[0], "values")
                self.id_seleccionado = valores[0]
            self.ver_detalles()
        self.tabla.bind("<<TreeviewSelect>>", seleccionar_fila)

        self.frame_botones = Frame(self.frameVENTA, bg=COLOR_FRAME)
        self.frame_botones.pack(padx=20, pady=10)

        self.btn_anadir = Button(self.frame_botones, text="Add", font=("Arial", 16, "bold"), width=15,
                            fg="white", bg="#86B7D6",
                            command=lambda: self.controlador.mostrar_pantalla("insertarventas"))
        self.btn_anadir.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.btn_actualizar = Button(self.frame_botones, text="Update", font=("Arial", 16, "bold"), width=15,
                                fg="white", bg="#86B7D6",
                                command=lambda: self.validar_id())
        self.btn_actualizar.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.btn_eliminar = Button(self.frame_botones, text="Delete", font=("Arial", 16, "bold"), width=15,
                              fg="white", bg="#86B7D6",
                              command=lambda: self.eliminar_venta())
        self.btn_eliminar.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        self.buscar_venta("All","")

        self.modo_actual = "wide"
        self.frameVENTA.bind("<Configure>", self.ajustar_layout)

        lbl_titulo = Label(frameDETALLES,text="Sale Details",font=("Arial", 22),
                            bg=COLOR_FRAME, fg="white")
        lbl_titulo.pack(pady=20)

        columnas_detalles = ["ID", "Sale_ID", "Product","Qty","Subtotal"]
        frame_tabladetalles = Frame(frameDETALLES,height=200)
        frame_tabladetalles.pack(fill="x")

        self.tabla2 = tabla(
            frame_tabladetalles,
            columnas_detalles,
            anchos=[5,15,120,20,30]
        )
        
        for child in frame_tabladetalles.winfo_children():
            if isinstance(child, ttk.Scrollbar):
                child.pack_forget() 

        frameREPORTES = Frame(body, bg=COLOR_FRAME, height=1200) 
        frameREPORTES.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
        frameREPORTES.pack_propagate(False)
        
        frame_header_rep = Frame(frameREPORTES, bg=COLOR_FRAME)
        frame_header_rep.pack(anchor="nw",padx=(20,0),pady=(30,5))

        lbl_reportes = Label(frame_header_rep, text="SALES REPORTS", 
                             font=("Arial", 24), bg=COLOR_FRAME, fg="white")
        lbl_reportes.pack(side="left",pady=10)

        lbl_seccion1 = Label(frameREPORTES, text="Sales by Product", 
                             font=("Arial", 20), bg=COLOR_FRAME, fg="white")
        lbl_seccion1.pack(anchor="w", padx=40,pady=5)

        frame_botones_rep1 = Frame(frameREPORTES, bg=COLOR_FRAME)
        frame_botones_rep1.pack(padx=40,anchor="w")
        
        Button(frame_botones_rep1, text="Weekly", font=("Arial", 16, "bold"), width=12, fg="white", bg="#86B7D6",
               command=lambda: self.actualizar_grafico_vp("Weekly")).grid(row=0,column=0,padx=5,pady=2)
        Button(frame_botones_rep1, text="Monthly", font=("Arial", 16, "bold"), width=12, fg="white", bg="#86B7D6",
               command=lambda: self.actualizar_grafico_vp("Monthly")).grid(row=0,column=1,padx=5,pady=2)
        Button(frame_botones_rep1, text="Quarterly", font=("Arial", 16, "bold"), width=12, fg="white", bg="#86B7D6",
               command=lambda: self.actualizar_grafico_vp("Quarterly")).grid(row=0,column=2,padx=5,pady=2)
         
        self.lbl_imagen_grafico_vp = Label(frameREPORTES, bg=COLOR_FRAME)
        self.lbl_imagen_grafico_vp.pack(padx=(40,0), pady=10,anchor="w")

        lbl_seccion2 = Label(frameREPORTES, text="Business Income", 
                             font=("Arial", 20), bg=COLOR_FRAME, fg="white")
        lbl_seccion2.pack(anchor="w", padx=40, pady=(20, 5))

        frame_botones_rep2 = Frame(frameREPORTES, bg=COLOR_FRAME)
        frame_botones_rep2.pack(padx=40, anchor="w")

        Button(frame_botones_rep2, text="Weekly", font=("Arial", 16, "bold"), width=12, fg="white", bg="#86B7D6",
               command=lambda: self.actualizar_grafico_ingresos("Weekly")).grid(row=0, column=0, padx=5, pady=2)
        Button(frame_botones_rep2, text="Monthly", font=("Arial", 16, "bold"), width=12, fg="white", bg="#86B7D6",
               command=lambda: self.actualizar_grafico_ingresos("Monthly")).grid(row=0, column=1, padx=5, pady=2)
        Button(frame_botones_rep2, text="Quarterly", font=("Arial", 16, "bold"), width=12, fg="white", bg="#86B7D6",
               command=lambda: self.actualizar_grafico_ingresos("Quarterly")).grid(row=0, column=2, padx=5, pady=2)

        self.lbl_imagen_grafico_ingresos = Label(frameREPORTES, bg=COLOR_FRAME)
        self.lbl_imagen_grafico_ingresos.pack(padx=(40, 0), pady=10, anchor="w")
        
        self.actualizar_grafico_vp("Weekly") 
        self.actualizar_grafico_ingresos("Weekly")

    def ajustar_layout(self, event):
        if event.width < 600 and self.modo_actual != "compact":
            self.lbl_filtrar.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0,5))
            self.combo_campo.grid(row=1, column=0, sticky="ew", padx=2)
            self.combo_valor.grid(row=1, column=1, sticky="ew", padx=2)
            self.btn_buscar.grid(row=1, column=2, sticky="ew", padx=2)
            
            self.btn_anadir.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
            self.btn_actualizar.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
            self.btn_eliminar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
            
            self.modo_actual = "compact"

        elif event.width >= 600 and self.modo_actual != "wide":
            self.lbl_filtrar.grid(row=0, column=0, columnspan=1, sticky="w", pady=0)
            self.combo_campo.grid(row=0, column=1, sticky="nsew", padx=5)
            self.combo_valor.grid(row=0, column=2, sticky="nsew", padx=5)
            self.btn_buscar.grid(row=0, column=3, sticky="nsew", padx=5)

            self.btn_anadir.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
            self.btn_actualizar.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
            self.btn_eliminar.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
            
            self.modo_actual = "wide"

    def actualizar_grafico_vp(self, periodo):
        datos = ventasCRUD.reportes.obtener_datos_grafico(periodo)
        if not datos:
            self.lbl_imagen_grafico_vp.config(image="", text="No data for this period")
            return
        self.generar_imagen_grafico_vp(datos, periodo)

    def generar_imagen_grafico_vp(self, datos, periodo):
        productos = [fila[0] for fila in datos]
        cantidades = [float(fila[1]) for fila in datos]
        totales = [float(fila[2]) for fila in datos]

        fig, ax1 = plt.subplots(figsize=(10, 4))
        
        ax1.set_title(f'Sales by Product ({periodo})', fontsize=14)
        color = 'tab:blue'
        ax1.set_xlabel('Product')
        ax1.set_ylabel('Quantity Sold (Units)', color=color)
        ax1.bar(productos, cantidades, color=color, alpha=0.6, label='Units')
        ax1.tick_params(axis='y', labelcolor=color)
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=15, ha="right")

        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Revenue Generated ($)', color=color)  
        ax2.plot(productos, totales, color=color, marker='o', linewidth=2, label='Revenue')
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        ruta_carpeta = os.path.join(base_dir, "images")
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)
            
        nombre_archivo = f"grafico_ventas_{periodo}.png"
        ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
        plt.savefig(ruta_completa)
        plt.close(fig)

        self.img_grafico = obtener_imagen(nombre_archivo, 800, 450)
        if self.img_grafico:
            self.lbl_imagen_grafico_vp.config(image=self.img_grafico, text="")
        else:
            self.lbl_imagen_grafico_vp.config(text="Error loading image")
    
    def actualizar_grafico_ingresos(self, periodo):
        datos = ventasCRUD.reportes.obtener_ingresos_grafico(periodo)
        if not datos:
            self.lbl_imagen_grafico_ingresos.config(image="", text="No income data for this period")
            return
        self.generar_imagen_grafico_ingresos(datos, periodo)

    def generar_imagen_grafico_ingresos(self, datos, periodo):
        fechas = [fila[0] for fila in datos]
        ingresos = [float(fila[1]) for fila in datos]

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.set_title(f'Business Income ({periodo})', fontsize=14)
        ax.set_xlabel('Date')
        ax.set_ylabel('Total Income ($)')
        ax.plot(fechas, ingresos, marker='o', linestyle='-', color='green', linewidth=2)
        fig.autofmt_xdate() 
        fig.tight_layout()

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        ruta_carpeta = os.path.join(base_dir, "images")
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)
            
        nombre_archivo = f"grafico_ingresos_{periodo}.png"
        ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
        plt.savefig(ruta_completa)
        plt.close(fig)

        self.img_grafico_ingresos = obtener_imagen(nombre_archivo, 800, 420)
        if self.img_grafico_ingresos:
            self.lbl_imagen_grafico_ingresos.config(image=self.img_grafico_ingresos, text="")
        else:
            self.lbl_imagen_grafico_ingresos.config(text="Error loading income chart")

    def buscar_venta(self,campo,valor):
        registros = ventasCRUD.ventas.buscar(campo,valor)
        self.tabla.cargar(registros)

    def eliminar_venta(self):
        if self.id_seleccionado == 0:
            messagebox.showinfo("Notice", "Select a record to continue.")
            return
        confirmar = messagebox.askyesno(
            "WARNING",
            f"Deleting sale ID = {self.id_seleccionado} will also delete all associated details.\n\nContinue?"
        )
        if not confirmar:
            return

        ok_det = ventasCRUD.detalleVenta.eliminar_por_venta(self.id_seleccionado)
        if not ok_det:
            messagebox.showerror("Error", "Could not delete sale details. Operation cancelled.")
            return

        ok_venta = ventasCRUD.ventas.eliminar(self.id_seleccionado)
        if ok_venta:
            messagebox.showinfo("Success", f"Sale ID = {self.id_seleccionado} and details deleted successfully.")
            self.buscar_venta("All","")
            for row in self.tabla2.get_children():
                self.tabla2.delete(row)
            self.id_seleccionado = 0
            self.actualizar_grafico_vp("Weekly") 
            self.actualizar_grafico_ingresos("Weekly")
        else:
            messagebox.showerror("Error", "Could not delete sale record.")

    def ver_detalles(self):
        registros = ventasCRUD.detalleVenta.buscar(self.id_seleccionado)
        for row in self.tabla2.get_children():
            self.tabla2.delete(row)
        for fila in registros:
            self.tabla2.insert("", "end", values=fila)

    def validar_id(self):
        if self.id_seleccionado == None:
            messagebox.showwarning("Warning","Select a record to continue")
        else:
            self.controlador.mostrar_pantalla("actualizarventas",self.id_seleccionado)

    def actualizar_id(self, id_recibido):
        self.id_seleccionado = id_recibido


class insertarVentas(Frame):
    def __init__(self, master, controlador,accion,id_seleccionado=None):
        super().__init__(master)
        self.controlador = controlador
        head = header(self, controlador)
        head.pack(fill="x")
        self.id_seleccionado = id_seleccionado
        
        container = Frame(self)
        container.pack(fill="both", expand=True, padx=30, pady=30)

        canvas = Canvas(container, bg=COLOR_FRAME, highlightthickness=0)
        vsb = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        body = Frame(canvas, bg=COLOR_FRAME)
        window_id = canvas.create_window((0, 0), window=body, anchor="nw")

        def _on_body_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        body.bind("<Configure>", _on_body_configure)

        def _on_canvas_configure(event):
            req_h = body.winfo_reqheight()
            canvas.itemconfig(window_id, width=event.width, height=max(event.height, req_h))
            canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.bind("<Configure>", _on_canvas_configure)

        def _on_mousewheel(event):
            if event.delta:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _on_linux_scroll_up(event):
            canvas.yview_scroll(-1, "units")

        def _on_linux_scroll_down(event):
            canvas.yview_scroll(1, "units")

        def _bind_mouse(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            canvas.bind_all("<Button-4>", _on_linux_scroll_up)
            canvas.bind_all("<Button-5>", _on_linux_scroll_down)

        def _unbind_mouse(event):
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")

        container.bind("<Enter>", _bind_mouse)
        container.bind("<Leave>", _unbind_mouse)
        self.bind("<Destroy>", _unbind_mouse)

        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        precios_result = ventasCRUD.menu.obtenerPrecios()
        self.precios = [fila[0] for fila in precios_result] if precios_result else []

        frame_prod = Frame(body,bg=COLOR_FRAME)
        frame_total = Frame(body,bg=COLOR_FRAME)

        #frame prod
        lbl_prod = Label(frame_prod,text="Product",font=("Arial", 24),fg="white",bg=COLOR_FRAME)
        lbl_prod.grid(row=0,column=0)

        lbl_cant = Label(frame_prod,text="Quantity",font=("Arial", 24),fg="white",bg=COLOR_FRAME)
        lbl_cant.grid(row=0,column=1)

        productos_result = ventasCRUD.menu.obtenerProductos()
        self.opciones_prod = [fila[0] for fila in productos_result] if productos_result else []

        for i in range(len(self.opciones_prod)):
            lbl = Label(frame_prod,text=self.opciones_prod[i],font=("Arial", 20),fg="black",bg="white", highlightthickness=2,
                            highlightbackground="black",
                            highlightcolor="black")
            lbl.grid(row=i+1,column=0,sticky="nsew")
        
        self.spinbox_prod = []

        for i in range(len(self.opciones_prod)):
            def make_vcmd(idx):
                return (self.register(lambda val, idx=idx: self.validar_spin(val, idx)), "%P")
            vcmd = make_vcmd(i)
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

        btn_agregar = Button(frame_total,text="Add Sale",width=20,font=("Arial",20),command=lambda:self.crearVenta(),bg="#669BBC",fg="white")
        btn_agregar.pack(pady=5)
        self.total_venta = 0
        btn_volver = Button(frame_total,text="Back",width=20,font=("Arial",20),command=lambda:self.controlador.mostrar_pantalla("mainventas"),bg="#669BBC",fg="white")
        btn_volver.pack(pady=5)

        f = len(self.opciones_prod)+1 
        self.fecha = DateEntry(
                 frame_prod,
                 date_pattern="yyyy-mm-dd", # Patrón ISO
                 locale="en_US",
                 font=("Arial", 20),
                 width=12
                )
        self.fecha.grid(row=f+1,column=1,pady=5)
        lbl_fecha = Label(frame_prod,text="Date: ",font=("Arial", 20),bg=COLOR_FRAME,fg="white")
        lbl_fecha.grid(row=f+1,column=0,pady=5,sticky="e")

        lbl_hora = Label(frame_prod,text="Time: ",font=("Arial", 20),bg=COLOR_FRAME,fg="white")
        lbl_hora.grid(row=f+2,column=0,pady=5,sticky="e")

        frame_hora = Frame(frame_prod,bg=COLOR_FRAME)
        frame_hora.grid(row=f+2,column=1,sticky="nsew")
        # --- CORRECCIÓN: HORARIO DE 19 A 23 ---
        self.spin_hora = Spinbox(
            frame_hora,
            from_=19, to=23,
            font=("Arial", 20),
            width=3
        )
        minutos = [f"{i:02d}" for i in range(60)]
        self.spin_minuto = Spinbox(
            frame_hora,
            values=minutos,
            font=("Arial", 20),
            width=3
        )

        self.spin_hora.grid(row=0,column=0)
        lbl_min = Label(frame_hora,text=":",font=("Arial", 30,"bold"),bg=COLOR_FRAME,fg="white")
        lbl_min.grid(row=0,column=1,pady=5,sticky="e")
        self.spin_minuto.grid(row=0,column=2)

        btn_menu = Button(frame_prod,text="Modify Menu Prices",font=("Arial",16),command=lambda:self.controlador.mostrar_pantalla("menu_crud"),bg="#669BBC",fg="white")
        btn_menu.grid(row=f+3,column=0,columnspan=2,sticky="nsew",padx=80)

        match accion:
            case "agregar":
                head.titulo = "Register Sale"
                frame_prod.grid(row=0,column=0,sticky="nsew",padx=(40,10),pady=50)
                frame_total.grid(row=0,column=1,sticky="nsew",padx=5,pady=50)
            case "actualizar":
                head.titulo = "Update Sale"
                frame_prod.grid(row=1,column=0,sticky="nsew",padx=(40,10),pady=5)
                frame_total.grid(row=1,column=1,sticky="nsew",padx=5,pady=5)
                body.rowconfigure(1, weight=1)
                frame_tablas = Frame(body,bg="white",height=260)
                frame_tablas.pack_propagate(False)
                frame_tablas.grid(row=0,column=0,sticky="nsew",pady=(20,0),padx=10,columnspan=2)
                columnas_ventas = ["ID", "Date","Time", "Total"]
                frame_tablaventas = Frame(frame_tablas,height=80)
                frame_tablaventas.pack_propagate(False)
                frame_tablaventas.pack(fill="x")
                self.tabla = tabla(
                    frame_tablaventas,
                    columnas_ventas
                )
                self.registros_venta = ventasCRUD.ventas.buscar("ID",self.id_seleccionado)
                self.tabla.cargar(self.registros_venta)

                columnas_detalle = ["ID", "Sale_ID", "Product","Qty","Subtotal"]
                frame_tabladetalles = Frame(frame_tablas,height=200)
                frame_tabladetalles.pack(fill="x")
                frame_tabladetalles.pack_propagate(False)
                self.tabla2 = tabla(
                    frame_tabladetalles,
                    columnas_detalle,
                    anchos=[5,15,120,20,30]
                )
                self.registros_detalles = ventasCRUD.detalleVenta.buscar(self.id_seleccionado)
                self.tabla2.cargar(self.registros_detalles)

                btn_agregar.config(text="Update Sale",command=lambda:self.actualizarVenta())

                self.cantidades = ventasCRUD.detalleVenta.obtener_cantidades(self.id_seleccionado)
                if not isinstance(self.cantidades, list) or len(self.cantidades) != len(self.opciones_prod):
                    self.cantidades = [0]*len(self.opciones_prod)
                registros = ventasCRUD.ventas.obtener_hora(self.id_seleccionado)

                fecha = registros[0][0]
                self.fecha.set_date(fecha)
                hora = str(registros[0][1])
                hora = hora.split(":")
                self.spin_hora.delete(0,"end")
                self.spin_minuto.delete(0,"end")
                self.spin_hora.insert(0,hora[0])
                self.spin_minuto.insert(0,hora[1])
            
                i=0
                for cantidad in self.cantidades:
                    self.spinbox_prod[i].delete(0, "end")
                    self.spinbox_prod[i].insert(0, str(cantidad))
                    i+=1
                total = 0
                for idx in range(len(self.opciones_prod)):
                    precio = float(self.precios[idx]) if idx < len(self.precios) else 0
                    total += int(self.cantidades[idx]) * precio
                self.total_venta = total
                self.lbl_total.config(text=f"$ {total:.2f}")

    def spin_cambio(self, index, valor):
        cant_prod = []
        for i in range(len(self.spinbox_prod)):
            val = self.spinbox_prod[i].get()
            try:
                num = int(val) if val != "" else 0
            except:
                num = 0
            cant_prod.append(num)
        total = 0
        for i in range(len(self.opciones_prod)):
            price = float(self.precios[i]) if i < len(self.precios) else 0
            total += float(cant_prod[i]) * float(price)
        self.lbl_total.config(text=f"$ {total:.2f}")
        self.total_venta = total

    def validar_spin(self, nuevo_valor, index):
        if nuevo_valor.isdigit() or nuevo_valor == "":
            self.spin_cambio(index, nuevo_valor)
            return True
        return False

    def limpiar(self):
        for i in range(len(self.spinbox_prod)):
            self.spinbox_prod[i].delete(0, "end")
            self.spinbox_prod[i].insert(0, "0")
        self.spin_hora.delete(0, "end")
        self.spin_hora.insert(0, "19")
        self.spin_minuto.delete(0, "end")
        self.spin_minuto.insert(0, "00")
        self.lbl_total.config(text="$_________")

    def crearVenta(self):
        if self.total_venta == 0:
            messagebox.showwarning("Warning","Enter products to continue")
            return
        try:
            fecha = self.fecha.get_date()
            int(self.spin_hora.get())
            int(self.spin_minuto.get())
            hora = f"{self.spin_hora.get()}:{self.spin_minuto.get()}"
            insertar,id = ventasCRUD.ventas.insertar(self.total_venta,fecha,hora)
            if not insertar:
                messagebox.showerror("Error","Could not insert sale.")
                return
            insertar_detalle_ok = True
            for i in range(len(self.spinbox_prod)):
                cantidad = int(self.spinbox_prod[i].get())
                if cantidad > 0:
                    ok = ventasCRUD.detalleVenta.insertar(id,self.opciones_prod[i],cantidad)
                    if not ok:
                        insertar_detalle_ok = False
            if insertar and insertar_detalle_ok:
                messagebox.showinfo("Success", "Sale saved successfully.")
                self.limpiar()
            else:
                messagebox.showerror("Error", "An error occurred saving sale details.")
        except ValueError:
                messagebox.showerror("Error", "Enter numbers only")

    def actualizarVenta(self):
        if self.id_seleccionado is None:
            messagebox.showerror("Error", "Sale ID undefined.")
            return
        try:
            int(self.spin_hora.get())
            int(self.spin_minuto.get())
        except ValueError:
            messagebox.showerror("Error", "Enter numbers only")
            return
        new_quantities = []
        for sp in self.spinbox_prod:
            try:
                new_quantities.append(int(sp.get()))
            except:
                messagebox.showerror("Error", "Enter numbers only")
                return

        if all(q == 0 for q in new_quantities):
            confirmar = messagebox.askyesno("Confirm Deletion", "All products are 0. Do you want to delete the entire sale?")
            if not confirmar:
                return
            ok_det = ventasCRUD.detalleVenta.eliminar_por_venta(self.id_seleccionado)
            ok_venta = ventasCRUD.ventas.eliminar(self.id_seleccionado)
            if ok_det and ok_venta:
                messagebox.showinfo("Success", "Sale and details deleted successfully.")
                self.controlador.mostrar_pantalla("mainventas")
            else:
                messagebox.showerror("Error", "Could not fully delete sale.")
            return

        any_error = False
        for i in range(len(self.opciones_prod)):
            prev = int(self.cantidades[i]) if i < len(self.cantidades) else 0
            new = int(new_quantities[i])
            if new == prev:
                continue

            if prev == 0 and new > 0:
                ok = ventasCRUD.detalleVenta.insertar(self.id_seleccionado, self.opciones_prod[i], new)
                if not ok:
                    any_error = True
            elif prev > 0 and new == 0:
                id_det = ventasCRUD.detalleVenta.obtener_id_detalle(self.id_seleccionado, i+1)
                if id_det is None:
                    any_error = True
                else:
                    ok = ventasCRUD.detalleVenta.eliminar(id_det)
                    if not ok:
                        any_error = True
            elif prev > 0 and new > 0:
                id_det = ventasCRUD.detalleVenta.obtener_id_detalle(self.id_seleccionado, i+1)
                if id_det is None:
                    ok = ventasCRUD.detalleVenta.insertar(self.id_seleccionado, self.opciones_prod[i], new)
                    if not ok:
                        any_error = True
                else:
                    ok = ventasCRUD.detalleVenta.actualizar(id_det, new, self.opciones_prod[i])
                    if not ok:
                        any_error = True

        detalles = ventasCRUD.detalleVenta.buscar(self.id_seleccionado)
        nuevo_total = 0.0
        for d in detalles:
            try:
                nuevo_total += float(d[4])
            except:
                pass
        fecha = self.fecha.get_date()
        hora = f"{self.spin_hora.get()}:{self.spin_minuto.get()}"
        ok_total = ventasCRUD.ventas.actualizar_total(self.id_seleccionado, nuevo_total,fecha,hora)
        if any_error or not ok_total:
            messagebox.showerror("Error", "Errors occurred updating sale. Check DB.")
        else:
            messagebox.showinfo("Success", "Sale updated successfully.")
            self.controlador.mostrar_pantalla("mainventas")

class tabla(ttk.Treeview):
    def __init__(self, parent, columnas, callback_seleccion=None,anchos=None):
        self.columnas = columnas
        self.callback = callback_seleccion  
        chartframe = Frame(parent, bg="white")
        chartframe.pack(fill="x")
        table_container = Frame(chartframe, bg="white")
        table_container.pack(fill="x")
        super().__init__(
            table_container,
            columns=self.columnas,
            show="headings",
            selectmode="browse",
            style="Custom.Treeview"
        )
        vsb = ttk.Scrollbar(
            table_container, orient="vertical", command=self.yview
        )
        self.configure(yscrollcommand=vsb.set)
        if anchos == None:
            for col in self.columnas:
                self.heading(col, text=col)
                self.column(col, anchor="center", width=120)
        else:
            for col,an in zip(self.columnas,anchos):
                self.heading(col, text=col)
                self.column(col, anchor="center", width=an)

        self.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        table_container.rowconfigure(0, weight=1)
        table_container.columnconfigure(0, weight=1)

    def limpiar(self):
        for row in self.get_children():
            self.delete(row)

    def cargar(self, registros):
        self.limpiar()
        for fila in registros:
            self.insert("", "end", values=fila)