# app/main.py
import logging
import time
import threading
from watchdog.observers import Observer
from .file_handler import FileHandler
from .file_processor import process_queue, sync_existing_files
from .config import DIRECTORY_PATH
from .logger import setup_logging


def main():
    setup_logging()
    logging.info("Script started")
    sync_existing_files(DIRECTORY_PATH)

    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, DIRECTORY_PATH, recursive=False)
    observer.start()

    threading.Thread(target=process_queue, daemon=True).start()

    try:
        while True:
            logging.debug("Monitoring directory...")
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Stopping directory monitoring")
        observer.stop()

    observer.join()
    logging.info("Directory monitoring stopped")


if __name__ == "__main__":
    main()
