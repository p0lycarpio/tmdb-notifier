from typing import Any, List
from json import dumps, loads

def find_difference(lst1: list, lst2: list) -> list:
    '''Returns elements in lst1 which are not in lst2'''
    set1 = dics_to_set(lst1)
    set2 = dics_to_set(lst2)

    # Deserialize elements in set1 that are not in set2
    return [loads(x) for x in set1.difference(set2)]  # items in set1 that are not in set2

def dics_to_set(lst: list[dict]) -> set:
    '''Convert list of dicts to set'''
    return set(dumps(x, sort_keys=True) for x in lst)  # sort_keys to control order of keys


def readable_list(seq: List[Any]) -> str:
    """Return a grammatically correct human readable string (with an Oxford comma)."""
    # Ref: https://stackoverflow.com/a/53981846/
    seq = [str(s) for s in seq]
    if len(seq) < 3:
        return ' et '.join(seq)
    return ', '.join(seq[:-1]) + ', et ' + seq[-1]