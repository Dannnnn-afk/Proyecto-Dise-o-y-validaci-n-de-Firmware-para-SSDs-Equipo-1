import re
import sys
from subprocess import Popen, PIPE
import subprocess

CONST_TIMEOUT_LIMIT = 120  # 2 mins
SECONDS_TO_MILISECONS = 1000  # second to miliseconds
CONST_NVME = "nvme"
ADMIN_CMD = 'admin-passthru'

# NVMe Command
DW0 = "DW0"
DW1 = "DW1"
DW2 = "DW2"
DW3 = "DW3"
DW4 = "DW4"
DW5 = "DW5"
DW6 = "DW6"
DW7 = "DW7"
DW8 = "DW8"
DW9 = "DW9"
DW10 = "DW10"
DW11 = "DW11"
DW12 = "DW12"
DW13 = "DW13"
DW14 = "DW14"
DW15 = "DW15"
CID = "CID"
PSDT = "PSDT"
FUSE = "FUSE"
OPC = "OPC"
NSID = "NSID"
PRP1A = "PRP1A"
PRP1B = "PRP1B"
PRP2A = "PRP2A"
PRP2B = "PRP2B"
MPTRA = "MPTRA"
MPTRB = "MPTRB"

# NVMe completion error
SQHP_BIT = 0
SQHP_MASK = 0xFFFF
SQID_BIT = 16
SQID_MASK = 0xFFFF
DNR_BIT = 31
DNR_MASK = 0x1
M_BIT = 30
M_MASK = 0x01
CRD_BIT = 28
CRD_MASK = 0x3
SCT_BIT = 25
SCT_MASK = 0x7
SC_BIT = 17
SC_MASK = 0xFF
PBIT_BIT = 16
PBIT_MASK = 0x1
COMP_CID_BIT = 0
COMP_CID_MASK = 0xFFFF

# Constants related to hosting path error
SC_HOST_PATH_START = 0X70
SC_HOST_PATH_END = 0X7F
HOST_PATHING_ERROR = 8

# definition of Status Code Type for NVMe Status
GENERIC_COMMAND_STATUS = 0
COMMAND_SPECIFIC_STATUS = 1
MEDIA_AND_DATA_INTEGRITY_ERROR = 2
PATH_RELATED_STATUS = 3
VENDOR_SPECIFIC_STATUS = 7


class SubmissionQueueEntry(object):
    def __init__(self):
        self.DW0 = None
        self.DW1 = None
        self.DW2 = None
        self.DW3 = None
        self.DW4 = None
        self.DW5 = None
        self.DW6 = None
        self.DW7 = None
        self.DW8 = None
        self.DW9 = None
        self.DW10 = None
        self.DW11 = None
        self.DW12 = None
        self.DW13 = None
        self.DW14 = None
        self.DW15 = None
        self.CID = None
        self.PSDT = None
        self.FUSE = None
        self.OPC = None
        self.NSID = None
        self.PRP1A = None
        self.PRP1B = None
        self.PRP2A = None
        self.PRP2B = None
        self.MPTRA = None
        self.MPTRB = None
        self.data_buffer = bytearray(0)


class CompletionQueueEntry(object):
    def __init__(self):
        self.dw0 = 0
        self.dw1 = 0
        self.dw2 = 0
        self.dw3 = 0
        self.cmdspec = 0
        self.reserved1 = 0
        self.sqid = 0
        self.sqhp = 0
        self.dnr = 0
        self.more = 0
        self.crd = 0
        self.status_code_type = 0
        self.status_code = 0
        self.phase_tag = 0
        self.cid = 0
        self.elapsed_time = 0
        self.latency = 0
        self.data_buffer = bytearray(0)

    def populate_cqe(self, status, data_buffer):
        self.dw0 = status[DW0]
        self.dw1 = status[DW1]
        self.dw2 = status[DW2]
        self.dw3 = status[DW3]
        self.cmdspec = self.dw0
        self.reserved1 = self.dw1
        self.sqhp = (self.dw2 >> SQHP_BIT) & SQHP_MASK
        self.sqid = (self.dw2 >> SQID_BIT) & SQID_MASK
        self.dnr = (self.dw3 >> DNR_BIT) & DNR_MASK
        self.more = (self.dw3 >> M_BIT) & M_MASK
        self.crd = (self.dw3 >> CRD_BIT) & CRD_MASK
        self.status_code_type = (self.dw3 >> SCT_BIT) & SCT_MASK
        self.status_code = (self.dw3 >> SC_BIT) & SC_MASK
        self.phase_tag = (self.dw3 >> PBIT_BIT) & PBIT_MASK
        self.cid = (self.dw3 >> COMP_CID_BIT) & COMP_CID_MASK

        self.latency, self.data_buffer = self.extract_latency_from_buffer(data_buffer)

        # data_buffer and metadata_buffer must be passed into SsdAbstractionReturn as a bytearray or None
        if self.data_buffer is not None:
            if isinstance(self.data_buffer, bytes):
                # Direct conversion from bytes to bytearray (best case)
                self.data_buffer = bytearray(self.data_buffer)
            elif isinstance(self.data_buffer, int):
                # Convert int to string, then to bytearray
                self.data_buffer = bytearray(str(self.data_buffer), encoding='utf-8')
            elif isinstance(self.data_buffer, str):
                # Check if string consists of hex values
                is_hex = re.fullmatch(r"^([0-9a-fA-F]{2})*$", self.data_buffer) is not None
                if is_hex:
                    self.data_buffer = bytearray.fromhex(self.data_buffer)
                else:
                    # For string data, use latin-1 encoding to preserve byte values 0-255
                    # This is safer than utf-8 for binary data that was decoded incorrectly
                    try:
                        self.data_buffer = bytearray(self.data_buffer, encoding='latin-1')
                    except UnicodeEncodeError:
                        # Fallback to utf-8 with error replacement
                        self.data_buffer = bytearray(self.data_buffer, encoding='utf-8', errors='replace')
            elif not isinstance(self.data_buffer, bytearray):
                self.data_buffer = bytearray(self.data_buffer)

    def extract_latency_from_buffer(self, output):
        latency = None
        data_buffer = output
        #MANEJO DE ERS
        # Handle binary data properly for raw_binary commands
        if isinstance(data_buffer, bytes):
            # Try to decode only if we expect text output (latency measurement)
            try:
                data_string = output.decode(encoding='utf-8', errors="strict")
                # Look for latency info in the text
                match = re.match(r".*latency: (\d+) us\n", data_string)
                if match is not None:
                    latency = int(match.group(1))  # latency in microsecs
                    latency = latency / 1000  # latency in millisecs and is a float value
                    data_startpos = match.regs[0][1]  # points to the end of match + 1 position
                    data_buffer = None
                    if len(output) > data_startpos:
                        data_buffer = output[data_startpos:]
                else:
                    # No latency info found, keep original binary data
                    data_buffer = output
            except UnicodeDecodeError:
                # This is binary data, keep it as-is
                data_buffer = output
                
        elif isinstance(data_buffer, str):
            # Already string, check for latency
            match = re.match(r".*latency: (\d+) us\n", data_buffer)
            if match is not None:
                latency = int(match.group(1))  # latency in microsecs
                latency = latency / 1000  # latency in millisecs and is a float value
                data_startpos = match.regs[0][1]  # points to the end of match + 1 position
                data_buffer = None
                if len(output) > data_startpos:
                    data_buffer = output[data_startpos:]
                    
        return latency, data_buffer


class AdminPassthru():

    def obtain_status_code(self, stdout_txt, stderr):
        status = {}

        dword0 = 0
        dword1 = 0
        dword2 = 0
        dword3 = 0

        if stdout_txt != "":
            try:
                dword0 = re.findall(r"value:([0x]*[0-9A-Fa-f]+)", stdout_txt)[-1]
                dword0 = int(dword0, 16)
            except:
                pass

        if stderr != "":
            # NVMe-CLI is printing response to stderr
            # see: https://github.com/linux-nvme/nvme-cli/blob/master/nvme.c#L5674
            success_pattern = r"^.*Success and result: 0x(?P<result>[0-9A-Fa-f]+)$"
            re_search = re.match(success_pattern, stderr)
            if re_search is not None:
                result = re_search.group("result")
                dword0 = int(result, 16)

            try:
                dword3 = re.findall(r"\(([0x]*[0-9A-Fa-f]+)\)", stderr)[-1]
                dword3 = int(dword3, 16) << 17
            except:
                pass

        status[DW0] = dword0
        status[DW1] = dword1
        status[DW2] = dword2
        status[DW3] = dword3

        return status

    def run_cmd(self, cmd):
        try:
            run_cmd = subprocess.run(cmd, capture_output=True, text=False, check=True)
            # return run_cmd.stdout
            # stdout_byte.decode(encoding=sys.stdout.encoding, errors="replace")
            returncode = run_cmd.returncode
            stdout_txt = run_cmd.stdout.decode(encoding=sys.stdout.encoding, errors="replace")
            stderr_txt = run_cmd.stderr.decode(encoding=sys.stdout.encoding, errors="replace")
            status_dwords = self.obtain_status_code(stdout_txt, stderr_txt)
            return stdout_txt, stderr_txt, returncode, status_dwords
        except subprocess.CalledProcessError as e:
            print(f"Error ejecutando el comando: {e}")
            return None

    def admin_passthru(self, opcode, flags=None, reserved=None, namespace_id=None, cdw2=None, cdw3=None, cdw10=None,
                       cdw11=None, cdw12=None, cdw13=None, cdw14=None, cdw15=None, data_len=None, metadata_len=None,
                       input_file=None, read=None, show_command=None, dry_run=None, raw_binary=None,
                       prefill=None, write=None, latency=None, use_controller_path=False, device_path=None,
                       stdin_data=None):

        timeout = CONST_TIMEOUT_LIMIT * SECONDS_TO_MILISECONS  # Converting to miliseconds

        params = {
            '-O': opcode,
            '-f': flags,
            '-R': reserved,
            '-n': namespace_id,
            '--cdw2': cdw2,
            '--cdw3': cdw3,
            '--cdw10': cdw10,
            '--cdw11': cdw11,
            '--cdw12': cdw12,
            '--cdw13': cdw13,
            '--cdw14': cdw14,
            '--cdw15': cdw15,
            '-r': read,
            '-w': write,
            '-i': input_file,
            '-l': data_len,
            '-m': metadata_len,
            '-s': show_command,
            '-d': dry_run,
            '-b': raw_binary,
            '-p': prefill,
            '-t': timeout,
            '-T': latency
        }

        command = [ CONST_NVME, ADMIN_CMD, device_path ]

        for param in params:
            if params[param] is None:
                continue
            command.append(param)
            command.append(str(params[param]))


        output, err, returncode, status_dwords = self.run_cmd(command)

        if returncode:
            match = re.match(r'NVMe command result:(\d+)', err)
            if not match:
                print(f"An error has occurred while running: {command}")
                print(f"Error: {err}")
                print(f"Output: {output}")
        return output, err, returncode, status_dwords
