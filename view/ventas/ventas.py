from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from view.header import *
from model import ventasCRUD
import matplotlib.pyplot as plt
import os
from controller.funciones import obtener_imagen

COLOR_FRAME = "#c60000"

class mainVentas(Frame):
    def __init__(self, master, controlador):
        super().__init__(master)
        self.controlador = controlador
        head = header(self, controlador)
        head.pack(fill="x")
        head.titulo = "Ventas"

        # --- SCROLLABLE BODY (Lógica Corregida) ---
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

        # --- Scroll con Mouse/Touchpad ---
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
        # --- fin scrollable ---

        self.id_seleccionado = 0
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)

        frameVENTA = Frame(body, bg=COLOR_FRAME)
        frameVENTA.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        frameVENTA.pack_propagate(False)
        
        frameDETALLES = Frame(body, bg=COLOR_FRAME)
        frameDETALLES.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        frameDETALLES.pack_propagate(False)

        # --- FRAME REPORTES (Modificado para gráficos) ---
        frameREPORTES = Frame(body, bg=COLOR_FRAME, height=600)
        frameREPORTES.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
        frameREPORTES.pack_propagate(False)
        
        # Contenedor para título y botones
        frame_header_rep = Frame(frameREPORTES, bg=COLOR_FRAME)
        frame_header_rep.pack(fill="x", pady=10)

        lbl_reportes = Label(frame_header_rep, text="REPORTES DE VENTA", 
                             font=("Arial", 22), bg=COLOR_FRAME, fg="white")
        lbl_reportes.pack(side="left", padx=20)

        # Botones de periodo
        frame_botones_rep = Frame(frame_header_rep, bg=COLOR_FRAME)
        frame_botones_rep.pack(side="right", padx=20)

        Button(frame_botones_rep, text="Semanal", font=("Arial", 12),
               command=lambda: self.actualizar_grafico("Semanal")).pack(side="left", padx=5)
        Button(frame_botones_rep, text="Mensual", font=("Arial", 12),
               command=lambda: self.actualizar_grafico("Mensual")).pack(side="left", padx=5)
        Button(frame_botones_rep, text="Trimestral", font=("Arial", 12),
               command=lambda: self.actualizar_grafico("Trimestral")).pack(side="left", padx=5)

        # Label para mostrar la imagen del gráfico
        self.lbl_imagen_grafico = Label(frameREPORTES, bg=COLOR_FRAME)
        self.lbl_imagen_grafico.pack(expand=True, fill="both", padx=10, pady=10)
        # --------------------------------------------------

        #FRAME VENTA - FILTRAR
        frame_filtrar = Frame(frameVENTA, bg=COLOR_FRAME)
        frame_filtrar.pack(pady=20)

        for i in range(4):
            frame_filtrar.columnconfigure(i, weight=0)
        frame_filtrar.rowconfigure(0, weight=0)
        
        lbl_filtrar = Label(frame_filtrar, text="Filtrar por:", font=("Arial", 22),
                            bg=COLOR_FRAME, fg="white")
        lbl_filtrar.grid(row=0, column=0, sticky="w")

        columnas = ["Todo","ID", "Fecha", "Total"]

        # ESTILOS
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview", font=("Arial", 16), rowheight=35)
        style.configure("Custom.Treeview.Heading", background="#4A90E2", foreground="white",
                        font=("Arial", 18, "bold"), relief="flat")
        style.map("Custom.Treeview.Heading", background=[("active", "#357ABD")])
        style.configure("Custom.TCombobox", fieldbackground="#4A90E2", background="#4A90E2",
                        foreground="black", bordercolor="#4A90E2", lightcolor="#4A90E2",
                        arrowcolor="white", font=("Arial", 22))
        style.map("Custom.TCombobox", fieldbackground=[("readonly", "#4A90E2")],
                  foreground=[("readonly", "white")], selectbackground=[("readonly", "#4A90E2")],
                  selectforeground=[("readonly", "white")])

        # COMBOBOX
        combo_campo = ttk.Combobox(frame_filtrar, values=columnas, state="readonly", style="Custom.TCombobox")
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
        combo_valor = ttk.Combobox(frame_filtrar, values=[], style="Custom.TCombobox")
        combo_valor.configure(font=("Arial", 22),width=10)
        combo_valor.grid(row=0, column=2, sticky="nsew")
        
        btn_buscar = Button(frame_filtrar, text="Buscar", font=("Arial", 13, "bold"),
                            command=lambda: self.buscar_venta(combo_campo.get(),combo_valor.get()))
        btn_buscar.grid(row=0, column=3, sticky="nsew")

        # TABLA VENTAS
        columnas_ventas = ["ID", "Fecha","Hora", "Total"]
        frame_tablaventas = Frame(frameVENTA,height=200)
        frame_tablaventas.pack(fill="x")
        self.tabla = tabla(
            frame_tablaventas,
            columnas_ventas,
            callback_seleccion=self.actualizar_id
        )

        # Fix: Desactivar scroll global SOLO en la tabla de ventas
        self.tabla.bind("<Enter>", _unbind_mouse)
        self.tabla.bind("<Leave>", _bind_mouse)

        def seleccionar_fila(event):
            fila = self.tabla.selection()
            if fila:
                valores = self.tabla.item(fila[0], "values")
                self.id_seleccionado = valores[0]
            self.ver_detalles()
        self.tabla.bind("<<TreeviewSelect>>", seleccionar_fila)

        frame_botones = Frame(frameVENTA, bg=COLOR_FRAME)
        frame_botones.pack_propagate(False)
        frame_botones.pack(padx=20, pady=10)

        btn_añadir = Button(frame_botones, text="Añadir", font=("Arial", 16, "bold"), width=15,
                            fg="white", bg="#86B7D6",
                            command=lambda: self.controlador.mostrar_pantalla("insertarventas"))
        btn_añadir.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        btn_actualizar = Button(frame_botones, text="Actualizar", font=("Arial", 16, "bold"), width=15,
                                fg="white", bg="#86B7D6",
                                command=lambda: self.controlador.mostrar_pantalla("actualizarventas",self.id_seleccionado))
        btn_actualizar.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        btn_eliminar = Button(frame_botones, text="Eliminar", font=("Arial", 16, "bold"), width=15,
                              fg="white", bg="#86B7D6",
                              command=lambda: self.eliminar_venta())
        btn_eliminar.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        self.buscar_venta("Todo","")

        # FRAME DETALLES
        lbl_titulo = Label(frameDETALLES,text="Detalles de venta",font=("Arial", 22),
                            bg=COLOR_FRAME, fg="white")
        lbl_titulo.pack(pady=20)

        columnas_detalles = ["ID", "ID_venta", "Producto","Cantidad","Subtotal"]
        frame_tabladetalles = Frame(frameDETALLES,height=200)
        frame_tabladetalles.pack(fill="x")

        self.tabla2 = tabla(
            frame_tabladetalles,
            columnas_detalles,
            anchos=[5,15,120,20,30]
        )
        
        # --- NUEVO: Ocultar Scrollbar de Detalles ---
        # Buscamos el widget Scrollbar dentro del frame y lo ocultamos
        for child in frame_tabladetalles.winfo_children():
            if isinstance(child, ttk.Scrollbar):
                child.pack_forget() # Ocultar
        # --------------------------------------------

        # Cargar gráfico inicial
        self.actualizar_grafico("Semanal")

    # --- LÓGICA DE GRÁFICOS ---
    def actualizar_grafico(self, periodo):
        datos = ventasCRUD.reportes.obtener_datos_grafico(periodo)
        if not datos:
            self.lbl_imagen_grafico.config(image="", text="No hay datos para este periodo")
            return
        
        self.generar_imagen_grafico(datos, periodo)

    def generar_imagen_grafico(self, datos, periodo):
        productos = [fila[0] for fila in datos]
        cantidades = [float(fila[1]) for fila in datos]
        totales = [float(fila[2]) for fila in datos]

        # Crear gráfico
        fig, ax1 = plt.subplots(figsize=(10, 4))
        
        ax1.set_title(f'Ventas por Producto ({periodo})', fontsize=14)
        color = 'tab:blue'
        ax1.set_xlabel('Producto')
        ax1.set_ylabel('Cantidad Vendida (Unidades)', color=color)
        ax1.bar(productos, cantidades, color=color, alpha=0.6, label='Unidades')
        ax1.tick_params(axis='y', labelcolor=color)
        
        # Rotar textos para que se lean bien
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=15, ha="right")

        # Eje secundario (Dinero)
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Dinero Generado ($)', color=color)  
        ax2.plot(productos, totales, color=color, marker='o', linewidth=2, label='Dinero')
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()

        # GUARDADO EN CARPETA IMAGES (RAÍZ)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        ruta_carpeta = os.path.join(base_dir, "images")
        
        if not os.path.exists(ruta_carpeta):
            os.makedirs(ruta_carpeta)
            
        nombre_archivo = "grafico_ventas.png"
        ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
        
        plt.savefig(ruta_completa)
        plt.close(fig)

        # Carga usando tu función
        self.img_grafico = obtener_imagen(nombre_archivo, 800, 450)
        
        if self.img_grafico:
            self.lbl_imagen_grafico.config(image=self.img_grafico, text="")
        else:
            self.lbl_imagen_grafico.config(text="Error al cargar la imagen generada")
    # ------------------------------------

    def buscar_venta(self,campo,valor):
        registros = ventasCRUD.ventas.buscar(campo,valor)
        self.tabla.cargar(registros)

    def eliminar_venta(self):
        if self.id_seleccionado == 0:
            messagebox.showinfo("Aviso", "Seleccione un registro para continuar.")
            return
        confirmar = messagebox.askyesno(
            "ADVERTENCIA",
            f"Al eliminar la venta con ID = {self.id_seleccionado}, también se eliminarán todos los detalles asociados a esa venta.\n\n¿Desea continuar?"
        )
        if not confirmar:
            return

        ok_det = ventasCRUD.detalleVenta.eliminar_por_venta(self.id_seleccionado)
        if not ok_det:
            messagebox.showerror("Error", "No se pudieron eliminar los detalles de la venta. Operación cancelada.")
            return

        ok_venta = ventasCRUD.ventas.eliminar(self.id_seleccionado)
        if ok_venta:
            messagebox.showinfo("Exito", f"El registro con ID = {self.id_seleccionado} y todos sus detalles se eliminaron exitosamente")
            self.buscar_venta("Todo","")
            for row in self.tabla2.get_children():
                self.tabla2.delete(row)
            self.id_seleccionado = 0
            self.actualizar_grafico("Semanal") # Actualizar gráfico al eliminar
        else:
            messagebox.showerror("Error", "No se pudo eliminar el registro de venta aunque los detalles fueron eliminados.")

    def ver_detalles(self):
        registros = ventasCRUD.detalleVenta.buscar(self.id_seleccionado)
        for row in self.tabla2.get_children():
            self.tabla2.delete(row)
        for fila in registros:
            self.tabla2.insert("", "end", values=fila)

    def actualizar_id(self, id_recibido):
        self.id_seleccionado = id_recibido


class insertarVentas(Frame):
    def __init__(self, master, controlador,accion,id_seleccionado=None):
        super().__init__(master)
        self.controlador = controlador
        head = header(self, controlador)
        head.pack(fill="x")
        self.id_seleccionado = id_seleccionado
        # --- SCROLLABLE BODY (vertical only) para insertarVentas ---
        container = Frame(self)
        container.pack(fill="both", expand=True, padx=30, pady=30)

        canvas = Canvas(container, bg=COLOR_FRAME, highlightthickness=0)
        vsb = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        body = Frame(canvas, bg=COLOR_FRAME)  # el 'body' original (nombre conservado)
        window_id = canvas.create_window((0, 0), window=body, anchor="nw")

        def _on_body_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        body.bind("<Configure>", _on_body_configure)

        def _on_canvas_configure(event):
            req_h = body.winfo_reqheight()
            canvas.itemconfig(window_id, width=event.width, height=max(event.height, req_h))
            canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.bind("<Configure>", _on_canvas_configure)
        # --- fin scrollable para insertarVentas ---

        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        precios_result = ventasCRUD.menu.obtenerPrecios()
        # precios_result is list of tuples (precio,) or empty list
        self.precios = [fila[0] for fila in precios_result] if precios_result else []

        frame_prod = Frame(body,bg=COLOR_FRAME)
        frame_total = Frame(body,bg=COLOR_FRAME)

        #frame prod
        #Comida
        lbl_prod = Label(frame_prod,text="Producto",font=("Arial", 24),fg="white",bg=COLOR_FRAME)
        lbl_prod.grid(row=0,column=0)

        lbl_cant = Label(frame_prod,text="Cantidad",font=("Arial", 24),fg="white",bg=COLOR_FRAME)
        lbl_cant.grid(row=0,column=1)


        #self.opciones_prod = ["Hamburguesa doble","Hamburguesa especial","Hamburguesa especial","Hotdog","Ingrediente extra","Refresco","Agua"]
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

        btn_agregar = Button(frame_total,text="Agregar venta",width=20,font=("Arial",20),command=lambda:self.crearVenta(),bg="#669BBC",fg="white")
        btn_agregar.pack(pady=5)
        self.total_venta = 0
        btn_volver = Button(frame_total,text="Volver",width=20,font=("Arial",20),command=lambda:self.controlador.mostrar_pantalla("mainventas"),bg="#669BBC",fg="white")
        btn_volver.pack(pady=5)

        #Fecha
        f = len(self.opciones_prod)+1 #Filas actuales del grid en frame_prod
        self.fecha = DateEntry(
                 frame_prod,
                 date_pattern="dd/mm/yyyy",
                 locale="es_MX",
                 font=("Arial", 20),
                 width=12
                )
        self.fecha.grid(row=f+1,column=1,pady=5)
        lbl_fecha = Label(frame_prod,text="Fecha: ",font=("Arial", 20),bg=COLOR_FRAME,fg="white")
        lbl_fecha.grid(row=f+1,column=0,pady=5,sticky="e")

        lbl_hora = Label(frame_prod,text="Hora: ",font=("Arial", 20),bg=COLOR_FRAME,fg="white")
        lbl_hora.grid(row=f+2,column=0,pady=5,sticky="e")


        frame_hora = Frame(frame_prod,bg=COLOR_FRAME)
        frame_hora.grid(row=f+2,column=1,sticky="nsew")
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



        match accion:
            case "agregar":
                head.titulo = "Registrar venta"
                frame_prod.grid(row=0,column=0,sticky="nsew",padx=40,pady=50)
                frame_total.grid(row=0,column=1,sticky="nsew",pady=50,padx=20)
                frame_prod.grid_propagate(False)
            case "actualizar":
                head.titulo = f"Actualizar venta {self.id_seleccionado}"
                frame_prod.grid(row=1,column=0,sticky="nsew",padx=40,pady=5)
                frame_total.grid(row=1,column=1,sticky="nsew",padx=20,pady=5)
                body.rowconfigure(1, weight=1)
                frame_tablas = Frame(body,bg="white",height=260)
                frame_tablas.pack_propagate(False)
                frame_tablas.grid(row=0,column=0,sticky="nsew",pady=(20,0),padx=10,columnspan=2)
                columnas_ventas = ["ID", "Fecha","Hora", "Total"]
                frame_tablaventas = Frame(frame_tablas,height=80)
                frame_tablaventas.pack_propagate(False)
                frame_tablaventas.pack(fill="x")
                self.tabla = tabla(
                    frame_tablaventas,
                    columnas_ventas
                )
                self.registros_venta = ventasCRUD.ventas.buscar("ID",self.id_seleccionado)
                self.tabla.cargar(self.registros_venta)

                columnas_detalle = ["ID", "ID_venta", "Producto","Cantidad","Subtotal"]
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

                btn_agregar.config(text="Actualizar venta",command=lambda:self.actualizarVenta())

                # obtener_cantidades devuelve lista de ints, en orden de menu
                self.cantidades = ventasCRUD.detalleVenta.obtener_cantidades(self.id_seleccionado)
                # si por alguna razón devuelve None o vacío, rellenar con ceros según cantidad de productos
                if not isinstance(self.cantidades, list) or len(self.cantidades) != len(self.opciones_prod):
                    # fallback: crear lista de ceros con la longitud de opciones_prod
                    self.cantidades = [0]*len(self.opciones_prod)
                registros = ventasCRUD.ventas.obtener_hora(self.id_seleccionado)

                fecha = registros[0][0]
                self.fecha.set_date(fecha)
                hora = registros[0][1]
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
                # calcular total inicial basado en cantidades y precios
                total = 0
                for idx in range(len(self.opciones_prod)):
                    precio = float(self.precios[idx]) if idx < len(self.precios) else 0
                    total += int(self.cantidades[idx]) * precio
                self.total_venta = total
                self.lbl_total.config(text=f"$ {total:.2f}")


    def spin_cambio(self, index, valor):
        # recalcula total cuando se cambia un spinbox
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
            # no pasar index por validatecommand, solo recalcular total
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
            messagebox.showwarning("Advertencia","Ingrese productos para continuar")
            return
        fecha = self.fecha.get_date()
        hora = f"{self.spin_hora.get()}:{"00" if self.spin_minuto.get() == "0" else self.spin_minuto.get()}"
        insertar,id = ventasCRUD.ventas.insertar(self.total_venta,fecha,hora)
        if not insertar:
            messagebox.showerror("Error","No se pudo insertar la venta.")
            return
        insertar_detalle_ok = True
        for i in range(len(self.spinbox_prod)):
            cantidad = int(self.spinbox_prod[i].get())
            if cantidad > 0:
                ok = ventasCRUD.detalleVenta.insertar(id,self.opciones_prod[i],cantidad)
                if not ok:
                    insertar_detalle_ok = False
        if insertar and insertar_detalle_ok:
            messagebox.showinfo("Exito", "La venta se guardó exitosamente.")
            self.limpiar()
        else:
            messagebox.showerror("Error", "Ocurrió un error al guardar los detalles de la venta.")
            

    def actualizarVenta(self):
        # toma las cantidades previas (self.cantidades) y las nuevas de los spinboxes
        if self.id_seleccionado is None:
            messagebox.showerror("Error", "ID de venta no definido.")
            return

        new_quantities = []
        for sp in self.spinbox_prod:
            try:
                new_quantities.append(int(sp.get()))
            except:
                new_quantities.append(0)

        # Si todos en cero -> eliminar todos los detalles y la venta
        if all(q == 0 for q in new_quantities):
            confirmar = messagebox.askyesno("Confirmar eliminación", "Todos los productos quedaron en 0. ¿Desea eliminar la venta completa?")
            if not confirmar:
                return
            ok_det = ventasCRUD.detalleVenta.eliminar_por_venta(self.id_seleccionado)
            ok_venta = ventasCRUD.ventas.eliminar(self.id_seleccionado)
            if ok_det and ok_venta:
                messagebox.showinfo("Éxito", "La venta y sus detalles se eliminaron correctamente.")
                self.controlador.mostrar_pantalla("mainventas")
            else:
                messagebox.showerror("Error", "No se pudo eliminar la venta por completo.")
            return

        # Caso general: revisar cada producto y aplicar insertar/actualizar/eliminar según cambio
        any_error = False
        for i in range(len(self.opciones_prod)):
            prev = int(self.cantidades[i]) if i < len(self.cantidades) else 0
            new = int(new_quantities[i])
            if new == prev:
                continue  # sin cambio

            # Si prev == 0 y new > 0 -> insertar nuevo detalle
            if prev == 0 and new > 0:
                ok = ventasCRUD.detalleVenta.insertar(self.id_seleccionado, self.opciones_prod[i], new)
                if not ok:
                    any_error = True

            # Si prev > 0 y new == 0 -> eliminar detalle
            elif prev > 0 and new == 0:
                id_det = ventasCRUD.detalleVenta.obtener_id_detalle(self.id_seleccionado, i+1)
                if id_det is None:
                    # no se encontró detalle: marcar error
                    any_error = True
                else:
                    ok = ventasCRUD.detalleVenta.eliminar(id_det)
                    if not ok:
                        any_error = True

            # Si prev >0 y new >0 (cambio de cantidad) -> actualizar
            elif prev > 0 and new > 0:
                id_det = ventasCRUD.detalleVenta.obtener_id_detalle(self.id_seleccionado, i+1)
                if id_det is None:
                    # intenta insertar si no existe (por seguridad)
                    ok = ventasCRUD.detalleVenta.insertar(self.id_seleccionado, self.opciones_prod[i], new)
                    if not ok:
                        any_error = True
                else:
                    ok = ventasCRUD.detalleVenta.actualizar(id_det, new, self.opciones_prod[i])
                    if not ok:
                        any_error = True

        # recalcular total y actualizar la fila de ventas
        # recalcula sum(subtotal) desde DB para evitar errores
        detalles = ventasCRUD.detalleVenta.buscar(self.id_seleccionado)
        nuevo_total = 0.0
        for d in detalles:
            # d => (id_detalle, id_venta, nombre, cantidad, subtotal)
            try:
                nuevo_total += float(d[4])
            except:
                pass
        fecha = self.fecha.get_date()
        hora = f"{self.spin_hora.get()}:{"00" if self.spin_minuto.get() == "0" else self.spin_minuto.get()}"
        ok_total = ventasCRUD.ventas.actualizar_total(self.id_seleccionado, nuevo_total,fecha,hora)
        if any_error or not ok_total:
            messagebox.showerror("Error", "Ocurrieron errores al actualizar la venta. Revise la consola o la base de datos.")
        else:
            messagebox.showinfo("Éxito", "La venta se actualizó correctamente.")
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