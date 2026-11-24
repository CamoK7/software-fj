"""
Módulo de configuración del archivo de logs.

Aquí se prepara el módulo "logging" de Python para que todos los eventos
y errores del sistema se guarden en el archivo logs/software_fj.log
"""

import logging  # módulo estándar de Python para registrar eventos
import os       # módulo para trabajar con carpetas y rutas

# Ruta de la carpeta "logs" (queda junto a este archivo, sin importar desde dónde se ejecute)
CARPETA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
# Ruta completa del archivo de logs
ARCHIVO_LOGS = os.path.join(CARPETA_LOGS, "software_fj.log")


def configurar_logs():
    """Crea la carpeta de logs (si no existe) y configura el formato del registro."""
    # Crea la carpeta "logs"; si ya existe no pasa nada
    os.makedirs(CARPETA_LOGS, exist_ok=True)
    # Configura el archivo, el nivel mínimo y cómo se ve cada línea del log
    logging.basicConfig(
        filename=ARCHIVO_LOGS,
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        encoding="utf-8",
    )
