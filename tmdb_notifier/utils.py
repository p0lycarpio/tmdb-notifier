import os
import logging
from typing import Any, List


def find_differences(set1: set, set2: set) -> tuple[set, set, int]:
    """Returns elements in set1 which are not in set2 and vice versa"""
    s1 = set1.difference(set2)
    s2 = set2.difference(set1)
    return (s1, s2, abs(len(s1) + len(s2)))


def readable_list(seq: List[Any]) -> str:
    """Return a correct human readable string (with an Oxford comma)."""
    # Ref: https://stackoverflow.com/a/53981846/
    seq = [str(s) for s in seq]
    if len(seq) < 3:
        return " & ".join(seq)
    return ", ".join(seq[:-1]) + " & " + seq[-1]


def check_env_vars(variables_names: list):
    error = False
    for var_name in variables_names:
        var_value = os.getenv(var_name)
        if var_value is None:
            logging.critical(f"The environnement variable {var_name} is not defined.")
            error = True
    if error:
        exit(1)


def search_in(reference: list, search: set) -> set:
    """Returns the set of elements in `reference` which are in `search`"""
    if not reference or "" in reference:
        return search
    else:
        return {w for w in reference for s in search if s in w}
