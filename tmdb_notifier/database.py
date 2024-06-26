import shelve
import logging
from tmdb_notifier.utils import *


class Database:
    def __init__(self, db: str):
        self.db = shelve.open(db, writeback=True)
        self.logger = logging.getLogger("app:Database")

    def close(self):
        """Save database and close connection"""
        self.db.close()

    def get(self, key: str):
        """Get value from database"""
        return self.db[key]

    def create(self, key: str, value: set):
        """Create new entry in database"""
        self.db[key] = value

    def update(self, key: str, value: set):
        """Update entry in database"""
        self.db[key] = value

    def delete(self, key: str):
        """Delete entry from database"""
        del self.db[key]

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

        logging.debug(f"stored object: {stored_obj}")
        diff, outdated, changes_nb = find_differences(requested_obj, stored_obj)

        if not stored_obj and requested_obj:
            self.db[object_name] = requested_obj
            self.logger.debug(f"Set {object_name} not found in database, entry added")
        elif diff or outdated:
            # update database with the new set
            self.db[object_name] = requested_obj
            self.logger.debug(f"Set {object_name} updated in database")

        self.logger.debug(
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
                self.delete(key)
                self.logger.debug(f"Outdated entry {key} in database removed")
