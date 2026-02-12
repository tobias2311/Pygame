# Contexto del Proyecto: Desafío Mental (Versión Pygame App)

Este documento proporciona una visión general del proyecto para cualquier agente de IA o colaborador.

## 📋 Descripción General
"Desafío Mental" es un juego de preguntas y respuestas multietapa. Estamos en una fase de **RECONSTRUCCIÓN PROFESIONAL** desde cero, migrando la lógica original de consola (`consola/`) y la versión gráfica previa (`Archivos/`) hacia una arquitectura modular, limpia y parametrizada en la carpeta `pygame_app/`.

## 🚀 Estado Actual de la Reconstrucción
Se ha diseñado una arquitectura basada en la separación de Lógica (Backend) y Gráfica (Frontend).

### 1. Módulos Completados:
- **`data/config.json`**: Centralización total de parámetros (ventana, colores, reglas, fuentes).
- **`logica/cargar_archivos.py`**: Motor de persistencia para CSV y JSON.
- **`grafica/carga_recursos.py`**: Gestor de assets con rutas relativas.
- **`pygame_app/main.py`**: Punto de entrada inicial con loop principal integrado.
- **`grafica/componentes.py`**: Sistema de UI (Clases `Boton` e `InputBox`) con efectos visuales.

### 2. Estructura de Carpetas:
- `pygame_app/`: Raíz del nuevo código fuente.
    - `logica/`: Procesamiento de datos y reglas de juego.
    - `grafica/`: Dibujado y componentes visuales.
- `assets/`: Imágenes (Fondo: `juego_ia.png`, `menu_ia.png`).
- `sounds/`: Audio.
- `data/`: Archivos de configuración y datos persistentes.

## 🎯 Próximo Paso
El siguiente paso es la implementación de un **Gestor de Pantallas (Screen Manager)**. Esto permitirá:
1. Navegar entre Menú, Juego, Configuración y Podio de manera modular.
2. Cada pantalla será una clase o módulo independiente dentro de `grafica/`.

---
*Ultima actualización: Febrero 2026 - Fase de Reconstrucción: Componentes finalizados*
