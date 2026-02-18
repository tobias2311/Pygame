import pygame
from grafica.componentes import (
    crear_boton, dibujar_boton, actualizar_boton, verificar_click_boton,
    crear_input_box, manejar_evento_input, dibujar_input_box
)
from logica.usuarios import autenticar_usuario, registrar_usuario

"""Módulo para la gestión del registro y login de usuarios."""

def inicializar_ui_usuarios(ancho_p, alto_p, fuentes, colores):
    x_centro = ancho_p // 2
    
    input_user_login = crear_input_box(x_centro - 150, 300, 300, 50, fuentes["cuerpo"], colores["celeste"], colores["gris"])
    input_pass_login = crear_input_box(x_centro - 150, 400, 300, 50, fuentes["cuerpo"], colores["celeste"], colores["gris"])
    
    btn_ingresar = crear_boton(x_centro - 150, 500, 300, 60, "INGRESAR", fuentes["cuerpo"], colores["azul_oscuro"], colores["celeste"])
    btn_ir_a_registro = crear_boton(x_centro - 150, 580, 300, 40, "No tengo cuenta", fuentes["info"], colores["rojo"], colores["magenta"])
    
    input_user_reg = crear_input_box(x_centro - 150, 300, 300, 50, fuentes["cuerpo"], colores["verde"], colores["gris"])
    input_pass_reg = crear_input_box(x_centro - 150, 400, 300, 50, fuentes["cuerpo"], colores["verde"], colores["gris"])
    
    btn_confirmar_reg = crear_boton(x_centro - 150, 500, 300, 60, "REGISTRARME", fuentes["cuerpo"], colores["verde"], colores["celeste"])
    btn_volver_a_login = crear_boton(x_centro - 150, 580, 300, 40, "Volver al Login", fuentes["info"], colores["azul_oscuro"], colores["celeste"])
    
    return {
        "login": {
            "user": input_user_login,
            "pass": input_pass_login,
            "btn_ok": btn_ingresar,
            "btn_switch": btn_ir_a_registro
        },
        "registro": {
            "user": input_user_reg,
            "pass": input_pass_reg,
            "btn_ok": btn_confirmar_reg,
            "btn_switch": btn_volver_a_login
        }
    }

def mostrar_pantalla_login(pantalla, recursos, fuentes, colores, ui, pos_mouse, eventos):
    ancho_p = pantalla.get_width()
    
    pantalla_destino = None
    usuario_identificado = None

    pantalla.fill(colores["azul_oscuro"])
    
    sup_titulo = fuentes["titulo"].render("INICIAR SESIÓN", True, colores["blanco"])
    pantalla.blit(sup_titulo, sup_titulo.get_rect(center=(ancho_p // 2, 150)))
    
    lbl_user = fuentes["info"].render("Usuario:", True, colores["amarillo"])
    pantalla.blit(lbl_user, (ancho_p // 2 - 150, 270))
    dibujar_input_box(pantalla, ui["user"])
    
    lbl_pass = fuentes["info"].render("Contraseña:", True, colores["amarillo"])
    pantalla.blit(lbl_pass, (ancho_p // 2 - 150, 370))
    dibujar_input_box(pantalla, ui["pass"])
    
    actualizar_boton(ui["btn_ok"], pos_mouse)
    actualizar_boton(ui["btn_switch"], pos_mouse)
    dibujar_boton(pantalla, ui["btn_ok"])
    dibujar_boton(pantalla, ui["btn_switch"])
    
    for evento in eventos:
        manejar_evento_input(ui["user"], evento)
        manejar_evento_input(ui["pass"], evento)
        
        if verificar_click_boton(ui["btn_switch"], evento):
            pantalla_destino = "registro"
            
        if verificar_click_boton(ui["btn_ok"], evento):
            nombre = ui["user"]["texto"]
            clave = ui["pass"]["texto"]
            exito, datos_u = autenticar_usuario(nombre, clave)
            
            if exito == True:
                pantalla_destino = "menu"
                usuario_identificado = datos_u
            else:
                print("Error: Usuario o contraseña incorrectos")
                
    return pantalla_destino, usuario_identificado

def mostrar_pantalla_registro(pantalla, recursos, fuentes, colores, ui, pos_mouse, eventos):
    ancho_p = pantalla.get_width()
    
    pantalla_destino = None

    pantalla.fill(colores["azul_oscuro"])
    
    sup_titulo = fuentes["titulo"].render("REGISTRO", True, colores["blanco"])
    pantalla.blit(sup_titulo, sup_titulo.get_rect(center=(ancho_p // 2, 150)))
    
    lbl_user = fuentes["info"].render("Nuevo Usuario:", True, colores["celeste"])
    pantalla.blit(lbl_user, (ancho_p // 2 - 150, 270))
    dibujar_input_box(pantalla, ui["user"])
    
    lbl_pass = fuentes["info"].render("Nueva Contraseña:", True, colores["celeste"])
    pantalla.blit(lbl_pass, (ancho_p // 2 - 150, 370))
    dibujar_input_box(pantalla, ui["pass"])
    
    actualizar_boton(ui["btn_ok"], pos_mouse)
    actualizar_boton(ui["btn_switch"], pos_mouse)
    dibujar_boton(pantalla, ui["btn_ok"])
    dibujar_boton(pantalla, ui["btn_switch"])
    
    for evento in eventos:
        manejar_evento_input(ui["user"], evento)
        manejar_evento_input(ui["pass"], evento)
        
        if verificar_click_boton(ui["btn_switch"], evento):
            pantalla_destino = "login"
            
        if verificar_click_boton(ui["btn_ok"], evento):
            nombre = ui["user"]["texto"]
            clave = ui["pass"]["texto"]
            exito, mensaje = registrar_usuario(nombre, clave)
            print(mensaje)
            if exito == True:
                pantalla_destino = "login"
                
    return pantalla_destino
