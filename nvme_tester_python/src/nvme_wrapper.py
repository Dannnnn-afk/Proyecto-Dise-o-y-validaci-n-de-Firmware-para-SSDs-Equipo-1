import subprocess
import json

from ..tests.test_logger import TestLogger

DEVICE = "/dev/nvme0"
NVME = "nvme"


class NvmeCommands():
    def __init__(self, logger, device=DEVICE, nvme_cli=NVME):
        self.logger = logger
        self.device = device
        self.nvme_cli = nvme_cli

    def run_command(self, cmd):
        command = " ".join(cmd)
        self.logger.debug(f"Executing command: {command}")
        try:
            run_cmd = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return run_cmd.stdout
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error found during execution")
            self.logger.error(f"Return Code: {e.returncode}")
            self.logger.error(f"STDout: {e.stdout}")
            self.logger.error(f"STDError: {e.stderr}")
            return None
        
    def list(self, verbose=False, json_output=False):
        cmd = [
            self.nvme_cli,
            "list"
        ]

        if verbose:
            cmd.append("-v")
        if json_output:
            cmd.append("--output-format=json")

        output = self.run_command(cmd)

        if json_output:
            output = json.loads(output)

        return output


test_logger = TestLogger("Prueba1")
logger = test_logger.initialize_logger()

nvme = NvmeCommands(logger)
list_output = nvme.list()
logger.debug(list_output)