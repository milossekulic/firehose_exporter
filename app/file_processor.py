# app/file_processor.py
import os
import time
import json
import logging
import threading
from queue import PriorityQueue
from botocore.exceptions import (
    NoCredentialsError,
    PartialCredentialsError,
    EndpointConnectionError,
    ClientError,
    BotoCoreError,
)
from .aws_client import firehose_client
from .config import DELIVERY_STREAM_NAME, POSITION_FILE, MAX_RETRIES, RETRY_DELAY

file_queue = PriorityQueue()
processing_lock = threading.Lock()


def load_positions():
    if os.path.exists(POSITION_FILE):
        with open(POSITION_FILE, "r") as f:
            return json.load(f)
    return {}


def save_positions(positions):
    temp_file = POSITION_FILE + ".tmp"
    with open(temp_file, "w") as f:
        json.dump(positions, f)
    os.replace(temp_file, POSITION_FILE)


processed_files = load_positions()


def send_data_to_firehose(record):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            firehose_client.put_record(
                DeliveryStreamName=DELIVERY_STREAM_NAME, Record={"Data": record}
            )
            logging.info(f"Record pushed to Firehose: {record.strip()}")
            return True
        except (
            NoCredentialsError,
            PartialCredentialsError,
            EndpointConnectionError,
        ) as e:
            retries += 1
            logging.error(
                f"Error sending data to Firehose: {e}. Retrying {retries}/{MAX_RETRIES}..."
            )
            time.sleep(RETRY_DELAY)
        except ClientError as e:
            logging.error(f"ClientError: {e}")
            return False
        except BotoCoreError as e:
            logging.error(f"BotoCoreError: {e}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return False
    return False


def process_new_data(file_path):
    logging.info(f"Processing new data in file: {file_path}")
    last_position = processed_files.get(file_path, 0)
    try:
        with open(file_path, "r") as file:
            file.seek(last_position)
            while True:
                line = file.readline()
                if not line:
                    break
                if send_data_to_firehose(line):
                    last_position = file.tell()
                    processed_files[file_path] = last_position
                    save_positions(processed_files)
                else:
                    logging.error(
                        f"Failed to send data for file: {file_path}. Stopping further processing."
                    )
                    return

        logging.info(f"Updated position for {file_path}: {last_position}")

    except PermissionError as e:
        logging.error(f"Permission error accessing file {file_path}: {e}")
    except FileNotFoundError as e:
        logging.error(f"File not found: {file_path}: {e}")
    except Exception as e:
        logging.error(f"Error processing file {file_path}: {e}")


def process_queue():
    while True:
        _, file_path = file_queue.get()
        with processing_lock:
            process_new_data(file_path)
        file_queue.task_done()


def sync_existing_files(directory_path):
    logging.info(f"Synchronizing existing files in directory: {directory_path}")
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path not in processed_files or processed_files[
                file_path
            ] != os.path.getsize(file_path):
                logging.info(f"Synchronizing file: {file_path}")
                file_queue.put((os.path.getctime(file_path), file_path))
