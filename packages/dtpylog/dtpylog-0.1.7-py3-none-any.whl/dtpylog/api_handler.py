import json
import logging
import requests
from time import sleep


class Logger:
    def __init__(self, logging_api_url, logging_api_key):
        self.api_url = logging_api_url
        self.api_key = logging_api_key

        self.headers = {
            "Authorization": f"{self.api_key}",
            "Content-Type": "application/json"
        }

    def log(self, details: dict):
        max_retries = 5
        backoff_seconds = 3
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.post(
                    url=self.api_url,
                    json=json.loads(json.dumps(details, default=str)),
                    headers=self.headers
                )
                response.raise_for_status()
                return True
            except requests.exceptions.RequestException as e:
                if attempt < max_retries:
                    sleep(backoff_seconds)
                else:
                    logging.error(f"Failed to send log to API: {e}")
                    raise


class LoggerHandler(logging.Handler):
    def __init__(self, logging_api_url, logging_api_key):
        super().__init__()
        self.logger = Logger(
            logging_api_url=logging_api_url,
            logging_api_key=logging_api_key,
        )

    def emit(self, record):
        log_entry = self.format(record)
        log_type = record.levelname.lower()
        details = record.__dict__.get('details') or {}
        details['log_type'] = details.get('log_type') or log_type
        details['subject'] = details.get('subject') or log_entry.split("-", 1)[0].strip()
        details['controller'] = details.get('subject') or record.funcName
        details['message'] = details.get('message') or log_entry
        self.logger.log(details=details)
