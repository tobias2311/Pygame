# Contexto del Proyecto: Desafío Mental (Estado Actual)

Este documento resume el progreso actual y las tareas pendientes para mantener el enfoque en el desarrollo.

## 🚀 Estado Actual
Hemos dado un salto importante en la estética y la experiencia de usuario, integrando recursos multimedia y un sistema de control de sonido dinámico.

### Módulos Finalizados (Mantenimiento):
- **Sistema de Archivos**: Carga de CSV y JSON centralizada.
- **UI Paramétrica**: Interfaz 100% dependiente de `config.json` (incluyendo botones de volumen).
- **Multimedia**: Fondos generados por IA aplicados al Menú y Juego. Música diferenciada para cada escena.
- **Control de Sonido**: Botones de Vol+, Vol- y Mute integrados en Menú y Juego con sincronización global.
- **Control de Usuarios**: Registro y Login con base de datos `cuentas.json`.
- **Motor de Juego**: Filtrado de preguntas por temática/dificultad y sistema de puntuación dinámica.

## 🎯 Plan de Trabajo Próximo
Prioridades para las siguientes sesiones:

1.  **Modo TDAH (Configuración)**:
    *   Habilitar/Deshabilitar el cronómetro.
    *   Simplificar la UI del juego para reducir distracciones.
2.  **Gestión de Récords**:
    *   Actualizar el `puntaje_maximo` en `cuentas.json` al terminar cada partida.
3.  **Pantalla de Ranking (Podio)**:
    *   Mostrar los mejores puntajes globales cargados desde `cuentas.json`.

---
*Última actualización: Febrero 2026 - Fase: Multimedia y Control de Sonido finalizados.*
