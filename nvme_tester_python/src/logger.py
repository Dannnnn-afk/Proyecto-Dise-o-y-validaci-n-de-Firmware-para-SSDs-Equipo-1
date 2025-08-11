import logging
import os
from datetime import datetime

class TestLogger:
    def __init__(self, name="TestLogger"):
        """
        Start logger functions.
        Input:
        name (str): Logger name.
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            self._setup_handlers()

    def _setup_handler(self):
        """
        File handler with date.
        """
        import logging
        import os
        from datetime import datetime

        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"{self.name}_{timestamp}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s'
        )
        file_handler.setFormatter(file_format)

        self.logger.addHandler(file_handler)

    def log_test_start(self, test_name):
        """
        Start logger.
        Input:
        test_name (str): Test Case (TC) name.
        """
        self.info(f"TEST START: {test_name}")
        self.info(f"Test {test_name} started at {datetime.now()}")

    def log_test_end(self, test_name, result):
        """
        Stop logger.
        Input:
        test_name (str): Test Case (TC) name.
        result (str): Test result
        """
        if result.upper() == "PASS":
            self.info(f" TEST COMPLETED: {test_name} - {result}")
        else:
            self.info(f" TEST FAILED: {test_name} - {result}")
        self.info(f"Test {test_name} ended at {datetime.now()}")

    def log_command(self, command, result):
        """
        Stop logger.
        Input:
        command (str): full command.
        result (str): output of command.
        """
        if result == 0:
            self.info(f"Comando ejecutado: {command}")
        else:
            self.info(f"Error en comando: {command} - {result}")
        self.info(f"Command details: {command} -> {result}")

    def set_level(self, level):
        """
        Change logging level.
        Args:
            level: logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
        """
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler):
                handler.setLevel(level)
