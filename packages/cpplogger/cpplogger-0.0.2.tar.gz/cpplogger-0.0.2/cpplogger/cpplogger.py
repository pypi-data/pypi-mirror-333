import datetime
import os

class myCustomLogger:
    
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.log_folder = "Logs"  # Folder where log files will be stored
        self.create_log_folder()

        # Create log file path
        self.log_file = os.path.join(self.log_folder, f"{self.name}_log.txt")
        
    def create_log_folder(self):
        """Create the Logs folder if it doesn't exist."""
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)
    
    def debug(self, message):
        self.log('DEBUG', message)
        
    def info(self, message):
        self.log('INFO', message)
        
    def warning(self, message):
        self.log('WARNING', message)
        
    def error(self, message):
        self.log('ERROR', message)
        
    def critical(self, message):
        self.log('CRITICAL', message)
        
    def log(self, level, message):
        """Log the message to both the console and the log file."""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f'{timestamp} [{self.name}] {level}: {message}'
        
        # Print log message to console
        print(log_message)
        
        # Append log message to the log file
        with open(self.log_file, 'a') as f:
            f.write(log_message + "\n")

