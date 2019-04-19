import pytest
from restfly.errors import UnexpectedValueError
from restfly.endpoint import APIEndpoint

examples = {
    'uuid': '00000000-0000-0000-0000-000000000000',
    'email': 'someone@company.tld',
    'hex': '1234567890abcdef',
    'url': 'http://company.com/path/of/stuff',
    'ipv4': '192.168.0.1',
    'ipv6': '2001:0db8:0000:0000:0000:ff00:0042:8329'
}

@pytest.fixture
def e(api):
    return APIEndpoint(api)

def test_check_single_type(e):
    assert isinstance(e._check('test', 1, int), int)

def test_check_list_items_type(e):
    assert isinstance(e._check('test', [1, 2], list, items_type=int), list)

def test_check_type_fail(e):
    with pytest.raises(TypeError):
        e._check('test', 1, str)

def test_check_list_items_fail(e):
    with pytest.raises(TypeError):
        e._check('test', [1, 2, '3'], list, items_type=int)

def test_check_choices(e):
    e._check('test', [1, 2, 3], list, choices=list(range(5)))

def test_check_choices_fail(e):
    with pytest.raises(UnexpectedValueError):
        e._check('test', [1, 2, 3, 500], list, choices=list(range(5)))

def test_check_patern_mapping_uuid(e):
    e._check('test', examples['uuid'], str, pattern='uuid')

def test_check_pattern_mapping_uuid_fail(e):
    with pytest.raises(UnexpectedValueError):
        e._check('test', 'abcdef', str, pattern='uuid')

def test_check_pattern_mapping_email(e):
    e._check('test', examples['email'], str, pattern='email')

def test_check_pattern_mapping_email_fail(e):
    with pytest.raises(UnexpectedValueError):
        e._check('test', 'abcdef', str, pattern='email')

def test_check_pattern_mapping_hex(e):
    e._check('test', examples['hex'], str, pattern='hex')

def test_check_pattern_mapping_hex_fail(e):
    with pytest.raises(UnexpectedValueError):
        e._check('test', 'something', str, pattern='hex')

def test_check_pattern_mapping_url(e):
    e._check('test', examples['url'], str, pattern='url')

def test_check_pattern_mapping_url_fail(e):
    with pytest.raises(UnexpectedValueError):
        e._check('test', 'abcdef', str, pattern='url')

def test_check_pattern_mapping_ipv4(e):
    e._check('test', examples['ipv4'], str, pattern='ipv4')

def test_check_pattern_mapping_ipv4_fail(e):
    with pytest.raises(UnexpectedValueError):
        e._check('test', 'abcdef', str, pattern='ipv4')

def test_check_pattern_mapping_ipv6(e):
    e._check('test', examples['ipv6'], str, pattern='ipv6')

def test_check_pattern_mapping_ipv6_fail(e):
    with pytest.raises(UnexpectedValueError):
        e._check('test', 'abcdef', str, pattern='ipv6')

def test_check_regex_pattern(e):
    e._check('test', '12345', str, regex=r'^\d+$')

def test_check_regex_fail(e):
    with pytest.raises(UnexpectedValueError):
        e._check('test', 'abcdef', str, regex=r'^\d+$')