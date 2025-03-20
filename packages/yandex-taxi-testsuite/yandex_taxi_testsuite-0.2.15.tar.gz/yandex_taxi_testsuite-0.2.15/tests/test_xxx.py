from testsuite.utils import matching


def test_foo():
    assert {'foo': {'bar': 123, 'foo': 321}} == {
        'foo': {'bar': matching.any_string, 'foo': matching.any_integer},
    }


def test_bar():
    assert {'foo': {'bar': 123, 'foo': 321}} == {
        'foo': matching.DictOf(matching.any_string, matching.any_string),
    }
