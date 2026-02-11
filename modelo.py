import sqlite3
import re
from mis_regex import MisRegex
import os
import datetime
import socket

#------------------- MODELO ---------------------


    # Decoradar de registro de log
def decorador_log(funcion):
    def f_interna(*args, **kwargs):
        nombre_de_accion = funcion.__name__
        fecha = datetime.datetime.now()
        texto = f"[{fecha}] Se ejecutó la acción: {nombre_de_accion}\n"
        with open("decorardor_log.txt", "a") as log:
            log.write(texto)
        resultado = funcion(*args, **kwargs)
        return resultado
    return f_interna

    #Patron Observador
class Sujeto:
    observadores = []

    def agregar(self, obj):
        self.observadores.append(obj)

    def notificar(self, *args):
        for observador in self.observadores:
            observador.update(args)

class Observador:
    def update(self, *args):
        raise NotImplementedError("Delegación de actualización")
    
class ObservadorConcreto(Observador):
    def __init__(self, obj):
        self.observador_concreto = obj
        self.observador_concreto.agregar(self)

    def update(self, *args):
        print("Actualización dentro de ObservadorConcreto")
        # Datos recibidos desde el sujeto
        print("Datos recibidos: ", args)
        dia_hora = datetime.datetime.now()
        mensaje = f"[{dia_hora}] Se guardaron datos en la BD: {args}\n"
        with open("patron_observador.txt", "a") as log:
            log.write(mensaje)

        # CLIENTE 
        HOST, PORT = "localhost", 9999
        mensaje_servidor = f"Registro Alta: {args}" 
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Enviamos el string al servidor de logs
            sock.sendto(mensaje_servidor.encode("utf-8"), (HOST, PORT))
            print("Datos enviados al servidor de logs.")
        except Exception as e:
            print("No se pudo conectar con el servidor de logs (¿Está prendido?)")
        finally:
            sock.close()




class BaseData(Sujeto):

    def __init__(self):
        super().__init__()
        try:
            con = self.crear_base()
            self.crear_tabla(con)
            print("Base de datos creada")
        except:
            print("Ya hay base de datos")

    # Crear Base de datos
    
    def crear_base(self, ):
        con = sqlite3.connect('base_planificador.db')
        return con

    # Crear Tabla
    def crear_tabla(self, con):
        cursor = con.cursor()
        sql = """CREATE TABLE IF NOT EXISTS productos
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                Nombre NOT NULL,
                Apellido NOT NUll,
                Dia NOT NULL
                )"""
        cursor.execute(sql)
        con.commit()
        con.close()

    # Alta
    @decorador_log
    def alta(self, nombre, apellido, dia): 
        cadena = nombre
        obj = MisRegex()
        patron = obj.regex_nombre()
        if(re.match(patron, cadena)):
            print(nombre, apellido, dia)
            con = self.crear_base()
            cursor = con.cursor()
            #mi_id = int(mi_id)
            data = (nombre, apellido, dia)
            sql = "INSERT INTO productos(nombre, apellido, dia) VALUES(?, ?, ?)"
            cursor.execute(sql, data)
            con.commit()
            con.close()
            # Notificamos a los observadores que se ha agregado un nuevo registro
            self.notificar(nombre, apellido, dia)
        else:
            print("Error de Campo")


    # Baja
    @decorador_log
    def borrar(self, tree):
        valor = tree.selection()
        item = tree.item(valor)
        mi_id = item['text']
        con=self.crear_base()
        cursor=con.cursor()
        data = (mi_id,)
        sql = "DELETE FROM productos WHERE id = ?;"
        cursor.execute(sql, data)
        con.commit()
        con.close()
        tree.delete(valor)
        # Notificamos a los observadores que se ha borrado un registro
        self.notificar(f"Se eliminó: {item['values']}")


    # Consulta
    def consulta_treeview(self,):
        if not os.path.exists('base_planificador.db'):
            return None
        
        try:
            sql = "SELECT * FROM productos ORDER BY id ASC"
            con=self.crear_base()
            cursor=con.cursor()
            datos=cursor.execute(sql)
            resultado = datos.fetchall()
            con.close()
            return resultado
        except:
            return None


        



