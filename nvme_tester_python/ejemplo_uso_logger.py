#!/usr/bin/env python3
"""
Ejemplo de uso de la estructura básica del logger
"""

import logging
from src.logger import TestLogger, create_logger

def ejemplo_basico():
    """Demostración básica del logger."""
    print("=" * 50)
    print("EJEMPLO 1: Uso básico del logger")
    print("=" * 50)
    
    # Crear logger
    logger = TestLogger("test_ejemplo")
    
    # Usar los 5 niveles de logging
    logger.debug("Mensaje de DEBUG (solo en archivo)")
    logger.info("Mensaje de INFO")
    logger.warning("Mensaje de WARNING")
    logger.error("Mensaje de ERROR")
    logger.critical("Mensaje CRITICAL")

def ejemplo_test_completo():
    """Ejemplo de un test completo."""
    print("\n" + "=" * 50)
    print("EJEMPLO 2: Test completo con logging")
    print("=" * 50)
    
    # Crear logger para un test específico
    logger = TestLogger("nvme_smart_test")
    
    # Simular un test completo
    logger.log_test_start("Verificación SMART del SSD")
    
    logger.info("Conectando con dispositivo /dev/nvme0n1")
    logger.log_command("nvme list", "SUCCESS")
    
    logger.info("Obteniendo datos SMART")
    logger.log_command("nvme smart-log /dev/nvme0n1", "SUCCESS")
    
    logger.warning("Temperatura alta detectada: 75°C")
    logger.info("Verificando umbral de temperatura")
    
    logger.log_test_end("Verificación SMART del SSD", "PASS")

def ejemplo_con_errores():
    """Ejemplo con manejo de errores."""
    print("\n" + "=" * 50)
    print("EJEMPLO 3: Manejo de errores")
    print("=" * 50)
    
    logger = TestLogger("test_con_errores")
    
    logger.log_test_start("Test con errores simulados")
    
    # Simular errores
    logger.error("No se puede acceder al dispositivo /dev/nvme0n1")
    logger.log_command("nvme id-ctrl /dev/nvme0n1", "FAILED - Device not found")
    
    logger.critical("Error crítico: Hardware no responde")
    
    logger.log_test_end("Test con errores simulados", "FAIL")

def ejemplo_niveles():
    """Ejemplo de cambio de niveles."""
    print("\n" + "=" * 50)
    print("EJEMPLO 4: Cambio de niveles de logging")
    print("=" * 50)
    
    logger = TestLogger("test_niveles")
    
    logger.info("Nivel por defecto: INFO")
    logger.debug("Este DEBUG no se ve en consola")
    
    # Cambiar a nivel DEBUG
    logger.set_level(logging.DEBUG)
    logger.info("Cambiado a nivel DEBUG")
    logger.debug("Ahora este DEBUG sí se ve")
    
    # Cambiar a nivel ERROR
    logger.set_level(logging.ERROR)
    logger.info("Este INFO ya no se ve")
    logger.error("Solo errores y críticos se ven ahora")

def ejemplo_funcion_auxiliar():
    """Ejemplo usando la función auxiliar."""
    print("\n" + "=" * 50)
    print("EJEMPLO 5: Función auxiliar create_logger")
    print("=" * 50)
    
    # Crear logger con función auxiliar
    logger = create_logger("quick_test", logging.WARNING)
    
    logger.info("Este INFO no se ve (nivel WARNING)")
    logger.warning("Este WARNING sí se ve")
    logger.error("Este ERROR también se ve")

if __name__ == "__main__":
    print("🧪 DEMOSTRACIÓN DE LA ESTRUCTURA BÁSICA DEL LOGGER\n")
    
    ejemplo_basico()
    ejemplo_test_completo()
    ejemplo_con_errores()
    ejemplo_niveles()
    ejemplo_funcion_auxiliar()
    
    print("\n" + "=" * 70)
    print("✅ Ejemplos completados. Revisa la carpeta 'logs/' para ver archivos.")
    print("=" * 70)
