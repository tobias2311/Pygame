# Documentación Detallada de Funciones - TP PYGAME

Este documento explica el propósito, funcionamiento y código de las funciones principales del proyecto.

---

## 📂 pygame_app/logica/cargar_archivos.py
*Módulo encargado de la persistencia de datos (JSON y CSV).*

### `cargar_preguntas(ruta_archivo)`
- **Qué hace**: Carga el banco de preguntas desde un archivo CSV.
- **Cómo funciona**: Abre el archivo en modo lectura, utiliza `csv.DictReader` para mapear las columnas a claves de un diccionario. Construye una lista de objetos donde cada pregunta tiene su enunciado, una lista de 4 opciones, la categoría, dificultad y los puntos asignados.
```python
def cargar_preguntas(ruta_archivo: str) -> list:
    preguntas = []
    if os.path.exists(ruta_archivo):
        with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                pregunta = {
                    "enunciado": fila.get("enunciado", ""),
                    "respuesta_correcta": fila.get("respuesta_correcta", ""),
                    "opciones": [fila.get("opcion1", ""), fila.get("opcion2", ""), fila.get("opcion3", ""), fila.get("opcion4", "")],
                    "categoria": fila.get("categoria", ""),
                    "dificultad": fila.get("dificultad", ""),
                    "puntos": int(fila.get("puntos", 0))
                }
                preguntas.append(pregunta)
    return preguntas
```

---

## 📂 pygame_app/logica/juego_logica.py
*Módulo que procesa las reglas del juego y el estado de la partida.*

### `verificar_respuesta(estado_juego, respuesta_usuario, respuesta_correcta)`
- **Qué hace**: Evalúa si la respuesta elegida por el usuario es correcta y actualiza el progreso.
- **Cómo funciona**: 
    1. Compara las cadenas (limpiando espacios y convirtiendo a minúsculas).
    2. Si es correcta: Suma puntos, incrementa el contador de aciertos y aumenta la **racha actual**.
    3. Si la racha llega a un múltiplo de 3 y el **modo TDAH** está activo, elige un mensaje motivador aleatorio para mostrar.
    4. Si es incorrecta: Resetea la racha a cero.
    5. Finalmente, avanza el índice de la pregunta y limpia los botones/input del estado para la siguiente ronda.
```python
def verificar_respuesta(estado_juego, respuesta_usuario, respuesta_correcta):
    es_correcta = False
    if respuesta_usuario.strip().lower() == respuesta_correcta.strip().lower():
        estado_juego["puntaje"] = estado_juego["puntaje"] + estado_juego["puntos_acierto"]
        estado_juego["correctas"] = estado_juego["correctas"] + 1
        estado_juego["racha_actual"] = estado_juego["racha_actual"] + 1
        es_correcta = True
        
        if estado_juego.get("tdah_activo", False) == True:
            if estado_juego["racha_actual"] > 0 and estado_juego["racha_actual"] % 3 == 0:
                indice_msg = random.randint(0, len(estado_juego["mensajes_motivadores"]) - 1)
                estado_juego["mensaje_racha"] = estado_juego["mensajes_motivadores"][indice_msg]
                estado_juego["timer_mensaje"] = 60 
    else:
        estado_juego["racha_actual"] = 0
    estado_juego["indice_actual"] = estado_juego["indice_actual"] + 1
    return es_correcta
```

---

## 📂 pygame_app/logica/usuarios.py
*Módulo de gestión de perfiles y récords.*

### `obtener_ranking(cantidad=3)`
- **Qué hace**: Calcula quiénes son los mejores jugadores basados en su puntaje máximo.
- **Cómo funciona**: Aplica un algoritmo de **Ordenamiento Burbuja (Bubble Sort)** sobre la lista de usuarios. Compara los `puntaje_maximo` de elementos adyacentes y los intercambia si el de la derecha es mayor. Al finalizar, retorna una porción (slice) de la lista con los N mejores.
```python
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
```

---

## 📂 pygame_app/grafica/componentes.py
*Módulo de construcción de la Interfaz de Usuario (UI).*

### `crear_boton(x, y, ancho, alto, texto, ...)`
- **Qué hace**: Define las propiedades de un botón interactivo.
- **Cómo funciona**: Crea un diccionario con un `pygame.Rect` para colisiones y almacena colores, fuentes y estados (si tiene el mouse encima o no). Esto permite que el botón se use en cualquier pantalla.
```python
def crear_boton(x, y, ancho, alto, texto, fuente, color_base, color_hover, ...):
    return {
        "rect": pygame.Rect(x, y, ancho, alto),
        "texto": texto,
        "fuente": fuente,
        "color_actual": color_base,
        "hovered": False
    }
```

### `dibujar_switch(superficie, switch)`
- **Qué hace**: Dibuja un interruptor deslizante premium (usado en Configuración).
- **Cómo funciona**: 
    1. Dibuja una sombra y un rectángulo redondeado (el "track"). 
    2. Cambia el color del fondo según si está `activo` (verde) o no (rojo).
    3. Dibuja un círculo (el "handle") que se posiciona suavemente a la izquierda o derecha.
    4. Renderiza el texto "ON" u "OFF" dentro del switch.
```python
def dibujar_switch(superficie, switch):
    color_fondo = switch["colores"]["on"] if switch["activo"] else switch["colores"]["off"]
    pygame.draw.rect(superficie, color_fondo, switch["rect"], border_radius=switch["rect"].height // 2)
    pygame.draw.circle(superficie, (255, 255, 255), (int(switch["x_actual"]), switch["y_centro"]), switch["radio_handle"])
```

---

## 📂 pygame_app/grafica/juego.py
*Módulo encargado de la experiencia visual durante la partida.*

### `dibujar_mensaje_racha(pantalla, estado_juego, ...)`
- **Qué hace**: Muestra un feedback visual positivo cuando el jugador acierta varias veces seguidas en modo TDAH.
- **Cómo funciona**: Si hay un mensaje activo y el cronómetro interno no ha llegado a cero:
    1. Renderiza el texto motivador.
    2. Dibuja un recuadro con borde magenta detrás del texto para que resalte.
    3. Disminuye el `timer_mensaje` en cada frame (proporcionando el efecto de que el mensaje desaparece tras unos segundos).
```python
def dibujar_mensaje_racha(pantalla, estado_juego, fuentes, colores, ancho_p):
    if estado_juego.get("mensaje_racha", "") != "" and estado_juego.get("timer_mensaje", 0) > 0:
        # Lógica de renderizado y dibujo del cuadro flotante
        estado_juego["timer_mensaje"] -= 1
```

---
*Nota: Este documento se centra en la lógica y el flujo de datos. Para ver la implementación completa de cada pantalla, revisa el archivo correspondiente en el código fuente.*
