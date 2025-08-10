from ..src.admin_passthru_wrappper import AdminPassthru, SubmissionQueueEntry, CompletionQueueEntry

### Get Features Consts
OPC_GET_ID_NS = 0x06

#Data Pointer
#pendiente

'''Figure 308: Identify – Command Dword 10'''
RSVD_BIT_DW10 = 16
RSVD_MASK_DW10 = 0xff << RSVD_BIT_DW10

CNTID_BIT = 16
CNTID_MASK = 0xffff << CNTID_BIT

CNS_BIT = 0
CNS_MASK = 0xff << CNS_BIT

'''Figure 309: Identify – Command Dword 11'''
RSVD_BIT_DW11 = 16
RSVD_MASK_DW11 = 0xff << RSVD_BIT_DW11

CSI_BIT = 24
CSI_MASK = 0xff << CSI_BIT

CNSSID_BIT = 0
CNSSID_MASK = 0xffff << CNSSID_BIT

'''Figure 309: Identify – Command Dword 14'''
RSVD_BIT_DW14 = 7
RSVD_MASK_DW14 = 0xffffff << RSVD_BIT_DW14

UIDX_BIT = 0
UIDX_MASK = 0x7f << UIDX_BIT


class passthruSmartLog(AdminPassthru):
   def get_ID_NS(self, cns=0, cntid=0, cnssid=0, uidx=0, nsid=0, device='/dev/nvme0', csi=0):
        sqe = SubmissionQueueEntry()
        sqe.NSID = nsid
        sqe.OPC = OPC_GET_ID_NS
        
        
        sqe.DW10 = (cntid << CNTID_BIT) & CNTID_MASK
        sqe.DW10 |= (cns << CNS_BIT) & CNS_MASK
        
        sqe.DW11 = (csi << CSI_BIT) & CSI_MASK
        sqe.DW11 |= (cnssid << CNSSID_BIT) & CNSSID_MASK
        
        sqe.DW14 = (uidx << UIDX_BIT) & UIDX_MASK
       
        try:
            output, err, return_code, status_dwords = self.admin_passthru(opcode=sqe.OPC,
                                                                          namespace_id=sqe.NSID,
                                                                          cdw10=sqe.DW10,
                                                                          cdw11=sqe.DW11,
                                                                          cdw12=sqe.DW12,
                                                                          cdw13=sqe.DW13,
                                                                          cdw14=sqe.DW14,
                                                                          cdw15=sqe.DW15,
                                                                          use_controller_path=True,
                                                                          latency=True,
                                                                          raw_binary=True,
                                                                          read=True,
                                                                          data_len=None,
                                                                          device_path=device)
        except:
        
        
        
        
        
        
        
            return None

        cqe = CompletionQueueEntry()
        cqe.populate_cqe(status_dwords, output)
        return cqe