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
Creamos una librería de UI propia para manejar la interacción con el usuario de manera profesional.

#### 📁 Módulo: `grafica/componentes.py`
- **Clase `Boton`**: Encapsula el dibujado, la detección de hover y el click.
    - *Defensa Técnica*: "Al crear una clase para los botones, logramos **reutilización de código**. En lugar de repetir la lógica del mouse en cada pantalla, simplemente instanciamos objetos que saben cómo reaccionar y dibujarse solos".
- **Posicionamiento Relativo**: Los botones se ubican usando porcentajes (0.0 a 1.0) de la pantalla.
    - *Defensa Técnica*: "Esto permite que la interfaz sea **adaptable**. Si cambiamos la resolución del juego en el JSON, los botones se reacomodan automáticamente manteniendo la proporción visual".

### Sprint 5: Punto de Entrada y Orquestación

#### 📁 Módulo: `pygame_app/main.py`
Es el cerebro que une la lógica de carga, los recursos y la interfaz.
- **Cero Hardcodeo**: Se eliminaron todos los valores fijos. Colores, dimensiones, textos y reglas de juego vienen del JSON.
    - *Defensa Técnica*: "Toda la configuración es externa. Esto permite realizar cambios estéticos o de dificultad sin necesidad de modificar el código fuente, garantizando una **separación total entre datos y ejecución**".
- **Loop de Eventos Explícito**: El bucle principal gestiona eventos, actualizaciones y dibujado de forma secuencial.
    - *Defensa Técnica*: "Mantenemos un loop limpio donde la lógica de actualización (`update`) y el renderizado (`draw`) están separados, siguiendo los estándares de desarrollo de videojuegos".

---

## 🛠️ Reglas Éticas y Técnicas de Programación
Durante todo el desarrollo, seguimos principios fundamentales para una defensa exitosa:
1. **Control de Flujo Explícito**: Se evitó el uso de `not` y `try-except` (fuera de la persistencia obligatoria) para demostrar un manejo lógico total de las variables.
2. **Comparación Explícita**: Usamos comparaciones como `if variable == True` para que el código sea autodocumentado y fácil de explicar ante una mesa de examen.
3. **Modularidad**: Cada carpeta y archivo tiene una única responsabilidad (Principio de Responsabilidad Única).

---
*Última actualización: Febrero 2026 - Versión: Componentes y Entry Point finalizados.*
