import os
import json
import logging
from datetime import datetime, timedelta
from app.core.logger import LOG_DIRECTORY

# Custom TimedRotatingFileHandler
class CustomTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def doRollover(self):
        """
        Custom rollover method to rename log files in the desired format.
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        
        # Determine the new file name
        current_time = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        new_filename = os.path.join(LOG_DIRECTORY, f"{current_time}.log")
        
        # Check if the new filename already exists
        if os.path.exists(new_filename):
            os.remove(new_filename)
        
        # Rename the current log file
        os.rename(self.baseFilename, new_filename)
        
        # Create a new log file
        self.stream = self._open()
        
        # Update the last rollover time
        self.rolloverAt = self.rolloverAt + self.interval

# Custom JSON formatter
class JsonFormatter(logging.Formatter):
    def format(self, record):
        # Extract default fields
        log_record = {
            "level": record.levelname,
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"),
            "msg": record.getMessage(),
            "name": record.name,
            "module": record.module,
            "funcName": record.funcName,
            "lineno": record.lineno,
        }

        # Add extra fields dynamically, excluding unwanted ones
        extra_fields = {
            key: value
            for key, value in record.__dict__.items()
            if key not in logging.LogRecord(None, None, "", 0, "", (), None).__dict__
        }

        log_record.update(extra_fields)

        return json.dumps(log_record, ensure_ascii=False) #, indent=2)