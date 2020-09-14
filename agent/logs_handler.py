# Constants
## Error Codes
FAULT_SUCCESSFUL = 100
FAILED_ACCESSING_CONF_FILE = 101
PROBES_BEFORE_METHODS_FAILED = 102
PROBES_AFTER_ROLLBACKS_FAILED = 106


class FaultSuccessful(Exception):
    def __init__(self):
        self.message = "Exit Code: 100\n" \
                       "Fault successfully finished."
        super().__init__(self.message)

class FailedAccessingConfFile(Exception):
    def __init__(self):
        self.message = "Exit Code: 101\n" \
                       "Failed accessing the conf file in the current directory."
        super().__init__(self.message)

class ProbesBeforeMethodsFailed(Exception):
    def __init__(self):
        self.message = "Exit Code: 102\n" \
                       "Probes before the methods stage have failed."
        super().__init__(self.message)

class ProbesAfterRollbacksFailed(Exception):
    def __init__(self):
        self.message = "Exit Code: 106\n" \
                       "Probes after the rollbacks stage have failed."
        super().__init__(self.message)


def send_log(error_code):
    log = {}
    log['general'] = []
    log['general'].append({
        'error_code': error_code
    })