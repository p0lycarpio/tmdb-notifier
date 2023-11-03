import os
import logging
from typing import Any, List


def find_difference(set1: set, set2: set) -> set:
    """Returns elements in set1 which are not in set2"""
    return set1.difference(set2)


def cross_difference_number(set1: set, set2: set) -> int:
    s1 = set1.difference(set2)
    s2 = set2.difference(set1)
    return len(s1) + len(s2)


def readable_list(seq: List[Any]) -> str:
    """Return a grammatically correct human readable string (with an Oxford comma)."""
    # Ref: https://stackoverflow.com/a/53981846/
    seq = [str(s) for s in seq]
    if len(seq) < 3:
        return " et ".join(seq)
    return ", ".join(seq[:-1]) + ", et " + seq[-1]


def check_env_vars(variables_names: list):
    error = False
    for var_name in variables_names:
        var_value = os.getenv(var_name)
        if var_value is None:
            logging.critical(f"[ERROR] La variable d'environnement {var_name} n'est pas définie.")
            error = True

    if error:
        exit(1)
