
from modelo import BaseData, ObservadorConcreto

# ---------- Funciones Enlaces ----------------

obj_control = BaseData()
obj_observador = ObservadorConcreto(obj_control)
def alta_controlador(nombre, apellido, dia):
    """
    Esta función es el controlador para dar de alta un nuevo registro en la base de datos.
    Recibe el nombre, apellido y día del turno, y llama a la función de alta del modelo.
    """
    return obj_control.alta(nombre, apellido, dia)

def borrar_controlador(tree):
    """
    Esta función es el controlador para borrar un registro de la base de datos.
    Recibe el treeview de la interfaz gráfica, y llama a la función de borrar del modelo.
    """
    return obj_control.borrar(tree)

def consulta_controlador():
    """
    Esta función es el controlador para consultar los registros de la base de datos.
    Llama a la función de consulta del modelo y devuelve los datos para ser mostrados en la interfaz gráfica.
    """
    return obj_control.consulta_treeview()
