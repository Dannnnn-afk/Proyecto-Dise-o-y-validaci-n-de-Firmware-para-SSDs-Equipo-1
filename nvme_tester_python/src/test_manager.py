import sys
import os

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .logger import TestLogger
from .nvme_wrapper import NvmeCommands

from tests.test_id_control import NvmeIdCtrlTest as testIdControl
from tests.test_smart_log import NvmeSmartLogTemperatureTest as NvmeSmartLogTemperatureTest
from tests.test_smart_log_healt import TestSmartLogHealt as testSmartLogHealt

# Define set of available tests
tests_pool = {
    "test_id_control": testIdControl,
    "test_smart_log": NvmeSmartLogTemperatureTest,
    "test_smart_log_healt": testSmartLogHealt,
    # Add more tests as needed  
              }


class TestManager(object):
    def __init__(self, serial_number, testname):
        self.serial_number = serial_number
        self.testname = testname
        self.nvme = None
        self.physical_path = None
        self.logger = TestLogger(self.testname)
        self.test = None

        if self.initialize() is None:
            self.logger.error(f"Unable to get Physical Path for SN: {self.serial_number}")
            return

        if testname not in tests_pool:
            test_list = list(tests_pool.keys())
            self.logger.error(f"Test {testname} was not found. Tests Available: {test_list}")
            self.logger.error(f"Make sure the test you are trying to execute has been defined.")
            return
        self.test = tests_pool[self.testname](self.nvme, self.logger)

    def initialize(self):
        """
        Inicializa el wrapper NVMe y obtiene la ruta física del dispositivo.
        
        Returns:
            str: Ruta física del dispositivo si se encuentra, None si falla
        """
        try:
            # Initialize the NVMe wrapper with temporary empty device for device discovery
            temp_nvme = NvmeCommands(self.logger)
            
            # Get the physical path of the NVMe device
            nvme_list_output = temp_nvme.command_list(json_output=True)
            if nvme_list_output is None:
                self.logger.error("Failed to get NVMe device list")
                return None
                
            self.physical_path = self.get_device_path(self.serial_number, nvme_list_output)
            
            if self.physical_path is None:
                self.logger.error(f"Device with serial number {self.serial_number} not found")
                return None
                
            self.logger.info(f"Device found: {self.physical_path}")
            
            # Now initialize the NVMe wrapper with the correct device path
            self.nvme = NvmeCommands(self.logger, device=self.physical_path)
            
            return self.physical_path
            
        except Exception as e:
            self.logger.error(f"Error during initialization: {e}")
            return None

    def run(self):
        """
        Ejecuta la prueba seleccionada.
        
        Returns:
            object: Resultado de la prueba si es exitosa, None si falla
        """
        try:
            if self.test is None:
                self.logger.error("No test instance available")
                return None
                
            if self.physical_path is None:
                self.logger.error("No physical path available")
                return None
                
            # Log inicio de la prueba
            self.logger.info(f"Running test: {self.testname} for device {self.physical_path}")
            
            # Ejecutar la prueba usando la instancia correcta
            result = self.test.run()
            
            if result is not None:
                self.logger.info(f"Test {self.testname} execution completed successfully.")
            else:
                self.logger.error(f"Test {self.testname} execution failed")
                
            return result
            
        except Exception as e:
            self.logger.error(f"Error during test execution: {e}")
            return None

    def set_final_result(self):
        """
        Procesa y valida los resultados finales de la prueba.
        """
        try:
            # Aquí puedes agregar lógica para:
            # - Validar resultados de la prueba
            # - Generar reportes finales
            # - Guardar métricas
            self.logger.info("Processing final test results...")
            
            # Placeholder para lógica de validación
            pass
            
        except Exception as e:
            self.logger.error(f"Error processing final results: {e}")

    def drive_check(self, discovery=True):
        """
        Realiza verificaciones de salud y discovery del dispositivo.
        
        Args:
            discovery (bool): True para discovery inicial, False para verificación final
        """
        try:
            if discovery:
                self.logger.info("Performing initial drive discovery and health check...")
                # Verificaciones iniciales:
                # - Comprobar que el dispositivo esté accesible
                # - Verificar estado de salud básico
                # - Obtener información del dispositivo
                
                if self.nvme:
                    # Ejemplo: obtener información básica del dispositivo
                    id_ctrl = self.nvme.idctrol(json_output=True)
                    if id_ctrl:
                        self.logger.info("Drive health check passed")
                    else:
                        self.logger.warning("Could not retrieve device information")
            else:
                self.logger.info("Performing final drive check...")
                # Verificaciones finales:
                # - Comprobar que el dispositivo sigue operativo
                # - Verificar que no hay errores críticos
                # - Log del estado final
                
        except Exception as e:
            self.logger.error(f"Error during drive check: {e}")

    def get_device_path(self, serial_number, nvme_list):
        """
        Busca la ruta física del dispositivo basado en el número de serie.
        
        Args:
            serial_number (str): Número de serie del dispositivo
            nvme_list (dict/list): Salida del comando nvme list
            
        Returns:
            str: Ruta del dispositivo (/dev/nvmeX) o None si no se encuentra
        """
        try:
            if not nvme_list:
                self.logger.error("Empty nvme list provided")
                return None
                
            # Si nvme_list es un diccionario con 'Devices'
            if isinstance(nvme_list, dict) and 'Devices' in nvme_list:
                devices = nvme_list['Devices']
            elif isinstance(nvme_list, list):
                devices = nvme_list
            else:
                self.logger.error("Unexpected nvme list format")
                return None
                
            # Buscar el dispositivo por número de serie
            for device in devices:
                if isinstance(device, dict):
                    # Diferentes campos posibles para el número de serie
                    device_sn = device.get('SerialNumber') or device.get('sn') or device.get('serial')
                    device_path = device.get('DevicePath') or device.get('device') or device.get('path')
                    
                    if device_sn and device_sn.strip() == serial_number.strip():
                        self.logger.info(f"Found device {device_path} with serial {device_sn}")
                        return device_path
                        
            self.logger.error(f"Device with serial number {serial_number} not found in nvme list")
            return None
            
        except Exception as e:
            self.logger.error(f"Error searching for device path: {e}")
            return None


