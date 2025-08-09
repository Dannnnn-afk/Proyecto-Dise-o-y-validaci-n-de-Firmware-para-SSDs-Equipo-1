from ..src.admin_passthru_wrappper import AdminPassthru, SubmissionQueueEntry, CompletionQueueEntry

### Get Features Consts
OPC_GET_FEATURES = 0x0A
'''Section 5.15, Figure 191: Get Features - Data Pointer'''
DPTR_BIT = 0
DPTR_MASK = 0xffff_ffff_ffff_ffff_ffff_ffff_ffff_ffff << DPTR_BIT

'''Section 5.15, Figure 192: Get Features - Command Dword 10'''
RSVD_BIT_DW10 = 11
RSVD_MASK_DW10 = 0x1fffff << RSVD_BIT_DW10
SEL_BIT = 8
SEL_MASK = 0x7 << SEL_BIT
#Opcional no hace el corrimiento
FID_BIT = 0
FID_MASK = 0xff << FID_BIT

'''Section 5.15, Figure 193: Get Features - Command Dword 14'''
RSVD_BIT_DW14 = 7
RSVD_MASK_DW14 = 0x1ffffff << RSVD_BIT_DW14

UUIDI_BIT = 0
UUIDI_MASK = 0x7f << UUIDI_BIT



class GetFeatures(AdminPassthru):
    def get_features(self, nsid=0, fid=0, sel=0, uuid=0, dw11=0, device='/dev/nvme0'):
        sqe = SubmissionQueueEntry()
        sqe.NSID = nsid
        sqe.OPC = OPC_GET_FEATURES

        sqe.DW10 = (fid << FID_BIT) & FID_MASK
        sqe.DW10 |= (sel << SEL_BIT) & SEL_MASK
        
        
        
        sqe.DW11 = dw11
        sqe.DW14 = (uuid << UUIDI_BIT) & UUIDI_MASK

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
