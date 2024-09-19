import pytest
import arrow
from restfly.errors import UnexpectedValueError
from restfly.utils import (
    check,
    dict_clean,
    dict_flatten,
    dict_merge,
    force_case,
    trunc,
    url_validator,
    redact_values,
)


def test_force_case_single():
    assert force_case('TEST', 'lower') == 'test'
    assert force_case('test', 'upper') == 'TEST'


def test_foce_case_list():
    assert force_case(['a', 'b', 'c'], 'upper') == ['A', 'B', 'C']
    assert force_case(['A', 'B', 'C'], 'lower') == ['a', 'b', 'c']


def test_dict_merge():
    with pytest.deprecated_call():
        assert dict_merge({'a': 1}, {'b': 2}) == {'a': 1, 'b': 2}
        assert dict_merge({'s': {'a': 1}, 'b': 2}, {'s': {'c': 3, 'a': 4}}) == {
            's': {'a': 4, 'c': 3},
            'b': 2,
        }
        assert dict_merge({'a': 1}, {'b': 2}, {'c': 3}, {'a': 5}) == {
            'a': 5,
            'b': 2,
            'c': 3,
        }


def test_dict_flatten():
    assert dict_flatten({'a': 1, 'b': {'c': 2}}) == {'a': 1, 'b.c': 2}
    assert dict_flatten({'A': 1, 'B': {'c': 2}}, lower_key=True) == {'a': 1, 'b.c': 2}
    assert dict_flatten({'a': 1, 'b': [{'c': 2, 'd': {'e': 1}}]}) == {
        'a': 1,
        'b': [{'c': 2, 'd.e': 1}],
    }


def test_dict_clean():
    dirty = {
        'a': 1,
        'b': {'c': 2, 'd': None},
        'e': None,
        'f': [{'g': 1, 'h': None}, {'i': None}],
        'j': [1, None, {}],
    }
    assert dict_clean(dirty) == {'a': 1, 'b': {'c': 2}, 'f': [{'g': 1}], 'j': [1, None]}


def test_trunc():
    assert trunc('Hello There!', 128) == 'Hello There!'
    assert trunc('Too Small', 6) == 'Too...'
    assert trunc('Too Small', 3, suffix=None) == 'Too'


examples = {
    'uuid': '00000000-0000-0000-0000-000000000000',
    'email': 'someone@company.tld',
    'hex': '1234567890abcdef',
    'url': 'http://company.com/path/of/stuff',
    'ipv4': '192.168.0.1',
    'ipv6': '2001:0db8:0000:0000:0000:ff00:0042:8329',
}


def test_check_single_type():
    assert isinstance(check('test', 1, int), int)


def test_check_list_items_type():
    assert isinstance(check('test', [1, 2], list, items_type=int), list)


def test_check_single_type_softchecking():
    assert isinstance(check('test', '1', int), int)


def test_check_single_type_softcheck_fail():
    with pytest.raises(TypeError):
        check('test', '1', int, softcheck=False)


def test_check_type_fail():
    with pytest.raises(TypeError):
        check('test', 1, str)


def test_check_list_items_fail():
    with pytest.raises(TypeError):
        check('test', [1, 2, 'three'], list, items_type=int)


def test_check_list_items_softcheck():
    assert check('test', [1, 2, '3'], list, items_type=int) == [1, 2, 3]


def test_check_choices():
    check('test', [1, 2, 3], list, choices=list(range(5)))


def test_check_choices_fail():
    with pytest.raises(UnexpectedValueError):
        check('test', [1, 2, 3, 500], list, choices=list(range(5)))


def test_check_patern_mapping_uuid():
    check('test', examples['uuid'], str, pattern='uuid')


def test_check_pattern_mapping_uuid_fail():
    with pytest.raises(UnexpectedValueError):
        check('test', 'abcdef', str, pattern='uuid')


def test_check_pattern_mapping_email():
    check('test', examples['email'], str, pattern='email')


def test_check_pattern_mapping_email_fail():
    with pytest.raises(UnexpectedValueError):
        check('test', 'abcdef', str, pattern='email')


def test_check_pattern_mapping_hex():
    check('test', examples['hex'], str, pattern='hex')


def test_check_pattern_mapping_hex_fail():
    with pytest.raises(UnexpectedValueError):
        check('test', 'something', str, pattern='hex')


def test_check_pattern_mapping_url():
    check('test', examples['url'], str, pattern='url')


def test_check_pattern_mapping_url_fail():
    with pytest.raises(UnexpectedValueError):
        check('test', 'abcdef', str, pattern='url')


def test_check_pattern_mapping_ipv4():
    check('test', examples['ipv4'], str, pattern='ipv4')


def test_check_pattern_mapping_ipv4_fail():
    with pytest.raises(UnexpectedValueError):
        check('test', 'abcdef', str, pattern='ipv4')


def test_check_pattern_mapping_ipv6():
    check('test', examples['ipv6'], str, pattern='ipv6')


def test_check_pattern_mapping_ipv6_fail():
    with pytest.raises(UnexpectedValueError):
        check('test', 'abcdef', str, pattern='ipv6')


def test_check_regex_pattern():
    check('test', '12345', str, regex=r'^\d+$')


def test_check_pattern_int_pass():
    check('test', 1, (int, str), pattern='ipv4')


def test_check_regex_fail():
    with pytest.raises(UnexpectedValueError):
        check('test', 'abcdef', str, regex=r'^\d+$')


def test_check_allow_none_fail():
    with pytest.raises(UnexpectedValueError):
        check('test', None, str, allow_none=False)


def test_arrow_type_inputs():
    arw = arrow.utcnow().floor('hour')

    # Test a floating point
    assert check('test', arw.timestamp(), arrow.Arrow) == arw

    # Test an integer
    assert check('test', int(arw.timestamp()), arrow.Arrow) == arw

    # Test a string
    assert check('test', arw.format(), arrow.Arrow) == arw

    # Test an arrow obj
    assert check('test', arw, arrow.Arrow) == arw


def test_bool_softchecks():
    assert check('test', 'yes', bool) is True
    assert check('test', 'true', bool) is True
    assert check('test', 'TRUE', bool) is True
    assert check('test', 'false', bool) is False
    assert check('test', 'FALSE', bool) is False
    assert check('test', 'no', bool) is False


def test_return_defaults():
    assert check('test', None, int) is None
    assert check('test', None, int, default=1) == 1


def test_pattern_map_failure():
    with pytest.raises(IndexError):
        check('test', 'something', str, pattern='something')


def test_url_validator():
    assert url_validator('https://google.com') is True
    assert (
        url_validator('https://httpbin.org/404', validate=['scheme', 'netloc', 'path'])
        is True
    )
    assert (
        url_validator('https://httpbin.org', validate=['scheme', 'netloc', 'path'])
        is False
    )
    assert url_validator('httpbin.org') is False


def test_redact_values():
    test = {'a': 1, 'b': 2, 'c': 3, 'd': {'e': 4, 'f': 5, 'g': 6}}
    assert redact_values(test, keys=['a', 'c', 'd', 'e']) == {
        'a': 'REDACTED',
        'b': 2,
        'c': 'REDACTED',
        'd': {'e': 'REDACTED', 'f': 5, 'g': 6},
    }
    assert redact_values(test) == test
