import os
from datetime import datetime
from app.utils.logger import LOG_DIRECTORY
from logging.handlers import TimedRotatingFileHandler

# Custom TimedRotatingFileHandler
class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def doRollover(self):
        """
        Custom rollover method to rename log files in the desired format.
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        
        # Determine the new file name
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        new_filename = os.path.join(LOG_DIRECTORY, f"{current_time}.log")
        
        # Rename the current log file
        os.rename(self.baseFilename, new_filename)
        
        # Create a new log file
        self.stream = self._open()