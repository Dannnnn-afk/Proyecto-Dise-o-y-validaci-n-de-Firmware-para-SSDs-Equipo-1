
import sys
import os
# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.admin_passthru_wrappper import AdminPassthru, SubmissionQueueEntry, CompletionQueueEntry
from utils.get_ID_NS import passthruID_NS
from src.nvme_wrapper import NvmeCommands
from src.logger import TestLogger

#Instanciar dentro de mi objeto de test clase
passthruIDInstance = passthruID_NS()

          

class TestSmartLogHealt():
   

    def __init__(self, nvme_wrapper, logger):
        self.nvme_wrapper = nvme_wrapper
        self.logger = logger  
        

    def run(self, command, *args):
        # Test 3: ID-NS
        # Purpose: Create a dynamic test to validate nvme id-ns command is working as expected.
        # Execution Steps:
        

        # - Take initial snapshot with ID-NS command via admin-passthru.
        cqe_result = passthruIDInstance.get_ID_NS(cns=0, cntid=0, cnssid=0, uidx=0, nsid=0, device='/dev/nvme0', csi=0)
        
        
        self.logger.log_command("passthruIDInstance.get_id_ns(csi=0, ot=0, uidx=0, nsid=1, rae=0, numdl=4095, lsp=0, device='/dev/nvme0', lopl=0, lpou=0, lsi=0, numdu=0)", cqe_result)
        if cqe_result.data_buffer and len(cqe_result.data_buffer) >= 4096:
            self.logger.log_info("get_id_ns executed successfully.")
            # - Verify block size, nuse, nsize, ncap, flbas, lbaf, dps match expected values.
            block_size = int.from_bytes(cqe_result.data_buffer[0:4], byteorder='little')
            nuse = int.from_bytes(cqe_result.data_buffer[4:8], byteorder='little')
            nsize = int.from_bytes(cqe_result.data_buffer[8:12], byteorder='little')
            ncap = int.from_bytes(cqe_result.data_buffer[12:16], byteorder='little')
            flbas = cqe_result.data_buffer[16]
            lbaf = cqe_result.data_buffer[17]
            dps = cqe_result.data_buffer[18]
            
            self.logger.info(f"Block size: {block_size}")
            self.logger.info(f"Nuse: {nuse}")
            self.logger.info(f"Nsize: {nsize}")
            self.logger.info(f"Ncap: {ncap}")
            self.logger.info(f"Flbas: {flbas}")
            self.logger.info(f"Lbaf: {lbaf}")
            self.logger.info(f"Dps: {dps}")
            
            
        

        # nvme admin-passthru /dev/nvme0 --opcode=0x6 --namespace-id=1 --data-len=4096 –read
        

        # - Delete all namespaces. --namespace-id=0xFFFFFFFF
        self.nvme_wrapper.delete_ns(nsid=0xFFFFFFFF)
        

        # - Create and attach a new namespace.
        self.nvme_wrapper.create_ns()
        self.nvme_wrapper.ns_attach()
        # - Format the block size of the drive
        self.nvme_wrapper.format_ns(nsid=1, block_size=4096)
        
        

        # -  execute nvme write.
        self.nvme_wrapper.write(start_block=1,block_count=1, data="test_data_smart_log_healt")

        # - Take final snapshot with ID-NS via admin-passthru.
        cqe_result_after = passthruID_NS.get_ID_NS(cns=0, cntid=0, cnssid=0, uidx=0, nsid=0, device='/dev/nvme0', csi=0)
        self.logger.log_command("smart_Log_InstanceAdminPassthru.get_smart_log(csi=0, ot=0, uidx=0, nsid=0, lid=2, rae=0, " \
                                        "numdl=511, lsp=0, device='/dev/nvme0', lopl=0, lpou=0, lsi=0, numdu=0)", cqe_result)

        # - Verify block size, nuse, nsize, ncap, flbas, lbaf, dps match expected values.
        if cqe_result_after.data_buffer and len(cqe_result_after.data_buffer) >= 4096:
            self.logger.log_info("get_id_ns executed successfully.")
    
            # - Verify block size, nuse, nsize, ncap, flbas, lbaf, dps match expected values.
            block_size_after = int.from_bytes(cqe_result_after.data_buffer[0:4], byteorder='little')
            nuse_after = int.from_bytes(cqe_result_after.data_buffer[4:8], byteorder='little')
            nsize_after = int.from_bytes(cqe_result_after.data_buffer[8:12], byteorder='little')
            ncap_after = int.from_bytes(cqe_result_after.data_buffer[12:16], byteorder='little')
            flbas_after = cqe_result_after.data_buffer[16]
            lbaf_after = cqe_result_after.data_buffer[17]
            dps_after = cqe_result_after.data_buffer[18]
            
            self.logger.info(f"Block size: {block_size}")
            self.logger.info(f"Nuse: {nuse}")
            self.logger.info(f"Nsize: {nsize}")
            self.logger.info(f"Ncap: {ncap}")
            self.logger.info(f"Flbas: {flbas}")
            self.logger.info(f"Lbaf: {lbaf}")
            self.logger.info(f"Dps: {dps}")
            # Verify all this information have changed:
            # o Block size must match with the one assigned during format.
            # o nuse attribute has increased based on the amount of writes executed.
            # o nsize and ncap should match with the ones defined when namespace was created. 
            # o flbas, lbaf, dps, must match with the one defined in format command.
            # After you evaluate all the fields required if all field match mark Test as PASSED, in
            # case of any error mark test as FAILED.
            
            if (block_size == 4096 and nuse_after > nuse and nsize_after == nsize and ncap_after == ncap and
                flbas_after == flbas and lbaf_after == lbaf and dps_after == dps):
                self.logger.info("All fields match expected values. Test passed.")
                self.logger.log_test_end("test_smart_log_healt", "PASS")
            else:
                self.logger.info("All fields did not match the expected values.")
                self.logger.log_test_end("test_smart_log_healt", "ERROR")

        # Expected Result: Test is PASSED if all fields match expected values; otherwise, FAILED.
        # Command Line: nvme id-ns /dev/nvme0n1

      