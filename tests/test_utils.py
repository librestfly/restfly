import pytest
from restfly.utils import dict_merge, force_case

def test_force_case_single():
    assert force_case('TEST', 'lower') == 'test'
    assert force_case('test', 'upper') == 'TEST'

def test_foce_case_list():
    assert force_case(['a', 'b', 'c'], 'upper') == ['A', 'B', 'C']
    assert force_case(['A', 'B', 'C'], 'lower') == ['a', 'b', 'c']

def test_dict_merge():
    assert dict_merge({'a': 1}, {'b': 2}) == {'a': 1, 'b': 2}
    assert dict_merge({'s': {'a': 1}, 'b': 2}, {'s': {'c': 3, 'a': 4}}) == {
        's': {'a': 4, 'c': 3},
        'b': 2
    }