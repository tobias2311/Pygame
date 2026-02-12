import os
import json
from logica.cargar_archivos import cargar_configuracion, guardar_datos_json

def obtener_ruta_cuentas():
    """Retorna la ruta absoluta del archivo de cuentas."""
    # Subimos un nivel desde logica/ y otro desde pygame_app/ para llegar a la raíz
    ruta_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(ruta_base, "data", "cuentas.json")

def cargar_cuentas():
    """Carga la lista de usuarios desde el archivo JSON."""
    ruta = obtener_ruta_cuentas()
    datos = cargar_configuracion(ruta)
    return datos.get("usuarios", [])

def guardar_cuentas(lista_usuarios):
    """Guarda la lista de usuarios en el archivo JSON."""
    ruta = obtener_ruta_cuentas()
    datos = {"usuarios": lista_usuarios}
    return guardar_datos_json(ruta, datos)

def registrar_usuario(nombre, password):
    """
    Intenta registrar un nuevo usuario. 
    Retorna (True, "mensaje") si tiene éxito, (False, "error") si no.
    """
    if len(nombre) < 3 or len(password) < 3:
        return False, "Nombre y clave deben tener al menos 3 caracteres."
    
    usuarios = cargar_cuentas()
    
    # Verificar si el nombre ya existe
    for u in usuarios:
        if u["nombre"].lower() == nombre.lower():
            return False, "El nombre de usuario ya existe."
            
    nuevo_usuario = {
        "nombre": nombre,
        "password": password,
        "puntaje_maximo": 0
    }
    
    usuarios.append(nuevo_usuario)
    if guardar_cuentas(usuarios):
        return True, "Usuario registrado con éxito."
    return False, "Error al guardar los datos."

def autenticar_usuario(nombre, password):
    """
    Verifica si las credenciales son correctas.
    Retorna True si es válido, False si no.
    """
    usuarios = cargar_cuentas()
    for u in usuarios:
        if u["nombre"].lower() == nombre.lower() and u["password"] == password:
            return True, u
    return False, None
