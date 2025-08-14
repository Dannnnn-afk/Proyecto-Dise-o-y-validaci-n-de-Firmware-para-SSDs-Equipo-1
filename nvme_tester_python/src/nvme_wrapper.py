import subprocess
import json
from datetime import datetime

from .logger import TestLogger


NVME = "nvme"


class NvmeCommands():
    def __init__(self, logger, device="/dev/nvme0", nvme_cli=NVME):
        if logger is None:
            raise ValueError("You require logger instance object from logger.py Class")
        self.logger = logger
        self.device = device
        self.nvme_cli = nvme_cli
        self.logger.info(f"NvmeCommands initialized (device={self.device}, nvme_cli={self.nvme_cli})")


    def run_command(self, cmd):
        if isinstance(cmd, (list, tuple)):
            command = " ".join(cmd)
        else:
            command = str(cmd)
        self.logger.info(f"Executing command: {command}")
        try:
            run_cmd = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return run_cmd.stdout
        except subprocess.CalledProcessError as e:
            self.logger.info(f"Error found during execution")
            self.logger.info(f"Return Code: {e.returncode}")
            self.logger.info(f"STDout: {e.stdout}")
            self.logger.info(f"STDError: {e.stderr}")
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
            options.extend("--azr")
        
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
    def command_list(self, **kwargs):
        cmd = [
            self.nvme_cli,
            "list",
            self.device
        ]
        options = self.parametrizeOpcionsLogs(**kwargs)
        cmd.extend(options)
        
        output = self.run_command(cmd)
        if kwargs.get('json_output', False) and output:
            output = json.loads(output)
        return output
    
    def smart_log(self, **kwargs):
        cmd = [
            self.nvme_cli,
            "smart_log",
            self.device
        ]
        options = self.parametrizeOpcionsLogs(**kwargs)
        cmd.extend(options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            output = json.loads(output)
        return output


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
    def read(self, start_block=None, block_count=None, data_size=None, metadata_size=None, 
             ref_tag=None, data=None, metadata=None, prinfo=None, app_tag_mask=None, 
             app_tag=None, limited_retry=False, force_unit_access=False, dir_type=None, 
             dir_spec=None, dsm=None, show_command=False, dry_run=False, latency=False, 
             storage_tag=None, storage_tag_check=False, force=False, timeout=None, **kwargs):
        """
        Ejecuta comando NVMe read con los parámetros especificados.
        
        Args:
            start_block: Bloque lógico de inicio (SLBA)
            block_count: Número de bloques lógicos (NLB)
            data_size: Tamaño de datos
            metadata_size: Tamaño de metadatos
            ref_tag: Etiqueta de referencia
            data: Archivo de datos
            metadata: Archivo de metadatos
            prinfo: Información de protección
            app_tag_mask: Máscara de etiqueta de aplicación
            app_tag: Etiqueta de aplicación
            limited_retry: Retry limitado
            force_unit_access: Forzar acceso a unidad
            dir_type: Tipo de directiva
            dir_spec: Especificación de directiva
            dsm: Dataset Management
            show_command: Mostrar comando
            dry_run: Ejecución en seco
            latency: Mostrar latencia
            storage_tag: Etiqueta de almacenamiento
            storage_tag_check: Verificación de etiqueta de almacenamiento
            force: Forzar operación
            timeout: Tiempo de espera
            **kwargs: Opciones adicionales (json_output, verbose)
        """
        cmd = [
            self.nvme_cli,
            "read",
            self.device
        ]
        
        # Parámetros básicos
        if start_block is not None:
            cmd.extend(["--start-block", str(start_block)])
            
        if block_count is not None:
            cmd.extend(["--block-count", str(block_count)])
            
        if data_size is not None:
            cmd.extend(["--data-size", str(data_size)])
            
        if metadata_size is not None:
            cmd.extend(["--metadata-size", str(metadata_size)])
            
        if ref_tag is not None:
            cmd.extend(["--ref-tag", str(ref_tag)])
            
        if data is not None:
            cmd.extend(["--data", str(data)])
            
        if metadata is not None:
            cmd.extend(["--metadata", str(metadata)])
            
        if prinfo is not None:
            cmd.extend(["--prinfo", str(prinfo)])
            
        if app_tag_mask is not None:
            cmd.extend(["--app-tag-mask", str(app_tag_mask)])
            
        if app_tag is not None:
            cmd.extend(["--app-tag", str(app_tag)])
            
        # Flags booleanos
        if limited_retry:
            cmd.append("--limited-retry")
            
        if force_unit_access:
            cmd.append("--force-unit-access")
            
        if dir_type is not None:
            cmd.extend(["--dir-type", str(dir_type)])
            
        if dir_spec is not None:
            cmd.extend(["--dir-spec", str(dir_spec)])
            
        if dsm is not None:
            cmd.extend(["--dsm", str(dsm)])
            
        if show_command:
            cmd.append("--show-command")
            
        if dry_run:
            cmd.append("--dry-run")
            
        if latency:
            cmd.append("--latency")
            
        if storage_tag is not None:
            cmd.extend(["--storage-tag", str(storage_tag)])
            
        if storage_tag_check:
            cmd.append("--storage-tag-check")
            
        if force:
            cmd.append("--force")
            
        if timeout is not None:
            cmd.extend(["--timeout", str(timeout)])
        
        # Agregar opciones de logging
        log_options = self.parametrizeOpcionsLogs(**kwargs)
        cmd.extend(log_options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            try:
                output = json.loads(output)
            except json.JSONDecodeError:
                self.logger.warning("Failed to parse JSON output from read command")
                
        return output
        
    def write(self, namespace_id=None, start_block=None, block_count=None, data_size=None, metadata_size=None, 
              ref_tag=None, data=None, metadata=None, prinfo=None, app_tag_mask=None, 
              app_tag=None, limited_retry=False, force_unit_access=False, dir_type=None, 
              dir_spec=None, dsm=None, show_command=False, dry_run=False, latency=False, 
              storage_tag=None, storage_tag_check=False, force=False, timeout=None, **kwargs):
        """
        Ejecuta comando NVMe write con los parámetros especificados.
        
        Args:
            namespace_id: ID del namespace
            start_block: Bloque lógico de inicio (SLBA)
            block_count: Número de bloques lógicos (NLB)
            data_size: Tamaño de datos
            metadata_size: Tamaño de metadatos
            ref_tag: Etiqueta de referencia
            data: Archivo de datos
            metadata: Archivo de metadatos
            prinfo: Información de protección
            app_tag_mask: Máscara de etiqueta de aplicación
            app_tag: Etiqueta de aplicación
            limited_retry: Retry limitado
            force_unit_access: Forzar acceso a unidad
            dir_type: Tipo de directiva
            dir_spec: Especificación de directiva
            dsm: Dataset Management
            show_command: Mostrar comando
            dry_run: Ejecución en seco
            latency: Mostrar latencia
            storage_tag: Etiqueta de almacenamiento
            storage_tag_check: Verificación de etiqueta de almacenamiento
            force: Forzar operación
            timeout: Tiempo de espera
            **kwargs: Opciones adicionales (json_output, verbose)
        """
        cmd = [
            self.nvme_cli,
            "write",
            self.device
        ]
        
        # Namespace ID parameter
        if namespace_id is not None:
            cmd.extend(["--namespace-id", str(namespace_id)])
        
        # Parámetros básicos
        if start_block is not None:
            cmd.extend(["--start-block", str(start_block)])
            
        if block_count is not None:
            cmd.extend(["--block-count", str(block_count)])
            
        if data_size is not None:
            cmd.extend(["--data-size", str(data_size)])
            
        if metadata_size is not None:
            cmd.extend(["--metadata-size", str(metadata_size)])
            
        if ref_tag is not None:
            cmd.extend(["--ref-tag", str(ref_tag)])
            
        if data is not None:
            cmd.extend(["--data", str(data)])
            
        if metadata is not None:
            cmd.extend(["--metadata", str(metadata)])
            
        if prinfo is not None:
            cmd.extend(["--prinfo", str(prinfo)])
            
        if app_tag_mask is not None:
            cmd.extend(["--app-tag-mask", str(app_tag_mask)])
            
        if app_tag is not None:
            cmd.extend(["--app-tag", str(app_tag)])
            
        # Flags booleanos
        if limited_retry:
            cmd.append("--limited-retry")
            
        if force_unit_access:
            cmd.append("--force-unit-access")
            
        if dir_type is not None:
            cmd.extend(["--dir-type", str(dir_type)])
            
        if dir_spec is not None:
            cmd.extend(["--dir-spec", str(dir_spec)])
            
        if dsm is not None:
            cmd.extend(["--dsm", str(dsm)])
            
        if show_command:
            cmd.append("--show-command")
            
        if dry_run:
            cmd.append("--dry-run")
            
        if latency:
            cmd.append("--latency")
            
        if storage_tag is not None:
            cmd.extend(["--storage-tag", str(storage_tag)])
            
        if storage_tag_check:
            cmd.append("--storage-tag-check")
            
        if force:
            cmd.append("--force")
            
        if timeout is not None:
            cmd.extend(["--timeout", str(timeout)])
        
        # Agregar opciones de logging
        log_options = self.parametrizeOpcionsLogs(**kwargs)
        cmd.extend(log_options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            try:
                output = json.loads(output)
            except json.JSONDecodeError:
                self.logger.warning("Failed to parse JSON output from write command")
                
        return output
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

    
    def parametrizeOpcionesConfigGeneral(self, nsid=None, controllers=None, json_output=None, verbose=None ):
        options = []
        
        # Agregar opciones de configuración según los argumentos
        if nsid is not None:
            options.extend(["-n", str(nsid)])  # Use extend instead of append
        if controllers is not None:
            options.extend(["-c", str(controllers)])  # Use extend instead of append
        if json_output:
            options.append("--output-format=json")
        if verbose:
              options.append("-v")
     
        
        return options

    # --- Comandos de configuración ---
    def id_ns(self,**kwargs):
        cmd = [
            self.nvme_cli,
            "id-ns",
            self.device
        ]
        
        # Agregar opciones de configuración usando la función parametrize
        config_options = self.parametrizeOpcionesConfigGeneral(**kwargs)
        cmd.extend(config_options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            output = json.loads(output)
            
        return output
    def set_feature(self,**kwargs ):
        cmd = [
            self.nvme_cli,
            "set-feature",
            self.device
        ]
        
        # Agregar opciones de configuración usando la función parametrize
        config_options = self.parametrizeOpcionesConfigGeneral(**kwargs)
        cmd.extend(config_options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            output = json.loads(output)
            
        return output
    def get_property(self,**kwargs ):
        cmd = [
            self.nvme_cli,
            "get-property",
            self.device
        ]
        
        # Agregar opciones de configuración usando la función parametrize
        config_options = self.parametrizeOpcionesConfigGeneral(**kwargs)
        cmd.extend(config_options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            output = json.loads(output)
            
        return output
    def set_property(self,**kwargs):
        cmd = [
            self.nvme_cli,
            "set-property",
            self.device
        ]
        
        # Agregar opciones de configuración usando la función parametrize
        config_options = self.parametrizeOpcionesConfigGeneral(**kwargs)
        cmd.extend(config_options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            output = json.loads(output)
            
        return output
    def ns_attach(self, **kwargs):
        cmd = [
            self.nvme_cli,
            "attach-ns",
            "/dev/nvme0",  
        ]
        
        # Agregar opciones de configuración usando la función parametrize
        config_options = self.parametrizeOpcionesConfigGeneral(**kwargs)
        cmd.extend(config_options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            output = json.loads(output)
            
        return output

    def ns_detach(self, **kwargs):
        cmd = [
            self.nvme_cli,
            "detach-ns",
            self.device
        ]
        
        # Agregar opciones de configuración usando la función parametrize
        config_options = self.parametrizeOpcionesConfigGeneral(**kwargs)
        cmd.extend(config_options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            output = json.loads(output)
            
        return output
    def create_ns(self, **kwargs):
        cmd = [
            self.nvme_cli,
            "create-ns",
            "/dev/nvme0"
        ]
        
        # Agregar opciones de configuración usando la función parametrize
        config_options = self.parametrizeOpcionsConfig(**kwargs)
        cmd.extend(config_options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            output = json.loads(output)
            
        return output
    
    def delete_ns(self, **kwargs ):
        cmd = [
            self.nvme_cli,
            "delete-ns",
            "/dev/nvme0"
        ]
        
        # Agregar opciones de configuración usando la función parametrize
        config_options = self.parametrizeOpcionesConfigGeneral(**kwargs)
        cmd.extend(config_options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            output = json.loads(output)
            
        return output
    def ns_rescan(self,**kwargs):
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
    
    def format_ns(self, nsid=None, lbaf=None, block_size=None, ses=None, pil=None, 
                  pi=None, ms=None, reset=False, force=False, timeout=None, **kwargs):
        """
        Ejecuta comando NVMe format con los parámetros especificados.
        
        Args:
            nsid: Namespace ID
            lbaf: LBA Format (Logical Block Address Format)
            block_size: Tamaño del bloque
            ses: Secure Erase Settings
            pil: Protection Information Location
            pi: Protection Information
            ms: Metadata Settings
            reset: Reset flag
            force: Force flag
            timeout: Tiempo de espera
            **kwargs: Opciones adicionales (json_output, verbose)
        """
        cmd = [
            self.nvme_cli,
            "format",
            self.device
        ]
        
        # Parámetros básicos
        if nsid is not None:
            cmd.extend(["--namespace-id", str(nsid)])
            
        if lbaf is not None:
            cmd.extend(["--lbaf", str(lbaf)])
            
        if block_size is not None:
            cmd.extend(["--block-size", str(block_size)])
            
        if ses is not None:
            cmd.extend(["--ses", str(ses)])
            
        if pil is not None:
            cmd.extend(["--pil", str(pil)])
            
        if pi is not None:
            cmd.extend(["--pi", str(pi)])
            
        if ms is not None:
            cmd.extend(["--ms", str(ms)])
            
        # Flags booleanos
        if reset:
            cmd.append("--reset")
            
        if force:
            cmd.append("--force")
            
        if timeout is not None:
            cmd.extend(["--timeout", str(timeout)])
        
        # Agregar opciones de logging
        log_options = self.parametrizeOpcionsLogs(**kwargs)
        cmd.extend(log_options)
        
        output = self.run_command(cmd)
        
        if kwargs.get('json_output', False) and output:
            try:
                output = json.loads(output)
            except json.JSONDecodeError:
                self.logger.warning("Failed to parse JSON output from format command")
                
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
