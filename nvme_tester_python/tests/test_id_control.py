import json
import sys
import os

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.nvme_wrapper import NvmeCommands
from src.logger import TestLogger

file_path = r"nvme_tester_python/utils/json/idcontrol.json"  # Path to the JSON file with expected values


class NvmeIdCtrlTest:
    def __init__(self, nvme_wrapper, logger):
        self.nvme = nvme_wrapper
        self.logger = logger
    
    def run(self):
        self.logger.log_test_start("test_id_ctrl")
        
        output = self.nvme.idctrol(json_output=True)
        if output is None:
            self.logger.log_test_end("test_id_ctrl", "FAIL")
            return False
        
        with open(file_path, "r") as f:
            reference = json.load(f)
        
        ignore_fields = ["sn", "fguid", "unvmcap", "subnqn"]
        errors = 0
        
        for key, expected_value in reference.items():
            if key in ignore_fields:
                continue
            actual_value = output.get(key)
            if actual_value != expected_value:
                errors += 1
                self.logger.info(f"Error en campo '{key}': esperado '{expected_value}', encontrado '{actual_value}'")
            else:
                self.logger.info(f"Campo '{key}' coincide: {actual_value}")
        
        if errors == 0:
            self.logger.log_test_end("test_id_ctrl", "PASS")
            return True
        else:
            self.logger.log_test_end("test_id_ctrl", "FAIL")
            return False

