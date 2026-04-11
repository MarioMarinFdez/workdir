import logging
import sys

# Configuración global que funciona con uvicorn
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True
)

# Forzar que el root logger también muestre
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    return logger
