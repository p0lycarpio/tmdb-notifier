from tmdb_notifier.utils import *


def test_find_differences():
    set1 = {"Canal+", "OCS", "Disney+", "Paramount+"}
    set2 = {"Disney+", "Paramount+", "MUBI", "Arte"}
    diff1, diff2, total_diff = find_differences(set1, set2)
    assert diff1 == {"Canal+", "OCS"}
    assert diff2 == {"MUBI", "Arte"}
    assert total_diff == 4


def test_readable_list():
    seq1 = [1, 2]
    seq2 = ["Canal+", "Netflix", "OCS"]
    seq3 = ["MUBI"]
    assert readable_list(seq1) == "1 & 2"
    assert readable_list(seq2) == "Canal+, Netflix & OCS"
    assert readable_list(seq3) == "MUBI"


def test_search_in():
    reference = ["Canal+", "Netflix", "OCS"]
    search1 = {"Canal", "Disney+"}
    search2 = {"Netflix"}
    search3 = {"OCS", "Canal+"}
    search4 = {"MUBI"}
    assert search_in(reference, search1) == {"Canal+"}
    assert search_in(reference, search2) == {"Netflix"}
    assert search_in(reference, search3) == {"Canal+", "OCS"}
    assert search_in(reference, search4) == set()
