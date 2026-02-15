# Guía de Defensa Final: Desafío Mental

Este documento detalla el desarrollo del proyecto desde cero, explicando la lógica y las decisiones de diseño para la defensa del examen final.

## 📖 Introducción
El proyecto nació de la necesidad de crear un juego educativo y accesible. Se optó por una estructura de "Sprints" para asegurar un crecimiento modular y robusto.

## 🔹 Fase 1: El Núcleo (Consola)
### Sprint 1: Lógica Básica
En esta etapa, definimos la estructura de las preguntas usando diccionarios. 
- **Decisión:** Usamos una lista de diccionarios para facilitar la iteración y el acceso a claves como `pregunta`, `opciones` y `respuesta`.

## 🔹 Fase 1: El Motor Lógico (Backend)

### Sprint 2: Persistencia y Parametrización
En esta fase, la prioridad es que el juego sea **dinámico**. Esto significa que el código no debe tener valores fijos, sino que debe "alimentarse" de archivos externos.

#### 📁 Módulo: `logica/cargar_archivos.py`
Este módulo es el responsable de toda la entrada de datos.
- **Lectura de CSV (`cargar_preguntas`)**: Utilizamos `csv.DictReader` para transformar las filas del archivo en diccionarios. 
    - *Defensa Técnica*: "Usamos diccionarios para que el acceso sea por nombre de columna (ej. `fila['enunciado']`), lo que hace al código más legible y resistente a cambios en el orden del CSV".
- **Configuración JSON (`cargar_configuracion`)**: Centralizamos los parámetros en un archivo `.json`.
    - *Defensa Técnica*: "JSON nos permite manejar tipos de datos complejos y nativos de Python (como listas de colores o booleanos) de forma externa al código".

## 🔹 Fase 2: Infraestructura Gráfica (Frontend)

### Sprint 3: Gestión de Recursos
Para que el juego sea fluido, los recursos (imágenes, sonidos, fuentes) deben gestionarse de manera inteligente.

#### 📁 Módulo: `grafica/carga_recursos.py`
Este módulo centraliza la carga de assets, asegurando que se realice **una sola vez** al inicio.
- **Automatización de Rutas**: Utilizamos la biblioteca `os` para calcular rutas relativas.
    - *Defensa Técnica*: "Al usar `os.path.join` y detectar la ubicación del proyecto dinámicamente, aseguramos la **portabilidad**. El juego funcionará en cualquier computadora sin necesidad de cambiar las rutas de las carpetas".
- **Robustez sin Excepciones**: Verificamos la existencia de archivos con `os.path.exists`.
    - *Defensa Técnica*: "En lugar de usar `try-except`, aplicamos validación por flujo lógico para que el programa sea predecible y cumpla con las restricciones de la cátedra, cargando superficies de color como placeholders si faltan imágenes".

### Sprint 4: Componentes de Interfaz e Interacción
Creamos una librería de UI propia para manejar la interacción con el usuario de manera profesional, optando por un enfoque de **programación funcional**.

#### 📁 Módulo: `grafica/componentes.py`
- **Funciones de Componentes (`crear_boton`, `crear_input_box`)**: En lugar de clases, usamos funciones que retornan **diccionarios de estado**.
    - *Defensa Técnica*: "Representamos los botones e inputs como diccionarios. Esto nos permite una manipulación de datos más directa y simple, alineada con los temas de la cátedra, facilitando el pasaje de parámetros y el control de estado sin la complejidad de los objetos".
- **Posicionamiento Relativo**: Los botones se ubican usando porcentajes o cálculos dinámicos basados en el ancho/alto de pantalla.
    - *Defensa Técnica*: "Esto permite que la interfaz sea **adaptable**. Si cambiamos la resolución del juego en el JSON, los componentes se reacomodan automáticamente".

### Sprint 5: Punto de Entrada y Orquestación
#### 📁 Módulo: `pygame_app/main.py`
Es el cerebro que une la lógica de carga, los recursos y la interfaz.
- **Gestor de Pantallas (Screen Manager)**: Implementamos una máquina de estados lógica usando una variable `pantalla_actual`.
    - *Defensa Técnica*: "Cada pantalla es un módulo independiente que se ejecuta solo según el estado del juego. Esto garantiza orden y evita que la lógica de una pantalla interfiera con otra".
- **Cero Hardcodeo**: Se eliminaron los valores fijos, trayendo todo desde el JSON.

### Sprint 6: Sistema de Usuarios y Cuentas
Implementamos un sistema de persistencia para los jugadores en `data/cuentas.json`.
- **Módulo `logica/usuarios.py`**: Gestiona el registro y autenticación.
    - *Defensa Técnica*: "Utilizamos estructuras de listas y diccionarios para buscar usuarios y validar credenciales. Separamos la lógica de validación de la interfaz para que el sistema sea más seguro y organizado".
- **Interfaces `Login` y `Registro`**: Uso de `InputBox` para capturar datos.

### Sprint 7: Lógica de Partida y Selección Dinámica
#### 📁 Módulos: `seleccion.py` y `juego.py`
- **Selección de Temática y Dificultad**: El usuario personaliza su partida antes de empezar.
- **Filtrado Dinámico**: Se filtran las preguntas del CSV según lo elegido.
- **Filtrado Dinámico**: Se filtran las preguntas del CSV según lo elegido.
    - *Defensa Técnica*: "Aplicamos algoritmos de búsqueda y filtrado sobre la base de preguntas. La puntuación se ajusta dinámicamente (1, 2 o 5 puntos) basándose en la dificultad. Se implementó una lógica de **aislamiento de temáticas**, donde si un tema no llega a las 12 preguntas, el sistema no las rellena con otros temas para mantener la integridad de la elección del usuario".

### Sprint 8: Multimedia y Experiencia de Usuario (UX)
Agregamos la "capa de brillo" al proyecto para que se sienta como un producto final.
- **Gestión de Música Diferenciada**: Se implementó una lógica en el loop principal que cambia la música según el contexto (Menú vs Juego) sin reiniciar el streaming si la escena pertenece al mismo grupo.
- **Sincronización de Sonido Global**: Creamos un diccionario `control_volumen` que persiste entre todas las pantallas.
    - *Defensa Técnica*: "Los botones de volumen en el juego y el menú operan sobre una misma referencia de datos, asegurando que si el usuario mutea el juego, el silencio se mantenga al volver al menú principal".
- **UI Progresiva y Arte IA**: El fondo de IA se escala dinámicamente al tamaño de la ventana definido en el JSON.
    - *Defensa Técnica*: "Reservamos el fondo principal para el menú post-login, mejorando la jerarquía visual. Además, el escalado dinámico garantiza portabilidad gráfica".

### Sprint 9: Modo Experto y Entrada de Texto Dinámica
#### 📁 Módulos: `juego.py` y `componentes.py`
- **Modo de Juego Diferenciado**: Implementamos una lógica condicional donde, según la dificultad, la interfaz muta de "opciones múltiples" a "entrada de texto directa".
    - *Defensa Técnica*: "En el modo experto, eliminamos las opciones para aumentar la dificultad cognitiva. Implementamos un sistema de comparación de cadenas normalizado (strip/lower) para validar la respuesta escrita del usuario, demostrando manejo de procesamiento de texto".
- **Caja de Entrada Inteligente**: La caja de texto (`InputBox`) ahora soporta auto-enfoque y límites de caracteres dinámicos (hasta 50).

### Sprint 10: Refactorización y Arquitectura Decoupled (Desacoplada)
#### 📁 Módulos: `logica/sonido.py` y `logica/juego_logica.py`
- **Centralización de Sonido**: Extrajimos toda la lógica de volumen y mute a un módulo único.
    - *Defensa Técnica*: "Aplicamos el principio de **No Repetición (DRY)**. Antes, la lógica de volumen estaba duplicada en cada pantalla; ahora, todas las interfaces llaman a una única función central, lo que facilita el mantenimiento y asegura coherencia sonora en todo el software".
- **Separación de Concernimientos (Visual vs Lógica)**: Movimos la carga y validación de preguntas de `grafica/juego.py` a `logica/juego_logica.py`.
    - *Defensa Técnica*: "Descentralizamos la pantalla de juego. Ahora, el código gráfico solo se encarga de dibujar (renderizar), mientras que el módulo de lógica toma las decisiones sobre puntajes y selección de preguntas. Esto hace que el código sea testeable y mucho más legible".

### Sprint 12: Super-Modularización de Datos (High-Level Configuration)
#### 📁 Carpeta: `data/*.json`
- **Fragmentación de Configuración**: Dividimos el archivo `config.json` en 4 módulos especializados: `estilo.json` (estética), `layout.json` (posiciones), `sonidos.json` (audio) y `config.json` (reglas).
    - *Defensa Técnica*: "Llevamos la arquitectura al siguiente nivel separando la **estética**, la **estructura** y la **lógica**. Esto permite que un diseñador gráfico pueda cambiar colores en `estilo.json` o mover botones en `layout.json` sin riesgo de romper la lógica de juego en Python, logrando un desacoplamiento casi total".

### Sprint 13: Refinamiento de Código y Restricciones Técnicas
#### 📁 Módulos: `seleccion.py`, `usuarios_ui.py` y `main.py`
- **Eliminación de `enumerate`**: Reemplazamos todos los bucles `enumerate` por `range(len(...))`.
    - *Defensa Técnica*: "Utilizamos iteraciones basadas en índices manuales para demostrar un control total sobre el recorrido de las estructuras de datos, siguiendo las restricciones pedagógicas de evitar funciones de alto nivel simplificadoras".
- **Lógica de Estado en Retornos**: Sustituimos los retornos múltiples (`None, None`) por variables descriptivas de estado.
    - *Defensa Técnica*: "Mejoramos la legibilidad del código utilizando el patrón de **punto de salida único**. Declaramos variables de estado al inicio de la función (ej. `pantalla_destino`) y las retornamos al final, haciendo que el flujo sea mucho más fácil de seguir y entender".
- **Limpieza de Documentación**: Profesionalizamos los comentarios del código.
    - *Defensa Técnica*: "Eliminamos comentarios redundantes o informales, dejando únicamente docstrings técnicos y explicaciones de propósito. El código ahora es autodocumentado por la claridad de sus nombres de variables y estructuras".

### Sprint 14: Refinamiento de UI e Integridad de Código
#### 📁 Módulos: `grafica/componentes.py`, `grafica/configuracion.py` y `grafica/juego.py`
- **Componente Switch Premium**: Desarrollamos un interruptor deslizante desde cero con animaciones de suavizado (easing).
    - *Defensa Técnica*: "En lugar de usar un checkbox estándar, creamos un componente visual personalizado que maneja su propio estado de animación mediante cálculos de interpolación. Esto demuestra la capacidad de crear interfaces de usuario ricas usando solo Pygame".
- **Lógica Exclusiva del Modo TDAH**: Refinamos el sistema para que las ayudas visuales y auditivas sean granulares.
    - *Defensa Técnica*: "Aseguramos que características como los mensajes motivadores y el temporizador sean exclusivos de este modo, manteniendo una experiencia pura para el resto de los jugadores. Esto demuestra un manejo avanzado de estados de configuración".
- **Eliminación de Operadores Ternarios y `not`**: Refactorizamos el código para usar solo estructuras de control explícitas.
    - *Defensa Técnica*: "Eliminamos el operador `not` y las asignaciones `if/else` en una sola línea (ternarios). Aunque son comunes en Python, optamos por bloques `if/else` explícitos para maximizar la claridad lógica y adherirnos a las metodologías de enseñanza de algoritmos básicos".

---

## 🛠️ Reglas Éticas y Técnicas de Programación
Durante todo el desarrollo, seguimos principios fundamentales para una defensa exitosa:
1. **Control de Flujo Explícito**: Se eliminó totalmente el uso de `not` y `try-except` (permitido únicamente en `logica/cargar_archivos.py` para persistencia obligatoria).
2. **Sin Operadores Ternarios**: Todas las condiciones usan bloques `if/else` multilínea para garantizar la legibilidad.
3. **Comparación Explícita**: Usamos comparaciones como `if variable == True` para que el código sea autodocumentado y predecible.
4. **Cero Comentarios Internos**: El código se autodocumenta mediante nombres claros de variables y funciones; los comentarios solo se usan para descripciones técnicas de módulos/funciones.
5. **Modularidad Estricta**: División clara en capas: Lógica (backend), Gráfica (frontend) y Datos (configuración externa).

---
*Última actualización: Febrero 2026 - Versión: Refinamiento de UI y Cumplimiento Estricto de Restricciones finalizados.*
