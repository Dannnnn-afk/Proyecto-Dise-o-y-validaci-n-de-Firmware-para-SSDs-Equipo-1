


class ErrorReport():
    """
    Class to handle error reporting in NVMe tests.
    """

    def __init__(self, logger):
        self.logger = logger

    def report_error(self, error_message):
        """
        Report an error message to the logger.
        
        :param error_message: The error message to log.
        """
        self.logger.error(error_message)