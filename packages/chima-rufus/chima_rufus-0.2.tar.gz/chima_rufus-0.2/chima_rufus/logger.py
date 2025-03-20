import logging

# Setting up the logger
logging.basicConfig(level=logging.INFO)

# Logs only the WARNINGS
logging.getLogger("WDM").setLevel(logging.WARNING)

class Logger:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def _log_error(self, message, e=None, bypass=False):
        if self.verbose or bypass:
            if e != None:
                logging.error(f"{message}, {e}")
            else:
                logging.error(message)
    
    def _log_info(self, message):
        if self.verbose:
            logging.info(message)


