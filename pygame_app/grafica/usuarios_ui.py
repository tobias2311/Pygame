import pygame
from grafica.componentes import crear_boton, dibujar_boton, actualizar_boton, verificar_click_boton
from grafica.componentes import crear_input_box, manejar_evento_input, dibujar_input_box
from logica.usuarios import autenticar_usuario, registrar_usuario

def inicializar_ui_usuarios(ancho_p, alto_p, fuentes, colores):
    """Inicializa los input boxes y botones para login/registro."""
    x_centro = ancho_p // 2
    
    # Inputs para Login
    input_user_login = crear_input_box(x_centro - 150, 300, 300, 50, fuentes["cuerpo"], colores["celeste"], colores["gris"])
    input_pass_login = crear_input_box(x_centro - 150, 400, 300, 50, fuentes["cuerpo"], colores["celeste"], colores["gris"])
    
    # Botones Login
    btn_ingresar = crear_boton(x_centro - 150, 500, 300, 60, "INGRESAR", fuentes["cuerpo"], colores["azul_oscuro"], colores["celeste"])
    btn_ir_a_registro = crear_boton(x_centro - 150, 580, 300, 40, "No tengo cuenta", fuentes["info"], colores["rojo"], colores["magenta"])
    
    # Inputs para Registro
    input_user_reg = crear_input_box(x_centro - 150, 300, 300, 50, fuentes["cuerpo"], colores["verde"], colores["gris"])
    input_pass_reg = crear_input_box(x_centro - 150, 400, 300, 50, fuentes["cuerpo"], colores["verde"], colores["gris"])
    
    # Botones Registro
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
    """Dibuja y gestiona la pantalla de login."""
    ancho_p = pantalla.get_width()
    
    # Variables de estado para el retorno (lo que el main necesita saber)
    pantalla_destino = None
    usuario_identificado = None

    # 1. Fondo (Color sólido para login)
    pantalla.fill(colores["azul_oscuro"])
    
    # 2. Título
    sup_titulo = fuentes["titulo"].render("INICIAR SESIÓN", True, colores["blanco"])
    pantalla.blit(sup_titulo, sup_titulo.get_rect(center=(ancho_p // 2, 150)))
    
    # 3. Etiquetas e Inputs
    lbl_user = fuentes["info"].render("Usuario:", True, colores["amarillo"])
    pantalla.blit(lbl_user, (ancho_p // 2 - 150, 270))
    dibujar_input_box(pantalla, ui["user"])
    
    lbl_pass = fuentes["info"].render("Contraseña:", True, colores["amarillo"])
    pantalla.blit(lbl_pass, (ancho_p // 2 - 150, 370))
    dibujar_input_box(pantalla, ui["pass"])
    
    # 4. Botones
    actualizar_boton(ui["btn_ok"], pos_mouse)
    actualizar_boton(ui["btn_switch"], pos_mouse)
    dibujar_boton(pantalla, ui["btn_ok"])
    dibujar_boton(pantalla, ui["btn_switch"])
    
    # 5. Manejo de Eventos
    for evento in eventos:
        manejar_evento_input(ui["user"], evento)
        manejar_evento_input(ui["pass"], evento)
        
        # Click en "No tengo cuenta" -> Ir a Registro
        if verificar_click_boton(ui["btn_switch"], evento):
            pantalla_destino = "registro"
            
        # Click en "Ingresar" -> Autenticar
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
    """Dibuja y gestiona la pantalla de registro."""
    ancho_p = pantalla.get_width()
    
    # Variable de estado para el retorno
    pantalla_destino = None

    # 1. Fondo (Color sólido para registro)
    pantalla.fill(colores["azul_oscuro"])
    
    # 2. Título
    sup_titulo = fuentes["titulo"].render("REGISTRO", True, colores["blanco"])
    pantalla.blit(sup_titulo, sup_titulo.get_rect(center=(ancho_p // 2, 150)))
    
    # 3. Etiquetas e Inputs
    lbl_user = fuentes["info"].render("Nuevo Usuario:", True, colores["celeste"])
    pantalla.blit(lbl_user, (ancho_p // 2 - 150, 270))
    dibujar_input_box(pantalla, ui["user"])
    
    lbl_pass = fuentes["info"].render("Nueva Contraseña:", True, colores["celeste"])
    pantalla.blit(lbl_pass, (ancho_p // 2 - 150, 370))
    dibujar_input_box(pantalla, ui["pass"])
    
    # 4. Botones
    actualizar_boton(ui["btn_ok"], pos_mouse)
    actualizar_boton(ui["btn_switch"], pos_mouse)
    dibujar_boton(pantalla, ui["btn_ok"])
    dibujar_boton(pantalla, ui["btn_switch"])
    
    # 5. Manejo de Eventos
    for evento in eventos:
        manejar_evento_input(ui["user"], evento)
        manejar_evento_input(ui["pass"], evento)
        
        # Click en "Volver al Login"
        if verificar_click_boton(ui["btn_switch"], evento):
            pantalla_destino = "login"
            
        # Click en "Registrarme"
        if verificar_click_boton(ui["btn_ok"], evento):
            nombre = ui["user"]["texto"]
            clave = ui["pass"]["texto"]
            exito, mensaje = registrar_usuario(nombre, clave)
            print(mensaje)
            if exito == True:
                pantalla_destino = "login"
                
    return pantalla_destino
