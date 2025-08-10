#!/usr/bin/env python3
import os
import json
import subprocess
import sys
from ..src.nvme_wrapper import NvmeCommands
from jsondiff import diff
from ..src.logger import TestLogger
from ..src.test_manager import TestManager

myIDControlTest = TestManager("PHA42142004Y1P2A", "test_id_control")

IGNORE_FIELDS = {"sn", "fguid", "unvmcap", "subnqn"}

class idControlTest:
    def __init__(self, serial_number, testname):
        self.serial_number = serial_number
        self.testname = testname
        self.nvme = None
        self.physical_path = None
        self.logger = TestLogger(self.testname).initialize_logger()
        self.test = None

        if self.initialize() is None:
            self.logger.error(f"Unable to get Physical Path for SN: {self.serial_number}")
            return

        if testname not in tests_pool:
            test_list = list(tests_pool.keys())
            self.logger.error(f"Test {testname} was not found. Tests Available: {test_list}")
            self.logger.error(f"Make sure the test you are trying to execute has been defined.")
            return
        self.test = tests_pool[self.testname](self.logger, self.nvme)
