from ..src.admin_passthru_wrappper import AdminPassthru, SubmissionQueueEntry, CompletionQueueEntry

### Get Features Consts
OPC_get_SMART_LOG = 0x02

#Data Pointer
#pendiente

'''Figure 198: Get Log Page – Command Dword 10'''
NUMDL_BIT = 16
NUMDL_MASK = 0xffff << NUMDL_BIT

RAE_BIT = 15
RAE_MASK = 1 << RAE_BIT

LSP_BIT = 8
LSP_MASK = 0x7f << LSP_BIT

LID_BIT = 0
LID_MASK = 0xff << LID_BIT

'''Figure 199: Get Log Page – Command Dword 11'''
LSI_BIT = 16
LSI_MASK = 0xffff << LSI_BIT

NUMDU_BIT = 0
NUMDU_MASK = 0xffff << NUMDU_BIT


'''Figure 199: Get Log Page – Command Dword 12'''
#Pasa directo, ya que es solo un campo y no hay que operar para concatenar 

'''Figure 199: Get Log Page – Command Dword 13'''
#Pasa directo, ya que es solo un campo y no hay que operar para concatenar 

'''Figure 199: Get Log Page – Command Dword 14'''
#Pasa directo, ya que es solo un campo y no hay que operar para concatenar 

RSVD_BIT_DW14 = 7
RSVD_MASK_DW14 = 0xffff << RSVD_BIT_DW14

CSI_BIT= 24
CSI_MASK = 0xff << CSI_BIT

OT_BIT = 23
OT_MASK = 1 << OT_BIT


UIDX_BIT = 0
UIDX_MASK = 0x7f << UIDX_BIT

class passthruSmartLog(AdminPassthru):
   def get_smart_log(self, csi=0, ot=0, uidx=0, nsid=0, lid=0, rae=0, numdl=0, lsp=0, device='/dev/nvme0', lopl=0, lpou=0, lsi=0, numdu=0):
        sqe = SubmissionQueueEntry()
        sqe.NSID = nsid
        sqe.OPC = OPC_get_SMART_LOG
        
        sqe.DW10 = (numdl << NUMDL_BIT) & NUMDL_MASK
        sqe.DW10 |= (rae << RAE_BIT) & RAE_MASK
        sqe.DW10 |= (lsp << LSP_BIT) & LSP_MASK
        sqe.DW10 |= (lid << LID_BIT) & LID_MASK
        sqe.DW11 = (lsi << LSI_BIT) & LSI_MASK
        sqe.DW11 |= (numdu << NUMDU_BIT) & NUMDU_MASK
        sqe.DW12 = lopl
        sqe.DW13 = lpou
        sqe.DW14 = (CSI_BIT << CSI_MASK) & CSI_MASK
        sqe.DW14 |= (OT_BIT << OT_MASK) & OT_MASK
        
        #tengo duda aca el RSVD si tiene orden no?
        #pq no se opera namas se reserva
        sqe.DW14 |= (csi << CSI_BIT) & CSI_MASK
        sqe.DW14 |= (ot << OT_BIT) & OT_MASK
        sqe.DW14 |= (uidx << UIDX_BIT) & UIDX_MASK
        
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
                                                                          data_len=4,
                                                                          device_path=device)
        except:
            return None
        
        cqe = CompletionQueueEntry()
        cqe.populate_cqe(status_dwords, output)
        return cqe