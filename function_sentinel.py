import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

# Set up logging
logging.basicConfig(
    filename=r'C:\gamsync\automate\servicemanagement_*\sentinelaudit.log',  # Log file name
    level=logging.INFO,         # Log level
    format='%(asctime)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date format
)

class FileModificationHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        # Log the file modification
        logging.info(f'Modified file: {event.src_path}')

    def on_created(self, event):
        if event.is_directory:
            return
        # Log the file creation
        logging.info(f'Created file: {event.src_path}')

    def on_deleted(self, event):
        if event.is_directory:
            return
        # Log the file deletion
        logging.info(f'Deleted file: {event.src_path}')

    def on_moved(self, event):
        if event.is_directory:
            return
        # Log the file moved/renamed
        logging.info(f'Moved file: {event.src_path} to {event.dest_path}')

if __name__ == "__main__":
    # Define the path to watch
    path_to_watch = r"C:\gamsync\automate\servicemanagement_*\share"  # Change to the directory you want to monitor

    # Create the event handler
    event_handler = FileModificationHandler()
    
    # Create the observer
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)

    # Start the observer
    observer.start()
    print(f"Monitoring started on {path_to_watch}. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
