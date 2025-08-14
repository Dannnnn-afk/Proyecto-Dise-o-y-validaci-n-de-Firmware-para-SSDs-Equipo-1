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
        # Create unique logger name to avoid conflicts
        unique_name = f"{name}_{id(self)}"
        self.logger = logging.getLogger(unique_name)
        self.logger.setLevel(logging.INFO)
        
        # Clear any existing handlers to avoid duplicates
        self.logger.handlers = []
        
        self._setup_handler()

    def _setup_handler(self):
        """
        File handler with date and organized by test case.
        Creates structure: nvme_tester_python/logs/test_name/
        """
        import logging
        import os
        from datetime import datetime

        # Get the project root directory (nvme_tester_python)
        # Assuming this file is in src/ subdirectory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)  # Go up one level from src/
        
        # Create logs directory inside nvme_tester_python
        base_log_dir = os.path.join(project_root, "logs")
        if not os.path.exists(base_log_dir):
            os.makedirs(base_log_dir)
        
        # Create subdirectory for each test case
        # Extract test name from logger name (remove any prefixes/suffixes if needed)
        test_name = self.name
        if test_name.startswith("test_"):
            clean_test_name = test_name
        else:
            clean_test_name = f"test_{test_name}"
        
        # Create test-specific subdirectory inside nvme_tester_python/logs/
        test_log_dir = os.path.join(base_log_dir, clean_test_name)
        if not os.path.exists(test_log_dir):
            os.makedirs(test_log_dir)
        
        # Generate timestamp and log file path with uniqueness guarantee
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_log_name = f"{self.name}_{timestamp}.log"
        log_file = os.path.join(test_log_dir, base_log_name)
        
        # Ensure unique filename to avoid overwriting
        counter = 1
        while os.path.exists(log_file):
            unique_log_name = f"{self.name}_{timestamp}_{counter:03d}.log"
            log_file = os.path.join(test_log_dir, unique_log_name)
            counter += 1
            
            # Safety check to avoid infinite loop
            if counter > 999:
                # Use microseconds for even more precision
                microsecond_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                unique_log_name = f"{self.name}_{microsecond_timestamp}.log"
                log_file = os.path.join(test_log_dir, unique_log_name)
                break
        
        # Setup file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s'
        )
        file_handler.setFormatter(file_format)

        self.logger.addHandler(file_handler)
        
        # Log initial information about this log session
        self.logger.info(f"=== LOG SESSION STARTED ===")
        self.logger.info(f"Test Name: {self.name}")
        self.logger.info(f"Log File: {os.path.basename(log_file)}")
        self.logger.info(f"Log Directory: {test_log_dir}")
        self.logger.info(f"Session ID: {id(self)}")
        self.logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"=============================")

    def log_test_start(self, test_name):
        """
        Start logger.
        Input:
        test_name (str): Test Case (TC) name.
        """
        self.logger.info(f"TEST START: {test_name}")
        self.logger.info(f"Test {test_name} started at {datetime.now()}")

    def log_test_end(self, test_name, result):
        """
        Stop logger.
        Input:
        test_name (str): Test Case (TC) name.
        result (str): Test result
        """
        if result.upper() == "PASS":
            self.logger.info(f" TEST COMPLETED: {test_name} - {result}")
        else:
            self.logger.info(f" TEST FAILED: {test_name} - {result}")
        self.logger.info(f"Test {test_name} ended at {datetime.now()}")

    def log_command(self, command, result):
        """
        Stop logger.
        Input:
        command (str): full command.
        result (str): output of command.
        """
        if result == 0:
            self.logger.info(f"Comando ejecutado: {command}")
        else:
            self.logger.info(f"Error en comando: {command} - {result}")
        self.logger.info(f"Command details: {command} -> {result}")

    def info(self, message):
        """Log an info message"""
        self.logger.info(message)
    
    def debug(self, message):
        """Log a debug message"""
        self.logger.debug(message)
    
    def warning(self, message):
        """Log a warning message"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log an error message"""
        self.logger.error(message)
    
    def critical(self, message):
        """Log a critical message"""
        self.logger.critical(message)

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
    
    def debug(self, message: str):
        self.logger.debug(str(message))

    def info(self, message: str):
        self.logger.info(str(message))

    def warning(self, message: str):
        self.logger.warning(str(message))

    def error(self, message: str):
        self.logger.error(str(message))

    def critical(self, message: str):
        self.logger.critical(str(message))
