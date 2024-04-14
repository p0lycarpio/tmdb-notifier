from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class HTTPSession(Session):
    def __init__(self) -> None:
        super().__init__()
        self.__retry_strategy = Retry(
            total=4,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
            backoff_factor=1,
        )
        self.__adapter = HTTPAdapter(max_retries=self.__retry_strategy)
        self.mount("https://", self.__adapter)
