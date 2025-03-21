from byuhbll_django_dry.utils import deep_get


def test_deep_get():
    """Test the deep_get function."""
    data = {
        'a': {
            'b': {
                'c': 'd',
            },
        },
    }

    assert deep_get(data, 'a.b.c') == 'd'
    assert deep_get(data, 'a.b') == {'c': 'd'}
    assert deep_get(data, 'a') == {'b': {'c': 'd'}}

    assert deep_get(data, 'a.b.c.d') is None
    assert deep_get(data, 'a.b.d') is None
    assert deep_get(data, 'a.d') is None
    assert deep_get(data, 'd') is None

    assert deep_get(data, 'a.b.c', 'default') == 'd'
    assert deep_get(data, 'a.b', 'default') == {'c': 'd'}
    assert deep_get(data, 'a', 'default') == {'b': {'c': 'd'}}

    assert deep_get(data, 'a.b.c.d', 'default') == 'default'
    assert deep_get(data, 'a.b.d', 'default') == 'default'
    assert deep_get(data, 'a.d', 'default') == 'default'
    assert deep_get(data, 'd', 'default') == 'default'

    assert deep_get({}, 'a.b.c') is None
    assert deep_get([], 'a.b.c') is None
    assert deep_get(None, 'a.b.c') is None
