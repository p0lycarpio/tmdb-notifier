from datetime import timedelta

import logging
import redis
from src.utils import *


class Database:
    def __init__(self, default_ttl: timedelta):
        self.db = redis.Redis(
            unix_socket_path="/var/run/redis.sock",
            socket_timeout=5,
            retry_on_timeout=True,
            decode_responses=True,
        )
        self.ttl = default_ttl
        self.__logger = logging.getLogger("app:Database")

    def compare_and_update(
        self, object_name: str, requested_obj: set[str]
    ) -> tuple[set, int]:
        """
        Compare the given object with database and returns differences.
        Updates the record in the databse if it doesn't exist or if it is outdated.
        """
        stored_obj = self.db.smembers(object_name)
        self.db.expire(object_name, self.ttl)
        
        diff = find_difference(requested_obj, stored_obj)
        
        if stored_obj == set() and requested_obj != set():
            self.db.sadd(object_name, *requested_obj)
            self.__logger.debug(f"Set {object_name} not found in database, entry added")
        elif diff != set():
            self.__logger.debug(f"Set {object_name} updated in database")
            self.db.sadd(object_name, *diff)

        changes_nb = cross_difference_number(stored_obj, requested_obj)
        self.__logger.debug(f"Set {object_name} has {changes_nb} changes : {diff}")
        return (diff, changes_nb)
