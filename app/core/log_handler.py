import os
import json
import logging
from contextvars import ContextVar
from datetime import datetime, timedelta

# Ensure logs directory exists
LOG_DIRECTORY = "logs"
os.makedirs(LOG_DIRECTORY, exist_ok=True)


# --- ContextVar setup for dynamic log context ---
_log_context: ContextVar[dict] = ContextVar("_log_context", default={})

def set_log_context(**kwargs):
    _log_context.set(kwargs)

def get_log_context():
    return _log_context.get()

class ContextLogFilter(logging.Filter):
    def filter(self, record):
        context = get_log_context()
        for key, value in context.items():
            setattr(record, key, value)
        return True
    

# --- Custom file handler with midnight rotation ---
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


# --- JSON formatter that includes dynamic context ---
class JsonFormatter(logging.Formatter):
    def format(self, record):
        # Extract default fields
        log_record = {
            "level": record.levelname,
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%SZ"),
            "msg": record.getMessage(),
            # "name": record.name,
            "module": record.module,
            # "funcName": record.funcName,
            # "lineno": record.lineno,
        }

        # --- Add context from ContextVar ---
        context = get_log_context()
        for key, value in context.items():
            # Convert non-serializable types like UUID to string
            log_record[key] = str(value) if not isinstance(value, (str, int, float, bool, type(None))) else value

        # Add extra fields dynamically, excluding unwanted ones
        standard_attrs = logging.LogRecord(None, None, "", 0, "", (), None).__dict__
        extra_fields = {
            key: value
            for key, value in record.__dict__.items()
            if key not in standard_attrs
        }

        log_record.update(extra_fields)

        return json.dumps(log_record, ensure_ascii=False)#, indent=2)