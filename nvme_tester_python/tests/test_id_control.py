import json
import sys
import os

# Path to read the json from anywhere
file_path = os.path.join(os.path.dirname(os.path.abspath(os.path.join(__file__, ".."))),  # up to main.py's folder
                         "utils", "json", "idcontrol.json"
                         )

from src.nvme_wrapper import NvmeCommands
from src.logger import TestLogger

# Path to the JSON file with expected values (relative to this file)
file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "utils", "json", "idcontrol.json")


class NvmeIdCtrlTest:
    def __init__(self, nvme_wrapper, logger):
        self.nvme = nvme_wrapper
        self.logger = logger
    
    def run(self):
        self.logger.log_test_start("test_id_ctrl")
        
        self.logger.info("Ejecutando comando nvme id-ctrl...")
        output = self.nvme.idctrol(json_output=True)
        if output is None:
            self.logger.error("No se pudo obtener la salida del comando nvme id-ctrl")
            self.logger.log_test_end("test_id_ctrl", "FAIL")
            return False
        
        self.logger.info(f"Comando ejecutado exitosamente. Cargando archivo de referencia: {file_path}")
        
        try:
            with open(file_path, "r") as f:
                reference = json.load(f)
            self.logger.info(f"Archivo de referencia cargado exitosamente con {len(reference)} campos")
        except FileNotFoundError:
            self.logger.error(f"No se encontró el archivo de referencia: {file_path}")
            self.logger.log_test_end("test_id_ctrl", "FAIL")
            return False
        except json.JSONDecodeError as e:
            self.logger.error(f"Error al decodificar JSON: {e}")
            self.logger.log_test_end("test_id_ctrl", "FAIL")
            return False
        
        ignore_fields = ["sn", "fguid", "unvmcap", "subnqn"]
        self.logger.info(f"Campos ignorados en la comparación: {ignore_fields}")
        
        errors = 0
        matches = 0
        total_fields = len([k for k in reference.keys() if k not in ignore_fields])
        
        self.logger.info(f"Iniciando comparación de {total_fields} campos...")
        
        for key, expected_value in reference.items():
            if key in ignore_fields:
                self.logger.debug(f"Campo '{key}' ignorado como se esperaba")
                continue
                
            actual_value = output.get(key)
            if actual_value != expected_value:
                errors += 1
                self.logger.error(f" Campo '{key}': esperado '{expected_value}', encontrado '{actual_value}'")
            else:
                matches += 1
                self.logger.info(f" Campo '{key}' coincide: {actual_value}")
        
        # Resumen de resultados
        self.logger.info(f"Resumen de comparación:")
        self.logger.info(f"  - Total de campos comparados: {total_fields}")
        self.logger.info(f"  - Campos que coinciden: {matches}")
        self.logger.info(f"  - Campos con errores: {errors}")
        self.logger.info(f"  - Tasa de éxito: {(matches/total_fields)*100:.1f}%")
        
        if errors == 0:
            self.logger.info(" Todos los campos coinciden perfectamente!")
            self.logger.log_test_end("test_id_ctrl", "PASS")
            return True
        else:
            self.logger.warning(f" Se encontraron {errors} errores en la comparación")
            self.logger.log_test_end("test_id_ctrl", "FAIL")
            return False

