import json
import subprocess
DEVICE = "/dev/nvme0"
NVME = "nvme"

class NvmeIdCtrlTest:
    def __init__(self, device=DEVICE, nvme_cli=NVME):
        #self.nvme = nvme_wrapper
        #self.logger = logger
        self.device = device
        self.nvme_cli = nvme_cli
        
    def run_command(self, cmd):
        command = " ".join(cmd)
        print(f"Executing command: {command}")
        try:
            run_cmd = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return run_cmd.stdout
        except subprocess.CalledProcessError as e:
            return None

    def idctrol(self, **kwargs):
        cmd = [
            self.nvme_cli,
            "id-ctrl",
            self.device
        ]
        options = self.parametrizeOpcionsLogs(**kwargs)
        cmd.extend(options)
        output = self.run_command(cmd)
    
        if kwargs.get('json_output', False) and output:
            output = json.loads(output)
        return output

    def run(self, reference_file_path):
        # self.logger.log_test_start("test_id_ctrl")

        output = self.idctrol(json_output=True)
        if output is None:
            # self.logger.log_test_end("test_id_ctrl", "FAIL")
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
                # self.logger.error(f"Error en campo '{key}': esperado '{expected_value}', encontrado '{actual_value}'")
            else:
                # self.logger.info(f"Campo '{key}' coincide: {actual_value}")
                pass

        if errors == 0:
            # self.logger.log_test_end("test_id_ctrl", "PASS")
            return True
        else:
            # self.logger.log_test_end("test_id_ctrl", "FAIL")
            return False

# --- Esto es para testear el archivo directamente ---

if __name__ == "__main__":
   # logger = TestLogger("id_ctrl_test").initialize_logger()
   # nvme = NvmeCommands(logger)
    test = NvmeIdCtrlTest()
    test.run("tests/id-ctrl-main.json")  # Ruta relativa al JSON de referencia
