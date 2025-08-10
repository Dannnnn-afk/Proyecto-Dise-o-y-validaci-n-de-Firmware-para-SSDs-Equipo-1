class TestCases():
    """
    This class contains test cases for NVMe commands.
    It is designed to be used with the NVMe wrapper to execute various NVMe commands.
    """

    def __init__(self, nvme_wrapper):
        self.nvme_wrapper = nvme_wrapper

    def run_test_case(self, command, *args):
        """
        Run a specific NVMe command test case.
        
        :param command: The NVMe command to execute.
        :param args: Additional arguments for the command.
        :return: Result of the command execution.
        """
        return self.nvme_wrapper.execute_command(command, *args)