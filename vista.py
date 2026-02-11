from tkinter import Tk, StringVar, Label, Entry, Button, Menu
from tkinter import ttk
from tkinter.messagebox import*
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
from tkcalendar import *
from controlador import alta_controlador, borrar_controlador, consulta_controlador
import subprocess
import sys
import os
   
    #------------------- VISTA ---------------------
class VistaPrincipal():
    def __init__(self, ):
        master = Tk()
        master.title("Planificador POO")
        # Sorpresa

        def color():
            resultado = askcolor(color="#00ff00", title="El título")
            master["bg"] = resultado[1]

        # ---------- Vista -----------------
        # Menu
        menubar = Menu(master)

        menu_archivo = Menu(menubar, tearoff=0)
        menu_archivo.add_command(label="Sorpresa", command=color)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=master.quit)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        master.config(menu=menubar)

        # Campos de entrada

        titulo = Label(master, text="PLANIFICADOR DE TURNOS", bg="#BD93F9", height=1, width=60)
        titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky="w")
        titulo.configure(font=("Calibri", 16, "bold"))

        nombre = Label(master, text="Nombre")
        nombre.grid(row=1, column=0)
        apellido=Label(master, text="Apellido")
        apellido.grid(row=2, column=0)
        dia=Label(master, text="Día")
        dia.grid(row=3, column=0)
        nombre.configure(font=("Calibri", 12))
        apellido.configure(font=("Calibri", 12))
        dia.configure(font=("Calibri", 12))


        # Variables campo de entrada 

        a_val = StringVar() 

        b_val = StringVar() 

        c_val = StringVar()

        w_ancho = 20

        entrada1 = Entry(master, textvariable = a_val, width = w_ancho) 
        entrada1.grid(row = 1, column = 1)
        entrada2 = Entry(master, textvariable = b_val, width = w_ancho) 
        entrada2.grid(row = 2, column = 1)
        entrada3 = DateEntry(master, width=w_ancho, background="#8BE9FD", foreground="#424450", borderwidth=2, textvariable=c_val)
        entrada3.grid(row=3, column=1)

        # ----------- Treeview -------------

        tree = ttk.Treeview(master)
        tree["columns"]=("col1", "col2", "col3")
        tree.column("#0", width=90, minwidth=50, anchor="w")
        tree.column("col1", width=200, minwidth=80)
        tree.column("col2", width=200, minwidth=80)
        tree.column("col3", width=200, minwidth=80)
        tree.heading("#0", text="ID")
        tree.heading("col1", text="Nombre")
        tree.heading("col2", text="Apellido")
        tree.heading("col3", text="Dia")
        tree.grid(row=10, column=0, columnspan=4)

        # ---------- Funciones AUxiliares ----------------

        # Modificacion
        def alta_vista(nombre, apellido, dia, tree):
            nombre = a_val.get()
            apellido = b_val.get()
            dia = c_val.get()
            retorno = alta_controlador(nombre, apellido, dia)
            actualizar_treeview(tree)
            return retorno

        def borrar_vista(tree):
            borrando = borrar_controlador(tree)
            print(borrando)
            showinfo("Aceptar", "Acaba de borrar un turno")
            return borrando


        def actualizar_treeview(mitreview):
            # Eliminamos registros
            records = mitreview.get_children()
            for element in records:
                mitreview.delete(element)
            # Consulta base de datos
            resultado = consulta_controlador()
            #Verificacion
            if not resultado:
                showinfo("Aviso", "No hay turnos cargados")
                return None
            # Carga de datos
            for fila in resultado:
                mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3]))


        boton_alta=Button(master, text="Alta", command=lambda:alta_vista(a_val.get(), b_val.get(), c_val.get(), tree))
        boton_alta.grid(row=6, column=1)

        boton_borrar=Button(master, text="Borrar", command=lambda:borrar_vista(tree))
        boton_borrar.grid(row=6, column=3)

        boton_borrar=Button(master, text="Actualizar", command=lambda:actualizar_treeview(tree))
        boton_borrar.grid(row=6, column=0)

        # Variable para el proceso del servidor
        self.proceso_servidor = None

        # --- FUNCIONES PARA EL SERVIDOR ---
        def lanzar_servidor():
            if self.proceso_servidor is None:
                # Buscamos la ruta del servidor
                ruta_script = os.path.join(os.path.dirname(__file__), "servidor.py")
                self.proceso_servidor = subprocess.Popen([sys.executable, ruta_script])
                showinfo("Servidor", "Servidor de logs INICIADO")
            else:
                showinfo("Servidor", "El servidor ya está corriendo")

        def detener_servidor():
            if self.proceso_servidor:
                self.proceso_servidor.terminate()
                self.proceso_servidor = None
                showinfo("Servidor", "Servidor de logs DETENIDO")
            else:
                showinfo("Servidor", "El servidor no está encendido")

        # --- BOTONES DEL SERVIDOR ---
        boton_server_on = Button(master, text="Prender Servidor", bg="PaleGreen1", command=lanzar_servidor)
        boton_server_on.grid(row=7, column=1, pady=10)

        boton_server_off = Button(master, text="Apagar Servidor", bg="IndianRed1", command=detener_servidor)
        boton_server_off.grid(row=7, column=3, pady=10)

        master.mainloop()
