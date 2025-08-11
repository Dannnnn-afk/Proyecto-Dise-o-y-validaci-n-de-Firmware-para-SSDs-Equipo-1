import json
from src.nvme_wrapper import NvmeCommands
from src.logger import TestLogger

class NvmeIdCtrlTest:
    def __init__(self, nvme_wrapper, logger):
        self.nvme = nvme_wrapper
        self.logger = logger
    
    def run(self, reference_file_path):
        self.logger.log_test_start("test_id_ctrl")
        
        output = self.nvme.idctrol(json_output=True)
        if output is None:
            self.logger.log_test_end("test_id_ctrl", "FAIL")
            return False
        
        with open(reference_file_path, "r") as f:
            reference = json.load(f)
        
        ignore_fields = ["sn", "fguid", "unvmcap", "subnqn"]
        errors = 0
        
        for key, expected_value in reference.items():
            if key in ignore_fields:
                continue
            actual_value = output.get(key)
            if actual_value != expected_value:
                errors += 1
                self.logger.error(f"Error en campo '{key}': esperado '{expected_value}', encontrado '{actual_value}'")
            else:
                self.logger.info(f"Campo '{key}' coincide: {actual_value}")
        
        if errors == 0:
            self.logger.log_test_end("test_id_ctrl", "PASS")
            return True
        else:
            self.logger.log_test_end("test_id_ctrl", "FAIL")
            return False


# --- Esto es para testear el archivo directamente ---

if __name__ == "__main__":
    logger = TestLogger("id_ctrl_test").initialize_logger()
    nvme = NvmeCommands(logger)
    test = NvmeIdCtrlTest(nvme, logger)
    test.run("tests/id-ctrl-main.json")  # Ruta relativa al JSON de referencia
