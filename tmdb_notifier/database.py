import shelve
import logging
from tmdb_notifier.utils import *


class Database:
    def __init__(self, db: str):
        self.db = shelve.open(db, writeback=True)
        self.__logger = logging.getLogger("app:Database")

    def close(self):
        """Save database and close connection"""
        self.db.close()

    def compare_and_update(
        self, object_name: str, requested_obj: set
    ) -> tuple[set, int]:
        """
        Compare the given object with database and returns differences.
        Updates the record in the databse if it doesn't exist or if it is outdated.
        """
        try:
            stored_obj: set = self.db[object_name]
        except KeyError:
            stored_obj = set()

        diff, outdated, changes_nb = find_differences(requested_obj, stored_obj)

        if not stored_obj and requested_obj:
            self.db[object_name] = requested_obj
            self.__logger.debug(f"Set {object_name} not found in database, entry added")
        elif diff or outdated:
            # force update of watchlist
            if object_name == "watchlist":
                self.db[object_name] = requested_obj
            else:
                self.db[object_name] = diff
            self.__logger.debug(f"Set {object_name} updated in database")

        self.__logger.debug(
            f"Set {object_name} has {changes_nb} changes : {diff or outdated}"
        )
        return (diff, changes_nb)

    def cleanup(self):
        """Removes outdated entries from the database"""
        self.db.sync()
        for key in self.db.keys():
            if key == "watchlist":
                continue
            id = int(key.split(":")[1])
            if id not in self.db["watchlist"]:
                self.__logger.debug(f"Outdated entry {key} in database removed")
                del self.db[key]
