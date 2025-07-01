from database import crear_base_si_no_existe, crear_tablas
from ui import pantalla_bienvenida

if __name__ == "__main__":
    crear_base_si_no_existe()
    crear_tablas()
    pantalla_bienvenida()
