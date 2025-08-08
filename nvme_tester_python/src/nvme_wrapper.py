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

    # --- Comandos de logs y diagnóstico ---
    def fw_log(self):
        pass
    def effects_log(self):
        pass
    def endurance_log(self):
        pass
    def predictable_lat_log(self):
        pass
    def telemetry_log(self):
        pass
    def changed_ns_list_log(self):
        pass
    def persistent_event_log(self):
        pass
    def sanitize_log(self):
        pass
    def get_log(self):
        pass

    # --- Comandos de I/O y testing ---
    def read(self):
        pass
    def write(self):
        pass
    def write_zeros(self):
        pass
    def write_uncor(self):
        pass
    def compare(self):
        pass
    def verify(self):
        pass
    def flush(self):
        pass
    def dsm(self):
        pass
    def copy(self):
        pass

    # --- Comandos de configuración ---
    def set_feature(self):
        pass
    def get_property(self):
        pass
    def set_property(self):
        pass
    def ns_attach(self):
        pass
    def ns_detach(self):
        pass
    def create_ns(self):
        pass
    def delete_ns(self):
        pass
    def ns_rescan(self):
        pass

    # --- Comandos de seguridad ---
    def security_send(self):
        pass
    def security_recv(self):
        pass
    def sanitize(self):
        pass
    def crypto_scramble(self):
        pass

    # --- Comandos administrativos ---
    def reset(self):
        pass
    def subsystem_reset(self):
        pass
    def rescan(self):
        pass
    def show_regs(self):
        pass
    def discover(self):
        pass
    def connect(self):
        pass
    def disconnect(self):
        pass
    def dim(self):
        pass

    # --- Comandos de firmware ---
    def fw_download(self):
        pass
    def fw_commit(self):
        pass
    def fw_download_status(self):
        pass

    # --- Comandos de utilidad ---
    def help(self):
        pass
    def version(self):
        pass
    def show_topology(self):
        pass
    def monitor(self):
        pass
    


test_logger = TestLogger("Prueba1")
logger = test_logger.initialize_logger()

nvme = NvmeCommands(logger)
list_output = nvme.list()
logger.debug(list_output)