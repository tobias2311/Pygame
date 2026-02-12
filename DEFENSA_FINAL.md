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

### Sprint 5: Gestión de Recursos
Para que el juego sea fluido, los recursos (imágenes, sonidos, fuentes) deben gestionarse de manera inteligente.

#### 📁 Módulo: `grafica/carga_recursos.py`
Este módulo centraliza la carga de assets, asegurando que se realice **una sola vez** al inicio.
- **Automatización de Rutas**: Utilizamos la biblioteca `os` para calcular rutas relativas.
    - *Defensa Técnica*: "Al usar `os.path.join` y detectar la ubicación del proyecto dinámicamente, aseguramos la **portabilidad**. El juego funcionará en cualquier computadora sin necesidad de cambiar las rutas de las carpetas".
- **Carga de Imágenes**: Implementamos una carga directa y simple.
    - *Defensa Técnica*: "Mantenemos una función centralizada de carga de imágenes para facilitar futuros cambios en el formato de los archivos visuales".
- **Fuentes Parametrizadas**: A diferencia de la versión anterior, los tamaños de las fuentes vienen del JSON de configuración.
    - *Defensa Técnica*: "La función `cargar_fuentes` recibe los tamaños de un diccionario externo. Esto es un ejemplo de **Inyección de Dependencias**, donde la interfaz gráfica no necesita saber de dónde vienen los datos, solo cómo usarlos".
- **Gestión de Sonido**: Separamos el streaming de música para optimizar el uso de memoria.
    - *Defensa Técnica*: "Centralizamos la música para poder escalarla fácilmente y permitir que cualquier parte del programa pueda disparar pistas de audio".

---
*(Este documento se irá completando con explicaciones técnicas de cada función clave)*
