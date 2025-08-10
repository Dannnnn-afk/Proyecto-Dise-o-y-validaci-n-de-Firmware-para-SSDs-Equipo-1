import subprocess
import json

from ..src.logger import TestLogger



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
    
    def parametrizeOpcionsLogs(self, verbose=False, json_output=False, binary_raw=False):
        options = []
        if verbose:
            options.append("-v")
        if json_output:
            options.append("--output-format=json")
        if binary_raw:
            options.append("-b")
        return options
    
    """Ejemplo de como se llamaria una funcion #Crear namespace con configuración completa
    nvme.create_ns(
    nsze=1000000,        # 1M bloques
    ncap=1000000,        # 1M capacidad
    flbas=0,             # Formato LBA 0
    dps=0,               # Sin protección de datos
    block_size=4096,     # Bloques de 4KB
    timeout=30,          # Timeout de 30s
    azr=True,            # Habilitar ZNS
    json_output=True,    # Salida en JSON
    verbose=True         # Verbose output
    #)  """      

    def parametrizeOpcionsConfig(self, nsze=None, ncap=None, flbas=None, dps=None, nmic=None, 
                                anagrp_id=None, nvmset_id=None, endg_id=None, csi=None, 
                                lbstm=None, nphndls=None, block_size=None, timeout=None,
                                nsze_si=None, ncap_si=None, azr=False, rar=None, ror=None,
                                rnumzrwa=None, phndls=None):
        options = []
        
        # Namespace Size (nsze) - número de bloques lógicos
        if nsze is not None:
            options.extend(["--nsze", str(nsze)])
        
        # Namespace Capacity (ncap) - capacidad del namespace
        if ncap is not None:
            options.extend(["--ncap", str(ncap)])
        
        # Formatted LBA Size (flbas) - tamaño del bloque lógico formateado
        if flbas is not None:
            options.extend(["--flbas", str(flbas)])
        
        # Data Protection Settings (dps) - configuración de protección de datos
        if dps is not None:
            options.extend(["--dps", str(dps)])
        
        # Namespace Multi-path I/O and Namespace Sharing (nmic) 
        if nmic is not None:
            options.extend(["--nmic", str(nmic)])
        
        # ANA Group Identifier (anagrp-id) - identificador del grupo ANA
        if anagrp_id is not None:
            options.extend(["--anagrp-id", str(anagrp_id)])
        
        # NVM Set Identifier (nvmset-id) - identificador del conjunto NVM
        if nvmset_id is not None:
            options.extend(["--nvmset-id", str(nvmset_id)])
        
        # Endurance Group Identifier (endg-id) - identificador del grupo de resistencia
        if endg_id is not None:
            options.extend(["--endg-id", str(endg_id)])
        
        # Command Set Identifier (csi) - identificador del conjunto de comandos
        if csi is not None:
            options.extend(["--csi", str(csi)])
        
        # Logical Block Storage Tag Mask (lbstm) - máscara de etiqueta de almacenamiento
        if lbstm is not None:
            options.extend(["--lbstm", str(lbstm)])
        
        # Number of Placement Handles (nphndls) - número de manejadores de ubicación
        if nphndls is not None:
            options.extend(["--nphndls", str(nphndls)])
        
        # Block Size (block-size) - tamaño del bloque
        if block_size is not None:
            options.extend(["--block-size", str(block_size)])
        
        # Timeout (timeout) - tiempo límite
        if timeout is not None:
            options.extend(["--timeout", str(timeout)])
        
        # Namespace Size SI (nsze-si) - tamaño del namespace en unidades SI
        if nsze_si is not None:
            options.extend(["--nsze-si", str(nsze_si)])
        
        # Namespace Capacity SI (ncap-si) - capacidad del namespace en unidades SI
        if ncap_si is not None:
            options.extend(["--ncap-si", str(ncap_si)])
        
        # Allocate Zoned Random Write Area (azr) - asignar área de escritura aleatoria zonificada
        if azr:
            options.append("--azr")
        
        # Random Area Requested (rar) - área aleatoria solicitada
        if rar is not None:
            options.extend(["--rar", str(rar)])
        
        # Random Optimal Requested (ror) - óptimo aleatorio solicitado
        if ror is not None:
            options.extend(["--ror", str(ror)])
        
        # Random Number Zoned Random Write Area (rnumzrwa) - número aleatorio de área de escritura aleatoria zonificada
        if rnumzrwa is not None:
            options.extend(["--rnumzrwa", str(rnumzrwa)])
        
        # Placement Handles (phndls) - manejadores de ubicación
        if phndls is not None:
            options.extend(["--phndls", str(phndls)])

        return options
   # --- Comandos de logs y diagnóstico ---
    def command_list(self,verbose=False, json_output=False, binary_raw=False):
        cmd = [
            self.nvme_cli,
            "list",
            self.device
        ]
        options = self.parametrizeOpcionsLogs(verbose, json_output, binary_raw)
        cmd.extend(options)
        

        output = self.run_command(cmd)

        if json_output:
            output = json.loads(output)

        return output
    def smart_log(self, verbose=False, json_output=False, binary_raw=False):
        cmd = [
            self.nvme_cli,
            "smart_log",
            self.device
        ]
        options = self.parametrizeOpcionsLogs(verbose, json_output, binary_raw)
        cmd.extend(options)
        #Logger 

        output = self.run_command(cmd)
        
        if json_output:
            output = json.loads(output)
        return output


    def idctrol(self, verbose=False, json_output=False, binary_raw=False):
        cmd = [
            self.nvme_cli,
            "id-ctrl",
            self.device
        ]
        options = self.parametrizeOpcionsLogs(verbose, json_output, binary_raw)
        cmd.extend(options)
        
        output = self.run_command(cmd)
        
        if json_output:
            output = json.loads(output)
        return output
        

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
    def set_feature(self, **kwargs):
        cmd = [
            self.nvme_cli,
            "set-feature",
            self.device
        ]
        
        # Agregar opciones de configuración usando la función parametrize
        config_options = self.parametrizeOpcionsConfig(**kwargs)
        cmd.extend(config_options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            output = json.loads(output)
            
        return output
    def get_property(self, **kwargs):
        cmd = [
            self.nvme_cli,
            "get-property",
            self.device
        ]
        
        # Agregar opciones de configuración usando la función parametrize
        config_options = self.parametrizeOpcionsConfig(**kwargs)
        cmd.extend(config_options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            output = json.loads(output)
            
        return output
    def set_property(self, **kwargs):
        cmd = [
            self.nvme_cli,
            "set-property",
            self.device
        ]
        
        # Agregar opciones de configuración usando la función parametrize
        config_options = self.parametrizeOpcionsConfig(**kwargs)
        cmd.extend(config_options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            output = json.loads(output)
            
        return output
    def ns_attach(self, **kwargs):
        cmd = [
            self.nvme_cli,
            "ns-attach",
            self.device
        ]
        
        # Agregar opciones de configuración usando la función parametrize
        config_options = self.parametrizeOpcionsConfig(**kwargs)
        cmd.extend(config_options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            output = json.loads(output)
            
        return output
    def ns_detach(self, **kwargs):
        cmd = [
            self.nvme_cli,
            "ns-detach",
            self.device
        ]
        
        # Agregar opciones de configuración usando la función parametrize
        config_options = self.parametrizeOpcionsConfig(**kwargs)
        cmd.extend(config_options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            output = json.loads(output)
            
        return output
    def create_ns(self, **kwargs):
        cmd = [
            self.nvme_cli,
            "create-ns",
            self.device
        ]
        
        # Agregar opciones de configuración usando la función parametrize
        config_options = self.parametrizeOpcionsConfig(**kwargs)
        cmd.extend(config_options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            output = json.loads(output)
            
        return output
    def delete_ns(self, **kwargs):
        cmd = [
            self.nvme_cli,
            "delete-ns",
            self.device
        ]
        
        # Agregar opciones de configuración usando la función parametrize
        config_options = self.parametrizeOpcionsConfig(**kwargs)
        cmd.extend(config_options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            output = json.loads(output)
            
        return output
    def ns_rescan(self, **kwargs):
        cmd = [
            self.nvme_cli,
            "ns-rescan",
            self.device
        ]
        
        # Agregar opciones de configuración usando la función parametrize
        config_options = self.parametrizeOpcionsConfig(**kwargs)
        cmd.extend(config_options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            output = json.loads(output)
            
        return output

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