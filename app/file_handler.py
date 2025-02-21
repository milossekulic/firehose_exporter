# app/file_handler.py
import logging
import os
from watchdog.events import FileSystemEventHandler
from .file_processor import file_queue, save_positions, processed_files


class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"New file created: {event.src_path}")
            file_queue.put((os.path.getctime(event.src_path), event.src_path))

    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"File modified: {event.src_path}")
            file_queue.put((os.path.getmtime(event.src_path), event.src_path))

    def on_deleted(self, event):
        if not event.is_directory:
            logging.info(f"File deleted: {event.src_path}")
            if event.src_path in processed_files:
                del processed_files[event.src_path]
                save_positions(processed_files)

    def on_moved(self, event):
        if not event.is_directory:
            logging.info(f"File moved: from {event.src_path} to {event.dest_path}")
            if event.src_path in processed_files:
                processed_files[event.dest_path] = processed_files.pop(event.src_path)
                save_positions(processed_files)
            file_queue.put((os.path.getctime(event.dest_path), event.dest_path))
