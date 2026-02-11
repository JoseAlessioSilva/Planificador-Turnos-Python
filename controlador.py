
from modelo import BaseData, ObservadorConcreto

# ---------- Funciones Enlaces ----------------

obj_control = BaseData()
obj_observador = ObservadorConcreto(obj_control)
def alta_controlador(nombre, apellido, dia):
    return obj_control.alta(nombre, apellido, dia)

def borrar_controlador(tree):
    return obj_control.borrar(tree)

def consulta_controlador():
    return obj_control.consulta_treeview()
