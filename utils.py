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
