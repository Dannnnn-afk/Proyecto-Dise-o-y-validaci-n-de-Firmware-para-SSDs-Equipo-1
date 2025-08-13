import sys
import os
import random

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.admin_passthru_wrappper import AdminPassthru, SubmissionQueueEntry, CompletionQueueEntry
from utils.get_smart_log import passthruSmartLog
from src.nvme_wrapper import NvmeCommands
from src.logger import TestLogger

#Instanciar dentro de mi objeto de test clase
smart_Log_InstanceAdminPassthru = passthruSmartLog()



class NvmeSmartLogTemperatureTest():
    """
    This class contains test cases for NVMe commands.
    It is designed to be used with the NVMe wrapper to execute various NVMe commands.
    """
    def __init__(self, nvme_wrapper, logger):
        self.nvme_wrapper = nvme_wrapper
        self.logger = logger   
        

    def run(self):
        self.logger.log_test_start("test_smart_log")
        # Test 2: SMART-LOG
        #     Purpose: Create a dynamic test to validate nvme smart-log command is working as expected.
        #     Execution Steps:
        #     - Take initial snapshot with SMART-LOG command via admin-passthru.
            
        #     nvme admin-passthru /dev/nvme0 --opcode=0x02 --data-len=512 --read --cdw10=0x7f0002 
               
        try:
            
            #     - Verify no media errors exist.
            #     Check bits 175:160 🡪 0xAF : 0xA0
            #     List = [00 00 00 00 00 00]

            List = ["00 00 00 00 00 00"]
            cqe_result = smart_Log_InstanceAdminPassthru.get_smart_log(csi=0, ot=0, uidx=0, nsid=0, lid=2, rae=0, numdl=127, lsp=0, device='/dev/nvme0', lopl=0, lpou=0, lsi=0, numdu=0)
            
            
            self.logger.log_command("smart_Log_InstanceAdminPassthru.get_smart_log(csi=0, ot=0, uidx=0, nsid=0, lid=2, rae=0, " \
                                    "numdl=511, lsp=0, device='/dev/nvme0', lopl=0, lpou=0, lsi=0, numdu=0)", cqe_result)
             #     nvme admin-passthru /dev/nvme0 --opcode=0x0A --cdw10=0x04 --data-len=16 --read
            if cqe_result.data_buffer and len(cqe_result.data_buffer) >= 512:
                self.logger.log_info("get_smart_log executed successfully.")
                 # Critical Warning (byte 0)
                critial_warning = cqe_result.data_buffer[0:1]
                #logger
                #     - Check temperature is within threshold using Get Features FID 0x4.
               
                #     - Change temperature threshold and critical warning using set-feature.
                #Temperature (byte 1-2)
                temp_kelvin = int.from_bytes(cqe_result.data_buffer[1:3], byteorder='little')
                temp_celsius = temp_kelvin - 273.15 > 0 # Convert Kelvin to Celsius
                self.logger.info(f"Temperature in Kelvin: {temp_kelvin}")
                self.logger.info(f"Temperature in Celsius: {temp_celsius}")
                #     - Validate POH (Power On Hours) is less than 1000.
                #     Check bits 143:128 🡪 0x8F : 0x80
                #     Power On Hours (POH) (byte 3-6)
                #     POH = 0x09 0x13 = 2,323
                poh_bytes = cqe_result.data_buffer[128:144]
                poh = int.from_bytes(poh_bytes, byteorder='little')
                #logger
                self.logger.info(f"Time awake: {poh}")
                
                
                #Media ERRORs (byte 160-175, 16 bytes little endian)
                #     MDIE = 0
                media_errors_bytes = cqe_result.data_buffer[160:176]
                media_errors = int.from_bytes(media_errors_bytes, byteorder='little')
                #logger
                self.logger.info(f"Little endian media errors: {media_errors}")
                                
                #     - Verify percentage usage is less than 100%.
                usage_percentage = cqe_result.data_buffer[5]
                self.logger.info(f"Usage percentage: {usage_percentage}")
                if usage_percentage < 100:
                    self.logger.info("Usage percentage is less than 100%. Test passed.")
                else:
                    self.logger.error("Usage percentage 100% or more. Test failed.")
                    self.logger.log_test_end("test_smart_log", "FAIL")
                    return None
                
                #     - Execute nvme read and write commands N times (1 ≤ N ≤ 200).
                N_times = random.randint(1, 200)
                self.logger.info(f"Executing nvme read and write commands {N_times} times.")
                for _ in range(N_times):
                    self.nvme_wrapper.write(start_block=1,block_count=1, data="test_data_smart_log")
                    self.nvme_wrapper.read(start_block=0, block_count=1)
                #- Take final snapshot with SMART-LOG via admin-passthru.
                cqe_result = smart_Log_InstanceAdminPassthru.get_smart_log(csi=0, ot=0, uidx=0, nsid=0, lid=2, rae=0, numdl=511, lsp=0, device='/dev/nvme0', lopl=0, lpou=0, lsi=0, numdu=0)
                self.logger.log_command("smart_Log_InstanceAdminPassthru.get_smart_log(csi=0, ot=0, uidx=0, nsid=0, lid=2, rae=0, " \
                                        "numdl=511, lsp=0, device='/dev/nvme0', lopl=0, lpou=0, lsi=0, numdu=0)", cqe_result)
                if cqe_result.data_buffer and len(cqe_result.data_buffer) >= 512:
                    self.logger.log_info("Final get_smart_log executed successfully.")
                #     - Verify host_read_commands and host_write_commands increased by N.
                host_read_commands = int.from_bytes(cqe_result.data_buffer[8:12], byteorder='little')
                host_write_commands = int.from_bytes(cqe_result.data_buffer[12:16], byteorder='little')
                self.logger.info(f"Host read commands: {host_read_commands}")
                self.logger.info(f"Host write commands: {host_write_commands}")
                #     - Validate critical warning was updated and temperature reset.
                critial_warning_after = cqe_result.data_buffer[0:1]
                temp_kelvin_after = int.from_bytes(cqe_result.data_buffer[1:3],byteorder='little')
                self.logger.info(f"Critical warning after: {critial_warning_after}")
                self.logger.info(f"Temperature in Kelvin after: {temp_kelvin_after}")
                if critial_warning_after == critial_warning and temp_kelvin_after == temp_kelvin:
                    self.logger.info("Critical warning and temperature after match expected values. Test passed.")
                    self.logger.log_test_end("test_smart_log", "PASS")
                else:
                    self.logger.error("Critical warning or temperature after do not match expected values. Test failed.")
                    self.logger.log_test_end("test_smart_log", "FAIL")
                    return None
                #     - Return cqe_result.
                self.logger.info("Test completed successfully.")
                self.logger.log_test_end("test_smart_log", "PASS")
   
                return cqe_result
            else: 
                self.logger.info("get_smart_log returned insufficient data.")
                self.logger.log_test_end("test_smart_log", "ERROR")
                return None
            
        

        #     
        #     Expected Result: Test is PASSED if all fields match expected values; otherwise, FAILED.

        #     
    
        
        
        
        
        
        
        

   





















        except Exception as e:
            self.logger.info(f"Error executing get_smart_log: {e}")
            self.logger.log_test_end("test_smart_log", "ERROR")
            return None
        

        
       
        
        
        
        
     
        
        
        





        

