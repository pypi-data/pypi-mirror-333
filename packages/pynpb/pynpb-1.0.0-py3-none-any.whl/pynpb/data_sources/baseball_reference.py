import datetime

from time import sleep
from typing import Any, Optional

import requests

from ..data_helpers import Singleton

class baseball_reference_session(Singleton):
    # Class variable to pull data from baseball reference
    def __init__(self, max_requests_per_minute: int = 18) -> None:
        # Has a variable for max_requests_per_minute to prevent making too many requests and getting timed out by the website
        self.max_requests_per_minute = max_requests_per_minute
        self.last_request: Optional[datetime.datetime] = None
        self.session = requests.Session()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://www.baseball-reference.com/",
            "Upgrade-Insecure-Requests": "1",
            "TE": "Trailers"
        }

        self.session.headers.update(headers)

    def get(self, url : str, **kwargs: Any) -> requests.Response:
        if self.last_request:
            delta = datetime.datetime.now() - self.last_request
            sleep_length = (60 / self.max_requests_per_minute) - delta.total_seconds()
            if sleep_length > 0:
                sleep(sleep_length)

        self.last_request = datetime.datetime.now()

        return self.session.get(url, **kwargs)