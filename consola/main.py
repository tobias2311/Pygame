from funciones_basicas import limpiar_pantalla
from inicio_sesion import abrir_juego
import sys

def main() -> None:
    limpiar_pantalla()
    abrir_juego()

if __name__ == "__main__":
    sys.exit(main())