import os
import json
from logica.cargar_archivos import cargar_configuracion, guardar_datos_json

"""Módulo de gestión de cuentas de usuario, autenticación y ranking."""

def obtener_ruta_cuentas():
    ruta_base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(ruta_base, "data", "cuentas.json")

def cargar_cuentas():
    ruta = obtener_ruta_cuentas()
    datos = cargar_configuracion(ruta)
    return datos.get("usuarios", [])

def guardar_cuentas(lista_usuarios):
    ruta = obtener_ruta_cuentas()
    datos = {"usuarios": lista_usuarios}
    return guardar_datos_json(ruta, datos)

def registrar_usuario(nombre, password):
    if len(nombre) < 3 or len(password) < 3:
        return False, "Nombre y clave deben tener al menos 3 caracteres."
    
    usuarios = cargar_cuentas()
    
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
    usuarios = cargar_cuentas()
    for u in usuarios:
        if u["nombre"].lower() == nombre.lower() and u["password"] == password:
            return True, u
    return False, None

def actualizar_puntaje_maximo(usuario_actual, puntaje_obtenido):
    usuarios = cargar_cuentas()
    nuevo_record = False
    
    for u in usuarios:
        if u["nombre"].lower() == usuario_actual["nombre"].lower():
            if puntaje_obtenido > u["puntaje_maximo"]:
                u["puntaje_maximo"] = puntaje_obtenido
                nuevo_record = True
                usuario_actual["puntaje_maximo"] = puntaje_obtenido
            break 
            
    if nuevo_record == True:
        guardar_cuentas(usuarios)
        
    return nuevo_record

def obtener_ranking(cantidad=3):
    usuarios = cargar_cuentas()
    
    n = len(usuarios)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if usuarios[j]["puntaje_maximo"] < usuarios[j + 1]["puntaje_maximo"]:
                aux = usuarios[j]
                usuarios[j] = usuarios[j + 1]
                usuarios[j + 1] = aux
                
    return usuarios[:cantidad]
