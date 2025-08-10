import logging
import os
from datetime import datetime

class TestLogger:
    """
    Estructura básica de logger usando la biblioteca logging de Python.
    
    Componentes principales:
    1. Logger: Objeto principal que registra mensajes
    2. Handlers: Definen dónde van los logs (consola, archivo, etc.)
    3. Formatters: Definen el formato de los mensajes
    4. Levels: Definen la severidad (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    
    def __init__(self, name="TestLogger"):
        """
        Inicializar el logger con configuración básica.
        
        Args:
            name (str): Nombre del logger
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Nivel más bajo para capturar todo
        
        # Evitar duplicar handlers si ya existen
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """
        Configurar los handlers (dónde van los logs).
        """
        # 1. HANDLER PARA CONSOLA
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 2. HANDLER PARA ARCHIVO
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"{self.name}_{timestamp}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # 3. FORMATTERS (cómo se ven los mensajes)
        # Formato para consola (más simple)
        console_format = logging.Formatter(
            '%(levelname)-8s | %(message)s'
        )
        
        # Formato para archivo (más detallado)
        file_format = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s'
        )
        
        # 4. ASIGNAR FORMATTERS A HANDLERS
        console_handler.setFormatter(console_format)
        file_handler.setFormatter(file_format)
        
        # 5. AGREGAR HANDLERS AL LOGGER
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    # =====================================
    # MÉTODOS BÁSICOS DE LOGGING
    # =====================================
    
    def debug(self, message):
        """Mensajes de depuración (solo en archivo)."""
        self.logger.debug(message)
    
    def info(self, message):
        """Mensajes informativos."""
        self.logger.info(message)
    
    def warning(self, message):
        """Mensajes de advertencia."""
        self.logger.warning(message)
    
    def error(self, message):
        """Mensajes de error."""
        self.logger.error(message)
    
    def critical(self, message):
        """Mensajes críticos."""
        self.logger.critical(message)
    
    # =====================================
    # MÉTODOS ESPECÍFICOS PARA TESTS
    # =====================================
    
    def log_test_start(self, test_name):
        """Iniciar un test."""
        self.info(f" INICIANDO TEST: {test_name}")
        self.debug(f"Test {test_name} started at {datetime.now()}")
    
    def log_test_end(self, test_name, result):
        """Finalizar un test."""
        if result.upper() == "PASS":
            self.info(f" TEST COMPLETADO: {test_name} - {result}")
        else:
            self.error(f" TEST FALLIDO: {test_name} - {result}")
        self.debug(f"Test {test_name} ended at {datetime.now()}")
    
    def log_command(self, command, result="SUCCESS"):
        """Log de ejecución de comandos."""
        if result.upper() == "SUCCESS":
            self.info(f" Comando ejecutado: {command}")
        else:
            self.error(f" Error en comando: {command} - {result}")
        self.debug(f"Command details: {command} -> {result}")
    
    # =====================================
    # CONFIGURACIÓN AVANZADA
    # =====================================
    
    def set_level(self, level):
        """
        Cambiar el nivel de logging.
        
        Args:
            level: logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
        """
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                handler.setLevel(level)
    
    def add_file_handler(self, filename):
        """Agregar un handler de archivo adicional."""
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)-8s | %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.debug(f"Added file handler: {filename}")
    
    def get_logger(self):
        """Obtener el objeto logger nativo."""
        return self.logger


# =====================================
# FUNCIÓN AUXILIAR PARA CREAR LOGGER
# =====================================

def create_logger(name="TestLogger", level=logging.INFO):
    """
    Función auxiliar para crear un logger rápidamente.
    
    Args:
        name (str): Nombre del logger
        level: Nivel de logging
    
    Returns:
        TestLogger: Instancia configurada
    """
    logger = TestLogger(name)
    logger.set_level(level)
    return logger


# =====================================
# EJEMPLO DE USO
# =====================================

if __name__ == "__main__":
    # Crear logger
    logger = TestLogger("ejemplo_nvme")
    
    # Usar métodos básicos
    logger.info("Iniciando sistema de logging")
    logger.debug("Este mensaje solo aparece en el archivo")
    logger.warning("Esta es una advertencia")
    logger.error("Este es un error")
    
    # Usar métodos específicos
    logger.log_test_start("test_smart_log")
    logger.log_command("nvme id-ctrl /dev/nvme0n1")
    logger.log_test_end("test_smart_log", "PASS")
    
    print(f"\n📁 Logs guardados en: logs/{logger.name}_*.log")
