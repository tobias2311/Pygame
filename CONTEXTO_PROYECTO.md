# Contexto del Proyecto: Desafío Mental (Versión Pygame App)

Este documento proporciona una visión general del proyecto para cualquier agente de IA o colaborador.

## 📋 Descripción General
"Desafío Mental" es un juego de preguntas y respuestas multietapa. Estamos en una fase de **RECONSTRUCCIÓN PROFESIONAL** desde cero, migrando la lógica original de consola (`consola/`) y la versión gráfica previa (`Archivos/`) hacia una arquitectura modular, limpia y parametrizada en la carpeta `pygame_app/`.

## 🚀 Estado Actual de la Reconstrucción
Se ha diseñado una arquitectura basada en la separación de Lógica (Backend) y Gráfica (Frontend).

### 1. Módulos Completados:
- **`data/config.json`**: Centralización total de parámetros (ventana, colores, reglas, fuentes).
- **`logica/cargar_archivos.py`**: Motor de persistencia para CSV y JSON. Sin `try/except` (por restricciones de cátedra) y con validación por flujo lógico.
- **`grafica/carga_recursos.py`**: Gestor de assets. Carga imágenes, sonidos y fuentes parametrizadas. Implementa gestión de rutas relativas con `os.path`.

### 2. Estructura de Carpetas (Nueva):
- `pygame_app/`: Raíz del nuevo código fuente.
    - `logica/`: Procesamiento de datos y reglas de juego.
    - `grafica/`: Dibujado y componentes visuales.
- `assets/`: Imágenes.
- `sounds/`: Audio.
- `data/`: Archivos de configuración y datos persistentes.

## 🎯 Próximo Paso
El siguiente paso es la creación del **`main.py`** en la raíz de `pygame_app/` para actuar como punto de entrada (entry point). Este archivo deberá:
1. Cargar la configuración total desde el JSON.
2. Inicializar los módulos de recursos y lógica.
3. Arrancar el loop principal de Pygame y la navegación de pantallas.

---
*Ultima actualización: Febrero 2026 - Fase de Reconstrucción: Inicio del Entry Point*
